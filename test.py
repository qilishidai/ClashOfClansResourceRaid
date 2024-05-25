import datetime
import queue
import sys
import threading
from tkinter import *
from tkinter import ttk

from mainGUI import 窗口调用
import json
import os
from tkinter import *
from tkinter import ttk

class 设置窗口(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("设置")
        self.geometry("400x350")

        self.settings_file = "settings.json"
        self.settings = self.加载设置()

        self.创建设置选项()
        self.载入设置()

    def 创建设置选项(self):
        Label(self, text="雷电模拟器索引").grid(row=0, column=0, sticky=W, padx=10, pady=5)
        self.雷电模拟器索引 = Entry(self)
        self.雷电模拟器索引.grid(row=0, column=1, padx=10, pady=5)

        Label(self, text="部落冲突包名").grid(row=1, column=0, sticky=W, padx=10, pady=5)
        self.包名选择 = ttk.Combobox(self, values=["国服", "国际服", "自定义"])
        self.包名选择.grid(row=1, column=1, padx=10, pady=5)
        self.包名选择.bind("<<ComboboxSelected>>", self.更新包名输入框)

        self.自定义包名 = Entry(self)
        self.自定义包名.grid(row=2, column=1, padx=10, pady=5)
        self.自定义包名.grid_remove()

        self.一直执行 = BooleanVar()
        self.一直执行_check = Checkbutton(self, text="一直执行", variable=self.一直执行, command=self.更新一直执行输入框)
        self.一直执行_check.grid(row=3, columnspan=1, padx=10, pady=5)

        self.需要执行多少秒_label = Label(self, text="需要执行多少秒")
        self.需要执行多少秒_label.grid(row=4, column=0, sticky=W, padx=10, pady=5)
        self.需要执行多少秒 = Entry(self)
        self.需要执行多少秒.grid(row=4, column=1, padx=10, pady=5)

        self.是否开启刷墙 = BooleanVar()
        self.是否开启刷墙_check = Checkbutton(self, text="是否开启刷墙", variable=self.是否开启刷墙, command=self.更新刷墙输入框)
        self.是否开启刷墙_check.grid(row=3, columnspan=2, padx=10, pady=5)

        self.循环最大等待秒数_label = Label(self, text="循环最大等待秒数")
        self.循环最大等待秒数_label.grid(row=6, column=0, sticky=W, padx=10, pady=5)
        self.循环最大等待秒数 = Entry(self)
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
        # 关闭窗口
        self.destroy()

    def 加载设置(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as file:
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
        self.queue = queue.Queue()
        self.op = None
        self.顶层窗口句柄 = None
        self.绑定窗口句柄 = None
        self.要求脚本停止 = False
        self.脚本线程 = None

    def 创建窗口(self):
        self.菜单栏 = Menu(self.master)
        self.菜单栏.add_command(label="启动", command=self.启动脚本)
        self.菜单栏.add_command(label="停止", command=self.停止脚本)

        # 更多子菜单,并添加相关选项
        self.更多子菜单 = Menu(self.菜单栏, tearoff=0)
        self.更多子菜单.add_command(label="隐藏模拟器", command=self.隐藏模拟器)
        self.更多子菜单.add_command(label="显示模拟器", command=self.显示模拟器)
        self.更多子菜单.add_separator()  # 添加分割线
        self.更多子菜单.add_command(label="禁止操作模拟器", command=self.禁止操作模拟器)
        self.更多子菜单.add_command(label="恢复操作模拟器", command=self.恢复操作模拟器)
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

    def 打印状态(self, 打印的内容):
        current_time = datetime.datetime.now()
        当前时间 = current_time.strftime("%Y-%m-%d %H:%M:%S    ")
        打印的内容 = 当前时间 + 打印的内容
        if self.列表框.size() >= 500:
            self.列表框.delete(0)
        self.列表框.insert('end', 打印的内容)
        self.列表框.yview_moveto(1)

    def 启动脚本(self):
        if self.脚本线程 is None:
            self.要求脚本停止 = False
            self.脚本线程 = threading.Thread(target=self.调用窗口函数, args=(self, self.queue))
            self.脚本线程.start()
            print("启动线程")
        else:
            if not self.脚本线程.is_alive():
                self.要求脚本停止 = False
                self.脚本线程 = threading.Thread(target=self.调用窗口函数, args=(self, self.queue))
                self.脚本线程.start()
            else:
                self.要求脚本停止 = False
                self.打印状态("脚本线程已存在,已通知脚本,继续执行")

    def 调用窗口函数(self, window, queue):
        try:
            窗口调用(window)
        except Exception as e:
            queue.put(f"Error: {e}")

    def 停止脚本(self):
        if self.脚本线程.is_alive():
            self.脚本线程.terminate()
            self.要求脚本停止 = True
            self.打印状态("已通知脚本进程停止脚本,打完毕本场鱼即刻停止")
        else:
            self.打印状态("别乱玩,你都没启动脚本")

    def 隐藏模拟器(self):
        if self.op is None:
            self.打印状态("未成功绑定窗口")
        else:
            self.op.MoveWindow(self.顶层窗口句柄, 1920, 1080)

    def 显示模拟器(self):
        if self.op is None:
            self.打印状态("未成功绑定窗口")
        else:
            self.op.MoveWindow(self.顶层窗口句柄, 100, 100)
            self.op.SetWindowState(self.顶层窗口句柄, 7)

    def 禁止操作模拟器(self):
        if self.op is None:
            self.打印状态("未成功绑定窗口")
        else:
            self.op.SetWindowState(self.顶层窗口句柄, 10)
            self.打印状态("禁止操作模拟器")

    def 恢复操作模拟器(self):
        if self.op is None:
            self.打印状态("未成功绑定窗口")
        else:
            self.op.SetWindowState(self.顶层窗口句柄, 11)
            self.打印状态("恢复操作模拟器")

    def 打开设置窗口(self):
        设置窗口(self)


def 关闭窗口():
    print("用户点击了关闭按钮")
    sys.exit()

根窗口 = Tk()
根窗口.geometry("600x250+700+400")
根窗口.title("部落冲突夜世界辅助")
根窗口.protocol("WM_DELETE_WINDOW", 关闭窗口)

我的程序 = 界面程序(根窗口)
根窗口.mainloop()
