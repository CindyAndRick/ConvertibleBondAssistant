from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pymysql
from args import parser

args = parser.parse_args()
# driver = webdriver.PhantomJS(executable_path='F:\\工具\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
# 无头打开chrome
option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=option)

driver.get('https://www.jisilu.cn/account/login/')

# with open(file='./tmp.html', mode='w+', encoding='utf-8') as f:
#         f.write(driver.page_source)
#         f.close()

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

# with open(file='./tmp.html', mode='w+', encoding='utf-8') as f:
#         f.write(driver.page_source)
#         f.close()

db = pymysql.connect(host=args.db_host, user=args.db_username, password=args.db_password, database=args.db_name)
cursor = db.cursor()

for index, item in enumerate(driver.find_elements_by_xpath("//div[@class='jsl-table-body-wrapper']/table[@class='jsl-table-body']/tbody/tr")):
    # 序号
    print(index + 1)
    # 代码
    # print('代码', item.find_element_by_xpath("//div[@class='jsl-table-body-wrapper']/table[@class='jsl-table-body']/tbody/tr[{}]/td[3]/a[1]".format(index+1)).text)
    # 可转债名称
    print('可转债名称', item.find_element_by_xpath("//div[@class='jsl-table-body-wrapper']/table[@class='jsl-table-body']/tbody/tr[{}]/td[4]/span[1]".format(index+1)).text)
    # 当日价格
    # print('当日价格', item.find_element_by_xpath("//div[@class='jsl-table-body-wrapper']/table[@class='jsl-table-body']/tbody/tr[{}]/td[5]/span[1]".format(index+1)).text)
    # 到期时间
    # print('到期时间', item.find_element_by_xpath("//div[@class='jsl-table-body-wrapper']/table[@class='jsl-table-body']/tbody/tr[{}]/td[24]/span[1]".format(index+1)).text)
    code = item.find_element_by_xpath("//div[@class='jsl-table-body-wrapper']/table[@class='jsl-table-body']/tbody/tr[{}]/td[3]/a[1]".format(index+1)).text
    name = item.find_element_by_xpath("//div[@class='jsl-table-body-wrapper']/table[@class='jsl-table-body']/tbody/tr[{}]/td[4]/span[1]".format(index+1)).text
    # price = item.find_element_by_xpath("//div[@class='jsl-table-body-wrapper']/table[@class='jsl-table-body']/tbody/tr[{}]/td[5]/span[1]".format(index+1)).text
    expire = item.find_element_by_xpath("//div[@class='jsl-table-body-wrapper']/table[@class='jsl-table-body']/tbody/tr[{}]/td[24]/span[1]".format(index+1)).text
    try:
        sql = 'insert into cb_list(code, name, expire) values ({}, "{}", "{}")'.format(code, name, expire)
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

driver.quit()
db.close()
print('finish')