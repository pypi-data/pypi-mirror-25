import asyncio as aio
import concurrent
from concurrent import futures

import pycurl
from contextlib import suppress, contextmanager

from loader.util.context import AOPWrapper

from netboy.util.aop_wrapper import pre_process, post_process
from ..util.payload import Payload
from loader.function import load


import atexit

import aiohttp
import uvloop

from netboy.curl.result import Result
from netboy.curl.setup import Setup

import json

from netboy.util.grouper import grouper_it


class CurlBoy:
    def run(self, payload=None):
        curl, result = self._setup_curl(payload)

        curl.perform()
        resp = result.result(curl, 'normal', None)

        resp = self._update_response(payload, resp, result)
        curl.close()
        return resp

    def view(self, result, filters):
        return {key: result.get(key) for key in filters}

    def get(self, url, **kwargs):
        payload = kwargs
        payload['url'] = url
        return self.run(payload=payload)

    def post(self, url, payload, **kwargs):
        p = kwargs
        p['url'] = url
        p['postfields'] = payload
        return self.run(payload=p)

    async def _runs(self, payload=None, info=None, curl_loop=None):

        Payload.update(payload, info, ['max_workers, chunk_size'])
        payload = pre_process(payload)
        # pre_func = payload.get('pre_func')
        # if pre_func:
        #     pre_func = load(pre_func)
        #     pre_ret = pre_func(payload)
        #     if pre_ret:
        #         payload = pre_ret
        curl, result = self._setup_curl(payload)
        resp = await self.run_async(curl, payload.get('aiohttp_timeout', 10), curl_loop)
        resp = self._update_response(payload, resp, result)
        resp = post_process(payload, resp)
        # post_func = payload.get('post_func')
        # if post_func:
        #     post_func = load(post_func)
        #     post_ret = post_func(payload, resp)
        #     if post_ret:
        #         resp = post_ret
        return resp

    async def run_async(self, curl, aiohttp_timeout=10, curl_loop=None):
        with aiohttp.Timeout(aiohttp_timeout):
            # resp = await CurlLoop.handler_ready(curl)
            resp = await curl_loop.handler_ready(curl)
            # resp = await .handler_ready(curl)
        return resp

    def _setup_curl(self, payload):
        curl = pycurl.Curl()
        setup = Setup()
        result = Result(setup)
        if payload.get('postfields'):
            method = payload.get('method', 'post')
            if method == 'post':
                curl = setup.method_post(curl, payload)  #
        else:
            curl = setup.method_get(curl, payload)  #
        return curl, result

    def _update_response(self, payload, resp, result):
        resp['url'] = payload.get('url')
        resp['id'] = payload.get('id')
        resp['payload'] = payload
        if payload.get('postfields'):
            resp = result.response(payload, resp, json_data=True)
        else:
            resp = result.response(payload, resp)
        return resp


class CurlLoop:
    def __init__(self):
        self._multi = pycurl.CurlMulti()
        self._multi.setopt(pycurl.M_PIPELINING, 1)
        atexit.register(self._multi.close)
        self._futures = {}

    async def handler_ready(self, c):
        self._futures[c] = aio.Future()
        self._multi.add_handle(c)
        try:
            # with suppress(aio.CancelledError):
            try:
                curl_ret = await self._futures[c]
            except concurrent.futures._base.CancelledError as e:
                return {
                    'spider': 'pycurl',
                    'state': 'error',
                    'error_code': -1,
                    'error_desc': "{} - {}: maybe timeout".format(type(e), str(e)),
                }
            except Exception as e:
                return {
                    'spider': 'pycurl',
                    'state': 'critical',
                    'error_code': -2,
                    'error_desc': "{} - {}".format(type(e), str(e)),
                }
            return curl_ret
        finally:
            self._multi.remove_handle(c)

    def perform(self):
        if self._futures:
            res = Result()
            while True:
                status, num_active = self._multi.perform()
                if status != pycurl.E_CALL_MULTI_PERFORM:
                    break
            while True:
                num_ready, success, fail = self._multi.info_read()
                for c in success:
                    cc = self._futures.pop(c)
                    result = res.result(c, 'normal')
                    if not cc.cancelled():
                        cc.set_result(result)
                for c, err_num, err_msg in fail:
                    cc = self._futures.pop(c)
                    result = res.result(c, 'error')
                    result['error_code'] = err_num
                    result['error_desc'] = err_msg
                    if not cc.cancelled():
                        cc.set_result(result)
                if num_ready == 0:
                    break


class ConcurrentBoy:
    def run(self, data, loop=None):
        d = data.get('data')
        i = data.get('info')
        mode = i.get('mode', 'threaded')
        if mode == 'threaded':
            i['mode'] = 'threaded'
            return self._run_threaded(d, i, loop)
        else:
            i['mode'] = 'normal'
            return self._run_simple(d, i, loop)

    def _run_threaded(self, data, info, loop):
        results = []
        with futures.ThreadPoolExecutor(max_workers=info.get('max_workers')) as executor:
            future_to_url = {}

            for payload in grouper_it(data, info.get('chunk_size', 20)):
                future_to_url[executor.submit(self._run, payload, info, loop)] = payload

            for future in futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                else:
                    results.extend(data)
        return results

    def _run_simple(self, data, info, loop):
        results = []
        self._curl_loop = CurlLoop()
        for payload in grouper_it(data, info.get('chunk_size', 20)):
            result = self._run(payload, info, loop=loop)
            results.extend(result)
        return results

    def _run(self, payload, info, loop=None):
        def exception_handler(context):
            print('context:', context)

        if loop is None:
            loop = uvloop.new_event_loop()
            # loop = aio.get_event_loop()
        aio.set_event_loop(loop)
        curl_loop = CurlLoop()
        loop.set_exception_handler(exception_handler)
        # Payload.update(payload, info, ['max_workers, chunk_size', 'mode'])
        r, _ = loop.run_until_complete(self._task(self._coro(payload, info, curl_loop), curl_loop))
        loop.close()
        return r

    async def _coro(self, payload, info, curl_loop=None):
        targets = []
        boy = CurlBoy()
        for p in payload:
            d = {'url': p} if type(p) is str else p
            targets.append(boy._runs(d, info, curl_loop))
        res = await aio.gather(
            *targets, return_exceptions=False
        )
        return res

    async def _task(self, coro, curl_loop=None):
        pycurl_task = aio.ensure_future(self._loop(curl_loop))
        try:
            r = await coro
        finally:
            pycurl_task.cancel()
            with suppress(aio.CancelledError):
                await pycurl_task
        return r, pycurl_task

    async def _loop(self, curl_loop=None, wait=0):
        while True:
            await aio.sleep(wait)
            # CurlLoop.perform()
            curl_loop.perform()

    def view(self, results, filters):
        scene = []
        for result in results:
            updated = {key: result.get(key) for key in filters}
            scene.append(updated)
        return scene

def post_test(payload, resp):
    print('haha')
    return resp


if __name__ == '__main__':
    # boy = CurlBoy()
    # r = boy.get('http://www.douban.com', useragent='Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0')
    # print(json.dumps(boy.view(r, ['title']), indent=2, ensure_ascii=False))

    # boy = CurlBoy()
    # r = boy.post('http://192.168.199.212:8006/v1/spider_query',
    #              payload={
    #                  "charset": "UTF-8",
    #                  "filters": [
    #                      "title"
    #                  ],
    #                  "pagenum": 1,
    #                  "pagesize": 10,
    #                  "state": "normal"
    #
    #              })
    # print(json.dumps(boy.view(r, ['data']), indent=2, ensure_ascii=False))
    boy = ConcurrentBoy()
    data = {
        "data": [
            {'url': 'http://www.sohu.com',
             'post_func': 'netboy.curl.boy.post_test'},
            {"url":"http://www.baidu.com",
             'post_func': 'netboy.curl.boy.post_test'},
            "http://www.douban.com",
            # {
            #     'url': 'http://192.168.199.212:8006/v1/spider_query',
            #     'postfields': {
            #         "charset": "UTF-8",
            #         "filters": [
            #             "title"
            #         ],
            #         "pagenum": 1,
            #         "pagesize": 10,
            #         "state": "normal"
            #     }
            # },
            # 'http://www.sohu.com',
            # {'url': 'http://www.bing.com'},
            # {'url': 'http://www.baidu.com'},
            # {'url': 'http://www.facebook.com'},
            # {'url': 'http://www.google.com'},
            # {'url': 'http://www.youtube.com'}, {'url': 'http://www.github.com'},
        ],
        "info": {
            "chunk_size": 2,
            "max_workers": 2,
            "useragent":'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0',
            # "mode": 'threaded'
        }
    }
    r = boy.run(data)
    # print(r)
    print(json.dumps(boy.view(r, ["title", "url", "state", "error_desc", "error_code", "total_time", "mode"]), indent=2,
                     ensure_ascii=False))
    print(len(r))
