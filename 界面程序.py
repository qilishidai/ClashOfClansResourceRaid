import ctypes
import datetime
import json
import multiprocessing
import os
import queue

from tkinter import *
from tkinter import ttk

import psutil
import win32api
import win32com
import win32con

import 脚本主进程入口

import tkinter as tk
from 模拟器状态 import 雷电模拟器


class 工具提示:
    def __init__(self, 控件, 文本):
        self.控件 = 控件
        self.文本 = 文本
        self.控件.bind("<Enter>", self.进入)
        self.控件.bind("<Leave>", self.离开)

    def 进入(self, 事件):
        self.提示框 = tk.Toplevel(self.控件)
        x, y, _, _ = self.控件.bbox("insert")
        x += self.控件.winfo_rootx() + 25
        y += self.控件.winfo_rooty() + 25
        self.提示框.wm_overrideredirect(True)
        self.提示框.wm_geometry(f"+{x}+{y}")
        标签 = tk.Label(self.提示框, text=self.文本, background="#ffffe0", relief="solid", borderwidth=1)
        标签.pack(ipadx=1)

    def 离开(self, 事件):
        if hasattr(self, '提示框'):
            self.提示框.destroy()

    def leave(self, event):
        if hasattr(self, 'tip'):
            self.tip.destroy()


class 设置窗口(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("设置")
        self.geometry("350x300+700+400")

        self.settings_file = "settings.json"
        self.settings = self.加载设置(self.settings_file)

        self.创建设置选项()
        self.载入设置()

    def 创建设置选项(self):
        Label(self, text="雷电模拟器索引").grid(row=0, column=0, sticky=W, padx=10, pady=5)
        self.雷电模拟器索引 = Entry(self)
        self.雷电模拟器索引.grid(row=0, column=1, padx=10, pady=5)
        工具提示(self.雷电模拟器索引,
                 "在雷电多开器中创建了多个模拟器，此处应填写要启动的模拟器的索引。例如，如果多开器页面中第一个模拟器索引为0，第二个为1，依此类推。")

        Label(self, text="部落冲突包名").grid(row=1, column=0, sticky=W, padx=10, pady=5)
        self.包名选择 = ttk.Combobox(self, values=["国服", "国际服", "自定义"])
        self.包名选择.grid(row=1, column=1, padx=10, pady=5)
        self.包名选择.bind("<<ComboboxSelected>>", self.更新包名输入框)
        工具提示(self.包名选择,
                 "注意:错误的选择会导致无法打开部落冲突,如果你模拟器打开了,而游戏没打开,请检查这一项设置")
        self.自定义包名 = Entry(self)
        self.自定义包名.grid(row=2, column=1, padx=10, pady=5)
        self.自定义包名.grid_remove()

        self.一直执行 = BooleanVar()
        self.一直执行_check = Checkbutton(self, text="一直执行", variable=self.一直执行,
                                          command=self.更新一直执行输入框)
        self.一直执行_check.grid(row=3, columnspan=1, padx=10, pady=5)

        self.需要执行多少秒_label = Label(self, text="需要执行多少秒")
        self.需要执行多少秒_label.grid(row=4, column=0, sticky=W, padx=10, pady=5)
        self.需要执行多少秒 = Entry(self)
        self.需要执行多少秒.grid(row=4, column=1, padx=10, pady=5)
        工具提示(self.需要执行多少秒,
                 "如果你需要按照小时来设置定时,计算方法为你要挂机的小时数乘以3600,")

        self.是否开启刷墙 = BooleanVar()
        self.是否开启刷墙_check = Checkbutton(self, text="是否开启刷墙", variable=self.是否开启刷墙,
                                              command=self.更新刷墙输入框)
        self.是否开启刷墙_check.grid(row=3, columnspan=2, padx=10, pady=5)

        self.循环最大等待秒数_label = Label(self, text="循环最大等待秒数")

        self.循环最大等待秒数_label.grid(row=6, column=0, sticky=W, padx=10, pady=5)
        self.循环最大等待秒数 = Entry(self)
        工具提示(self.循环最大等待秒数,
                 "这个设置决定了游戏上线时脚本等待的最大时间,卡白云的最大等待时间.如果你不知道你在做什么,请不要动这个设置")
        self.循环最大等待秒数.grid(row=6, column=1, padx=10, pady=5)

        self.至少多少金币开始刷墙_label = Label(self, text="至少多少金币开始刷墙")
        self.至少多少金币开始刷墙_label.grid(row=7, column=0, sticky=W, padx=10, pady=5)
        self.至少多少金币开始刷墙 = Entry(self)
        self.至少多少金币开始刷墙.grid(row=7, column=1, padx=10, pady=5)

        self.至少多少圣水开始刷墙_label = Label(self, text="至少多少圣水开始刷墙")
        self.至少多少圣水开始刷墙_label.grid(row=8, column=0, sticky=W, padx=10, pady=5)
        self.至少多少圣水开始刷墙 = Entry(self)
        self.至少多少圣水开始刷墙.grid(row=8, column=1, padx=10, pady=5)

        Button(self, text="保存", command=self.保存设置).grid(row=9, columnspan=2, pady=10)
        Label(self, text="注意:保存的设置会在下一次启动脚本时生效").grid(row=10, columnspan=2, )

    def 更新包名输入框(self, event):
        if self.包名选择.get() == "自定义":
            self.自定义包名.grid()
        else:
            self.自定义包名.grid_remove()

    def 更新一直执行输入框(self):
        if self.一直执行.get():
            self.需要执行多少秒_label.grid_remove()
            self.需要执行多少秒.grid_remove()
        else:
            self.需要执行多少秒_label.grid()
            self.需要执行多少秒.grid()

    def 更新刷墙输入框(self):
        if self.是否开启刷墙.get():
            self.至少多少金币开始刷墙_label.grid()
            self.至少多少金币开始刷墙.grid()
            self.至少多少圣水开始刷墙_label.grid()
            self.至少多少圣水开始刷墙.grid()
        else:
            self.至少多少金币开始刷墙_label.grid_remove()
            self.至少多少金币开始刷墙.grid_remove()
            self.至少多少圣水开始刷墙_label.grid_remove()
            self.至少多少圣水开始刷墙.grid_remove()

    def 保存设置(self):
        # 根据选择的包名设置
        if self.包名选择.get() == "国服":
            部落冲突包名 = "com.tencent.tmgp.supercell.clashofclans"
        elif self.包名选择.get() == "国际服":
            部落冲突包名 = "com.supercell.clashofclans"
        else:
            部落冲突包名 = self.自定义包名.get()

        # 保存设置到文件
        设置参数 = {
            "雷电模拟器索引": self.雷电模拟器索引.get(),
            "部落冲突包名": 部落冲突包名,
            "一直执行": self.一直执行.get(),
            "需要执行多少秒": int(self.需要执行多少秒.get()) if not self.一直执行.get() else None,
            "是否开启刷墙": self.是否开启刷墙.get(),
            "循环最大等待秒数": int(self.循环最大等待秒数.get()),
            "至少多少金币开始刷墙": int(self.至少多少金币开始刷墙.get()) if self.是否开启刷墙.get() else None,
            "至少多少圣水开始刷墙": int(self.至少多少圣水开始刷墙.get()) if self.是否开启刷墙.get() else None
        }
        with open(self.settings_file, "w") as file:
            json.dump(设置参数, file)

        print("保存设置:", 设置参数)
        # messagebox.showinfo("标题", "下一次启动脚本时生效,配置为\n"+str(设置参数))
        # 关闭窗口
        self.destroy()

    @staticmethod
    def 加载设置(文件路径名="settings.json"):
        if os.path.exists(文件路径名):
            with open(文件路径名, "r") as file:
                return json.load(file)
        return {}

    def 载入设置(self):
        if "雷电模拟器索引" in self.settings:
            self.雷电模拟器索引.insert(0, self.settings["雷电模拟器索引"])
        if "部落冲突包名" in self.settings:
            if self.settings["部落冲突包名"] == "com.tencent.tmgp.supercell.clashofclans":
                self.包名选择.current(0)
            elif self.settings["部落冲突包名"] == "com.supercell.clashofclans":
                self.包名选择.current(1)
            else:
                self.包名选择.current(2)
                self.自定义包名.insert(0, self.settings["部落冲突包名"])
                self.自定义包名.grid()
        if "一直执行" in self.settings:
            self.一直执行.set(self.settings["一直执行"])
            self.更新一直执行输入框()
        if "需要执行多少秒" in self.settings and not self.settings["一直执行"]:
            self.需要执行多少秒.insert(0, self.settings["需要执行多少秒"])
        if "是否开启刷墙" in self.settings:
            self.是否开启刷墙.set(self.settings["是否开启刷墙"])
            self.更新刷墙输入框()
        if "循环最大等待秒数" in self.settings:
            self.循环最大等待秒数.insert(0, self.settings["循环最大等待秒数"])
        if "至少多少金币开始刷墙" in self.settings and self.settings["是否开启刷墙"]:
            self.至少多少金币开始刷墙.insert(0, self.settings["至少多少金币开始刷墙"])
        if "至少多少圣水开始刷墙" in self.settings and self.settings["是否开启刷墙"]:
            self.至少多少圣水开始刷墙.insert(0, self.settings["至少多少圣水开始刷墙"])


class 界面程序(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.pack(fill=BOTH, expand=True)
        self.创建窗口()
        self.脚本进程 = None
        self.运行状态消息队列 = multiprocessing.Queue()

        # 定时检查队列中的消息
        self.检查消息()
        self.暂停状态 = False

        # 加载注册com组件的dll
        免注册dll = ctypes.windll.LoadLibrary(R"op-0.4.5_with_model/tools.dll")
        # 调用免注册dll中的setupA函数注册opdll
        是否注册成功 = 免注册dll.setupA(bytes(R"op-0.4.5_with_model/op_x64.dll", encoding="utf-8"))
        # 创建op对象
        self.op = win32com.client.Dispatch("op.opsoft")

    def 创建窗口(self):
        self.菜单栏 = Menu(self.master)
        self.菜单栏.add_command(label="启动", command=self.启动或恢复脚本)
        self.菜单栏.add_command(label="暂停", command=self.暂停脚本)
        self.菜单栏.add_command(label="停止", command=self.停止脚本,state=tk.DISABLED)

        # 更多子菜单,并添加相关选项
        self.更多子菜单 = Menu(self.菜单栏, tearoff=0)

        # self.更多子菜单.add_command(label="隐藏模拟器", command=self.隐藏模拟器,state=tk.DISABLED)
        self.更多子菜单.add_command(label="隐藏模拟器", command=self.隐藏模拟器)
        self.更多子菜单.add_command(label="显示模拟器", command=self.显示模拟器)

        self.更多子菜单.add_separator()  # 添加分割线
        self.更多子菜单.add_command(label="禁止操作模拟器", command=self.禁止操作模拟器)
        self.更多子菜单.add_command(label="恢复操作模拟器", command=self.恢复操作模拟器)
        self.更多子菜单.add_separator()  # 添加分割线
        self.更多子菜单.add_command(label="设置", command=self.打开设置窗口)  # 添加设置选项

        # 将更多子菜单添加到菜单栏
        self.菜单栏.add_cascade(label="更多", menu=self.更多子菜单)

        # 将我们建立好的整一个菜单栏在root窗口中显示
        self.master.config(menu=self.菜单栏)

        Label(self, text="当前运行状态").grid(row=0, column=0)

        # 创建滚动条并关联到列表框
        self.滚动条 = Scrollbar(self)
        self.列表框 = Listbox(self, width=50, yscrollcommand=self.滚动条.set)
        self.滚动条.config(command=self.列表框.yview)

        # 使用grid布局
        self.列表框.grid(row=1, column=0, sticky=N + S + E + W)
        self.滚动条.grid(row=1, column=1, sticky=N + S)

        # 配置行和列的权重，使列表框和滚动条可以扩展
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.打印状态("欢迎使用脚本，具体使用步骤如下:\n")
        self.打印状态("1.在模拟器中安装部落冲突并登录你的账号，确保进入**夜世界**。")
        self.打印状态("2.模拟器分辨率设置宽800，高600，dpi160\n")
        self.打印状态("3.部落冲突中设置配兵推荐全亡灵，或者全弓箭手。主要是还没写其它兵种判断（偷懒）")
        self.打印状态("4.点击'更多'的'设置'可以对脚本进行配置\n")
        self.打印状态("5.点击'启动'按钮运行脚本\n")

    def 打印状态(self, 打印的内容):
        current_time = datetime.datetime.now()
        # 格式化当前时间，精确到秒
        当前时间 = current_time.strftime("%Y-%m-%d %H:%M:%S    ")
        打印的内容 = 当前时间 + 打印的内容
        # print(打印的内容)
        # 检查列表框中的项数是否超过500，如果是则删除最早的一项
        if self.列表框.size() >= 500:
            self.列表框.delete(0)
        # 插入新项到列表框
        self.列表框.insert('end', 打印的内容)
        # 滚动到列表框的最底部
        self.列表框.yview_moveto(1)

    def 检查消息(self):
        while not self.运行状态消息队列.empty():
            消息 = self.运行状态消息队列.get()
            self.打印状态(消息)
        self.after(100, self.检查消息)  # 每100毫秒检查一次消息

    def 启动或恢复脚本(self):

        self.设置参数 = 设置窗口.加载设置()

        if self.脚本进程 is None or not self.脚本进程.is_alive():
            self.脚本进程 = multiprocessing.Process(target=脚本主进程入口.窗口调用,
                                                    args=(self.运行状态消息队列, self.设置参数,))

            self.脚本进程.start()
            self.打印状态(f"启动了脚本进程，进程PID: {self.脚本进程.pid}")
            self.暂停状态 = False  # 启动脚本时重置暂停状态
            # self.禁止操作模拟器()
        elif self.暂停状态:
            self.打印状态("恢复脚本")
            进程 = psutil.Process(self.脚本进程.pid)
            进程.resume()
            self.暂停状态 = False
        else:
            self.打印状态("脚本已启动且未暂停")

    def 暂停脚本(self):

        if self.脚本进程 is not None and self.脚本进程.is_alive():
            self.恢复操作模拟器()
            self.打印状态("暂停脚本")
            进程 = psutil.Process(self.脚本进程.pid)
            进程.suspend()
            self.暂停状态 = True
        else:
            self.打印状态("脚本未启动或已停止")

    def 停止脚本(self):

        if self.脚本进程 is not None:
            self.恢复操作模拟器()
            self.脚本进程.terminate()
            self.脚本进程.join()  # 确保进程终止
            self.打印状态(f"停止脚本，进程PID: {self.脚本进程.pid}")
        else:
            self.打印状态("脚本未启动")

    def 隐藏模拟器(self):

        # 获取屏幕宽高
        屏幕宽度 = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        屏幕高度 = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        配置信息 = 设置窗口.加载设置()
        雷电模拟器索引 = int(配置信息.get("雷电模拟器索引", "0"))
        雷电模拟器实例 = 雷电模拟器(雷电模拟器索引)
        if 雷电模拟器实例.模拟器是否启动():
            #因为直接隐藏后台键盘操作会失效，所以移动到屏幕右下角藏起来
            # self.op.SetWindowState(雷电模拟器实例.取顶层窗口句柄(), 6)
            self.op.MoveWindow(雷电模拟器实例.取顶层窗口句柄(),屏幕宽度, 屏幕高度)
            self.打印状态("隐藏模拟器")
        else:
            self.打印状态(f"{雷电模拟器实例.取模拟器名称()},未启动")



    def 显示模拟器(self):
        配置信息 = 设置窗口.加载设置()
        雷电模拟器索引 = int(配置信息.get("雷电模拟器索引", "0"))
        雷电模拟器实例 = 雷电模拟器(雷电模拟器索引)
        if 雷电模拟器实例.模拟器是否启动():
            self.op.MoveWindow(雷电模拟器实例.取顶层窗口句柄(), 100, 100)
            self.op.SetWindowState(雷电模拟器实例.取顶层窗口句柄(), 7)
            self.打印状态("显示模拟器")
        else:
            self.打印状态(f"{雷电模拟器实例.取模拟器名称()},未启动")



        # if self.op is None:
        #     self.打印状态("未成功绑定窗口")
        # else:
        #     self.op.MoveWindow(self.顶层窗口句柄, 100, 100)
        #     self.op.SetWindowState(self.顶层窗口句柄, 7)

    def 禁止操作模拟器(self):
        配置信息 = 设置窗口.加载设置()
        雷电模拟器索引 = int(配置信息.get("雷电模拟器索引", "0"))
        雷电模拟器实例 = 雷电模拟器(雷电模拟器索引)
        if 雷电模拟器实例.模拟器是否启动():
            self.op.SetWindowState(雷电模拟器实例.取顶层窗口句柄(), 10)
            self.打印状态("禁止操作模拟器")
        else:
            self.打印状态(f"{雷电模拟器实例.取模拟器名称()},未启动")

        # if self.脚本进程 is not None and self.脚本进程.is_alive():
        #     self.禁用启用模拟器关闭监听线程消息队列.put("禁止操作模拟器")
        # else:
        #     self.打印状态("脚本进程未启动")

    def 恢复操作模拟器(self):

        配置信息 = 设置窗口.加载设置()
        雷电模拟器索引 = int(配置信息.get("雷电模拟器索引", "0"))
        雷电模拟器实例 = 雷电模拟器(雷电模拟器索引)
        if 雷电模拟器实例.模拟器是否启动():
            self.op.SetWindowState(雷电模拟器实例.取顶层窗口句柄(), 11)
            self.打印状态("恢复操作模拟器")
        else:
            self.打印状态(f"{雷电模拟器实例.取模拟器名称()},未启动")

        # if self.脚本进程 is not None and self.脚本进程.is_alive():
        #     self.禁用启用模拟器关闭监听线程消息队列.put("恢复操作模拟器")
        # else:
        #     self.打印状态("脚本进程未启动")

    def 打开设置窗口(self):
        设置窗口(self)
