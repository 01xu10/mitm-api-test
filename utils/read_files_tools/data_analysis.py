# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/4/25 15:51
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : data_analysis.py
# ----------------------
import json
import allure
import jsonpath_ng
from typing import Dict, List, Any
from utils.logging_tools.log_controller import ERROR, INFO
from utils.other_tools.models import InterfaceData
from utils.time_tools.time_control import timestamp_conversion_ms


class DataAnalysis:
    @staticmethod
    def check_call_intervals(interface_calls, threshold_ms=300):
        try:
            call_times = [timestamp_conversion_ms(call[1]['request_start']) for call in interface_calls]
            print(call_times)
        except Exception as e:
            ERROR.logger.error(f"时间转换错误: {e}")
            return False

        if not call_times:
            ERROR.logger.error("时间列表为空，接口调用次数为0，无法计算调用间隔")
            return False

        for prev_call, next_call in zip(call_times, call_times[1:]):
            interval_ms = (next_call - prev_call).total_seconds() * 1000
            INFO.logger.info(f"调用间隔: {interval_ms} 毫秒")
            INFO.logger.info(f"规定间隔: {threshold_ms} 毫秒")
            if interval_ms < threshold_ms:
                return False
        return True

    @staticmethod
    def check_field_change(interface_calls, key):
        try:
            key_list = []
            for interface_call in interface_calls:
                interface_data = InterfaceData(**interface_call[1])
                v = DataAnalysis.extract_with_jsonpath(interface_data.request.request_content, key)
                if v:
                    key_list.append(v)

        except Exception as e:
            ERROR.logger.error(f"提取报错: {e}")
            return False

        if not key_list:
            ERROR.logger.error("列表为空，提取失败")
            return False

        for prev_v, next_v in zip(key_list, key_list[1:]):
            INFO.logger.info(f"1: {prev_v} 毫秒")
            INFO.logger.info(f"2: {next_v} 毫秒")
            if prev_v == next_v:
                return False
        return True

    @staticmethod
    def get_interface_data(data_structure: Dict[str, Dict[str, Any]], *paths_to_find: str) -> List[Dict]:
        """
        :param data_structure: 接口字典
        :param paths_to_find: 对接路径列表
        :return:
        """

        matching_items = []

        if not isinstance(data_structure, Dict):
            raise ValueError("data_structure 必须是一个字典。")

        if not all(isinstance(path, str) for path in paths_to_find):
            raise ValueError("所有 path_to_find 必须是字符串。")

        for key, value in data_structure.items():
            if value.get('path') in paths_to_find:
                matching_items.append((key, value))

        return matching_items

    @staticmethod
    def extract_with_jsonpath(info, key):
        try:
            jsonpath_expr = f"$..{key}"
            if isinstance(info, str):
                info = json.loads(info)
            # 解析jsonpath表达式
            jsonpath_expression = jsonpath_ng.parse(jsonpath_expr)
            # 应用jsonpath表达式并提取匹配的内容
            match = jsonpath_expression.find(info)
            # 如果找到匹配项，返回提取的值
            if match:
                return match[0].value
            else:
                # 如果没有匹配项，则记录到Allure报告并返回空列表
                with allure.step(f"JsonPath Extraction Failed: {jsonpath_expr}"):
                    allure.attach(str(info), "JSON Data", allure.attachment_type.JSON)
                    allure.attach("No match found", "Error Message", allure.attachment_type.TEXT)
                return []
        except Exception as e:
            # 如果提取过程中出现异常，记录错误到Allure报告
            with allure.step(f"JsonPath Extraction Exception: {jsonpath_expr}"):
                allure.attach(str(info), "JSON Data", allure.attachment_type.JSON)
                allure.attach(str(e), "Exception Message", allure.attachment_type.TEXT)
            # 仍然返回空列表，不终止程序运行
            return 0

    @staticmethod
    def log_api_data(interface_data: InterfaceData):
        # 将接口的结构体数据转换成 JSON 格式并附加到 allure 报告中
        with allure.step(f"请求地址:{interface_data.host + interface_data.path}"):
            allure.attach(interface_data.host + interface_data.path, name="url",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step(f"请求方法: {interface_data.request.method}"):
            allure.attach(interface_data.request.method, name="method",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step(f"请求时间: {interface_data.request_start}"):
            allure.attach(interface_data.request_start, name="request_start",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step(f"请求参数: {interface_data.request.request_content}"):
            allure.attach(interface_data.request.request_content, name="request",
                          attachment_type=allure.attachment_type.JSON)
        with allure.step(f"响应结果: {interface_data.response.response_content}"):
            allure.attach(interface_data.response.response_content, name="response",
                          attachment_type=allure.attachment_type.JSON)
