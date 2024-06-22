# 主窗口的實現，包含所有的 GUI 元件和用戶交互。你可以在這裡設計主窗口的佈局，並定義按鈕、菜單等的操作。
import tkinter as tk
from tkinter import ttk
from kubectlcommands import KubectlCommands
from kubectlutils import KubectlUtils

class MainWindow(tk.Frame):
  def __init__(self, parent):
    super().__init__(parent)
      
    self.parent = parent
    self.parent.title("LazyKubectl")
    
    # 上半部分：表格顯示區域
    self.table_frame = ttk.Frame(self.parent)
    self.table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    self.table_label = ttk.Label(self.table_frame, text="Table View")
    self.table_label.pack(pady=10)
    
    self.table = ttk.Treeview(self.table_frame, columns=("Name", "Status", "Age"), show="headings")
    self.table.heading("Name", text="Name")
    self.table.heading("Status", text="Status")
    self.table.heading("Age", text="Age")
    self.table.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    
    # 下半部分：文字訊息顯示區域
    self.text_frame = ttk.Frame(self.parent)
    self.text_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
    self.text_label = ttk.Label(self.text_frame, text="Text View")
    self.text_label.pack(pady=10)
    
    self.textbox = tk.Text(self.text_frame, wrap=tk.WORD)
    self.textbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    
    # 按鈕區域
    self.button_frame = ttk.Frame(self.parent)
    self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    self.load_button = ttk.Button(self.button_frame, text="get namespaces", command=self.load_namespaces)
    self.load_button.pack(side=tk.LEFT, padx=10, pady=5)
    
    self.load_button = ttk.Button(self.button_frame, text="get pods", command=self.load_pods, state=tk.DISABLED)
    self.load_button.pack(side=tk.LEFT, padx=10, pady=5)
    
    self.show_log_button = ttk.Button(self.button_frame, text="Show Log", command=self.show_selected_log)
    self.show_log_button.pack(side=tk.LEFT, padx=10, pady=5)
  
  def load_namespaces(self):
    output = KubectlCommands.get_namespaces()
    namespaces = KubectlUtils.parse_namespaces(output)
    
    if isinstance(namespaces, list):
      self.update_namespace_listbox(namespaces)
    else:
      self.update_textbox(namespaces)

  def update_namespace_listbox(self, namespaces):
    self.table.delete(0, tk.END)
    for namespace in namespaces:
      self.table.insert(tk.END, namespace)
  
  def load_pods(self):
    output = KubectlCommands.get_pods()
    pods = KubectlUtils.parse_pods(output)
    
    if isinstance(pods, list):
      self.update_table(pods)
    else:
      self.update_textbox(pods)
  
  def show_selected_log(self):
    selected_item = self.table.focus()
    if selected_item:
      pod_name = self.table.item(selected_item)["values"][0]  # Assuming first column is pod name
      log_output = KubectlCommands.get_pod_log(pod_name)
      self.update_textbox(log_output)
    else:
      self.update_textbox("Please select a pod first.")

  def update_table(self, data):
    self.table.delete(*self.table.get_children())
    
    if isinstance(data, list) and data:
      # Determine columns dynamically based on the first item in data
      columns = list(data[0].keys())
      
      # Setup Treeview columns if not already set
      if not self.table["columns"]:
        self.table["columns"] = columns
        for col in columns:
          self.table.heading(col, text=col)
      
      # Insert data into the table
      for item in data:
        values = [item[col] for col in columns]
        self.table.insert("", tk.END, values=values)
    else:
      # If data is not a list or empty list, show error message
      self.update_textbox(f"Invalid data: {data}")

  def update_textbox(self, message):
    self.textbox.delete("1.0", tk.END)
    self.textbox.insert(tk.END, message)