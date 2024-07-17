# 主程式入口，負責初始化 GUI 和管理主要的應用邏輯。這裡你可以初始化 GUI，設置事件處理，並將 GUI 元件與命令生成器和命令執行器連接起來。
import tkinter as tk
from gui.main_window import MainWindow

class LazyKubectlApp:
  def __init__(self, root):
    self.root = root
    self.root.title("LazyKubectl")
    
    self.main_window = MainWindow(self.root)
    self.main_window.grid(row=0, column=0, sticky="nsew")

def main():
  root = tk.Tk()
  app = LazyKubectlApp(root)
  root.mainloop()

if __name__ == "__main__":
  main()
