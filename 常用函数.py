import random






def 将雷电模拟器命令行返回信息解析为字典(text):
    """
            将雷电模拟器命令行的返回的文本给定的文本解析为字典。

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
    """
    从输入字符串中寻找第一个非零x坐标的位置。


    :param input_str: 包含坐标信息的字符串，格式如下：'x1,y1,任意数字1x| x2,y2,任意数字2x| ...'，
                     其中每个段落表示一个坐标，由逗号分隔。

    :return:
            tuple: 如果找到第一个非零x坐标，则返回该坐标的(x, y)元组，否则返回默认坐标 (131, 550)。

    注意:
    - 如果类型部分识别为字母 'o' 或 'O'，将跳过该坐标的分析。
    - 如果无法将类型部分转换为数字，将跳过该坐标。


    """
    段落列表 = input_str.split('|')

    for 段落 in 段落列表:
        if 'x' in 段落:
            片段 = 段落.split(',')

            #片段[2][:-1]的意思是，取483,507,4x这个字符串中x前面的4，意思是第一个截取到倒数第一个
            #如果x前面的数字识别为O的英文字母则
            if 片段[2][:-1] == 'o' or 片段[2][:-1] == 'O':
                continue
            #出现转换错误
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
    根据给定的点列表计算相邻点所确定的直线方程，并可选择在图像上绘制这些直线。

    :param points: 包含点坐标的列表，每个点坐标表示为(x, y)元组。
    :param image: 用于显示结果的图像数组，默认为None。
    :return: 包含相邻点所确定直线方程的列表。

    注意:
    - 如果提供了image参数，则函数将在图像上绘制相邻点所确定的直线，并显示该图像。
    - 返回的直线方程以lambda函数的形式返回，接受一个参数x，并返回对应的y值。

    示例：
    points = [(0, 0), (50, 100), (100, 50), (150, 150)]
    lines = calculate_and_draw_lines(points)
    for line in lines:
         print(line(10))
    """
    # 检查是否提供了图像
    if image is not None:
        import cv2
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
    """
    在给定的四条直线中选择一条，然后在该直线上随机选择指定数量的点，并返回这些点的列表。

    :param 传入4条直线: 包含四条直线函数的列表。
    :param 对应直线x取值范围: 包含每条直线对应的x取值范围的[(最小x值1, 最大x值1), (最小x值2, 最大x值2), ...]。
    :param 选择的直线: 表示要选择的直线的索引。
    :param 返回点的个数: 要返回的点的数量。
    :param image: 用于显示结果的图像数组，默认为None。
    :return: 包含返回点的(x, y)坐标的列表。

    注意:

    - 对应直线x取值范围应为字典，格式为 {直线索引: (最小x值, 最大x值)}。

    - 传入4条直线应为包含四个函数的列表，函数应接受x值作为输入并返回对应的y值。

    - 如果提供了image参数，则函数将在图像上绘制随机点，并显示该图像。
    """
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



