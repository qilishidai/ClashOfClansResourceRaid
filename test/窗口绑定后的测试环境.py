import random
import winreg
import cv2
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
#





#往下滑
# op.Delay(500)
# op.MoveTo(467,363)
# op.LeftDown()
# for _ in range(30):
#     op.MoveR(0,-5)
#     op.Delay(5)
# op.LeftUp()
# op.Delay(1000)



import re


def 点击(x, y, 延时=300):
    op.MoveTo(x, y)
    op.LeftClick()
    op.Delay(延时)

def 将Ocr识别返回的字符串格式化为列表(输入字符串):
    # 用|分割字符串
    split_list = 输入字符串.split("|")

    # 对每个分割后的子字符串再用,分割，并形成最终列表
    final_list = [item.split(",") for item in split_list]

    return final_list

def 升级2建筑(op,要升级的建筑物名称):
    """


    :param op:
    :param 要升级的建筑物名称:
    :return: 返回,执行状态,是否为需要重启的致命性错误,指定建筑物需要的资源,资源类型
    """
    识别到的字符串 = None
    是否识别到指定建筑 = False
    #打开建筑升级的地方
    点击(415,11)
    op.Delay(1000)
    while 是否识别到指定建筑 is False:

        上一次建筑字符串 = 识别到的字符串#将上一次次循环后的识别内容用一个变量保存起来,要不等等重新识别覆盖掉了.如果是第一次进入循环,None,如果已经经过循环了,识别到的字符串保存的当然是上一次循环的识别内容,
        识别到的字符串 = op.OcrEx(362, 71, 581, 388, "ffffff", 0.7)
        # 将英文字母o和O都替换为数字0,因为识别可能将数字0错误地识别为英文字母o或O
        识别到的字符串 = 识别到的字符串.replace('o', '0').replace('O', '0')
        建筑和价格列表 = 将Ocr识别返回的字符串格式化为列表(识别到的字符串)
        print(识别到的字符串)

        #循环找建筑中,第一找那么打开建筑界面则判断是否正常打开,不是第一次就判断是否到底了
        if 上一次建筑字符串 is None:
            if not ("升级" in 识别到的字符串):
                print("打开建筑升级栏失败")
                return f"打开建筑升级栏失败", True, -1, ""
                # break

        else:
            if 将Ocr识别返回的字符串格式化为列表(上一次建筑字符串)[-1][2] == 建筑和价格列表[-1][2]:
                op.MoveTo(415, 11)
                op.LeftClick()
                op.Delay(1000)
                print("滑到底部了")
                return f"滑到底部了,找不到指定的建筑", True, -1, ""
                # break
        #如果识别到的字符串包含了设定的建筑名称
        if 要升级的建筑物名称 in 识别到的字符串:
            for 第几个建筑物 in range(len(建筑和价格列表)):
                if 要升级的建筑物名称 in 建筑和价格列表[第几个建筑物][2]:
                    是否识别到指定建筑 = True


                    建筑所在x, 建筑所在y = int(建筑和价格列表[第几个建筑物][0]), int(建筑和价格列表[第几个建筑物][1])


                    #识别价格####
                    价格字符串=op.OcrEx(建筑所在x + 50, 建筑所在y - 5, 建筑所在x + 250, 建筑所在y + 15, "ffffff", 0.7)
                    print(价格字符串)
                    # 识别引擎会混淆英文字母Oo,全部替换为0
                    价格字符串 = 价格字符串.replace('o', '0').replace('O', '0')
                    包含价格的字符串 = 价格字符串.split(",")[2]
                    # 使用正则表达式提取数字部分,剔除识别引擎错误识别多的奇怪符号,剔除完毕后转为整数
                    当前指定升级建筑的价格 = re.findall(r'\d+', 包含价格的字符串)[0]
                    当前指定升级建筑的价格=int(当前指定升级建筑的价格)


                    # print("要升级的建筑物在", 第几个建筑物)
                    print("价格为",当前指定升级建筑的价格)
                    print("价格所在的坐标是", 建筑所在x, 建筑所在y)

                    点击(建筑所在x, 建筑所在y)
                    op.Delay(2000)

                    #在基于建筑物名称偏移量确定的区域内确定升级建筑物的类型,该区域可以用下面代码截图查阅
                    op.Capture(建筑所在x + 50, 建筑所在y - 5, 建筑所在x + 250, 建筑所在y + 15, "your_image.bmp")
                    #0代表金币,1代表圣水
                    升级需要的资源类型,_,_=op.FindPic(建筑所在x + 50, 建筑所在y - 5, 建筑所在x + 250, 建筑所在y + 15,
                               r"C:\Users\Hello\Desktop\部落冲突夜世界脚本开发\pythonProject\img\金币色块.bmp|C:\Users\Hello\Desktop\部落冲突夜世界脚本开发\pythonProject\img\圣水色块.bmp", "000000", 0.8,
                                                      0)
                    if 升级需要的资源类型==0:
                        print("升级需要金币")
                        _,x,y=op.FindPic(243, 445, 549, 465, r"C:\Users\Hello\Desktop\部落冲突夜世界脚本开发\pythonProject\img\金币色块.bmp", "000000", 0.8, 0)
                        # 打开升级页面
                        点击(x,y)
                        #返回0,那么是白色,否则不是
                        字体为白,_,_=op.FindPic(369,459,421,509,r"C:\Users\Hello\Desktop\部落冲突夜世界脚本开发\pythonProject\img\白色色块.bmp","000000",0.98,0)
                        是否为红=op.GetColor(127, 496)=="E1433F"#升级框旁边不红,红了代表大本营等级不够,不能升级

                        if int(字体为白)==0 and 是否为红 is False:
                            点击(414,480)
                            # print(f"升级了{要升级的建筑物名称}耗资{当前指定升级建筑的价格}")
                            return f"升级了{要升级的建筑物名称}耗资{当前指定升级建筑的价格}",False,当前指定升级建筑的价格,"金币"
                        else:
                            # 下一次判断建筑至少拥有金币=当前指定升级建筑的价格
                            print(f"不够资源升级,等你金币到了{当前指定升级建筑的价格}再判断是否升级建筑")

                            return f"不够资源升级,等你金币到了{当前指定升级建筑的价格}再判断是否升级建筑",False,当前指定升级建筑的价格,"金币"
                        # break

                    elif 升级需要的资源类型==1:
                        print("升级需要圣水")
                        _,x,y=op.FindPic(243, 445, 549, 465, r"C:\Users\Hello\Desktop\部落冲突夜世界脚本开发\pythonProject\img\圣水色块.bmp", "000000", 0.8, 0)
                        点击(x,y)
                        #返回0,那么是白色,否则不是
                        字体为白,_,_=op.FindPic(369,459,421,509,r"C:\Users\Hello\Desktop\部落冲突夜世界脚本开发\pythonProject\img\白色色块.bmp","000000",0.98,0)
                        是否为红=op.GetColor(127, 496)=="E1433F"#升级框旁边不红,红了代表大本营等级不够,不能升级

                        if int(字体为白)==0 and 是否为红 is False:

                            点击(414,480)
                            # print(f"升级了{要升级的建筑物名称}耗资{当前指定升级建筑的价格}")
                            return f"升级了{要升级的建筑物名称}耗资{当前指定升级建筑的价格}",False,当前指定升级建筑的价格,"圣水"
                        else:
                            下一次判断建筑至少拥有圣水=当前指定升级建筑的价格
                            print(f"不够资源升级,等你圣水需要{当前指定升级建筑的价格}")
                            return f"不够资源升级,等你圣水到了{当前指定升级建筑的价格}再判断是否升级建筑",False,当前指定升级建筑的价格,"圣水"
                        # break

                    else:
                        print("无法确定升级资源的类型")
                        return f"无法确定升级资源的类型", True, -1, ""

                    break
        else:    #如果没有识别到的字符串包含了设定的建筑名称,往下滑动继续找
            print("未找到要升级的建筑物")
            op.Delay(500)
            op.MoveTo(467,363)
            op.LeftDown()
            for _ in range(30):
                op.MoveR(0,-3)
                op.Delay(5)
            op.LeftUp()
            op.Delay(2000)



        # op.MoveTo(415, 11)
        # op.LeftClick()
        # op.Delay(1000)

# print(升级建筑(op,"防空火炮"))

# op.SetWindowTransparent(雷电模拟器运行信息[1]["顶层窗口句柄"],255)
#
# op.SetWindowState(雷电模拟器运行信息[1]["顶层窗口句柄"], 11)
# # op.MoveWindow(雷电模拟器运行信息[1]["顶层窗口句柄"],1920,1080)
# op.SetWindowState(雷电模拟器运行信息[1]["绑定窗口句柄"], 11)
# op.MoveWindow(雷电模拟器运行信息[1]["顶层窗口句柄"],35,35)
# print(1111)
# print(op.GetWindowRect(雷电模拟器运行信息[1]["顶层窗口句柄"]))
# op.Delay(1000)

雷电模拟器是否最小化 = op.GetWindowState(雷电模拟器运行信息[1]["顶层窗口句柄"],3)
if 雷电模拟器是否最小化 ==1:
  print("窗口已经最小化了,修改为还原状态")
  op.SetWindowState(雷电模拟器运行信息[1]["顶层窗口句柄"],5)

else:
    print("没有最小化")
