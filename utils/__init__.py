# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/1/30 11:17
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : __init__.py.py
# ----------------------
from common.setting import ensure_path_sep
from utils.other_tools.models import Config
from utils.read_files_tools.yaml_control import GetYamlData

_data = GetYamlData(ensure_path_sep("\\resources\\config.yaml")).get_yaml_data()
Config.update_forward_refs()
config = Config(**_data)


