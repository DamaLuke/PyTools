import tkinter as tk
import tkinter.filedialog as fd
import sys



# GUI基本界面设计/文件选择、参数输入控件组
class AddWidgets:
    def __init__(self, parent, param, i):
        self.parent = parent
        self.param = param
        self.i = i
        
    def CreateFrame(self):
        frame = tk.Frame(self.parent)
        frame.grid(row=self.i, padx=15, pady=15, sticky="w")
        return frame
    
    def FileSelector(self):
        frame = self.CreateFrame()
        param = "请选择" + self.param + "文件"
        self.button = tk.Button(
            frame,
            text=param,
            command=lambda: self.get_filename(),
            relief=tk.RAISED,
            borderwidth=1,
        )
        self.label = tk.Label(frame, width=75)
        self.button.pack(side="left", padx=5, pady=5)
        self.label.pack(side="right", padx=5, pady=5)
        
    def get_filename(self):
        file_path = fd.askopenfilename()
        file_name = file_path.split("/")[-1]
        self.label.configure(text=file_name, bg="white")
        setattr(self.parent, f"arg{self.i}", file_path)
        
    def text_entry(self):
        frame = self.CreateFrame()
        param = "请输入" + self.param.split('_')[1]
        self.entry_text = tk.StringVar()

        self.entry = tk.Entry(frame, textvariable=self.entry_text)
        self.label = tk.Label(frame, text=param, relief=tk.RAISED, borderwidth=1)
        self.label.pack(side="left", padx=5, pady=5)        
        self.entry.pack(side="right", padx=5, pady=5)
        setattr(self.parent, f"arg{self.i}", self.entry_text)
        
        
class Root:
    def __init__(self, title="选择对应的文件"):  # title default value
        self.root = tk.Tk()
        self.root.title(title)
        self.widgets = []

        
    def resize_root(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = round((screen_width - width) / 2)
        y = round((screen_height - height) / 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def add_widgets(self, *params): 
        """添加文件选择器和参数输入两种控件，若是后一种，需要在文本面前添加'Entry'，并用'_'隔开""" 
        for i, param in enumerate(params, start=1):     
            added_widget = AddWidgets(self.root, param, i)
            if param.split('_')[0] != 'En':
                added_widget.FileSelector()       
            else:
                added_widget.text_entry()
            self.widgets.append(added_widget)
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

