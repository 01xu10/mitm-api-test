# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/4/25 16:47
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : role_lvlup_service.py
# ----------------------
from utils.assertions.assert_type import equals, equals_type
from utils.other_tools.models import InterfaceData
from utils.read_files_tools.data_analysis import DataAnalysis


class RoleLvlupService:

    def __init__(self, interface_calls):
        self.interface_calls = interface_calls
        
    def verify_role_lvlup(self):
        DataAnalysis.check_call_intervals(self.interface_calls)

        for interface_call in self.interface_calls:
            interface_data = InterfaceData(**interface_call[1])
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

    def verify_role_lvlup_fx(self):
        DataAnalysis.check_call_intervals(self.interface_calls)

        for interface_call in self.interface_calls:
            interface_data = InterfaceData(**interface_call[1])
            DataAnalysis.log_api_data(interface_data)
            equals(
                interface_data.response.status_code,
                "200"
            )

            equals(
                DataAnalysis.extract_with_jsonpath(interface_data.response.response_content, "code"),
                "200"
            )

            equals(
                DataAnalysis.extract_with_jsonpath(interface_data.response.response_content, "state"),
                1
            )



