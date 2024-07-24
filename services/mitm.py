import json
from datetime import datetime
from typing import Text, Dict
from mitmproxy import tls, http
from ruamel import yaml
from utils.cache_process.cache_control import Cache
from common.setting import ensure_path_sep
from utils.time_tools.time_control import now_time_m


class Counter:
    """
    基于 mitmproxy 库拦截获取网络请求
    参考资料: https://blog.wolfogre.com/posts/usage-of-mitmproxy/
    """

    def __init__(self, intercept_hosts: tuple, keywords: tuple, filter_url_type: list):
        self.num = 0
        self.counter = 1
        self.now_time_m = now_time_m()
        Cache("time").set_cache("time", self.now_time_m)
        # 需要拦截的 host
        self.intercept_hosts = intercept_hosts
        # 需要拦截的 关键字
        self.keywords = keywords
        self.filter_url_type = filter_url_type
        self.url_path_set = set()

    def is_intercept_host(self, host_name):
        """
            判断是否拦截请求
        """
        if host_name in self.intercept_hosts:
            return True
        if any(kw in host_name for kw in self.keywords):
            return True
        return False

    # def tls_clienthello(self, data: tls.ClientHelloData):
    #     srv = data.context.server
    #     server_name = srv.address or srv.peername
    #     if not self.is_intercept_host(server_name[0]):
    #         # True: http hock 不生效; 不进行请求拦截处理，直接转发给源服务器。
    #         data.ignore_connection = True

    def response(self, flow: http.HTTPFlow):
        # 判断过滤掉含 filter_url_type 中后缀的 url

        if (
                not any(i in flow.request.url for i in self.filter_url_type) and
                flow.request.host in intercept_host and
                flow.request.method != "OPTIONS"
        ):
            request_header = flow.request.headers
            response_header = flow.response.headers
            content = flow.request.text
            start_time = datetime.fromtimestamp(flow.timestamp_start).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            print("id: {}".format(flow.id))
            print("====== Request ======")
            print("start_time:{}".format(start_time))
            print("url: {}".format(flow.request.url))
            print("method: {}".format(flow.request.method))
            print("header: {}".format(request_header.get("Content-Type", "")))
            print("content: {}".format(content))
            print("===== Response =====")
            print("status_code: {}".format(flow.response.status_code))
            print("header: {}".format(response_header.get("Content-Type", "")))
            print("content: {}".format(flow.response.text))

            # 收集request信息
            request_data = {
                'url': flow.request.url,
                'method': flow.request.method,
                'request_header': flow.request.headers.get("Content-Type", ""),
                'request_content': flow.request.text
            }

            # 收集response信息
            response_data = {
                'status_code': flow.response.status_code,
                'response_header': flow.response.headers.get("Content-Type", ""),
                'response_content': flow.response.text
            }

            path, params = self.parse_get_request(flow.request.path)
            data = {
                str(flow.id):
                    {
                        "path": path,
                        "host": flow.request.host,
                        "request_start": start_time,
                        "params": params,
                        "request": request_data,
                        "response": response_data
                    }
            }
            self.write_to_yaml(data)

    @staticmethod
    def parse_get_request(url):
        path = url.split('?')[0]  # 获取路径部分
        params = url.split('?')[1] if '?' in url else None  # 获取参数部分，如果没有参数则为None
        return path, params

    def write_to_yaml(self, data: Dict) -> None:
        """
        写入 yaml 数据
        :param data: 测试用例数据
        :return:
        """
        file_path = ensure_path_sep(
            "\\logs\\html_logs\\http_flow_{}.yaml".format(self.now_time_m))
        with open(file_path, "a", encoding="utf-8") as file:
            yaml.dump(data, file, Dumper=yaml.RoundTripDumper, allow_unicode=True, default_flow_style=False)
            file.write('\n')


intercept_host = (
    "webapi.zkyouxi.com",
    "trackapi.zkyouxi.com",
    "userapi.zkyouxi.com",
    "payapi.zkyouxi.com",
    "mapi.zkyouxi.com",
    "ares.zkyouxi.com",
    "api-hk.redkylin.info",
    "fxapi.zkmob.net"
)

kws = ("zkyouxi", "zkmob", "x56l.com",)

fil_url_type = ['.css', '.js', '.map', '.ico', '.png', '.woff', '.map3', '.jpeg', '.jpg', '.html']

addons = [
    Counter(intercept_host, kws, fil_url_type)
]