from tkinter import *


class 界面程序(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=BOTH, expand=True)
        self.创建窗口()

    def 创建窗口(self):
        self.菜单栏 = Menu(self.master)
        self.菜单栏.add_command(label="启动", command=self.启动脚本)
        self.菜单栏.add_command(label="停止", command=self.停止脚本)

        # 更多子菜单,并添加相关选项
        self.更多子菜单 = Menu(self.菜单栏, tearoff=0)
        self.更多子菜单.add_command(label="隐藏模拟器", command=self.隐藏模拟器)
        self.更多子菜单.add_command(label="显示模拟器", command=self.显示模拟器)
        self.更多子菜单.add_separator()  # 添加分割线
        self.更多子菜单.add_command(label="禁止操作模拟器", command=self.禁止操作模拟器)
        self.更多子菜单.add_command(label="恢复操作模拟器", command=self.恢复操作模拟器)

        # 将更多子菜单添加到菜单栏
        self.菜单栏.add_cascade(label="更多", menu=self.更多子菜单)

        # 将我们建立好的整一个菜单栏在root窗口中显示
        self.master.config(menu=self.菜单栏)

        Label(self, text="当前运行状态").grid(row=0, column=0)

        # 创建滚动条并关联到列表框
        self.滚动条 = Scrollbar(self)
        self.列表框 = Listbox(self, width=50, yscrollcommand=self.滚动条.set)
        self.滚动条.config(command=self.列表框.yview)

        # 使用grid布局
        self.列表框.grid(row=1, column=0, sticky=N + S + E + W)
        self.滚动条.grid(row=1, column=1, sticky=N + S)

        # 配置行和列的权重，使列表框和滚动条可以扩展
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        Button(self, text="添加列表项", command=self.添加列表项).grid(row=2, column=0, columnspan=2)

    def 添加列表项(self):
        # 检查列表框中的项数是否超过500，如果是则删除最早的一项
        if self.列表框.size() >= 500:
            self.列表框.delete(0)
        # 插入新项到列表框
        self.列表框.insert(END, "新项")
        # 滚动到列表框的最底部
        self.列表框.yview_moveto(1)

    def 启动脚本(self):
        print("启动脚本")

    def 停止脚本(self):
        print("停止脚本")

    def 隐藏模拟器(self):
        print("隐藏模拟器")

    def 显示模拟器(self):
        print("显示模拟器")

    def 禁止操作模拟器(self):
        print("禁止操作模拟器")

    def 恢复操作模拟器(self):
        print("恢复操作模拟器")


根窗口 = Tk()
根窗口.geometry("400x250+700+400")
根窗口.title("部落冲突夜世界辅助")

我的程序 = 界面程序(根窗口)
根窗口.mainloop()
