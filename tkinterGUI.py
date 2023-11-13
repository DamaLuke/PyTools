import tkinter as tk
import tkinter.filedialog as fd
import sys

#GUI基本界面设计/文件选择控件组
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
    def __init__(self, title, width, height, color):
        self.root = tk.Tk()
        self.width = width
        self.height = height
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.title(title)
        self.root.geometry(f"{self.width}x{self.height}+{round((self.screen_width - self.width)/2)}+{round((self.screen_height - self.height)/2)}")
        self.root.config(bg=color)
        self.file_selectors = []

    def add_fileSelector(self, btntexts):
        for i, btntext in enumerate(btntexts, start=1):
            btntext = "请选择" + btntext + "文件"
            pathname = f"file{i}_path"
            file_selector = FileSelector(self.root, btntext, i, pathname)
            self.file_selectors.append(file_selector)
        self.confirm_cancel_(i + 1)

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
