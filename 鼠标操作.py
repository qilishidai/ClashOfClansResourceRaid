import win32api
import win32con
import win32gui
import time


import win32api
import win32con
import win32gui
import time

class 鼠标控制器:
    def __init__(self, 窗口句柄=None , 模式='Windows消息模式', 每英寸点数=1,):
        self._每英寸点数 = 每英寸点数
        self._模式 = 模式
        self._窗口句柄 = 窗口句柄
        self._x = 0
        self._y = 0

    def 移动到(self, x, y):
        x *= self._每英寸点数
        y *= self._每英寸点数
        返回值 = 0

        if self._模式 == '普通模式':
            if self._窗口句柄:
                点 = win32gui.ClientToScreen(self._窗口句柄, (x, y))
                x, y = 点[0], 点[1]

            屏幕宽度值 = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) - 1
            屏幕高度值 = win32api.GetSystemMetrics(win32con.SM_CYSCREEN) - 1
            fx = x * (65535.0 / 屏幕宽度值)
            fy = y * (65535.0 / 屏幕高度值)

            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(fx), int(fy))
            返回值 = 1

        elif self._模式 == 'Windows消息模式':
            返回值 = win32gui.SendMessageTimeout(self._窗口句柄, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y),
                                                 win32con.SMTO_BLOCK, 2000)

        self._x, self._y = x, y
        return 返回值

    def 左键点击(self):
        返回值, 返回值2 = 0, 0

        if self._模式 == '普通模式':
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.01)  # 鼠标普通延迟
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            返回值, 返回值2 = 1, 1

        elif self._模式 == 'Windows消息模式':
            返回值 = win32gui.SendMessageTimeout(self._窗口句柄, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON,
                                                 win32api.MAKELONG(self._x, self._y), win32con.SMTO_BLOCK, 2000)
            time.sleep(0.01)  # 鼠标Windows延迟
            返回值2 = win32gui.SendMessageTimeout(self._窗口句柄, win32con.WM_LBUTTONUP, 0,
                                                  win32api.MAKELONG(self._x, self._y), win32con.SMTO_BLOCK, 2000)

        return 返回值 and 返回值2

    def 绑定(self, 窗口句柄, 模式='Windows消息模式'):
        if not win32gui.IsWindow(窗口句柄):
            return 0
        self._窗口句柄 = 窗口句柄
        self._模式 = 模式
        return 1

    def 解除绑定(self):
        self._窗口句柄 = None
        self._模式 = 0
        return 1

    def 移动相对位置(self, rx, ry):
        if self._模式 == '普通模式':
            self._x += rx
            self._y += ry

            输入 = win32api.INPUT()
            输入.type = win32con.INPUT_MOUSE
            输入.mi = win32api.MOUSEINPUT(dx=rx, dy=ry, dwFlags=win32con.MOUSEEVENTF_MOVE)
            return win32api.SendInput(1, [输入], win32api.sizeof(输入)) > 0
        return self.移动到(self._x + rx, self._y + ry)

    def 左键按下(self):
        if self._模式 == '普通模式':
            输入 = win32api.INPUT()
            输入.type = win32con.INPUT_MOUSE
            输入.mi = win32api.MOUSEINPUT(dwFlags=win32con.MOUSEEVENTF_LEFTDOWN)
            return win32api.SendInput(1, [输入], win32api.sizeof(输入)) > 0
        return win32gui.SendMessageTimeout(self._窗口句柄, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON,
                                           win32api.MAKELONG(self._x, self._y), win32con.SMTO_BLOCK, 2000)

    def 左键抬起(self):
        if self._模式 == '普通模式':
            输入 = win32api.INPUT()
            输入.type = win32con.INPUT_MOUSE
            输入.mi = win32api.MOUSEINPUT(dwFlags=win32con.MOUSEEVENTF_LEFTUP)
            return win32api.SendInput(1, [输入], win32api.sizeof(输入)) > 0
        return win32gui.SendMessageTimeout(self._窗口句柄, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON,
                                           win32api.MAKELONG(self._x, self._y), win32con.SMTO_BLOCK, 2000)



# 使用示例
# 鼠标控制 = 鼠标控制器(67174)
# 鼠标控制.移动到(376,273)
# 鼠标控制.左键点击()
# time.sleep(1)
# 鼠标控制.移动到(376, 376)
# 鼠标控制.左键按下()
# for _ in range(30):
#     鼠标控制.移动相对位置(0,-3)
#     time.sleep(0.08)
# 鼠标控制.左键抬起()
# # 鼠标控制.左键点击()

#
#

# op.Delay(500)
# op.MoveTo(467, 363)
# op.LeftDown()
# for _ in range(30):
#     op.MoveR(0, -3)
#     op.Delay(5)
# op.LeftUp()
# op.Delay(2000)
# class 鼠标控制器:
#     def __init__(self, 窗口句柄=None , 模式='Windows消息模式', 每英寸点数=1,):
#         self._每英寸点数 = 每英寸点数
#         self._模式 = 模式
#         self._窗口句柄 = 窗口句柄
#         self._x = 0
#         self._y = 0
#
#     def 绑定(self, 窗口句柄, 模式):
#         if not win32gui.IsWindow(窗口句柄):
#             return 0
#         self._窗口句柄 = 窗口句柄
#         self._模式 = 模式
#         return 1
#
#     def 解除绑定(self):
#         self._窗口句柄 = None
#         self._模式 = 'Windows消息模式'
#         return 1
#
#     def 移动到(self, x, y):
#         x *= self._每英寸点数
#         y *= self._每英寸点数
#         返回值 = 0
#
#         if self._模式 == '普通模式':
#             if self._窗口句柄:
#                 点 = win32gui.ClientToScreen(self._窗口句柄, (x, y))
#                 x, y = 点[0], 点[1]
#
#             屏幕宽度值 = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) - 1
#             屏幕高度值 = win32api.GetSystemMetrics(win32con.SM_CYSCREEN) - 1
#             fx = x * (65535.0 / 屏幕宽度值)
#             fy = y * (65535.0 / 屏幕高度值)
#
#             win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(fx), int(fy))
#             返回值 = 1
#
#         elif self._模式 == 'Windows消息模式':
#             返回值 = win32gui.SendMessageTimeout(self._窗口句柄, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y),
#                                                  win32con.SMTO_BLOCK, 2000)
#
#         self._x, self._y = x, y
#         return 返回值
#
#     def 左键点击(self):
#         返回值, 返回值2 = 0, 0
#
#         if self._模式 == '普通模式':
#             win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
#             time.sleep(0.01)  # 鼠标普通延迟
#             win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
#             返回值, 返回值2 = 1, 1
#
#         elif self._模式 == 'Windows消息模式':
#             返回值 = win32gui.SendMessageTimeout(self._窗口句柄, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON,
#                                                  win32api.MAKELONG(self._x, self._y), win32con.SMTO_BLOCK, 2000)
#             time.sleep(0.01)  # 鼠标Windows延迟
#             返回值2 = win32gui.SendMessageTimeout(self._窗口句柄, win32con.WM_LBUTTONUP, 0,
#                                                   win32api.MAKELONG(self._x, self._y), win32con.SMTO_BLOCK, 2000)
#
#         return 返回值 and 返回值2

#
# # 使用示例
# 鼠标控制 = 鼠标控制器(198252)
# 鼠标控制.移动到(225, 148)
# 鼠标控制.左键点击()
