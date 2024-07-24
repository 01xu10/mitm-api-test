# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/3/7 18:28
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : test_init.py
# ----------------------
import allure
import pytest

from services.common_srv.login_service import LoginService
from services.common_srv.params_service import ParamsService
from test_cases.conftest import get_time
from utils.other_tools.models import LoginApi, OrderApi
from utils.read_files_tools.data_analysis import DataAnalysis
from utils.read_files_tools.yaml_control import GetYamlData
from common.setting import ensure_path_sep

y = GetYamlData(ensure_path_sep("\\logs\\html_logs\\http_flow_{}.yaml".format(get_time())))
data = y.get_yaml_data()


@allure.epic('游戏对接自动化测试框架')
@allure.feature('公共模块')
class TestLogin:
    @allure.story('测试参数值')
    @allure.title('server_name 参数')
    @pytest.mark.common
    def test_login(self):
        # 我需要找到 路径为 init的接口，并对接口的传参 + 响应进行断言
        interface_calls = DataAnalysis.get_interface_data(data, LoginApi.LOGIN_PATH.value, LoginApi.FX_LOGIN_PATH.value)
        assert interface_calls, f"{LoginApi.LOGIN_PATH.value} 没有正常调用"
        ParamsService(interface_calls).verify_params_value()


