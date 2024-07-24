# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/3/7 18:28
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : test_init.py
# ----------------------
import allure
import pytest

from services.common_srv.game_login_service import GameLoginService
from test_cases.conftest import get_time
from utils.other_tools.models import GameApi
from utils.read_files_tools.data_analysis import DataAnalysis
from utils.read_files_tools.yaml_control import GetYamlData
from common.setting import ensure_path_sep

y = GetYamlData(ensure_path_sep("\\logs\\html_logs\\http_flow_{}.yaml".format(get_time())))
data = y.get_yaml_data()


@allure.epic('游戏对接自动化测试框架')
@allure.feature('登录模块')
class TestGameLogin:
    @allure.story('进登录服')
    @allure.title('买量进登录服接口')
    @pytest.mark.common
    def test_role_login_fx(self):
        # 我需要找到 路径为 init的接口，并对接口的传参 + 响应进行断言
        interface_calls = DataAnalysis.get_interface_data(data, GameApi.GAME_LOGIN_PATH.value)
        assert interface_calls, f"{GameApi.GAME_LOGIN_PATH.value} 没有正常调用"
        GameLoginService(interface_calls).verify_game_login()


