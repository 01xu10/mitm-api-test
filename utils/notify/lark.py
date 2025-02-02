# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/4/7 14:51
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : lark.py
# ----------------------
import base64
import hashlib
import hmac
import json
import logging
import time
import datetime
import requests
import urllib3

from utils import config
from utils.other_tools.get_local_ip import get_host_ip
from utils.other_tools.models import TestMetrics

urllib3.disable_warnings()

try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError

timestamp = str(int(time.time()))[:10]


def gen_sign(t, secret):
    # 拼接timestamp和secret
    string_to_sign = '{}\n{}'.format(t, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')

    return sign


def is_not_null_and_blank_str(content):
    """
  非空字符串
  :param content: 字符串
  :return: 非空 - True，空 - False
  """
    return bool(content and content.strip())


class FeiShuTalkChatBot:
    """飞书机器人通知"""

    def __init__(self, metrics: TestMetrics):
        self.metrics = metrics

    def send_text(self, msg: str):
        """
    消息类型为text类型
    :param msg: 消息内容
    :return: 返回消息发送结果
    """
        data = {"msg_type": "text", "at": {}}
        if is_not_null_and_blank_str(msg):  # 传入msg非空
            data["content"] = {"text": msg}
        else:
            logging.error("text类型，消息内容不能为空！")
            raise ValueError("text类型，消息内容不能为空！")

        logging.debug('text类型：%s', data)
        return self.post()

    def post(self):
        """
    发送消息（内容UTF-8编码）
    :return: 返回消息发送结果
    """
        rich_text = {
            "timestamp": timestamp,
            "sign": gen_sign(timestamp, config.lark.secret),
            "email": "chenxingxu@izkun.com",
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": f"【{config.project_name}】",
                        "content": [
                            [
                                {
                                    "tag": "a",
                                    "text": "测试报告",
                                    "href": f"http://{get_host_ip()}:{config.allure_port}/index.html"
                                },
                                # {
                                #     "tag": "at",
                                #     "user_id": "ou_18eac85d35a26f989317ad4f02e8bbbb",
                                # }
                            ],
                            [
                                {
                                    "tag": "text",
                                    "text": "测试  人员 : "
                                },
                                {
                                    "tag": "text",
                                    "text": config.tester_name
                                }
                            ],
                            [
                                {
                                    "tag": "text",
                                    "text": "运行  环境 : "
                                },
                                {
                                    "tag": "text",
                                    "text": config.env
                                }
                            ],
                            [{
                                "tag": "text",
                                "text": "成   功   率 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.pass_rate} %"
                                }],  # 成功率

                            [{
                                "tag": "text",
                                "text": "成功用例数 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.passed}"
                                }],  # 成功用例数

                            [{
                                "tag": "text",
                                "text": "失败用例数 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.failed}"
                                }],  # 失败用例数
                            [{
                                "tag": "text",
                                "text": "异常用例数 : "
                            },
                                {
                                    "tag": "text",
                                    "text": f"{self.metrics.failed}"
                                }],  # 损坏用例数
                            [
                                {
                                    "tag": "text",
                                    "text": "时  间 : "
                                },
                                {
                                    "tag": "text",
                                    "text": f"{datetime.datetime.now().strftime('%Y-%m-%d')}"
                                }
                            ],

                            # [
                            #     {
                            #         "tag": "img",
                            #         "image_key": "",
                            #         "width": 300,
                            #         "height": 300
                            #     }
                            # ]
                        ]
                    }
                }
            }
        }
        headers = {'Content-Type': 'application/json; charset=utf-8'}

        post_data = json.dumps(rich_text)
        response = requests.post(
            config.lark.webhook,
            headers=headers,
            data=post_data,
            verify=False
        )
        result = response.json()

        if result.get('StatusCode') != 0:
            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            result_msg = result['errmsg'] if result.get('errmsg', False) else '未知异常'
            error_data = {
                "msgtype": "text",
                "text": {
                    "content": f"[注意-自动通知]飞书机器人消息发送失败，时间：{time_now}，"
                               f"原因：{result_msg}，请及时跟进，谢谢!"
                },
                "at": {
                    "isAtAll": False
                }
            }
            logging.error("消息发送失败，自动通知：%s", error_data)
            requests.post(config.lark.webhook, headers=headers, data=json.dumps(error_data))
        return result


