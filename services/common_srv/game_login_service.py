# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/4/25 15:40
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : game_login_service.py
# ----------------------
from utils.assertions.assert_type import equals, equals_type, not_equals, not_equals_any
from utils.other_tools.models import InterfaceData
from utils.read_files_tools.data_analysis import DataAnalysis


class GameLoginService:

    def __init__(self, interface_calls):
        self.interface_calls = interface_calls

    def verify_game_login(self):

        DataAnalysis.check_call_intervals(self.interface_calls)

        for interface_call in self.interface_calls:
            interface_data = InterfaceData(**interface_call[1])
            # 报告打印
            DataAnalysis.log_api_data(interface_data)

            # 响应状态码验证
            equals(
                interface_data.response.status_code,
                "200"
            )

            # 区服 id 验证
            not_equals(
                DataAnalysis.extract_with_jsonpath(interface_data.request.request_content, "$..server_id"),
                "0"
            )

            equals(
                DataAnalysis.extract_with_jsonpath(interface_data.response.response_content, "code"),
                "200"
            )

            equals(
                DataAnalysis.extract_with_jsonpath(interface_data.response.response_content, "state"),
                1
            )
