

# import moudles
from win32com.client import Dispatch

import time;
import ctypes
from ctypes import *
LD = ctypes.windll.LoadLibrary;
#参数自己设置成FreeCom.dll的路径
freeCOM = LD(R"E:\project\op\bin\x86\tools.dll");
#参数自己设置成op_x86.dll的路径

ret = freeCOM.setupA(bytes(R"E:\project\op\bin\x86\op_x86.dll",encoding="utf-8"));

print("setupA:{}".format(ret));
# create op instance
op = Dispatch("op.opsoft");
print(op.Ver())
op.MoveTo(30,30)