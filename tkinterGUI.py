import tkinter as tk
import tkinter.filedialog as fd
import sys


# GUI基本界面设计/文件选择控件组
class FileSelector:
    def __init__(self, parent, btntext, i, pathname):
        self.parent = parent
        self.btntext = btntext
        self.i = i
        frame = tk.Frame(self.parent)
        frame.grid(row=i, padx=15, pady=15, sticky="w")
        self.button = tk.Button(
            frame,
            text=self.btntext,
            command=lambda: self.get_filename(),
            relief=tk.RAISED,
            borderwidth=1,
        )
        self.label = tk.Label(frame, width=75)
        self.button.pack(side="left", padx=5, pady=5)
        self.label.pack(side="right", padx=5, pady=5)
        self.pathname = pathname

    def get_filename(self):
        file_path = fd.askopenfilename()
        file_name = file_path.split("/")[-1]
        self.label.configure(text=file_name, bg="white")
        setattr(self.parent, self.pathname, file_path)


class Root:
    def __init__(self, title = "选择对应的文件"): #title default value
        self.root = tk.Tk()
        self.root.title(title)
        self.file_selectors = []
        
    def resize_root(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = round((screen_width - width) / 2)
        y = round((screen_height - height) / 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def add_fileSelector(self, *btntexts): #设为可变参数，简化输入
        for i, btntext in enumerate(btntexts, start=1):
            btntext = "请选择" + btntext + "文件"
            pathname = f"file{i}_path"
            file_selector = FileSelector(self.root, btntext, i, pathname)
            self.file_selectors.append(file_selector) 
        self.confirm_cancel_(i + 1)
        self.resize_root()

    def confirm_cancel_(self, loc):
        frame = tk.Frame(self.root)
        frame.grid(row=loc, padx=15, pady=15)
        self.confirm_btn = tk.Button(
            frame,
            text="确定",
            command=lambda: self.on_confirm(),
            relief=tk.RAISED,
            borderwidth=1,
            width=10,
        )
        self.cancel_btn = tk.Button(
            frame,
            text="取消",
            command=lambda: self.on_cancel(),
            relief=tk.RAISED,
            borderwidth=1,
            width=10,
        )
        self.confirm_btn.pack(side="left", padx=5, pady=5)
        self.cancel_btn.pack(side="right", padx=5, pady=5)

    def on_confirm(self):
        self.root.destroy()
        print("confirm execution")

    def on_cancel(self):
        self.root.destroy()
        print("cancel execution")
        sys.exit()

    def mainloop(self):
        self.root.mainloop()
