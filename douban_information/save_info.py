from xlrd import open_workbook
from xlutils.copy import copy
from get_book_info import main


def write_data():
    database = main()
    print(len(database))
    print('start write data ....')
    print('Almost finished ...')
    rb = open_workbook('dd.xls')
    wb = copy(rb)
    ws = wb.get_sheet(0)
    for i in range(len(database)):
        try:
            ws.write(i + 1, 0, i + 1)
            ws.write(i + 1, 1, database[i][0])
            ws.write(i + 1, 2, database[i][1])
            ws.write(i + 1, 3, database[i][2])
            ws.write(i + 1, 4, database[i][3])
            ws.write(i + 1, 5, database[i][4])
            ws.write(i + 1, 6, database[i][5])
            ws.write(i + 1, 7, database[i][6])
        except:
            continue
    wb.save('dd.xls')


if __name__ == '__main__':
    write_data()
    print('OK !')
