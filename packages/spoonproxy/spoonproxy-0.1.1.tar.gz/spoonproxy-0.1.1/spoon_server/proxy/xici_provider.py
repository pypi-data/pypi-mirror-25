from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree


class XiciProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = ['http://www.xicidaili.com/nn',  # 高匿
                    'http://www.xicidaili.com/nt',  # 透明
                    ]
        return url_list

    def getter(self):
        for url in self.url_list:
            tree = get_html_tree(url)
            if tree is None:
                continue
            proxy_list = tree.xpath('.//table[@id="ip_list"]//tr')
            for px in proxy_list:
                yield ':'.join(px.xpath('./td/text()')[0:2])


if __name__ == "__main__":
    kd = XiciProvider()
    for proxy in kd.getter():
        print(proxy)
