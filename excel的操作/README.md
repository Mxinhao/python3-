# python3-
学习使用python，平时使用到的小代码

openpyxl库的使用

导入库

        import openpyxl
        from openpyxl.styles import Font,Border,Alignment,Side
        from openpyxl.worksheet.copier import WorksheetCopy
        import openpyxl.styles as sty

    1、创建新文件

        workbook=openpyxl.Workbook('hello.xlxs')
        sheet=workbook.create_sheet(title="Pi",index=1)

    2、打开已存在的文件

        workbook = openpyxl.load_workbook(filename="aaa.xlsx")
        <!-- 获取sheet1工作表 -->
        sheet = workbook.get_sheet_by_name("sheet1")
        <!-- 或者获取打开的默认活动页 -->
        ws = workbook.active

    3、从模板复制得到新sheet

        workbook = openpyxl.load_workbook(filename="aaa.xlsx")
        sheet=workbook.get_sheet_by_name("模板")
        copy_sheet=workbook.copy_worksheet(workbook,sheet) #默认得到的sheet名为"模板 Copy"，位置在最后一个
        copy_sheet.title="1111"  #设置sheet的名字

    4、获取和设置单元格的值

        #几种设置单元格值得方式
        sheet.cell(column=1, row=1).value="hello"
        sheet.cell(column=1, row=1,value="hello")
        sheet["A1"].value="word"
        sheet["A1"].value="=sum(A1:B2)"
        #获取单元格的值
        aa=sheet["A1"].value
        bb=sheet.cell(column=1, row=1).value
        <!-- 获取数据最大行和最大列 -->
        max_row=sheet.max_row
        max_row=sheet.max_column
        <!-- 获取sheet的名字和设置名字背景色，无色设为None -->
        title=sheet.title
        sheet.sheet_properties.tabColor = "1072BA"

    5、设置单元格样式

        <!-- 设置字体和大小 -->
        font=Font(name='华文细黑', size=9)
        <!-- 水平和垂直居中 -->
        alignment = Alignment(horizontal='center',
                 vertical='center')
        <!-- 左右下边框为黑色细边框 -->
        border = Border(left=Side(border_style="thin",color = '00000000'),
            right = Side(border_style="thin",color = '00000000'),
            bottom = Side(border_style="thin",color = '00000000')
            )
        
        sheet = workbook.get_sheet_by_name("sheet1")
        sheet["A1"].font = font
        sheet["A1"].alignment = alignment
        sheet["A1"].border = border
        <!-- 设置内容格式百分比保留两位小数 0.00%  设置整数格式为0 -->
        sheet["A1"].number_format = "0.00%"
        <!-- 日期格式 yyyy/m/d-->
        sheet["A1"].number_format = "yyyy/m/d"
        <!-- 千分位符 -->
        sheet["A1"].number_format = "#,##"
        <!-- sheet是否被选中，选中多个时会被锁定无法复制单元格数据 -->
        sheet.views.sheetView[0].tabSelected=False
        <!-- 设置背景色 -->
        sheet.cell(row=1, column=1).fill = sty.PatternFill(fill_type='solid', fgColor="00FF99FF")  #ARGB格式，前两位为透明度

    6、根据所在列获取对应的英文表示

        from openpyxl.utils import get_column_letter
        tag=get_column_letter(10)
