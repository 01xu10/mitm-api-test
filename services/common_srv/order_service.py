# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/4/25 16:12
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : order_service.py
# ----------------------
from utils.assertions.assert_type import equals, equals_type
from utils.other_tools.models import InterfaceData
from utils.read_files_tools.data_analysis import DataAnalysis


class OrderService:
    def __init__(self, interface_calls):
        self.interface_calls = interface_calls

    def verify_order(self):

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

            # 报告打印
            DataAnalysis.log_api_data(interface_data)

    def verify_order_fx(self):

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

    def verify_order_wechat(self):
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

