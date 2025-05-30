import os
import time
import uuid
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from ddddocr import DdddOcr
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
m_100 = 'https://sc.yuanda.biz/pg/234.html'
m_200 = 'https://sc.yuanda.biz/pg/235.html'
m_500 = 'https://sc.yuanda.biz/pg/237.html'
m_1000 = 'https://sc.yuanda.biz/pg/240.html'
m_2000 = 'https://sc.yuanda.biz/pg/241.html'

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

        # wait = WebDriverWait(driver, 4)
        # # 等待“立即购买”按钮出现并点击
        # icon_element = wait.until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cart-buy > a.buy-btn'))
        # )
        # icon_element.click()

        buy_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.cart-buy > a.buy-btn'))
        )
        # 使用JavaScript点击
        driver.execute_script("arguments[0].click();", buy_button)

        # 找“找人代付”并点击
        pay_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.ID, 'alipay'))
        )
        driver.execute_script("arguments[0].click();", pay_button)

        # 点击结算按钮
        submit_btn = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.ID, 'jiesuan'))
        )
        # 使用JavaScript点击
        driver.execute_script("arguments[0].click();", submit_btn)

        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'zhengwen'))
        )
        message_text = success_message.text
        print("成功信息：", message_text)

        print(number,"面额购买成功+1")
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
def get_code():
    session = requests.Session()
    response = session.get('https://sc.yuanda.biz/admin/login/checkVerify.html')
    with open('captcha.png', 'wb') as f:
        f.write(response.content)
    ocr = DdddOcr()
    with open('captcha.png', 'rb') as f:
        img_bytes = f.read()
    return ocr.classification(img_bytes)
def login():
        driver.get('https://sc.yuanda.biz/')
        # 点击登录
        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div//ul//li//a[text()="登录"]'))
        )
        login_btn.click()
        print("验证码：",get_code())
        input("登陆完成后，按Enter继续...")

def logout():
    try:
        # 点击退出登录按钮
        logout_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="/jingdian/User/loginOut.html"]'))
        )
        # 直接点击
        logout_link.click()
        print("已成功退出登录。")
    except Exception as e:
        print(f"退出登录失败：{e}")

def start():
    t1 = int(input("请输入间隔："))
    m100 = int(input("请输入要后买100的数量："))
    m200 = int(input("请输入要后买200的数量："))
    m500 = int(input("请输入要后买500的数量："))
    m1000 = int(input("请输入要后买1000的数量："))
    m2000 = int(input("请输入要后买2000的数量："))
    print("开始购买100面额：", m100, "张")
    for i in range(m100):
        buy(m_100, 100)
        time.sleep(t1)
    print("开始购买200面额：", m200, "张")
    for i in range(m200):
        buy(m_200, 200)
        time.sleep(t1)
    print("开始购买500面额：", m500, "张")
    for i in range(m500):
        buy(m_500, 500)
        time.sleep(t1)
    print("开始购买1000面额：", m1000, "张")
    for i in range(m1000):
        buy(m_1000, 1000)
        time.sleep(t1)
    print("开始购买2000面额：", m2000, "张")
    for i in range(m2000):
        buy(m_2000, 2000)
        time.sleep(t1)
    print("购买完成！")

def create_driver():
    options = Options()
    timestamp = str(int(time.time() * 1000))  # 毫秒时间戳
    profile_dir = os.path.join("./Temp/chrome_profile_", timestamp)
    options.add_argument(f'--user-data-dir={profile_dir}')
    return webdriver.Chrome(options=options)
driver=create_driver()
if __name__ == '__main__':
    # 获取MAC地址，并转为字符串
    # mac_address = uuid.getnode()
    # mac_str = str(mac_address)
    # print("检测MAC：", mac_str)
    # result = check(mac_str)
    # if result:
    #     print("验证通过，即将开始执行。")
    #     while True:
    #         login()
    #         start()
    #         cont = input("是否继续（1:登陆下一个账号，其他任意键，退出）：")
    #         if cont == '1':
    #             logout()
    #         else:
    #             break
    # else:
    #     print("MAC验证未通过或无权限。")
    login()
    get_code()