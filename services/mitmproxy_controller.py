# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/3/7 18:28
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : mitmproxy_controller.py
# ----------------------
import tkinter as tk
import subprocess
import threading
from common.setting import ensure_path_sep


class MitmproxyController:
    def __init__(self):
        # self.app = app
        self.mitmproxy_process = None

    def start_mitmproxy(self):
        self.mitmproxy_process = subprocess.Popen(["mitmdump", "-s", ensure_path_sep("\\services\\mitm.py"), "-p", "8888", "--ssl-insecure", "--quiet"])

        # def read_output(pipe):
        #     for line in iter(pipe.readline, ''):
        #         self.app.output_text.insert(tk.END, line)
        #         self.app.output_text.see(tk.END)
        #     pipe.close()
        #
        #     # 新增: 创建线程来读取标准输出和标准错误
        #
        # threading.Thread(target=read_output, args=(self.mitmproxy_process.stdout,)).start()
        # threading.Thread(target=read_output, args=(self.mitmproxy_process.stderr,)).start()

    def stop_mitmproxy(self):
        if self.mitmproxy_process:
            self.mitmproxy_process.terminate()
            self.mitmproxy_process.wait()
            self.mitmproxy_process = None