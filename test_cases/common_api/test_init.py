# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/3/7 18:28
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : test_init.py
# ----------------------
import allure
import pytest

from services.common_srv.init_service import InitService
from test_cases.conftest import get_time
from utils.other_tools.models import InitApi
from utils.read_files_tools.data_analysis import DataAnalysis
from utils.read_files_tools.yaml_control import GetYamlData
from common.setting import ensure_path_sep

y = GetYamlData(ensure_path_sep("\\logs\\html_logs\\http_flow_{}.yaml".format(get_time())))
data = y.get_yaml_data()


@allure.epic('游戏对接自动化测试框架')
@allure.feature('初始化模块')
class TestInit:
    @allure.story('SDK 初始化')
    @allure.title('游戏初始化接口')
    @pytest.mark.common
    def test_init(self):
        # 我需要找到 路径为 init的接口，并对接口的传参 + 响应进行断言
        interface_calls = DataAnalysis.get_interface_data(data, InitApi.INIT_PATH.value)
        assert interface_calls, f"{InitApi.INIT_PATH.value} 没有正常调用"
        InitService(interface_calls).verify_init()

    @allure.story('SDK 初始化')
    @allure.title('发行初始化接口')
    @pytest.mark.common
    def test_init_fx(self):
        # 我需要找到 路径为 init的接口，并对接口的传参 + 响应进行断言
        interface_calls = DataAnalysis.get_interface_data(data, InitApi.FX_INIT_PATH.value)
        assert interface_calls, f"{InitApi.FX_INIT_PATH.value} 没有正常调用"
        InitService(interface_calls).verify_fx_init()

