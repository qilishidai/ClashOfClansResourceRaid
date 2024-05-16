import random# 随机数生成模块
import winreg# Windows注册表操作模块
import cv2# OpenCV图像处理库
# Windows COM对象操作模块
from win32com.client import Dispatch  # import moudles 第一次运行python -m pip install pywin32
import time# 时间模块
# Windows动态链接库调用模块
import ctypes
from ctypes import *
# 子进程管理模块
import subprocess  # 系统命令
import os# 操作系统相关功能模块


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


def 寻找第一个非零x坐标(input_str):
    段落列表 = input_str.split('|')

    for 段落 in 段落列表:
        if 'x' in 段落:
            片段 = 段落.split(',')

            #片段为[481,510,ox]这样子的内容
            #如果识别成字母大小写o则跳过这一个
            if 片段[2][:-1] == 'o' or 片段[2][:-1] == 'O':
                continue
            #出现转换错误也跳过当前片段
            try:
                x前面的数字 = int(片段[2][:-1])
            except ValueError:
                continue

            if x前面的数字 > 0:
                return int(片段[0]), int(片段[1])
    #当所有识别到可能有兵的位置都无效时,返回默认的第一个兵种位置
    return 131, 550


def 计算相邻点所确定的直线(points, image=None):
    """
    绘制连接给定点并计算相应直线方程,。

    参数：
    points (list[tuple]): 一系列表示点的元组列表，每个元组包含两个整数值，代表 x 和 y 坐标。传入4个点的坐标
    image (numpy.ndarray, 可选): 一个可选的图像数组，如果提供，直线将在图像上绘制。

    返回：
    list[function]: 一个包含直线方程的函数列表，每个函数接受一个 x 值并返回对应的 y 值。

    注：
    - 如果提供了图像，则函数会在图像上绘制直线，并在窗口中显示结果。
    - 如果未提供图像，则仅计算直线方程，并返回函数列表。

    示例：
    points = [(0, 0), (50, 100), (100, 50), (150, 150)]
    lines = calculate_and_draw_lines(points)
    for line in lines:
         print(line(10))
    """
    # 检查是否提供了图像
    if image is not None:
        # 画出四个点
        for point in points:
            cv2.circle(image, point, 5, (0, 255, 0), -1)

        # 计算直线方程并画出直线
        lines = []
        for i in range(len(points) - 1):
            # 计算直线方程 y = mx + b
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            lines.append(lambda x, m=m, b=b: m * x + b)

            # 画出直线
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # 计算最后一条线，连接点4和点0
        x1, y1 = points[-1]
        x2, y2 = points[0]
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        lines.append(lambda x, m=m, b=b: m * x + b)
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # 显示画布
        cv2.imshow('Lines', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        lines = []
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            lines.append(lambda x, m=m, b=b: m * x + b)

        x1, y1 = points[-1]
        x2, y2 = points[0]
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        lines.append(lambda x, m=m, b=b: m * x + b)

    return lines


def 取直线上的随机点(传入4条直线, 对应直线x取值范围, 选择的直线, 返回点的个数, image=None):
    返回的列表 = []

    for _ in range(返回点的个数):
        x = random.randint(对应直线x取值范围[选择的直线][0], 对应直线x取值范围[选择的直线][1])
        y = 传入4条直线[选择的直线](x)
        返回的列表.append((x, int(y)))
        if image is not None:
            cv2.circle(image, (x, int(y)), 5, (0, 255, 0), -1)
    if image is not None:
        cv2.imshow('Lines', image)
        cv2.waitKey(0)
    return 返回的列表


def 点击(x, y, 延时=300):
    op.MoveTo(x, y)
    op.LeftClick()
    op.Delay(延时)


def 随机点击(x, y):
    op.MoveToEx(x, y, 50, 50)
    op.LeftClick()
    op.Delay(100)


def 关闭游戏(原因=None):
    subprocess.run(
        雷电模拟器安装目录 + "ldconsole.exe killapp  --index 1 --packagename \"com.tencent.tmgp.supercell.clashofclans\"",
        shell=True)
    op.Delay(1000)

    if 原因 is not None:
        print(原因)


# 注册表路径
key = winreg.HKEY_CURRENT_USER
sub_key = r"Software\leidian\LDPlayer9"
value_name = "InstallDir"

# 获取注册表值
雷电模拟器安装目录 = get_registry_value(key, sub_key, value_name)

LD = ctypes.windll.LoadLibrary
#参数自己设置成FreeCom.dll的路径
freeCOM = LD(R"op-0.4.5_with_model/tools.dll")
#参数自己设置成op_x86.dll的路径
ret = freeCOM.setupA(bytes(R"op-0.4.5_with_model/op_x64.dll", encoding="utf-8"))
print("setupA:{}".format(ret));
# create op instance
op = Dispatch("op.opsoft")

进攻完毕次数 = 0
循环最大等待秒数 = 30
找不到夜世界船的次数 = 0
正常结束上一轮打鱼而进入新一轮打鱼 = False  #用于判断是否跳过前面的开模拟器,开游戏等操作,该变量会在循环超时,一直找不到夜世界船关闭游戏是置为False
目前脚本工作目录 = os.getcwd()


开始执行脚本时间=time.time()
需要执行多少秒=4*3600#4个小时
当前金币=-1
当前圣水=-1
最大金币存储量=4700000
最大圣水存储量=5100000
while True:  #循环进攻
    if time.time()-开始执行脚本时间>需要执行多少秒:
        关闭游戏("到时间了")
        exit()

    if 正常结束上一轮打鱼而进入新一轮打鱼 is False:
        模拟器状态 = subprocess.run(雷电模拟器安装目录 + "ldconsole.exe list2", encoding='gbk', stdout=subprocess.PIPE)
        雷电模拟器运行信息 = 将雷电模拟器命令行返回信息解析为字典(模拟器状态.stdout)

        if 雷电模拟器运行信息[1]["绑定窗口句柄"] == 0:
            #启动模拟器并打开游戏
            subprocess.run(
                雷电模拟器安装目录 + "ldconsole.exe launchex --index 1 --packagename \"com.tencent.tmgp.supercell.clashofclans\"",
                shell=True)

            while True:  # 循环判断模拟器是否启动成功
                模拟器状态 = subprocess.run(雷电模拟器安装目录 + "ldconsole.exe list2", encoding='gbk',
                                            stdout=subprocess.PIPE)
                雷电模拟器运行信息 = 将雷电模拟器命令行返回信息解析为字典(模拟器状态.stdout)

                if 雷电模拟器运行信息[1]["绑定窗口句柄"] == 0:
                    print("等待模拟器启动")
                    continue
                else:
                    print("模拟器启动完毕")
                    break
        else:
            #模拟器如果已经启动了,就直接开游戏,这里有一个不好的地方是没有判断游戏是不是开启了,暴力直接打开游戏.因为如果不是因为错误关闭游戏的话新一轮打鱼游戏是已经开了的
            #进入这一个的情况有,用户干预,模拟器打开游戏未打卡;循环超时,计数器过大导致的关闭游戏
            subprocess.run(
                雷电模拟器安装目录 + "ldconsole.exe runapp  --index 1 --packagename \"com.tencent.tmgp.supercell.clashofclans\"",
                shell=True)

            #print("模拟器已经启动了,不需要启动")
            pass

        #为绑定窗口则绑定窗口
        if op.IsBind() == 0:
            是否成功绑定 = op.BindWindow(雷电模拟器运行信息[1]["绑定窗口句柄"], "dx2", "windows", "windows", 1)
            # 等待绑定窗口完成
            op.Delay(500)
            print("绑定窗口:", 是否成功绑定)
        else:
            #print("已经绑定窗口了,不需要再次绑定")
            pass

    print("新一轮打鱼,目前是第" + str(进攻完毕次数) + "次打鱼完毕了")
    print("等待进入夜世界主界面")
    # 判断循环是否超时间
    循环开始时间 = time.time()
    循环是否超时 = False
    while True:  #判断登录状态循环
        # 查找宝石数量旁边的宝石确定登录状态
        result, x, y = op.FindPic(752, 9, 789, 154, 目前脚本工作目录 + r"\img\宝石.jpg", "000000", 0.97, 0)
        # 找到了,证明已经登录,跳出循环
        if result != -1:
            break

        if time.time() - 循环开始时间 > 循环最大等待秒数:
            循环是否超时 = True
            关闭游戏("重启游戏,原因是一直没有成功登录！已经等待了" + str(循环最大等待秒数) + "秒")
            正常结束上一轮打鱼而进入新一轮打鱼 = False
            break
    #如果因为超时而关闭游戏,则回到循环开头,开游戏,进行下一次开游戏,打鱼等操作
    if 循环是否超时 is True:
        continue
    print("游戏成功登录")

    #拉远视距
    for _ in range(20):
        op.KeyPressChar("f5")
    op.Delay(500)

    #获取当前金币圣水数量
    识别到的金币圣水字符串 = op.OcrEx(610, 15, 789, 89, "ffffff", 0.7)
    段落列表 = 识别到的金币圣水字符串.split('|')
    识别的列表 = []
    for 段落 in 段落列表:
        分割的片段 = 段落.split(',')
        识别的列表.append(分割的片段)
    if int(识别的列表[0][1]) < int(识别的列表[1][1]):

        print(f"当前的金币为{识别的列表[0][2]},圣水为{识别的列表[1][2]}")
        # 当前金币=int(识别的列表[0][2])
        # 当前圣水=int(识别的列表[1][2])
    else:
        print(f"当前的金币为{识别的列表[1][2]},圣水为{识别的列表[0][2]}")
        # 当前金币=int(识别的列表[1][2])
        # 当前圣水=int(识别的列表[0][2])


    if 当前金币>=最大金币存储量 or 当前圣水>=最大圣水存储量:
        关闭游戏("关闭游戏,因为资源满了")
        exit()

    是否因为多次找不到船而关闭了游戏 = False
    #通过船判断领取圣水地方
    a, x, y = op.FindPic(0, 0, 2000, 2000, 目前脚本工作目录 + r"\img\船.jpg", "000000", 0.5, 0)
    if x != -1:
        # 点击车
        点击(x - 79, y + 35)
        # 点击收集
        点击(605, 471)
        op.Delay(1000)
        # 关闭领取界面
        点击(699, 103)
    else:
        print("没有找到夜世界的船")
        找不到夜世界船的次数 += 1
        if 找不到夜世界船的次数 > 10:
            关闭游戏("关闭游戏,原因:一直找不到夜世界的船")
            是否因为多次找不到船而关闭了游戏 = True
            正常结束上一轮打鱼而进入新一轮打鱼 = False
    #多次找不到船,游戏已经关闭,回到循环开始,重新进行下一次打鱼
    if 是否因为多次找不到船而关闭了游戏:
        continue

    #点击进攻
    点击(58, 536)

    #点击立即寻找
    点击(600, 380)

    # 判断循环是否进入战斗界面
    循环开始时间 = time.time()
    循环是否超时 = False
    while True:
        if time.time() - 循环开始时间 > 循环最大等待秒数:
            循环是否超时 = True
            关闭游戏(
                "重启游戏,原因是一直卡白云或者某处,导致一直没进入战斗界面！已经等待了" + str(循环最大等待秒数) + "秒")
            正常结束上一轮打鱼而进入新一轮打鱼 = False
            break

       # _, x, y = op.FindPic(0, 0, 2000, 2000,目前脚本工作目录 + r"\img\强化药水.jpg", "0", 0.9, 0)
        _, x, y = op.FindPic(0, 0, 257, 115, 目前脚本工作目录 + r"\img\举报.bmp", "000000", 0.8, 0)

        if x == -1:
            continue
        else:
            print("开始进攻")
            break

    # 如果因为超时而关闭游戏,则回到循环开头,进行下一次开游戏,打鱼等操作
    if 循环是否超时 is True:
        continue

    识别到的剩余兵力字符 = op.OcrEx(20, 500, 2000, 2000, "ffffff-303030", 0.7)
    #print(识别到的剩余兵力字符)
    x, y = 寻找第一个非零x坐标(识别到的剩余兵力字符)
    点击(x, y)

    points = [(14, 309), (366, 37), (764, 311), (375, 473)]
    for 出兵所在直线 in range(4):
        line_equations = 计算相邻点所确定的直线(points)
        出兵点 = 取直线上的随机点(line_equations, [(14, 366), (366, 764), (375, 764), (14, 375)], 出兵所在直线, 9)
        for 出兵点的元组 in 出兵点:
            点击(出兵点的元组[0], 出兵点的元组[1], 100)

    #点击选择英雄
    点击(47, 545)

    #出英雄
    点击(55, 299)

    #放英雄技能
    op.Delay(3000)
    点击(42, 554)

    第二场战斗是否已经开始 = False
    循环开始时间 = time.time()
    循环是否超时 = False
    while True:
        if time.time() - 循环开始时间 > 180:
            循环是否超时 = True
            关闭游戏("重启游戏,原因为因为战斗好久没结束,或一直没有开始第二场战斗.已经等待了" + str(180) + "秒")
            正常结束上一轮打鱼而进入新一轮打鱼 = False
            break

        #本循环有两个判断,判断是否存在第二次战斗和是否出现回营按钮
        #如果第二次战斗还没打就判断两个,否则就一直判断回营图标的出现
        if 第二场战斗是否已经开始 == False:
            _, 换兵箭头x, 换兵箭头y = op.FindPic(0, 0, 2000, 2000,
                                                 目前脚本工作目录 + r"\img\更换兵种箭头.bmp",
                                                 "000000", 0.6, 0)

            if 换兵箭头x != -1:
                循环开始时间 = time.time()#因为开始第二场战斗,重置等待回营的超时时间,从现在重新计算等待时间
                第二场战斗是否已经开始 = True
                print("第二场次战斗")
                #88,500,577,542
                op.Delay(500)
                识别到的剩余兵力字符 = op.OcrEx(20, 500, 2000, 2000, "ffffff-303030", 0.7)
                # print(识别到的剩余兵力字符)
                x, y = 寻找第一个非零x坐标(识别到的剩余兵力字符)
                点击(x, y)

                points = [(14, 309), (366, 37), (764, 311), (375, 473)]
                for 出兵所在直线 in range(4):
                    line_equations = 计算相邻点所确定的直线(points)
                    出兵点 = 取直线上的随机点(line_equations, [(14, 366), (366, 764), (375, 764), (14, 375)],
                                              出兵所在直线, 9)
                    for 出兵点的元组 in 出兵点:
                        点击(出兵点的元组[0], 出兵点的元组[1], 100)

                # 点击选择英雄
                点击(47, 545)

                # 出英雄
                点击(55, 299)

                # 放英雄技能
                op.Delay(3000)
                点击(42, 554)

        _, 回营x, 回营y = op.FindPic(0, 0, 2000, 2000, 目前脚本工作目录 + r"\img\回营.jpg", "0", 0.9, 0)
        if 回营x == -1:
            continue
        else:
            print("回营")
            点击(回营x, 回营y)
            进攻完毕次数 += 1
            print("进攻完毕了" + str(进攻完毕次数) + "次")
            正常结束上一轮打鱼而进入新一轮打鱼 = True
            点击(回营x, 回营y)
            正常结束上一轮打鱼而进入新一轮打鱼 = True
            break

    # 如果因为超时而关闭游戏,则回到循环开头,进行下一次开游戏,打鱼等操作
    if 循环是否超时 is True:
        continue
