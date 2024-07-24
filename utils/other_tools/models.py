# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/3/16 20:01
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : models.py
# ----------------------
import types
from dataclasses import dataclass
from enum import Enum, unique
from pydantic import BaseModel
from typing import Text, Dict, Callable, Union, Optional, List, Any


def load_module_functions(module) -> Dict[Text, Callable]:
    """ 获取 module中方法的名称和所在的内存地址 """
    module_functions = {}

    for name, item in vars(module).items():
        if isinstance(item, types.FunctionType):
            module_functions[name] = item
    return module_functions


class NotificationType(Enum):
    """ 自动化通知方式 """
    DEFAULT = 0
    FEI_SHU = 1


@dataclass
class TestMetrics:
    """ 用例执行数据 """
    passed: int
    failed: int
    broken: int
    skipped: int
    total: int
    pass_rate: float
    time: Text


class RequestType(Enum):
    """
    request请求发送，请求参数的数据类型
    """
    JSON = "JSON"
    PARAMS = "PARAMS"
    DATA = "DATA"
    FILE = 'FILE'
    EXPORT = "EXPORT"
    NONE = "NONE"


class TestCaseEnum(Enum):
    URL = ("url", True)
    HOST = ("host", True)
    METHOD = ("method", True)
    DETAIL = ("detail", True)
    IS_RUN = ("is_run", True)
    HEADERS = ("headers", True)
    REQUEST_TYPE = ("requestType", True)
    DATA = ("data", True)
    # DE_CASE = ("dependence_case", True)
    # DE_CASE_DATA = ("dependence_case_data", False)
    # CURRENT_RE_SET_CACHE = ("current_request_set_cache", False)
    # SQL = ("sql", False)
    ASSERT_DATA = ("assert", True)
    SETUP_SQL = ("setup_sql", False)
    TEARDOWN = ("teardown", False)
    TEARDOWN_SQL = ("teardown_sql", False)
    SLEEP = ("sleep", False)


class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTION = "OPTION"


class ResponseData(BaseModel):
    url: Text
    response_data: Text
    request_body: Any
    method: Text
    headers: Dict
    res_time: Union[int, float]
    status_code: int


class PhoneInfo(BaseModel):
    platform: Text
    uuid: Text
    package: Text
    dev: Text


class Config(BaseModel):
    project_name: Text
    env: Text
    tester_name: Text
    notification_type: int = 0
    excel_report: bool
    mirror_source: Text
    email: "Email"
    lark: "Lark"
    allure_port: int


class Lark(BaseModel):
    webhook: Union[Text, None]
    secret: Union[Text, None]


class Email(BaseModel):
    send_user: Union[Text, None]
    email_host: Union[Text, None]
    stamp_key: Union[Text, None]
    # 收件人
    send_list: Union[Text, None]


class HttpFlow(BaseModel):
    flow_id: Text
    url: Text
    method: Text
    request_headers: Text
    request_content: Text
    status_code: int
    response_headers: Text
    response_content: Text


class ParamPrepare(BaseModel):
    dependent_type: Text
    jsonpath: Text
    set_cache: Text


class SendRequest(BaseModel):
    dependent_type: Text
    jsonpath: Optional[Text]
    cache_data: Optional[Text]
    set_cache: Optional[Text]
    replace_key: Optional[Text]


class TearDown(BaseModel):
    case_id: Text
    param_prepare: Optional[List["ParamPrepare"]]
    send_request: Optional[List["SendRequest"]]


class CurrentRequestSetCache(BaseModel):
    type: Text
    jsonpath: Text
    name: Text


class DependentData(BaseModel):
    dependent_type: Text
    jsonpath: Text
    set_cache: Optional[Text]
    replace_key: Optional[Text]


class DependentCaseData(BaseModel):
    case_id: Text
    # dependent_data: List[DependentData]
    dependent_data: Union[None, List[DependentData]] = None


class TestCase(BaseModel):
    url: Text
    method: Text
    detail: Text
    # assert_data: Union[Dict, Text] = Field(..., alias="assert")
    assert_data: Union[Dict, Text]
    headers: Union[None, Dict, Text] = {}
    requestType: Text
    is_run: Union[None, bool, Text] = None
    data: Any = None
    dependence_case: Union[None, bool] = False
    dependence_case_data: Optional[Union[None, List["DependentCaseData"], Text]] = None
    sql: List = None
    setup_sql: List = None
    status_code: Optional[int] = None
    teardown_sql: Optional[List] = None
    teardown: Union[List["TearDown"], None] = None
    current_request_set_cache: Optional[List["CurrentRequestSetCache"]]
    sleep: Optional[Union[int, float]]


class RequestData(BaseModel):
    url: Text
    method: Text
    request_header: Text
    request_content: Text


class RespData(BaseModel):
    status_code: Text
    response_header: Text
    response_content: Text


class InterfaceData(BaseModel):
    path: Text
    host: Text
    request_start: Text
    params: Any
    request: "RequestData"
    response: "RespData"


@unique
class AssertMethod(Enum):
    """断言类型"""
    equals = "=="
    less_than = "lt"
    less_than_or_equals = "le"
    greater_than = "gt"
    greater_than_or_equals = "ge"
    not_equals = "not_eq"
    string_equals = "str_eq"
    length_equals = "len_eq"
    length_greater_than = "len_gt"
    length_greater_than_or_equals = 'len_ge'
    length_less_than = "len_lt"
    length_less_than_or_equals = 'len_le'
    contains = "contains"
    contained_by = 'contained_by'
    startswith = 'startswith'
    endswith = 'endswith'


class LoginApi(Enum):
    # 买量登录
    LOGIN_PATH = "/authorize"
    # 发行登录
    FX_LOGIN_PATH = "/user/authorize"
    # 通用 2.0
    BASE_LOGIN_PATH = "/api/users/v1.0/authorizations"


class PayApi(Enum):
    ...


class OrderApi(Enum):
    # 买量通用下单
    ORDER_PATH = "/api/v1/order/init"
    # 发行通用下单
    FX_ORDER_PATH = "/order/"
    FX_ORDER_V2_PATH = "/v2/sdk/order"
    # 微信小游戏下单
    WX_ORDER_PATH = "/v2/payments"


class InitApi(Enum):
    INIT_PATH = "/activate/init"
    FX_INIT_PATH = "/v2/sdkinit"


class GameApi(Enum):
    # 进登录服
    GAME_LOGIN_PATH = "/game/server_access"
    # 进游戏服
    ROLE_LOGIN_PATH = "/game/v1.0/role_login"
    FX_ROLE_LOGIN_PATH = "/game/game_access"
    # 升级
    ROLE_LVLUP_PATH = "/game/v1.0/role_lvlup"
    FX_ROLE_LVLUP_PATH = "/role/role_change"


class WeChatApi(Enum):
    # 敏感词检测
    WX_MSG_CHECK_PATH = "/api/v1/wxgame/msg/check"


class TtApi(Enum):
    # 内购
    PURCHASE_PATH = "/config"
    # 敏感词检测
    TT_MSG_CHECK_PATH = "/api/v1/dymgame/msg/check"
    # 一次性订阅上报
    SUBSCRIBE_PATH = "/api/v1/dymgame/subscribe/report"


class OtherApi(Enum):
    INIT_PATH = "/activate/init"

