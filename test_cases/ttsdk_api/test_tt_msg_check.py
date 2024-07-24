# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/3/7 18:28
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : test_init.py
# ----------------------
import allure
import pytest
from services.wechatsdk_srv.msg_check_service import MsgCheckService
from test_cases.conftest import get_time
from utils.other_tools.models import TtApi
from utils.read_files_tools.data_analysis import DataAnalysis
from utils.read_files_tools.yaml_control import GetYamlData
from common.setting import ensure_path_sep

y = GetYamlData(ensure_path_sep("\\logs\\html_logs\\http_flow_{}.yaml".format(get_time())))
data = y.get_yaml_data()


@allure.epic('游戏对接自动化测试框架')
@allure.feature('内容检查')
class TestTtMsgCheck:
    @allure.story('内容检查')
    @allure.title('微信内容检查接口')
    @pytest.mark.wechatsdk
    def test_init(self):
        # 我需要找到 路径为 init的接口，并对接口的传参 + 响应进行断言
        interface_calls = DataAnalysis.get_interface_data(data, TtApi.TT_MSG_CHECK_PATH.value)
        assert interface_calls, f"{TtApi.TT_MSG_CHECK_PATH.value} 没有正常调用"
        MsgCheckService(interface_calls).verify_check_api()
