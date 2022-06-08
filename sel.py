from multiprocessing.sharedctypes import Value
from re import A
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import random
import string
import requests
import json
from faker import Faker

fake = Faker()
a=string.ascii_letters+string.digits

def getname():
    #return str(fake.first_name()+fake.last_name())
    return str(fake.first_name())

def getpasswd():
    key=random.sample(a,8)
    keys="".join(key)
    return keys


name=getname()
passwd=getpasswd()
#print(name + "|" + passwd)

option = webdriver.ChromeOptions()
#无头模式
#option.add_argument("--headless")
# 添加UA
option.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"')
# 忽略无用的日志
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
option.add_experimental_option('useAutomationExtension', False)
#禁用缓存
option.add_argument("disable-cache")
#INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
option.add_argument('log-level=3')
s = Service("chromedriver.exe")

driver = webdriver.Chrome(chrome_options=option,service=s)    # Chrome浏览器
driver.set_window_size(480, 800)

#driver.get("https://mail.io/credentials")

driver.get("https://mail.io/register")
nowhandle = driver.current_window_handle # 得到当前窗口句柄

# 隐式等待。网页加载数据需要时间，智能化等待
driver.implicitly_wait(20)

html = driver.page_source

#输入用户名
driver.find_element_by_id('mat-input-0').send_keys(name)
time.sleep (4)
driver.find_element_by_xpath('//*[@id="cdk-step-content-0-0"]/form/div/span/button').click()
time.sleep (3)

#输入密码
driver.find_element_by_id('mat-input-1').send_keys(passwd)
driver.find_element_by_id('mat-input-2').send_keys(passwd)
time.sleep (3)
driver.find_element_by_xpath('//*[@id="cdk-step-content-0-1"]/form/div/div/button').click()
time.sleep (3)

#注册
driver.find_element_by_xpath('//*[@id="cdk-step-content-0-2"]/div/button').click()
time.sleep (5)
driver.find_element_by_xpath('//*[@id="cdk-step-content-0-2"]/div/button').click()

time.sleep (4)

newwindow = 'window.open("https://mail.io/mailbox/settings")'
driver.execute_script(newwindow)
nowhandle = driver.current_window_handle # 得到当前窗口句柄

#移动句柄，对新打开页面进行操作
#driver.switch_to_window(driver.window_handles[0])

driver.refresh()
c = driver.get_cookies()
cookies = {}

# 获取cookie中的name和value,转化成requests可以使用的形式
for cookie in c:
    cookies[cookie['name']] = cookie['value']
#print(cookies)
driver.close()



headers = {
    'Referer': 'https://mail.io/',
    'auth-mailio': cookies['auth-mailio'],
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
res=requests.get('https://api.mail.io/api/v1/emergencykit',headers=headers)

dict = json.loads(s=res.text)
dict['username_password_login_enabled']=True
body=json.dumps(dict)

res2=requests.put('https://api.mail.io/api/v1/emergencykit',headers=headers,data=body)




with open("mailio.txt","a") as file:
    file.write(name + "|" + passwd)
    file.write('\n') # 换行
print("注册成功：" + name + "|" + passwd)

