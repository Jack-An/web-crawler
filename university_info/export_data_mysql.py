import pymysql.cursors
from acquire_info_university import get_all_info
from acquire_info_university import url_format


def create_table():
    db = pymysql.connect("localhost", "root", "zt980516.", "mydata")
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("drop table if exists university")
    # 使用预处理语句创建表
    sql = """CREATE TABLE university (
             uniname  CHAR(20) NOT NULL,
             uniurl  CHAR(255),
             imgurl CHAR(255) 
             )"""

    cursor.execute(sql)

    # 关闭数据库连接
    db.close()


def write_data():
    page_num = 50
    all_info = get_all_info(page_num)
    database = url_format(all_info)
    data = []
    for item in database:
        if item not in data:
            data.append(item)
    con = pymysql.connect(host='localhost', user='root', password='zt980516.', db='mydata', charset='utf8mb4')
    sql = "insert into university values(%s,%s,%s)"
    try:
        for each in data:
            with con.cursor() as cursor:
                cursor.execute(sql, (each[0], each[1], each[2]))
            con.commit()
    finally:
        con.close()


def main():
    create_table()
    write_data()


if __name__ == '__main__':
    main()
