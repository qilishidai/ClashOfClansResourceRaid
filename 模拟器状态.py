
import subprocess
import time
import winreg
import win32gui


class 雷电模拟器:
    """
    雷电模拟器类，用于控制和管理雷电模拟器实例。

    属性:
    雷电模拟器安装目录 (str): 雷电模拟器的安装目录。
    雷电模拟器索引 (int): 要控制的模拟器实例索引。
    """

    def __init__(self, 模拟器索引=0):
        """
        初始化雷电模拟器实例。

        参数:
        模拟器索引 (int): 要控制的模拟器实例索引。默认值为0。
        """
        key = winreg.HKEY_CURRENT_USER
        sub_key = r"Software\leidian\LDPlayer9"
        value_name = "InstallDir"

        # 获取注册表值得到雷电模拟器安装目录
        self.雷电模拟器安装目录 = self.get_registry_value(key, sub_key, value_name)
        self.雷电模拟器索引 = 模拟器索引

    @staticmethod
    def get_registry_value(key, sub_key, value_name):
        """
        从注册表中获取指定的值。

        参数:
        key (winreg.HKEY_*): 注册表项根。
        sub_key (str): 注册表子项路径。
        value_name (str): 注册表值的名称。

        返回值:
        str: 注册表值的内容，如果注册表路径不存在或发生错误，返回None。
        """
        try:
            reg_key = winreg.OpenKey(key, sub_key)
            value, value_type = winreg.QueryValueEx(reg_key, value_name)
            winreg.CloseKey(reg_key)
            return value
        except FileNotFoundError:
            print("指定的注册表路径不存在,雷电模拟器未正确安装")
        except Exception as e:
            print("发生错误:", e)
            return None

    @staticmethod
    def 将雷电模拟器命令行返回信息解析为字典(text):
        """
        将雷电模拟器命令行返回的文本解析为字典。

        参数:
        text (str): 包含文本内容的字符串，每行代表一个条目，条目之间使用换行符分隔。
                    每个条目应包含逗号分隔的值，分别为索引、标题、顶层窗口句柄、绑定窗口句柄、
                    是否进入Android、进程PID、VBox进程PID、宽度、高度、DPI。

        返回值:
        dict: 包含解析后内容的字典。字典的键为索引，值为包含条目内容的字典。
              条目字典包含以下键值对：
                  - "标题"：标题字符串
                  - "顶层窗口句柄"：顶层窗口句柄整数
                  - "绑定窗口句柄"：绑定窗口句柄整数
                  - "是否进入Android"：是否进入Android布尔值
                  - "进程PID"：进程PID整数
                  - "VBox进程PID"：VBox进程PID整数
                  - "宽度"：宽度整数
                  - "高度"：高度整数
                  - "DPI"：DPI整数
        """
        result = {}
        lines = text.strip().split('\n')
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

    def 取模拟器所有状态(self):
        """
        获取所有模拟器实例的状态。

        返回值:
        dict: 当前模拟器实例的状态信息字典，包含以下键值对：
              - "标题"：标题字符串
              - "顶层窗口句柄"：顶层窗口句柄整数
              - "绑定窗口句柄"：绑定窗口句柄整数
              - "是否进入Android"：是否进入Android布尔值
              - "进程PID"：进程PID整数
              - "VBox进程PID"：VBox进程PID整数
              - "宽度"：宽度整数
              - "高度"：高度整数
              - "DPI"：DPI整数
        """
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        模拟器状态 = subprocess.run(
            [self.雷电模拟器安装目录 + "ldconsole.exe", "list2"],
            encoding='gbk',
            stdout=subprocess.PIPE,
            startupinfo=startupinfo
        )
        雷电模拟器运行信息 = self.将雷电模拟器命令行返回信息解析为字典(模拟器状态.stdout)
        return 雷电模拟器运行信息[self.雷电模拟器索引]

    def 模拟器是否启动(self):
        """
        检查当前模拟器实例是否启动。

        返回值:
        bool: 如果模拟器进程PID不为-1，则返回True，否则返回False。
        """
        return True if self.取模拟器所有状态()["进程PID"] != -1 else False

    def 取模拟器名称(self):
        """
        获取当前模拟器实例的的标题名称。

        返回值:
        str: 当前模拟器实例的的标题名称。
        """
        return self.取模拟器所有状态()["标题"]

    def 取顶层窗口句柄(self):
        """
        获取当前模拟器实例的顶层窗口句柄。

        返回值:
        int: 顶层窗口句柄。
        """
        return self.取模拟器所有状态()["顶层窗口句柄"]

    def 取绑定窗口句柄(self):
        """
        获取当前模拟器实例的绑定窗口句柄。

        返回值:
        int: 绑定窗口句柄。
        """
        return self.取模拟器所有状态()["绑定窗口句柄"]

    def 取绑定窗口句柄的下级窗口句柄(self):
        父窗口句柄 = self.取模拟器所有状态()["绑定窗口句柄"]
        子窗口列表 = []

        def 枚举子窗口回调(hwnd, param):
            子窗口列表.append(hwnd)
            return True

        win32gui.EnumChildWindows(父窗口句柄, 枚举子窗口回调, None)

        if 子窗口列表:
            # print(子窗口列表[0])
            return int(子窗口列表[0])
        else:
            return None

    def 启动模拟器并打开应用(self, 包名):
        """
        启动当前模拟器实例并打开指定的应用。

        参数:
        包名 (str): 要打开的应用的包名。
        """
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        subprocess.run(
            [self.雷电模拟器安装目录 + "ldconsole.exe", "launchex", "--index", str(self.雷电模拟器索引), "--packagename", 包名],
            shell=False,
            startupinfo=startupinfo
        )

    def 打开应用(self, 包名):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.run(
            [self.雷电模拟器安装目录 + "ldconsole.exe", "runapp", "--index", str(self.雷电模拟器索引), "--packagename", 包名],
            shell=False,
            startupinfo=startupinfo
        )

    def 关闭模拟器中的应用(self, 包名):
        """
        关闭当前模拟器实例中的指定应用。

        参数:
        包名 (str): 要关闭的应用的包名。
        """
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        subprocess.run(
            [self.雷电模拟器安装目录 + "ldconsole.exe", "killapp", "--index", str(self.雷电模拟器索引), "--packagename", 包名],
            shell=False,
            startupinfo=startupinfo
        )
        time.sleep(1)
