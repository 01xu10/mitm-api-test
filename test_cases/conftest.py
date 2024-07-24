# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/8 23:21
# @Author : xu
# @File : conftest.py
# ----------------------

import pytest
from common.setting import ensure_path_sep
from utils.cache_process.cache_control import Cache
from utils.logging_tools.log_controller import INFO
from utils.read_files_tools.clean_files import del_file


@pytest.fixture(scope="session", autouse=True)
def begin():
    print()
    INFO.logger.info("=======测试开始=======")
    yield
    INFO.logger.info("=======测试结束=======")


def get_time():
    s = Cache("time").get_cache()
    import ast
    items: dict = ast.literal_eval(s)
    time = items.get('time')
    print(f"time ->  {time}")
    return time

def pytest_addoption(parser):
    parser.addoption("--test_type", action="store", default="all")

def pytest_collection_modifyitems(config, items):
    """
    测试用例收集完成时，将收集到的 item 的 name 和 node_id 的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

    test_type = config.getoption("--test_type")
    selected_items = []
    deselected_items = []

    for item in items:
        if test_type == "all" or test_type in item.keywords or "common" in item.keywords:
            selected_items.append(item)
        else:
            deselected_items.append(item)

    config.hook.pytest_deselected(items=deselected_items)
    items[:] = selected_items

    print("收集到的测试用例:%s" % items)
    # 期望用例顺序
    appoint_items = ["test_cases", "test_resp"]

    # 指定运行顺序
    run_items = []
    for i in appoint_items:
        for item in items:
            module_item = item.name.split("[")[0]
            if i == module_item:
                run_items.append(item)

    for i in run_items:
        run_index = run_items.index(i)
        items_index = items.index(i)

        if run_index != items_index:
            n_data = items[run_index]
            run_index = items.index(n_data)
            items[items_index], items[run_index] = items[run_index], items[items_index]


@pytest.fixture(scope="session", autouse=True)
def clear_data():
    """如clean命令无法删除报告，手动删除"""
    del_file(ensure_path_sep("\\reports\\allure_reports"))
    del_file(ensure_path_sep("\\out_files\\cache"))


@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    """Called after building results table additional HTML."""
    report.nodeid.encode("unicode_escape").decode("utf-8")

