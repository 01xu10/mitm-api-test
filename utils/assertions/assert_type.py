# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/7/25 17:21
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : assert_type.py
# ----------------------

"""
Assert 断言类型
"""

from typing import Any, Union, Text, Type, List

import jsonpath


def equals(
        check_value: Any, expect_value: Any, message: Text = ""
):
    """判断是否相等"""

    assert check_value == expect_value, message or f"Expected {expect_value}, but got {check_value}."


def less_than(
        check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""
):
    """判断实际结果小于预期结果"""
    assert check_value < expect_value, message


def less_than_or_equals(
        check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""):
    """判断实际结果小于等于预期结果"""
    assert check_value <= expect_value, message


def greater_than(
        check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""
):
    """判断实际结果大于预期结果"""
    assert check_value > expect_value, message


def greater_than_or_equals(
        check_value: Union[int, float], expect_value: Union[int, float], message: Text = ""
):
    """判断实际结果大于等于预期结果"""
    assert check_value >= expect_value, message


def not_equals(
        check_value: Any, expect_value: Any, message: Text = ""
):
    """判断实际结果不等于预期结果"""
    assert check_value != expect_value, message


def not_equals_any(
        check_value: Any, expect_values: List[Any], message: Text = ""
):
    """判断实际结果不等于预期结果列表中的任意一个值"""
    assert not any(check_value == expect_val for expect_val in expect_values), message


def string_equals(
        check_value: Text, expect_value: Any, message: Text = ""
):
    """判断字符串是否相等"""
    assert check_value == expect_value, message


def length_equals(
        check_value: Text, expect_value: int, message: Text = ""
):
    """判断长度是否相等"""
    assert isinstance(
        expect_value, int
    ), "expect_value 需要为 int 类型"
    assert len(check_value) == expect_value, message


def length_greater_than(
        check_value: Text, expect_value: Union[int, float], message: Text = ""
):
    """判断长度大于"""
    assert isinstance(
        expect_value, (float, int)
    ), "expect_value 需要为 float/int 类型"
    assert len(str(check_value)) > expect_value, message


def length_greater_than_or_equals(
        check_value: Text, expect_value: Union[int, float], message: Text = ""
):
    """判断长度大于等于"""
    assert isinstance(
        expect_value, (int, float)
    ), "expect_value 需要为 float/int 类型"
    assert len(check_value) >= expect_value, message


def length_less_than(
        check_value: Text, expect_value: Union[int, float], message: Text = ""
):
    """判断长度小于"""
    assert isinstance(
        expect_value, (int, float)
    ), "expect_value 需要为 float/int 类型"
    assert len(check_value) < expect_value, message


def length_less_than_or_equals(
        check_value: Text, expect_value: Union[int, float], message: Text = ""
):
    """判断长度小于等于"""
    assert isinstance(
        expect_value, (int, float)
    ), "expect_value 需要为 float/int 类型"
    assert len(check_value) <= expect_value, message


def contains(check_value: Any, expect_value: Any, message: Text = ""):
    """判断期望结果内容包含在实际结果中"""
    assert isinstance(
        check_value, (list, tuple, dict, str, bytes)
    ), "expect_value 需要为  list/tuple/dict/str/bytes  类型"
    assert expect_value in check_value, message


def contained_by(check_value: Any, expect_value: Any, message: Text = ""):
    """判断实际结果包含在期望结果中"""
    assert isinstance(
        expect_value, (list, tuple, dict, str, bytes)
    ), "expect_value 需要为  list/tuple/dict/str/bytes  类型"

    assert check_value in expect_value, message


def startswith(
        check_value: Any, expect_value: Any, message: Text = ""
):
    """检查响应内容的开头是否和预期结果内容的开头相等"""
    assert str(check_value).startswith(str(expect_value)), message


def endswith(
        check_value: Any, expect_value: Any, message: Text = ""
):
    """检查响应内容的结尾是否和预期结果内容相等"""
    assert str(check_value).endswith(str(expect_value)), message


def equals_type(
        check_value: Any, expect_type: Type, message: Text = ""
):
    """判断值的类型是否与预期类型相等"""

    assert isinstance(check_value,
                      expect_type), message or f"Expected type {expect_type.__name__}, got {type(check_value).__name__} instead."


def assert_all_elements_equal(
        lst: List[Any], message: Text = ""
):
    """判断列表中的所有元素是否相同"""

    assert isinstance(lst, list), message or f"Expected type list, got {type(lst).__name__} instead."

    if not lst:
        return  # 空列表默认认为所有元素相同

    first_element = lst[0]
    assert all(x == first_element for x in lst), message or f"Not all elements in the list are equal."


def check_digits(
        value: Any, digits: int, message: Text = ""
):
    """判断值的位数是否符合限制"""

    value_str = str(value)  # 将传入的参数转换为字符串
    assert len(value_str) == digits, message or f"Expected {digits} digits, got {len(value_str)} digits instead."


if __name__ == '__main__':
    info: dict = {'path': '/activate/init', 'host': 'fxapi.zkmob.net', 'request_start': '2024-04-19 16:43:01.168', 'params': None, 'request': {'url': 'https://fxapi.zkmob.net/activate/init', 'method': 'POST', 'request_header': 'application/json', 'request_content': '{"game_id":180,"package_id":725,"chl_id":42,"time":1713516181,"client_info":"{\\"client_id\\":\\"f392028c-e812-4507-a061-edca360a2f58\\",\\"sdk_version\\":\\"2.0.0\\"}","sign":"1cc2074499738bd9aaa74bc6f1b7a522"}'}, 'response': {'status_code': 200, 'response_header': 'application/json; charset=utf-8', 'response_content': '{"state":1,"code":"200"}'}}
    status_code = jsonpath.jsonpath(info, '$..status_code')
    # print(info.get('status_code'))
    # equals('1', '0')
    print(status_code[0])
    equals(status_code[0], 200)