import os
import time
import winreg


进攻完毕次数 = 0
循环最大等待秒数 = 30
找不到夜世界船的次数 = 0
正常结束上一轮打鱼而进入新一轮打鱼 = False  # 用于判断是否跳过前面的开模拟器,开游戏等操作,该变量会在循环超时,一直找不到夜世界船关闭游戏是置为False
目前脚本工作目录 = os.getcwd()

开始执行脚本时间 = time.time()
需要执行多少秒 = 4 * 3600  # 4个小时
一直执行 = True
当前金币 = -1
当前圣水 = -1
最大金币存储量 = 4700000
最大圣水存储量 = 5100000
刷墙成功次数 = 0
雷电模拟器索引="1"
部落冲突包名="com.tencent.tmgp.supercell.clashofclans"
# 部落冲突包名=""com.supercell.clashofclans"#国际服
# 升级判断最低金币=0

# 注册表路径
key = winreg.HKEY_CURRENT_USER
sub_key = r"Software\leidian\LDPlayer9"
value_name = "InstallDir"


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

# 获取注册表值
雷电模拟器安装目录 = get_registry_value(key, sub_key, value_name)
