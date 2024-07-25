import random
import winreg

from win32com.client import Dispatch  # import moudles 第一次运行python -m pip install pywin32
import time
import ctypes
from ctypes import *
import subprocess  #系统命令
import os

from 升级 import 升级建筑


def get_registry_value(key, sub_key, value_name):
    try:
        # 打开注册表项
        reg_key = winreg.OpenKey(key, sub_key)
        # 读取注册表值
        value, value_type = winreg.QueryValueEx(reg_key, value_name)
        # 关闭注册表项
        winreg.CloseKey(reg_key)
        return value
    except FileNotFoundError:
        print("指定的注册表路径不存在")
    except Exception as e:
        print("发生错误:", e)


def 将雷电模拟器命令行返回信息解析为字典(text):
    """
            将给定的文本解析为字典。

            参数：
            text : str
                包含文本内容的字符串，每行代表一个条目，条目之间使用换行符分隔。
                每个条目应包含逗号分隔的值，分别为索引、标题、顶层窗口句柄、绑定窗口句柄、
                是否进入 Android、进程 PID、VBox 进程 PID、宽度、高度、DPI。

            返回值：
            dict
                包含解析后内容的字典。字典的键为索引，值为包含条目内容的字典。
                条目字典包含以下键值对：
                    - "标题"：标题字符串
                    - "顶层窗口句柄"：顶层窗口句柄整数
                    - "绑定窗口句柄"：绑定窗口句柄整数
                    - "是否进入Android"：是否进入 Android 布尔值
                    - "进程PID"：进程 PID 整数
                    - "VBox进程PID"：VBox 进程 PID 整数
                    - "宽度"：宽度整数
                    - "高度"：高度整数
                    - "DPI"：DPI 整数
            """
    # 初始化一个空字典
    result = {}

    # 按行分割文本
    lines = text.strip().split('\n')

    # 遍历每一行，将内容存储到字典中
    for line in lines:
        parts = line.split(',')
        index = int(parts[0])
        title = parts[1]
        top_window_handle = int(parts[2])
        bound_window_handle = int(parts[3])
        enter_android = bool(int(parts[4]))
        process_pid = int(parts[5])
        vbox_process_pid = int(parts[6])
        width = int(parts[7])
        height = int(parts[8])
        dpi = int(parts[9])

        # 将每一行的内容存储到字典中
        result[index] = {
            "标题": title,
            "顶层窗口句柄": top_window_handle,
            "绑定窗口句柄": bound_window_handle,
            "是否进入Android": enter_android,
            "进程PID": process_pid,
            "VBox进程PID": vbox_process_pid,
            "宽度": width,
            "高度": height,
            "DPI": dpi
        }

    return result


# 注册表路径
key = winreg.HKEY_CURRENT_USER
sub_key = r"Software\leidian\LDPlayer9"
value_name = "InstallDir"

# 获取注册表值
雷电模拟器安装目录 = get_registry_value(key, sub_key, value_name)

LD = ctypes.windll.LoadLibrary
#参数自己设置成FreeCom.dll的路径
freeCOM = LD(R"../op-0.4.5_with_model/tools.dll")
#参数自己设置成op_x86.dll的路径
ret = freeCOM.setupA(bytes(R"../op-0.4.5_with_model/op_x64.dll", encoding="utf-8"))
print("setupA:{}".format(ret));
# create op instance
op = Dispatch("op.opsoft")
# op.UnBindWindow()
句柄=3475412


# op_ret = op.BindWindow(句柄,"dx2","windows","windows",0)
op_ret = op.BindWindow(句柄,"opengl","windows","windows",0)
print(op_ret)
op.Delay(500)
op.Capture(0, 0, 200, 200, "a1231.bmp")
