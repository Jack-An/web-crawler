import xlrd
from acquire_info_university import get_all_info
from acquire_info_university import url_format


def integrate_data(page_num):
    data = xlrd.open_workbook('data.xls')
    table = data.sheet_by_index(0)
    uni_name = table.col_values(1)
    uni_name.pop(0)
    all_info = get_all_info(page_num)
    url_format(all_info)
    database = []
    for i in range(500):
        each_info = []
        if is_in_list(uni_name[i], all_info) != -1:
            index = is_in_list(uni_name[i], all_info)
            each_info.append(all_info[index][1])
            each_info.append(all_info[index][2])
            each_info.append(all_info[index][0])
            database.append(each_info)
        else:
            each_info.append(uni_name[i])
            each_info.append('http://――/')
            each_info.append('http://――/')
            database.append(each_info)
    return database


def is_in_list(name, all_info):
    for i in range(len(all_info)):
        if name in all_info[i]:
            return i
    return -1


def get_error_img_urls(database):
    count = 0
    for each in database:
        if each[2] == 'http://――/':
            count += 1
            print(each[0])
    print(count)


def main():
    page_num = 100
    database = integrate_data(page_num)
    print(database)
    get_error_img_urls(database)


if __name__ == "__main__":
    main()
