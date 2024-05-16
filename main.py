import random
import winreg

import cv2


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

        def parse_text_to_dict(text):
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

# import moudles 第一次运行python -m pip install pywin32
from win32com.client import Dispatch
import time
import ctypes
from ctypes import *
import subprocess#系统命令
import os

LD = ctypes.windll.LoadLibrary;
#参数自己设置成FreeCom.dll的路径
freeCOM = LD(R"op-0.4.5_with_model/tools.dll");
#参数自己设置成op_x86.dll的路径
ret = freeCOM.setupA(bytes(R"op-0.4.5_with_model/op_x64.dll", encoding="utf-8"));
print("setupA:{}".format(ret));
# create op instance
op = Dispatch("op.opsoft");

def 寻找第一个非零x坐标(input_str):
    段落列表 = input_str.split('|')

    for 段落 in 段落列表:
            if 'x' in 段落:
                片段 = 段落.split(',')

                #片段为[481,510,ox]这样子的内容
                #如果识别成字母大小写o则跳过这一个
                if  片段[2][:-1]=='o' or 片段[2][:-1]=='O':
                    continue
                #出现转换错误也跳过当前片段
                try:
                    x前面的数字=int(片段[2][:-1])
                except ValueError:
                    continue

                if x前面的数字>0:
                   return int(片段[0]),int(片段[1])
    #当所有识别到可能有兵的位置都无效时,返回默认的第一个兵种位置
    return 131,550



def parse_text_to_dict(text):
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



def calculate_and_draw_lines(points, image=None):
    # 检查是否提供了图像
    if image is not None:
        # 画出四个点
        for point in points:
            cv2.circle(image, point, 5, (0, 255, 0), -1)

        # 计算直线方程并画出直线
        lines = []
        for i in range(len(points)-1):
            # 计算直线方程 y = mx + b
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            lines.append(lambda x, m=m, b=b: m*x + b)

            # 画出直线
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # 计算最后一条线，连接点4和点0
        x1, y1 = points[-1]
        x2, y2 = points[0]
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        lines.append(lambda x, m=m, b=b: m*x + b)
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # 显示画布
        cv2.imshow('Lines', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        lines = []
        for i in range(len(points)-1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            lines.append(lambda x, m=m, b=b: m*x + b)

        x1, y1 = points[-1]
        x2, y2 = points[0]
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        lines.append(lambda x, m=m, b=b: m*x + b)

    return lines

def 取直线上的随机点(传入4条直线,对应直线x取值范围,选择的直线,返回点的个数,image=None):
    返回的列表=[]

    for _ in range(返回点的个数):
        x=random.randint(对应直线x取值范围[选择的直线][0], 对应直线x取值范围[选择的直线][1])
        y=传入4条直线[选择的直线](x)
        返回的列表.append((x,int(y)))
        if image is not None:
            cv2.circle(image, (x,int(y)), 5, (0, 255, 0), -1)
    if image is not None:
        cv2.imshow('Lines', image)
        cv2.waitKey(0)
    return 返回的列表


def 点击(x,y,延时=300):
    op.MoveTo(x, y)
    op.LeftClick()
    op.Delay(延时)

def 随机点击(x, y):
    op.MoveToEx(x,y,50,50)
    op.LeftClick()
    op.Delay(100)



进攻完毕次数=0
while True:
    #启动游戏
    print("启动游戏")


    # 启动游戏
    subprocess.run(雷电模拟器安装目录+"ldconsole.exe launchex --index 1 --packagename \"com.tencent.tmgp.supercell.clashofclans\"", shell=True)
    #等待游戏登录
    while True:
        模拟器状态 =  subprocess.run(雷电模拟器安装目录 + "ldconsole.exe list2", encoding='gbk', stdout=subprocess.PIPE)
        雷电模拟器运行信息 = parse_text_to_dict(模拟器状态.stdout)

        if 雷电模拟器运行信息[1]["绑定窗口句柄"]==0:
            print("等待模拟器启动")
            continue
        else:
            print("模拟器启动完毕")
            break

    op_ret = op.BindWindow(雷电模拟器运行信息[1]["绑定窗口句柄"],"dx2","windows","windows",1)
    print("绑定窗口:",op_ret)

    # op_ret = op.OcrEx(20,500,2000,2000, "ffffff-303030", 0.7)
    # print(op_ret, 12314)
    # exit()
    # 88,500,577,542
    # 设置循环开始时间
    start_time = time.time()
    # 循环调用函数
    while True:
        #print("等待游戏登录")
        op.Delay(500)
        # 调用函数
        result, _, _ = op.FindPic(752,9,789,154,r"C:\Users\Hello\Desktop\部落冲突夜世界脚本开发\pythonProject\img\baoshi.jpg","000000",0.97,0)

        # 判断第一个返回值是否不是-1，如果不是-1，跳出循环
        if result != -1:
            break

        # 如果循环时间超过10秒，给出提示并跳出循环
        if time.time() - start_time > 60:
            print("循环超时！")
            break



    print("游戏成功登录")


    for _ in range(20):
        op.KeyPressChar("f5")

    op.Delay(500)


    #通过船判断领取圣水地方
    a,x,y=op.FindPic(0,0,2000,2000,r"C:\Users\Hello\Desktop\部落冲突夜世界脚本开发\pythonProject\img\船.jpg","000000",0.5,0)
    if x!=-1:
        # a,x,y=op.FindPic(x-200,y,x,y+100,r"C:\Users\Hello\Desktop\部落冲突夜世界脚本开发\pythonProject\img\圣水标志1.bmp|C:\Users\Hello\Desktop\部落冲突夜世界脚本开发\pythonProject\img\圣水标志2.bmp", "000000", 0.7, 0)
        # if x!=-1:
        #     print("找到领取圣水的车坐标",x,y)
        #     #点击车
        #     点击(x+16,y+1)
        #     # 点击收集
        #     点击(605, 471)
        #     op.Delay(1000)
        #     # 关闭领取界面
        #     点击(699, 103)
        # else:
        #     print("没有圣水可以领取")
        #点击(x+,y-)

        # 点击车
        点击(x-79,y+35)
        # 点击收集
        点击(605, 471)
        op.Delay(1000)
        # 关闭领取界面
        点击(699, 103)
    else:
        print("没有找到夜世界的船")


    #点击进攻
    点击(58,536)

    #点击立即寻找
    点击(600,380)

    while True:
        _, x, y = op.FindPic(0, 0, 2000, 2000,r"C:\Users\Hello\Desktop\部落冲突夜世界脚本开发\pythonProject\img\强化药水.jpg", "0", 0.9, 0)
        if x == -1:
            continue
        else:
            print("开始进攻")
            break



    #点击选择英雄
    点击(47,545)

    #出英雄
    点击(55,299)

    # #选择亡灵
    # 点击(131,550)

    # input_str = "270,507,0x|130,510,4x|200,510,4x|340,510,4x|412,510,4x|483,507,4x|452,572,16|25,573,9|382,573,16 12314"
    input_str = op.OcrEx(20,500,2000,2000, "ffffff-303030", 0.7)
    print(input_str, 12314)
    x, y = 寻找第一个非零x坐标(input_str)
    点击(x, y)
    # for _ in range(20):
    #     # 执行点击操作
    #     随机点击(55, 299)
    #     随机点击(734, 317)
    #     随机点击(399, 70)
    #     随机点击(499,482)
    #
    points = [(14, 309), (366, 37), (764, 311), (375, 473)]
    for 出兵所在直线 in range(4):
        line_equations = calculate_and_draw_lines(points)
        出兵点 = 取直线上的随机点(line_equations, [(14, 366), (366, 764), (375, 764), (14, 375)], 出兵所在直线, 9)
        for 出兵点的元组 in 出兵点:
            点击(出兵点的元组[0], 出兵点的元组[1],100)

    #放英雄技能
    点击(42,554)


    # 进攻完毕次数+=1
    # print("进攻完毕了"+str(进攻完毕次数)+"次")
    #
    # subprocess.run(雷电模拟器安装目录+"ldconsole.exe killapp  --index 1 --packagename \"com.tencent.tmgp.supercell.clashofclans\"", shell=True)
    # op.Delay(1000)
    # subprocess.run(雷电模拟器安装目录+"ldconsole.exe runapp  --index 1 --packagename \"com.tencent.tmgp.supercell.clashofclans\"", shell=True)
    #
    # continue
    #
    #
    # 进攻完毕次数+=1
    # print("进攻完毕了"+str(进攻完毕次数)+"次")
    # 第一阶段后是否回营=False
    #

    第二场战斗完毕=False
    while True:
        if  第二场战斗完毕==False:
            _, 换兵箭头x, 换兵箭头y = op.FindPic(0, 0, 2000, 2000, r"C:\Users\Hello\Desktop\部落冲突夜世界脚本开发\pythonProject\img\更换兵种箭头.bmp", "000000", 0.6, 0)

            if 换兵箭头x!=-1:
                第二场战斗完毕 = True
                print("第二场次战斗")
                #88,500,577,542


                input_str = op.OcrEx(20, 500, 2000, 2000, "ffffff-303030", 0.7)
                print(input_str, 12314)
                x, y = 寻找第一个非零x坐标(input_str)
                点击(x, y)
                # for _ in range(20):
                #     # 执行点击操作
                #     随机点击(55, 299)
                #     随机点击(734, 317)
                #     随机点击(399, 70)
                #     随机点击(499,482)
                #
                points = [(14, 309), (366, 37), (764, 311), (375, 473)]
                for 出兵所在直线 in range(4):
                    line_equations = calculate_and_draw_lines(points)
                    出兵点 = 取直线上的随机点(line_equations, [(14, 366), (366, 764), (375, 764), (14, 375)],
                                              出兵所在直线, 9)
                    for 出兵点的元组 in 出兵点:
                        点击(出兵点的元组[0], 出兵点的元组[1], 100)

                # 点击选择英雄
                点击(47, 545)

                # 出英雄
                点击(55, 299)

                # 放英雄技能
                点击(42, 554)

        _, 回营x, 回营y = op.FindPic(0, 0, 2000, 2000,r"C:\Users\Hello\Desktop\部落冲突夜世界脚本开发\pythonProject\img\回营.jpg", "0", 0.9, 0)
        if 回营x == -1:
            continue
        else:
            print("回营")
            进攻完毕次数 += 1
            print("进攻完毕了" + str(进攻完毕次数) + "次")
            点击(回营x,回营y)
            break
