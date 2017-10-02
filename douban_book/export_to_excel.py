from acquire_information import acquire_info

from xlrd import open_workbook
from xlutils.copy import copy


# 写数据到excel表格中
def save_info():
    book_data = acquire_info()
    rb = open_workbook('book.xls')
    wb = copy(rb)
    ws = wb.get_sheet(0)
    for i in range(250):
        ws.write(i + 1, 0, i + 1)
        ws.write(i + 1, 1, book_data[i][0])
        ws.write(i + 1, 2, book_data[i][1])
        ws.write(i + 1, 3, book_data[i][2])
        ws.write(i + 1, 4, book_data[i][3])
        ws.write(i + 1, 5, book_data[i][4])

    wb.save('book.xls')


if __name__ == '__main__':
    save_info()
    print("OK !")
