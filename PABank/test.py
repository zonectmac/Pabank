import sys, traceback
import xlrd
from xlwt import Workbook
from tempfile import TemporaryFile


def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(traceback.print_exc())


# 根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file, colnameindex, by_index):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    colnames = table.row_values(colnameindex)  # 某一行数据
    list = []
    for rownum in range(1, nrows):

        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list


def excel_table_getlast(file, by_index):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    colnames = table.row_values(nrows - 1)  # 某一行数据
    print(colnames)
    print(type(colnames))
    print(table.row_values(0))
    list = []
    for rownum in range(1):

        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list


# 根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file, colnameindex=0, by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows  # 行数
    colnames = table.row_values(colnameindex)  # 某一行数据
    list = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list


def main():
    tables = excel_table_byindex('D:/pabank2/we.xls', 0, 0)
    for row in tables:
        print(row)

        # tables = excel_table_byname()
        # for row in tables:
        #     print(row)


def write_excel():
    book = Workbook()
    sheet1 = book.add_sheet('Sheet 1')
    sheet1.write(0, 0, 'A1')
    sheet1.write(0, 1, 'B1')
    row1 = sheet1.row(1)
    row1.write(0, 'A2')
    row1.write(1, 'B2')

    sheet1.col(0).width = 10000
    book.save('D:/pabank2/simple.xls')
    book.save(TemporaryFile())


def write_excel_ff(file, by_index):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    colnames = table.row_values(nrows - 1)  # 某一行数据
    book = Workbook()
    sheet1 = book.add_sheet('Sheet 1')
    row1 = sheet1.row(0)
    index = 0
    for text in colnames:
        row1.write(index, text)
        index += 1
    # sheet1.col(0).width = 10000
    book.save('D:/pabank2/simple2.xls')


if __name__ == "__main__":
    # main()
    tables = excel_table_getlast('D:/pabank2/we.xls', 0)
    # for row in tables:
    #     print(row)
    # write_excel()
    # write_excel_ff('D:/pabank2/we.xls', 0)