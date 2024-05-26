# import os
# import winreg
"""
该文件已过时,设置相关属性在用户界面进行设置.
"""
#
#
# # #用于多开,加入你在雷电多开器中建立了多个模拟器,这里是选的是辅助要启动的模拟器,多开器页面的第一个就写0,第二个就写1
# # 雷电模拟器索引 = "0"
# # #国服
# # # 部落冲突包名 = "com.tencent.tmgp.supercell.clashofclans"
# # #国际服
# # # 部落冲突包名="com.supercell.clashofclans"
# #
# # #如果一直执行 = True那么脚本会一直执行下去
# # 一直执行 = True
# # #如果一直执行 = False 那么会根据需要执行多少秒这个变量来确定运行的时间
# # 需要执行多少秒 = 4 * 3600  # 4个小时
# # #True开启刷墙,False关闭,开启一定要保证有工人,否则会出错
# # # 是否开启刷墙 = False
# #
# # 循环最大等待秒数 = 30
# # 至少多少金币开始刷墙 = 2000000
# # 至少多少圣水开始刷墙 = 2700000
# 目前脚本工作目录 = os.getcwd()
#
# # 注册表路径
# key = winreg.HKEY_CURRENT_USER
# sub_key = r"Software\leidian\LDPlayer9"
# value_name = "InstallDir"
#
#
# def get_registry_value(key, sub_key, value_name):
#     try:
#         # 打开注册表项
#         reg_key = winreg.OpenKey(key, sub_key)
#         # 读取注册表值
#         value, value_type = winreg.QueryValueEx(reg_key, value_name)
#         # 关闭注册表项
#         winreg.CloseKey(reg_key)
#         return value
#     except FileNotFoundError:
#         print("指定的注册表路径不存在")
#     except Exception as e:
#         print("发生错误:", e)
#
#
# # 获取注册表值
# 雷电模拟器安装目录 = get_registry_value(key, sub_key, value_name)