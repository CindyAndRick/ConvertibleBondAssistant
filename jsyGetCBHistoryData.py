from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pymysql
from args import parser

args = parser.parse_args()

# 无头打开chrome
option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=option)

driver.get('https://www.jisilu.cn/account/login/')

WAIT = WebDriverWait(driver,10,0.5)
username = WAIT.until(EC.presence_of_element_located((By.NAME, "user_name")))
pwd = WAIT.until(EC.presence_of_element_located((By.XPATH, "//div[@class='password_login']//input[@name='password']")))
username.send_keys(args.jsy_username)
pwd.send_keys(args.jsy_password)
checkbox = WAIT.until(EC.presence_of_element_located((By.XPATH, "//div[@class='password_login']//div[@class='user_agree']//input")))
checkbox.click()
submit = WAIT.until(EC.presence_of_element_located((By.XPATH, "//div[@class='password_login']//a[@class='btn btn-jisilu']")))
submit.click()
sleep(1)

# 此时已经到达了主页
button = WAIT.until(EC.presence_of_element_located((By.XPATH, "//div[@class='menu']//a[@id='nav_data']")))
button.click()
sleep(3)

codelist = []

for index, item in enumerate(driver.find_elements_by_xpath("//div[@class='jsl-table-body-wrapper']/table[@class='jsl-table-body']/tbody/tr")):
    code = item.find_element_by_xpath("//div[@class='jsl-table-body-wrapper']/table[@class='jsl-table-body']/tbody/tr[{}]/td[3]/a[1]".format(index+1)).text
    codelist.append(code)

# print(codelist)

url = 'https://www.jisilu.cn/data/convert_bond_detail/'

db = pymysql.connect(host=args.db_host, user=args.db_username, password=args.db_password, database=args.db_name)
cursor = db.cursor()

for code in codelist:
    driver.get(url + code)
    # with open(file='./tmp.html', mode='w+', encoding='utf-8') as f:
    #     f.write(driver.page_source)
    #     f.close()
    for index, item in enumerate(driver.find_elements_by_xpath("//table[@class='tablesorter fixedtableheader']/tbody/tr")):
        date = item.find_element_by_xpath("//table[@class='tablesorter fixedtableheader']/tbody/tr[{}]/td[2]".format(index + 1)).text
        price = item.find_element_by_xpath("//table[@class='tablesorter fixedtableheader']/tbody/tr[{}]/td[3]".format(index + 1)).text
        # print(date, price)
        try:
            sql = 'insert into jsy_data(code, price, date) values ({}, {}, "{}")'.format(code, price, date)
            cursor.execute(sql)
            db.commit()
            print(code, index + 1, 'success', date, price)
        except Exception as e:
            print(code, index + 1, 'failed', sql)
            db.rollback()
            driver.quit()
            exit()
    # break

driver.quit()