import time
import uuid
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def check(src):
    """通过网络请求验证MAC地址"""
    url = 'https://test-1312265679.cos.ap-chengdu.myqcloud.com/config.json'
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            json_data = response.json()
            checks_list = json_data.get('checks', [])
            if src in checks_list:
                return 1
        print('网络请求失败或未找到匹配的MAC')
        return 0
    except requests.RequestException as e:
        print('请求错误:', e)
        return 0

# 固定页面链接
m_100 = 'https://sc.yuanda.info/pg/234.html'
m_200 = 'https://sc.yuanda.info/pg/235.html'
m_500 = 'https://sc.yuanda.info/pg/237.html'
m_1000 = 'https://sc.yuanda.info/pg/240.html'
m_2000 = 'https://sc.yuanda.info/pg/241.html'

# global f_100,f_200,f_500,f_1000,f_2000
f_100 = 0
f_200 = 0
f_500 = 0
f_1000 = 0
f_2000 = 0
def buy(url, number):
    global f_100, f_200, f_500, f_1000, f_2000

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 4)
        # 等待“立即购买”按钮出现并点击
        icon_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cart-buy > a.buy-btn'))
        )
        icon_element.click()
        # 找“找人代付”并点击
        pay_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, 'alipay'))
        )
        driver.execute_script("arguments[0].click();", pay_button)

        # 点击结算按钮
        submit_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, 'jiesuan'))
        )
        # 使用JavaScript点击
        driver.execute_script("arguments[0].click();", submit_btn)
    except Exception as e:
        print(f"操作失败：{e}","金额:",number)
        if  number==100:
            f_100+=1
        elif number==200:
            f_200+=1
        elif number==500:
            f_500+=1
        elif number==1000:
            f_1000+=1
        elif number==2000:
            f_2000+=1

def login():
        driver.get('https://sc.yuanda.info/')
        # 点击登录
        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div//ul//li//a[text()="登录"]'))
        )
        login_btn.click()
        input("登陆完成后，按Enter继续...")


driver=webdriver.Chrome()
if __name__ == '__main__':
    # 获取MAC地址，并转为字符串
    mac_address = uuid.getnode()
    mac_str = str(mac_address)
    print("检测MAC：", mac_str)
    result = check(mac_str)
    if result:
        print("验证通过，即将开始执行。")
        m100=int(input("请输入要后买100的数量："))
        m200=int(input("请输入要后买200的数量："))
        m500=int(input("请输入要后买500的数量："))
        m1000=int(input("请输入要后买1000的数量："))
        m2000=int(input("请输入要后买2000的数量："))
        login()
        print("开始购买100面额：", m100,  "张")
        for i in range(m100):
            buy(m_100,100)
        print("开始购买200面额：", m200,  "张")
        for i in range(m200):
            buy(m_200,200)
        print("开始购买500面额：", m500,  "张")
        for i in range(m500):
            buy(m_500,500)
        print("开始购买1000面额：", m1000,  "张")
        for i in range(m1000):
            buy(m_1000,1000)
        print("开始购买2000面额：", m2000,  "张")
        for i in range(m2000):
            buy(m_2000,2000)
        print("购买完成")
        print("100面额购买失败次数：", f_100)
        print("200面额购买失败次数：", f_200)
        print("500面额购买失败次数：", f_500)
        print("1000面额购买失败次数：", f_1000)
        print("2000面额购买失败次数：", f_2000)
    else:
        print("MAC验证未通过或无权限。")