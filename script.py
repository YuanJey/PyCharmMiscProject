# 这是一个示例 Python 脚本。
import os
import time
# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。
import uuid
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
m_100='https://sc.yuanda.info/pg/234.html'
m_200='https://sc.yuanda.info/pg/235.html'
m_500='https://sc.yuanda.info/pg/237.html'
m_1000='https://sc.yuanda.info/pg/240.html'
m_2000='https://sc.yuanda.info/pg/241.html'
def play(driver,number):
    # driver.get('https://sc.yuanda.info/pg/234.html')
    if  number==100:
        driver.get(m_100)
    elif number==200:
        driver.get(m_200)
    elif number==500:
        driver.get(m_500)
    elif number==1000:
        driver.get(m_1000)
    elif number==2000:
        driver.get(m_2000)
    buy_button = driver.find_element(By.CSS_SELECTOR, 'a.buy-btn')
    buy_button.click()
    play = driver.find_element(By.XPATH, '//div//ul//li//a[text()="找人代付"]')
    play.click()
    submit_button = driver.find_element(By.ID, 'jiesuan')
    submit_button.click()


def check(src):
    url = 'https://test-1312265679.cos.ap-chengdu.myqcloud.com/config.json'
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        # print(json_data)
        checks_list = json_data['checks']
        for item in checks_list:
            if item==src:
               return 1
            else:
                continue
        return 0
    else:
        print('检查网络')
    return 0
def start():
    driver = webdriver.Chrome()
    driver.get('https://sc.yuanda.info/')
    login = driver.find_element(By.XPATH, '//div//ul//li//a[text()="登录"]')
    login.click()
    input("请在浏览器中完成登陆操作后，按Enter继续...")
    config_and_play(driver)
    input("请在浏览器中完成操作后，按Enter继续...")

# 读取本地配置文件是一个json
def config_and_play(driver):
    # 打印当前所在目录
    print(os.getcwd())
    with open('config.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        # print(data)
        number100 = data['100']
        for i in range(number100):
            play(driver,100)
            print("100面额已经完成"+i+1)
            time.sleep(10)
        print("100完成")
        number200 = data['200']
        for i in range(number200):
            play(driver,200)
        print("200完成")
        number500 = data['500']
        for i in range(number500):
            play(driver,500)
        print("500完成")
        number1000 = data['1000']
        for i in range(number1000):
            play(driver,1000)
        print("1000完成")
        number2000 = data['2000']
        for i in range(number2000):
            play(driver,2000)
        print("2000完成")


if __name__ == '__main__':
    mac_address = uuid.getnode()
    a=check(mac_address)
    if a:
        print("正在运行")
        start()