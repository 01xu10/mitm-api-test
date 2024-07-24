# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/3/7 18:28
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : test_init.py
# ----------------------
import allure
from test_cases.conftest import get_time
from utils.read_files_tools.data_analysis import DataAnalysis
from utils.read_files_tools.yaml_control import GetYamlData
from common.setting import ensure_path_sep
from utils.assertions.assert_type import equals

# y = GetYamlData(ensure_path_sep("\\logs\\html_logs\\http_flow_{}.yaml".format(get_time())))
# data = y.get_yaml_data()


@allure.epic('小游戏自动化测试框架')
@allure.feature('客服接口')
class TestCustomer:
    @allure.story('内容检查')
    @allure.title('内容检查接口')
    def test_customer(self):
        ...


