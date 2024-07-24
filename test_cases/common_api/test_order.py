# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/3/7 18:28
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : test_init.py
# ----------------------
import allure
import pytest

from services.common_srv.order_service import OrderService
from test_cases.conftest import get_time
from utils.other_tools.models import OrderApi
from utils.read_files_tools.data_analysis import DataAnalysis
from utils.read_files_tools.yaml_control import GetYamlData
from common.setting import ensure_path_sep

y = GetYamlData(ensure_path_sep("\\logs\\html_logs\\http_flow_{}.yaml".format(get_time())))
data = y.get_yaml_data()


@allure.epic('游戏对接自动化测试框架')
@allure.feature('订单模块')
class TestOrder:
    @allure.story('下单测试')
    @allure.title('买量下单接口')
    @pytest.mark.common
    def test_role_login(self):
        interface_calls = DataAnalysis.get_interface_data(data, OrderApi.ORDER_PATH.value)
        assert interface_calls, f"{OrderApi.ORDER_PATH.value} 没有正常调用"
        OrderService(interface_calls).verify_order()

    @allure.story('下单测试')
    @allure.title('发行下单接口')
    @pytest.mark.common
    def test_role_login_fx(self):
        interface_calls = DataAnalysis.get_interface_data(data, OrderApi.FX_ORDER_V2_PATH.value)
        assert interface_calls, f"{OrderApi.FX_ORDER_V2_PATH.value} 没有正常调用"
        OrderService(interface_calls).verify_order_fx()

    @allure.story('下单测试')
    @allure.title('微信小游戏下单接口')
    @pytest.mark.wechat
    def test_role_login_fx(self):
        interface_calls = DataAnalysis.get_interface_data(data, OrderApi.WX_ORDER_PATH.value)
        assert interface_calls, f"{OrderApi.WX_ORDER_PATH.value} 没有正常调用"
        OrderService(interface_calls).verify_order_wechat()




