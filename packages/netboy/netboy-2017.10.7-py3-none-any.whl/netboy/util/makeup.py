from bs4 import UnicodeDammit


class Makeup:
    @staticmethod
    def beautify(data):
        CHARSET_LIST =["utf8", "gb2312", "gbk", "big5", "gb18030"]
        dammit = UnicodeDammit(data, CHARSET_LIST, smart_quotes_to="html")
        charset = dammit.original_encoding
        data = dammit.unicode_markup
        # if charset in CHARSET_LIST:
        #     data = dammit.unicode_markup
        # else:
        #     charset = 'utf8'
        #     data = data.decode('utf8', 'ignore')

        return data, charset
