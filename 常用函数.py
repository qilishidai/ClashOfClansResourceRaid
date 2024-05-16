import random
import subprocess
import time
import cv2
from 配置文件 import 雷电模拟器安装目录, 雷电模拟器索引, 部落冲突包名




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



def 关闭游戏(原因=None):
    subprocess.run(
        雷电模拟器安装目录 + "ldconsole.exe killapp  --index "+雷电模拟器索引+" --packagename \""+部落冲突包名+"\"",
        shell=True)
    time.sleep(1)

    if 原因 is not None:
        print(原因)

