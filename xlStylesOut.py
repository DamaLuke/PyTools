import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
import pandas as pd
from tkinter import messagebox as msg


# 输出带格式的excel
class xlStyleFormat:
    def __init__(self):
        self.title_font = Font(
            name="MYingHei_18030_C-Medium", size=10, bold=True, color="00FFFFFF"
        )
        self.title_fill = PatternFill(
            fill_type="solid", start_color="3D5AAE", end_color="3D5AAE"
        )
        self.body_font = Font(
            name="MYingHei_18030_C-Medium", size=9, bold=False, color="000000"
        )
        self.body_fill = PatternFill(
            fill_type="solid", start_color="00FFFFFF", end_color="00FFFFFF"
        )
        thin = Side(border_style="thin", color="000000")
        self.border = Border(left=thin, right=thin, top=thin, bottom=thin)
        self.align = Alignment(horizontal="center", vertical="center", wrapText=True)
        self.format_excel
        self.completedInfo
        
    def format_col(self, cell):
        if cell.value:
            cell.font = self.title_font
            cell.fill = self.title_fill
            cell.border = self.border
            cell.alignment = self.align

    def format_row(self, row):
        for cell in row:
            cell.font = self.body_font
            cell.fill = self.body_fill
            cell.border = self.border
            cell.alignment = self.align

    def completedInfo(self):
        msg.showinfo("Completed", "已完成！")

    def format_excel(self, path, headers, info):
        wb = openpyxl.load_workbook(path)
        if  headers != None:
            heads = headers
        else:
            heads = 1
        for ws in wb:
            for col in range(ws.min_column, ws.max_column + 1):
                ws.column_dimensions[get_column_letter(col)].auto_size = True
                for i in range(1, heads + 1):
                    cell = ws.cell(i, col)
                    self.format_col(cell)
            ws.auto_filter.ref = f"A{heads}:{get_column_letter(col)}{heads}"
            for row in ws.iter_rows(min_row=2):
                self.format_row(row)
        wb.save(path)
        if info == True:
            self.completedInfo()

    def write_excel(self, path, dfs, headers = None, info=False):
        with pd.ExcelWriter(path) as writer:
            for sheet, df in dfs.items():
                df.to_excel(writer, sheet_name=sheet, index=False)
        print("outfile path is in:" + path)
        self.format_excel(path, headers, info)
