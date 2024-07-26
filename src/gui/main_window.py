import tkinter as tk
from tkinter import ttk
from tkinter import font, messagebox, Menu
from kubectlcommands import KubectlCommands
from language_manager import LanguageManager

class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.language_manager = LanguageManager()

        self.parent = parent
        self.parent.title("LazyKubectl")

        self.geometry()

        self.create_menu()
        self.create_table()
        self.create_command_panel()
        self.create_log()

        self.theme()
        self.update_language()

    def command_get_all_pods(self):
        data = KubectlCommands.get_all_pods()

        if isinstance(data, list):
            self.update_table(data)
        else:
            self.update_log(f"command_get_all_pods Error: {data}")

    def command_describe_pod(self):
        selected_item = self.table.focus()
        if selected_item:
            output = KubectlCommands.describe_pod(self.get_selected_name(), self.get_selected_namespace())
            self.update_log(output)
        else:
            self.update_log(self.language_manager.translate("no-pod-selected"))
    
    def command_delete_pod(self):
        selected_item = self.table.focus()
        if selected_item:
            confirm = messagebox.askyesno(self.language_manager.translate("confirm-delete"), f"Are you sure you want to delete pod '{self.get_selected_name()}' in namespace '{self.get_selected_namespace()}'?")
            if confirm:
                output = KubectlCommands.delete_pod(self.get_selected_name(), self.get_selected_namespace())
                self.update_log(output)

                self.command_get_all_pods()
        else:
            self.update_log(self.language_manager.translate("no-pod-selected"))
    
    def command_logs_pod(self):
        selected_item = self.table.focus()
        if selected_item:
            output = KubectlCommands.logs_pod(self.get_selected_name(), self.get_selected_namespace())
            self.update_log(output)
        else:
            self.update_log(self.language_manager.translate("no-pod-selected"))
    
    def get_selected_namespace(self):
        print(f"get_selected_namespace: {self.table.item(self.table.focus())['values'][0]}")
        return self.table.item(self.table.focus())["values"][0]
    
    def get_selected_name(self):
        print(f"get_selected_name: {self.table.item(self.table.focus())['values'][1]}")
        return self.table.item(self.table.focus())["values"][1]

    def copy_log(self):
        self.parent.clipboard_clear()
        self.parent.clipboard_append(self.log.get("1.0", tk.END))

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
            self.update_log(f"Invalid data: {data}")

    def update_log(self, message):
        self.log.config(state=tk.NORMAL)
        self.log.delete("1.0", tk.END)
        self.log.insert(tk.END, message)
        self.log.config(state=tk.DISABLED)
        self.log.see(tk.END)

    def create_menu(self):
        self.menubar = tk.Menu(self.parent)

        self.language_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.language_manager.translate("menubar-languages"), menu=self.language_menu)
        
        for lang, lang_name in self.language_manager.get_available_languages().items():
            self.language_menu.add_command(label=lang_name, command=lambda l=lang: self.set_language(l))

        self.parent.config(menu=self.menubar)

    def set_language(self, language):
        print(f"Setting language: {language}")
        self.language_manager.set_language(language)
        self.update_language()

    def update_language(self):
        print(f"Current language: {self.language_manager.current_language}")
        self.parent.title(self.language_manager.translate("title"))
        self.get_pod_A_button.config(text=self.language_manager.translate("get-pod-a-button"))
        self.describe_pod_button.config(text=self.language_manager.translate("describe-pod-button"))
        self.delete_pod_button.config(text=self.language_manager.translate("delete-pod-button"))
        self.copy_log_button.config(text=self.language_manager.translate("copy-log-button"))
        self.log_label.config(text=self.language_manager.translate("log-label"))
        self.logs_pod_button.config(text=self.language_manager.translate("logs-pod-button"))
        
    def create_table(self):
        self.table_frame = ttk.Frame(self.parent)
        self.table_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.table_scroll_x = ttk.Scrollbar(self.table_frame, orient="horizontal")
        self.table_scroll_y = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.table_scroll_x.grid(row=1, column=0, sticky="ew")
        self.table_scroll_y.grid(row=0, column=1, sticky="ns")

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
        self.table.grid(row=0, column=0, sticky="nsew")

        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        self.table_scroll_y.config(command=self.table.yview)
        self.table_scroll_x.config(command=self.table.xview)
    
    def create_command_panel(self):
        self.command_panel = ttk.Frame(self.parent)
        self.command_panel.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.get_pod_A_button = ttk.Button(self.command_panel, text=self.language_manager.translate("get-pod-a-button"), command=self.command_get_all_pods)
        self.get_pod_A_button.grid(row=0, column=0, padx=10, pady=10)

        self.describe_pod_button = ttk.Button(self.command_panel, text=self.language_manager.translate("describe-pod-button"), command=self.command_describe_pod)
        self.describe_pod_button.grid(row=0, column=1, padx=10)

        self.logs_pod_button = ttk.Button(self.command_panel, text=self.language_manager.translate("logs-pod-button"), command=self.command_logs_pod)
        self.logs_pod_button.grid(row=0, column=2, padx=10)

        self.delete_pod_button = ttk.Button(self.command_panel, text=self.language_manager.translate("delete-pod-button"), command=self.command_delete_pod)
        self.delete_pod_button.grid(row=0, column=3, padx=10)

        self.copy_log_button = ttk.Button(self.command_panel, text=self.language_manager.translate("copy-log-button"), command=self.copy_log)
        self.copy_log_button.grid(row=0, column=4, padx=10)

    def create_log(self):
        self.log_Frame = ttk.Frame(self.parent)
        self.log_Frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

        self.log_label = ttk.Label(self.log_Frame, text="Log:")
        self.log_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.log_scroll_x = ttk.Scrollbar(self.log_Frame, orient="horizontal")
        self.log_scroll_x.grid(row=2, column=0, sticky="ew")
        self.log_scroll_y = ttk.Scrollbar(self.log_Frame, orient="vertical")
        self.log_scroll_y.grid(row=1, column=1, sticky="ns")

        self.log = tk.Text(self.log_Frame, wrap=tk.WORD, state=tk.DISABLED, yscrollcommand=self.log_scroll_y.set, xscrollcommand=self.log_scroll_x.set)
        self.log.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.log_Frame.grid_rowconfigure(1, weight=1)
        self.log_Frame.grid_columnconfigure(0, weight=1)

        self.log_scroll_x.config(command=self.log.xview)
        self.log_scroll_y.config(command=self.log.yview)

    def theme(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#2e2e2e")
        self.style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
        self.style.configure("TButton", background="#4a4a4a", foreground="#ffffff")
        self.style.configure("Treeview", background="#2e2e2e", fieldbackground="#2e2e2e", foreground="#ffffff")
        self.style.configure("Treeview.Heading", background="#4a4a4a", foreground="#ffffff")
        self.style.map("TButton", background=[("active", "#4a4a4a")])
        self.style.map("Treeview.Heading", background=[("active", "#6a6a6a")])

        self.log.configure(background="#2e2e2e", foreground="#ffffff", insertbackground="white")
    
    def geometry(self):
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_rowconfigure(1, weight=0)
        self.parent.grid_rowconfigure(2, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        screen_width = self.parent.winfo_screenwidth()
        window_width = int(screen_width * 0.7)
        window_height = int(screen_width * 0.3)

        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((self.parent.winfo_screenheight() / 2) - (window_height / 2))
        self.parent.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    app.grid(row=0, column=0, sticky="nsew")
    root.mainloop()
