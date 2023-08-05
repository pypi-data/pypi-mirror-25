import re


class Checker(object):
    def __init__(self, url=None):
        self.url = url

    def checker_func(self, html=None):
        return True


class CheckerBaidu(Checker):
    def checker_func(self, html=None):
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        if re.match(r".*百度一下，你就知道.*", html):
            return True
        else:
            return False
