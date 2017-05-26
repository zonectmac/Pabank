import sys, traceback
import xlrd, os
from xlwt import Workbook

all_list = []


def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(traceback.print_exc())


# 根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_last_first(file, by_index):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    col_names_last = table.row_values(2)
    col_names_first = table.row_values(0)
    f = [col_names_first[0][3:col_names_first[0].find('开始')], col_names_last[5]]
    lf = [f]
    return lf


# path 文件夹路径
def get_all(path):
    file_list = os.listdir(path)
    for tmp in file_list:
        if os.path.splitext(tmp)[1] == '.xls':
            fw = excel_table_last_first(path + tmp, 0)
            all_list.append(fw[0])
    print(all_list)
    print(len(all_list))


# 写入第一行和最后一行
def write_excel_fl(save_path):
    book = Workbook()
    sheet1 = book.add_sheet('Sheet 1')
    row_index = 0
    for text in all_list:
        row = sheet1.row(row_index)
        index = 0
        for row_text in all_list[row_index]:
            row.write(index, row_text)
            index += 1
        row_index += 1
    # sheet1.col(0).width = 30000
    book.save(save_path)


def write_all_ecxel(path, save_path):
    get_all(path)
    write_excel_fl(save_path)
