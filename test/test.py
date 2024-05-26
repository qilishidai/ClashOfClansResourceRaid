import tkinter as tk
from tkinter import Menu, Toplevel, Label

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = Label(self.tooltip, text=self.text, background="yellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class CustomMenu(Menu):
    def __init__(self, master, **kwargs):
        Menu.__init__(self, master, **kwargs)
        self.tooltips = {}

    def add_command_with_tooltip(self, label, command, tooltip_text, state=tk.NORMAL):
        index = self.index(tk.END)
        self.add_command(label=label, command=command, state=state)
        if state == tk.DISABLED:
            # Create a hidden button to associate the tooltip
            hidden_button = tk.Button(self.master, state=tk.DISABLED)
            hidden_button.pack_forget()
            self.tooltips[index] = ToolTip(hidden_button, tooltip_text)
            self.bind("<Enter>", lambda e, idx=index: self.show_tooltip(idx, e), add="+")
            self.bind("<Leave>", lambda e, idx=index: self.hide_tooltip(idx, e), add="+")

    def show_tooltip(self, index, event):
        if index in self.tooltips:
            widget = self.tooltips[index].widget
            widget.event_generate("<Enter>", when="tail")

    def hide_tooltip(self, index, event):
        if index in self.tooltips:
            widget = self.tooltips[index].widget
            widget.event_generate("<Leave>", when="tail")

class 应用程序:
    def __init__(self, root):
        self.root = root
        self.创建菜单()

    def 创建菜单(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        self.更多子菜单 = CustomMenu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="更多", menu=self.更多子菜单)

        # 添加一个不可点击的菜单项，并设置提示信息
        self.更多子菜单.add_command_with_tooltip(label="隐藏模拟器", command=self.隐藏模拟器, tooltip_text="当前不可用", state=tk.DISABLED)

    def 隐藏模拟器(self):
        print("模拟器隐藏")

if __name__ == "__main__":
    root = tk.Tk()
    app = 应用程序(root)
    root.mainloop()
