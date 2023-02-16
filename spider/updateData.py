import pymysql
from datetime import date, datetime, timedelta
from args import parser

args = parser.parse_args()

db = pymysql.connect(host=args.db_host, port=args.db_port, user=args.db_username, password=args.db_password, database=args.db_name)

cursor = db.cursor()

today = date.today() - timedelta(days = 4)


sql1 = "SELECT DISTINCT code FROM jsy_data"
cursor.execute(sql1)
code_list = cursor.fetchall()

for code_item in code_list:
    # print(code_item[0])
    inc_d = "无"
    inc_w = "无"
    inc_m = "无"
    sql2 = "SELECT price, date FROM jsy_data WHERE code={} AND date>='{}' ORDER BY date DESC".format(code_item[0], date.today() - timedelta(days = 41))
    # print(sql2)
    num = cursor.execute(sql2)
    res = cursor.fetchall()
    # 可能今天并没有数据，故取最近数据
    closest = res[0]
    for item in res:
        if inc_d == "无" and (closest[1] - item[1]) >= timedelta(days = 1):
            inc_d = "{:.6f}".format((closest[0] - item[0]) / item[0])
            # print(item[1], inc_d)
        if inc_w == "无" and (closest[1] - item[1]) >= timedelta(days = 7):
            inc_w = "{:.6f}".format((closest[0] - item[0]) / item[0])
            # print(item[1], inc_w)
        if inc_m == "无" and (closest[1] - item[1]) >= timedelta(days = 30):
            inc_m = "{:.6f}".format((closest[0] - item[0]) / item[0])
            # print(item[1], inc_m)
            break

    sql3 = "SELECT name, expire FROM cb_list WHERE code={}".format(code_item[0])
    # print(sql3)
    num = cursor.execute(sql3)
    # print(num)
    name, expire = cursor.fetchone()
    sql4 = "INSERT INTO inc_data(code, name, inc_d, inc_w, inc_m, expire) VALUES ({}, '{}', '{}', '{}', '{}', '{}')".format(code_item[0], name, inc_d, inc_w, inc_m, expire)
    # print(sql4)
    try:
        cursor.execute(sql4)
        db.commit()
        print(code_item[0], 'success')
    except Exception as e:
        db.rollback()
        print(code_item[0], 'failed', e)

db.close()