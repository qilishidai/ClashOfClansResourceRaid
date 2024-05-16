import os
import winreg

目前脚本工作目录 = os.getcwd()
雷电模拟器索引 = "1"
部落冲突包名 = "com.tencent.tmgp.supercell.clashofclans"
# 部落冲突包名="com.supercell.clashofclans"#国际服
循环最大等待秒数 = 30
需要执行多少秒 = 4 * 3600  # 4个小时
一直执行 = True



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
