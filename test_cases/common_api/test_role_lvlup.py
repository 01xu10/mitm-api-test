# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/3/7 18:28
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : test_init.py
# ----------------------
import allure
import pytest

from services.common_srv.role_lvlup_service import RoleLvlupService
from test_cases.conftest import get_time
from utils.other_tools.models import GameApi
from utils.read_files_tools.data_analysis import DataAnalysis
from utils.read_files_tools.yaml_control import GetYamlData
from common.setting import ensure_path_sep

y = GetYamlData(ensure_path_sep("\\logs\\html_logs\\http_flow_{}.yaml".format(get_time())))
data = y.get_yaml_data()


@allure.epic('游戏对接自动化测试框架')
@allure.feature('角色升级上报模块')
class TestRoleLvlup:

    @allure.story('升级上报')
    @allure.title('买量角色升级接口')
    @pytest.mark.common
    def test_role_login(self):
        interface_calls = DataAnalysis.get_interface_data(data, GameApi.ROLE_LVLUP_PATH.value)
        assert interface_calls, f"{GameApi.ROLE_LVLUP_PATH.value} 没有正常调用"
        RoleLvlupService(interface_calls).verify_role_lvlup()

    @allure.story('升级上报')
    @allure.title('发行角色升级接口')
    @pytest.mark.common
    def test_role_login_fx(self):
        interface_calls = DataAnalysis.get_interface_data(data, GameApi.FX_ROLE_LVLUP_PATH.value)
        assert interface_calls, f"{GameApi.FX_ROLE_LVLUP_PATH.value} 没有正常调用"
        RoleLvlupService(interface_calls).verify_role_lvlup_fx()



