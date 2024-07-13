import tkinter as tk
from tkinter import ttk
from tkinter import font
from kubectlcommands import KubectlCommands
from kubectlutils import KubectlUtils

class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.parent.title("LazyKubectl")

        # 計算並設定視窗大小為螢幕寬度的70%
        screen_width = self.parent.winfo_screenwidth()
        window_width = int(screen_width * 0.7)
        window_height = 500  # 可以根據需要設定高度
        # 計算視窗在螢幕上的位置，使其居中
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((self.parent.winfo_screenheight() / 2) - (window_height / 2))
        self.parent.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        # 上半部分：表格顯示區域
        self.table_frame = ttk.Frame(self.parent)
        self.table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.table_button = ttk.Button(self.table_frame, text="get pod -A", command=self.command_get_all_pods)
        self.table_button.pack(pady=10)

        # 增加滾動條
        self.table_scroll_y = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.table_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.table_scroll_x = ttk.Scrollbar(self.table_frame, orient="horizontal")
        self.table_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.table = ttk.Treeview(self.table_frame, columns=("NAMESPACE", "NAME", "READY", "STATUS", "RESTARTS", "AGE", "IP", "NODE", "NOMINATED NODE", "READINESS GATES"), show="headings", yscrollcommand=self.table_scroll_y.set, xscrollcommand=self.table_scroll_x.set)
        self.table.heading("NAMESPACE", text="NAMESPACE")
        self.table.heading("NAME", text="NAME")
        self.table.heading("READY", text="READY")
        self.table.heading("STATUS", text="STATUS")
        self.table.heading("RESTARTS", text="RESTARTS")
        self.table.heading("AGE", text="AGE")
        self.table.heading("IP", text="IP")
        self.table.heading("NODE", text="NODE")
        self.table.heading("NOMINATED NODE", text="NOMINATED NODE")
        self.table.heading("READINESS GATES", text="READINESS GATES")
        self.table.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.table_scroll_y.config(command=self.table.yview)
        self.table_scroll_x.config(command=self.table.xview)

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

    def command_get_all_pods(self):
        output = KubectlCommands.get_all_pods()
        data = KubectlUtils.parse_get_all_pods(output)

        if isinstance(data, list):
            self.update_table(data)
        else:
            print(f"command_get_all_pods Error: {data}")

    def update_table(self, data):
        self.table.delete(*self.table.get_children())

        if isinstance(data, list) and data:
            # Determine columns dynamically based on the first item in data
            columns = list(data[0].keys())

            # Setup Treeview columns if not already set
            self.table["columns"] = columns
            for col in columns:
                self.table.heading(col, text=col)
                self.table.column(col, anchor=tk.W, width=font.Font().measure(col) + 20)  # Ensure text is left-aligned and add padding

            # Insert data into the table
            for item in data:
                values = [item[col] for col in columns]
                self.table.insert("", tk.END, values=values)

            # Adjust column widths to fit content
            for col in columns:
                max_width = font.Font().measure(col) + 20  # Start with the width of the column name
                for child in self.table.get_children():
                    cell_value = self.table.item(child)['values'][columns.index(col)]
                    cell_width = font.Font().measure(str(cell_value))
                    if cell_width > max_width:
                        max_width = cell_width
                self.table.column(col, width=max_width + 20)  # Add some padding
        else:
            # If data is not a list or empty list, show error message
            self.update_textbox(f"Invalid data: {data}")

    def update_textbox(self, message):
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.END, message)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
