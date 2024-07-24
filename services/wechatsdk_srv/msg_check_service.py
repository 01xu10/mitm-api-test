# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/4/25 16:45
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : msg_check_service.py
# ----------------------
from utils.assertions.assert_type import equals, equals_type
from utils.other_tools.models import InterfaceData
from utils.read_files_tools.data_analysis import DataAnalysis


class MsgCheckService:
    def __init__(self, interface_calls):
        self.interface_calls = interface_calls

    def verify_check_api(self):
        DataAnalysis.check_call_intervals(self.interface_calls)

        for interface_call in self.interface_calls:
            interface_data = InterfaceData(**interface_call[1])

            equals(
                interface_data.response.status_code,
                "200"
            )

            DataAnalysis.log_api_data(interface_data)
