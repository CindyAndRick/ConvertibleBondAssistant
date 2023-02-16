import pymysql
from args import parser

args = parser.parse_args()

db = pymysql.connect(host=args.db_host, port=args.db_port, user=args.db_username, password=args.db_password, database=args.db_name)

cursor = db.cursor()

try:
    sql1 = """create table jsy_data (
        code int not null primary key,
        price float,
        date date primary key)"""
    cursor.execute(sql1)

    sql2 = """create table cb_list (
        code int not null primary key,
        name char(20),
        expire char(20))"""
    cursor.execute(sql2)

    sql3 = """create table inc_data (
        code int not null primary key,
        name char(20),
        inc_d char(10),
        inc_w char(10),
        inc_m char(10),
        expire char(20))"""
    cursor.execute(sql3)

    sql4 = """create table follow (
        code int not null primary key,
        add_date date not null)"""
    cursor.execute(sql4)

    sql5 = """alter table jsy_data add index index_code_date (code, date)"""
    cursor.execute(sql5)

    sql6 = """create index index_code on cb_list (code)"""
    cursor.execute(sql6)

    sql7 = """create index index_code on inc_data (code)"""
    cursor.execute(sql7)

    sql8 = """create index index_code on follow (code)"""
    cursor.execute(sql8)
    
    db.commit()
except Exception as e:
    print(e)
    db.rollback()
