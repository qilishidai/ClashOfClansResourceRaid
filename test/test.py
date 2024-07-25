import winreg

from win32com.client import Dispatch  # import moudles 第一次运行python -m pip install pywin32
import time
import ctypes
LD = ctypes.windll.LoadLibrary
#参数自己设置成FreeCom.dll的路径
freeCOM = LD(R"../op-0.4.5_with_model/tools.dll")
#参数自己设置成op_x86.dll的路径
ret = freeCOM.setupA(bytes(R"../op-0.4.5_with_model/op_x64.dll", encoding="utf-8"))
print("setupA:{}".format(ret));
# create op instance
op = Dispatch("op.opsoft")
op.UnBindWindow()
print(op.BindWindow(658448,"opengl","windows","windows",1))
op.Delay(5000)
op.Capture(0, 0, 200, 200, "a1231.bmp")
# op.Capture(0,0,2000,2000,r"C:\Users\Hello\Downloads\OPTestTool-0.4.5\capture_file.bmp")
