import pymysql
from args import parser

args = parser.parse_args()

db = pymysql.connect(host=args.db_host, user=args.db_username, password=args.db_password, database=args.db_name)

cursor = db.cursor()

sql = """create table jsy_data (
    code int not null primary key,
    price float,
    date date)"""
cursor.execute(sql)

db.close()