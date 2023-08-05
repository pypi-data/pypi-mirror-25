from bs4 import UnicodeDammit


class Makeup:
    @staticmethod
    def beautify(data, charset):
        dammit = UnicodeDammit(data, [charset, "utf-8", "gb2312", "gbk", "big5", "gb18030"], smart_quotes_to="html")
        data = dammit.unicode_markup
        charset = dammit.original_encoding
        return data, charset
