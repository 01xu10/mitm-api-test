# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2024/3/7 18:29
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : app.py
# ----------------------
import tkinter as tk
import threading
from tkinter.scrolledtext import ScrolledText

from services.mitmproxy_controller import MitmproxyController
from common.setting import ensure_path_sep
import subprocess


def run_pytest(option):
    subprocess.call(['python', ensure_path_sep('\\services\\pytest_runner.py'), '--option', option])


class MitmProxyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("游戏对接测试工具")
        self.root.geometry("360x270")
        self.radio_var = tk.StringVar(value='jssdk')
        self.mitmproxy_controller = MitmproxyController()
        self.stop_button = None
        self.start_button = None
        # self.output_text = None
        self.setup_ui()

    def setup_ui(self):
        # 定义单选框
        options = {
            'jssdk': 'jssdk',
            'androidsdk': 'androidsdk',
            'wechatsdk': 'wechatsdk'
        }
        for index, (value, text) in enumerate(options.items()):
            radio_button = tk.Radiobutton(self.root, text=text, variable=self.radio_var, value=value)
            radio_button.place(x=20, y=150 + 30 * index)

        button_width = 110
        button_height = 30
        button_y_offset = 50
        button_spacing = 50

        # 创建按钮
        self.start_button = tk.Button(self.root, text="开始测试", command=self.on_start_clicked)
        self.start_button.place(x=(360 - button_width) / 2, y=button_y_offset, height=button_height, width=button_width)

        self.stop_button = tk.Button(self.root, text="结束测试", state='disabled', command=self.on_stop_clicked)
        self.stop_button.place(x=(360 - button_width) / 2, y=button_y_offset + button_spacing, height=button_height,
                               width=button_width)

        # # 新增: 创建一个用于显示输出的文本框
        # self.output_text = ScrolledText(self.root, wrap=tk.WORD, width=50, height=10)
        # self.output_text.place(x=10, y=280, width=340, height=120)

    def on_start_clicked(self):
        self.mitmproxy_controller.start_mitmproxy()
        self.start_button['state'] = 'disabled'
        self.stop_button['state'] = 'normal'

    def on_stop_clicked(self):
        self.mitmproxy_controller.stop_mitmproxy()
        self.stop_button['state'] = 'disabled'
        selected_option = self.radio_var.get()  # 获取选中的单选框的值
        pytest_thread = threading.Thread(target=run_pytest, args=(selected_option,))
        pytest_thread.start()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = MitmProxyApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
