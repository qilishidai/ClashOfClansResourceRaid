import multiprocessing
import sys
import time
from tkinter import Tk

from 界面程序 import 界面程序


def 关闭窗口(主界面):
    print("用户点击了关闭按钮")
    主界面.恢复操作模拟器()
    主界面.停止脚本()
    sys.exit()


if __name__ == '__main__':

    multiprocessing.freeze_support()#用于解决打包后重复执行创建窗口命令
    根窗口 = Tk()
    根窗口.geometry("620x300+700+400")
    根窗口.title("部落冲突夜世界辅助")

    我的程序 = 界面程序(根窗口)
    根窗口.protocol("WM_DELETE_WINDOW", lambda: 关闭窗口(我的程序))
    根窗口.mainloop()


