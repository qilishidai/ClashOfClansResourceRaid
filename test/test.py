import tkinter as tk


class ConfigGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("配置界面")

        # 雷电模拟器索引
        self.label1 = tk.Label(self, text="雷电模拟器索引:")
        self.label1.grid(row=0, column=0)
        self.entry1 = tk.Entry(self)
        self.entry1.grid(row=0, column=1)

        # 部落冲突包名
        self.label2 = tk.Label(self, text="部落冲突包名:")
        self.label2.grid(row=1, column=0)
        self.entry2 = tk.Entry(self)
        self.entry2.grid(row=1, column=1)

        # 循环最大等待秒数
        self.label3 = tk.Label(self, text="循环最大等待秒数:")
        self.label3.grid(row=2, column=0)
        self.entry3 = tk.Entry(self)
        self.entry3.grid(row=2, column=1)

        # 需要执行多少秒
        self.label4 = tk.Label(self, text="需要执行多少秒:")
        self.label4.grid(row=3, column=0)
        self.entry4 = tk.Entry(self)
        self.entry4.grid(row=3, column=1)

        # 一直执行
        self.check_var1 = tk.BooleanVar()
        self.check1 = tk.Checkbutton(self, text="一直执行", variable=self.check_var1)
        self.check1.grid(row=4, column=0)

        # 是否开启刷墙
        self.check_var2 = tk.BooleanVar()
        self.check2 = tk.Checkbutton(self, text="是否开启刷墙", variable=self.check_var2)
        self.check2.grid(row=5, column=0)

        # 至少多少金币开始刷墙
        self.label5 = tk.Label(self, text="至少多少金币开始刷墙:")
        self.label5.grid(row=6, column=0)
        self.entry5 = tk.Entry(self)
        self.entry5.grid(row=6, column=1)

        # 至少多少圣水开始刷墙
        self.label6 = tk.Label(self, text="至少多少圣水开始刷墙:")
        self.label6.grid(row=7, column=0)
        self.entry6 = tk.Entry(self)
        self.entry6.grid(row=7, column=1)

        # 确定按钮
        self.button = tk.Button(self, text="确定", command=self.get_config)
        self.button.grid(row=8, columnspan=2)

    def get_config(self):
        雷电模拟器索引 = self.entry1.get()
        部落冲突包名 = self.entry2.get()
        循环最大等待秒数 = self.entry3.get()
        需要执行多少秒 = self.entry4.get()
        一直执行 = self.check_var1.get()
        是否开启刷墙 = self.check_var2.get()
        至少多少金币开始刷墙 = self.entry5.get()
        至少多少圣水开始刷墙 = self.entry6.get()

        # 这里可以根据需要将获取到的配置参数传递给你的程序

        # 打印获取到的配置参数
        print("雷电模拟器索引:", 雷电模拟器索引)
        print("部落冲突包名:", 部落冲突包名)
        print("循环最大等待秒数:", 循环最大等待秒数)
        print("需要执行多少秒:", 需要执行多少秒)
        print("一直执行:", 一直执行)
        print("是否开启刷墙:", 是否开启刷墙)
        print("至少多少金币开始刷墙:", 至少多少金币开始刷墙)
        print("至少多少圣水开始刷墙:", 至少多少圣水开始刷墙)


# 创建界面对象
app = ConfigGUI()
app.mainloop()
