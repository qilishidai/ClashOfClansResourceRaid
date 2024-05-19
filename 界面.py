import ctypes
import datetime
import queue
import sys
import threading
from tkinter import *

import win32com

from mainGUI import 窗口调用
#
# # 加载注册com组件的dll
# 免注册dll = ctypes.windll.LoadLibrary(R"op-0.4.5_with_model/tools.dll")
# # 调用免注册dll中的setupA函数注册opdll
# 是否注册成功 = 免注册dll.setupA(bytes(R"op-0.4.5_with_model/op_x64.dll", encoding="utf-8"))
# # 创建op对象
# op = win32com.client.Dispatch("op.opsoft")

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
        # self.菜单栏.add_separator()
        # self.菜单栏.add_command(label="隐藏模拟器", command=self.隐藏模拟器)
        # self.菜单栏.add_command(label="显示模拟器", command=self.显示模拟器)
        # self.菜单栏.add_separator()
        # self.菜单栏.add_command(label="禁止操作模拟器", command=self.禁止操作模拟器)
        # self.菜单栏.add_command(label="恢复操作模拟器", command=self.恢复操作模拟器)

        # 更多子菜单,并添加相关选项
        self.更多子菜单 = Menu(self.菜单栏, tearoff=0)
        self.更多子菜单.add_command(label="隐藏模拟器", command=self.隐藏模拟器)
        self.更多子菜单.add_command(label="显示模拟器", command=self.显示模拟器)
        self.更多子菜单.add_separator()  # 添加分割线
        self.更多子菜单.add_command(label="禁止操作模拟器", command=self.禁止操作模拟器)
        self.更多子菜单.add_command(label="恢复操作模拟器", command=self.恢复操作模拟器)

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

        # Button(self, text="添加列表项", command=self.添加列表项).grid(row=2, column=0, columnspan=2)



    def 打印状态(self, 打印的内容):
        current_time = datetime.datetime.now()
        # 格式化当前时间，精确到秒
        当前时间 = current_time.strftime("%Y-%m-%d %H:%M:%S    ")
        打印的内容=当前时间+打印的内容
        # print(打印的内容)
        # 检查列表框中的项数是否超过500，如果是则删除最早的一项
        if self.列表框.size() >= 500:
            self.列表框.delete(0)
        # 插入新项到列表框
        self.列表框.insert('end', 打印的内容)
        # 滚动到列表框的最底部
        self.列表框.yview_moveto(1)

    def 启动脚本(self):
        if self.脚本线程 is None:
            self.要求脚本停止 = False
            self.脚本线程=threading.Thread(target=self.调用窗口函数, args=(self, self.queue))
            self.脚本线程.start()
            print("启动线程")
        else:
            if self.脚本线程.is_alive() is False:
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


def 关闭窗口():
    print("用户点击了关闭按钮")
    sys.exit()
    exi
    # 这里可以添加你想要的关闭操作

根窗口 = Tk()
根窗口.geometry("600x250+700+400")
根窗口.title("部落冲突夜世界辅助")

根窗口.protocol("WM_DELETE_WINDOW", 关闭窗口)

我的程序 = 界面程序(根窗口)
根窗口.mainloop()
