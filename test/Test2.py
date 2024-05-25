import multiprocessing
import psutil
import time

def 窗口启动(字符):
    while True:
        print(字符)
        time.sleep(1)

def 启动进程(字符):
    进程 = multiprocessing.Process(target=窗口启动, args=(字符,))
    进程.start()
    return 进程

def 挂起进程(进程ID):
    进程 = psutil.Process(进程ID)
    进程.suspend()

def 恢复进程(进程ID):
    进程 = psutil.Process(进程ID)
    进程.resume()

def 销毁进程(进程ID):
    进程 = psutil.Process(进程ID)
    进程.terminate()

def 判断进程是否存在(进程ID):
    return psutil.pid_exists(进程ID)

if __name__ == '__main__':
    # 启动进程
    进程 = 启动进程('A')
    print(f"启动了进程，进程ID: {进程.pid}")

    # 等待一段时间，让进程运行
    time.sleep(5)

    # 挂起进程
    挂起进程(进程.pid)
    print(f"挂起了进程，进程ID: {进程.pid}")

    # 等待一段时间，观察进程挂起效果
    time.sleep(5)

    # 恢复进程
    恢复进程(进程.pid)
    print(f"恢复了进程，进程ID: {进程.pid}")

    # 再次等待一段时间，让进程运行
    time.sleep(5)

    # 销毁进程
    销毁进程(进程.pid)
    print(f"销毁了进程，进程ID: {进程.pid}")

    # 等待一段时间，确保进程终止
    time.sleep(2)

    # 检查进程是否存在
    if not 判断进程是否存在(进程.pid):
        print(f"进程ID: {进程.pid} 不再运行.")
    else:
        print(f"进程ID: {进程.pid} 仍在运行.")
