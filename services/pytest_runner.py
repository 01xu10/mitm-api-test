# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/3/11 16:29
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : pytest_runner.py
# ----------------------
import os
import pytest
from common.setting import ensure_path_sep
from utils.notify.lark import FeiShuTalkChatBot
from utils.other_tools.allure_data.get_allure_data import AllureFileClean
from utils.other_tools.models import NotificationType
from utils import config
from utils.time_tools.time_control import now_time
import argparse


parser = argparse.ArgumentParser(description='Run pytest with options.')
parser.add_argument('--option', help='Option to pass to pytest', default='')


if __name__ == '__main__':
    args = parser.parse_args()  # 解析命令行参数
    option = args.option  # 获取 option 参数的

    pytest.main(['-s', '-W', 'ignore:Module already imported:pytest.PytestWarning',
                 '--alluredir={}'.format(ensure_path_sep("\\reports\\allure_reports")),
                 '--html={}'.format(ensure_path_sep("\\reports\\html_reports\\html_report_{}.html".format(now_time()))),
                 '--capture=sys', '--clean-alluredir',
                 '--test_type={}'.format(option)
                 # "-n", "2", "--dist=loadscope",
                 ])
    os.system('allure generate ./reports/allure_reports -o ./reports/allure_reports/html --clean')
    """统计用例数量"""
    allure_data = AllureFileClean.get_case_count()
    notification_mapping = {
        NotificationType.FEI_SHU.value: FeiShuTalkChatBot(allure_data).post
    }
    # 判断是否发送通知
    if config.notification_type != NotificationType.DEFAULT.value:
        notification_mapping.get(config.notification_type)()

    os.system('allure serve --port {} ./reports/allure_reports'.format(config.allure_port))