# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/4/25 16:46
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : role_login_service.py
# ----------------------
import json
from common.setting import ensure_path_sep
from utils import GetYamlData
from utils.assertions.assert_type import equals, equals_type, not_equals, not_equals_any, assert_all_elements_equal
from utils.other_tools.models import InterfaceData
from utils.read_files_tools.data_analysis import DataAnalysis


class RoleLoginService:

    def __init__(self, interface_calls):
        self.interface_calls = interface_calls

    def verify_role_login(self):
        DataAnalysis.check_call_intervals(self.interface_calls)

        for interface_call in self.interface_calls:
            interface_data = InterfaceData(**interface_call[1])
            # 报告打印
            DataAnalysis.log_api_data(interface_data)
            equals(
                interface_data.response.status_code,
                "200"
            )

            equals_type(
                DataAnalysis.extract_with_jsonpath(interface_data.request.request_content, "server_zone"),
                str
            )

            equals(
                DataAnalysis.extract_with_jsonpath(interface_data.response.response_content, "code"),
                "200"
            )

            equals(
                DataAnalysis.extract_with_jsonpath(interface_data.response.response_content, "state"),
                1
            )

    def verify_role_login_fx(self):
        DataAnalysis.check_call_intervals(self.interface_calls)

        for interface_call in self.interface_calls:
            interface_data = InterfaceData(**interface_call[1])
            # 报告打印
            DataAnalysis.log_api_data(interface_data)
            equals(
                interface_data.response.status_code,
                "200"
            )




























if __name__ == '__main__':
    y = GetYamlData(ensure_path_sep("\\logs\\html_logs\\http_flow_2024-05-20_15-47.yaml"))
    data = y.get_yaml_data()
    interface_calls = DataAnalysis.get_interface_data(data, '/user/456180343', '/user/v1.0/identity_get')
    # print(DataAnalysis.check_call_intervals(interface_calls, 300))
    params_value_list = []
    for interface_call in interface_calls:
        interface_data = InterfaceData(**interface_call[1])
        print(interface_data)
        print()

        print(DataAnalysis.extract_with_jsonpath(interface_data.response.response_content, "code"))



            # 响应状态码验证
    #     params_value_list.append(
    #         DataAnalysis.extract_with_jsonpath(interface_data.request.request_content, "$..access_token"))
    # print(params_value_list)
    # assert_all_elements_equal(params_value_list)

    #     print(type(interface_data.request.request_content))
    #     print(DataAnalysis.extract_with_jsonpath(interface_data.request.request_content, "server_id"))
    #     not_equals_any(
    #         DataAnalysis.extract_with_jsonpath(interface_data.request.request_content, "server_id"),
    #         ["0", "12346", "61000"],
    #         "区服id值异常"
    #     )


        # pprint(interface_call[1])
        # print(interface_call[1]['request_content'])
        # print(DataAnalysis.extract_with_jsonpath(interface_call[1]['request_content'], "$..server_zone"))
        # d = DataAnalysis.extract_with_jsonpath(interface_call, "$..request_content")
        # print(d)
        # print(type(d))
        # print(type(DataAnalysis.extract_with_jsonpath(interface_call, "$..request_content")))
        # # request_content = json.loads(d)
        # print(DataAnalysis.extract_with_jsonpath(d, "$..server_zone"))
        # from utils.other_tools.models import InterfaceData
        #
        # interface = interface_call[1]
        # interface_data_instance = InterfaceData(**interface)
        # DataAnalysis.log_api_data(interface_data_instance)