import os
import uuid
import json

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 固定页面链接
m_100 = 'https://sc.yuanda.info/pg/234.html'
m_200 = 'https://sc.yuanda.info/pg/235.html'
m_500 = 'https://sc.yuanda.info/pg/237.html'
m_1000 = 'https://sc.yuanda.info/pg/240.html'
m_2000 = 'https://sc.yuanda.info/pg/241.html'


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


def play(driver, number):
    """根据编号访问对应页面并模拟操作"""
    wait = WebDriverWait(driver, 5)
    url_map = {
        100: m_100,
        200: m_200,
        500: m_500,
        1000: m_1000,
        2000: m_2000
    }
    url = url_map.get(number)
    if not url:
        print(f"无效的编号：{number}")
        return

    try:
        driver.get(url)
        # 等待“立即购买”按钮出现并点击
        icon_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cart-buy > a.buy-btn'))
        )
        icon_element.click()
        # 找“找人代付”并点击
        icon_element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//div//ul//li//a[text()="找人代付"]'))
        )
        icon_element.click()
        # 点击结算按钮
        icon_element = wait.until(
            EC.presence_of_element_located((By.ID, 'jiesuan'))
        )
        icon_element.click()
    except Exception as e:
        print(f"操作失败：{e}")


def config_and_play(driver):
    """读取配置文件然后执行"""
    try:
        print("当前目录：", os.getcwd())
        with open('config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        # 按照配置逐个执行
        for key in ['100', '200', '500', '1000', '2000']:
            count = data.get(key, 0)
            number = int(key)
            for _ in range(count):
                play(driver, number)
            print(f"{key} 完成：{count}次")
    except FileNotFoundError:
        print("配置文件未找到！")
    except json.JSONDecodeError:
        print("配置文件格式错误！")
    except Exception as e:
        print(f"执行过程中出错：{e}")


def start():
    """启动浏览器，登录并执行"""
    # 指定你的chromedriver路径（如果不在环境变量中）
    driver_path = 'chromedriver'  # 替换成你的chromedriver路径
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # 如果不需要界面，可以开启无头模式
    # driver = None
    driver = webdriver.Chrome()
    try:
        # driver = webdriver.Chrome(executable_path=driver_path, options=options)
        driver.get('https://sc.yuanda.info/')
        # 点击登录
        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div//ul//li//a[text()="登录"]'))
        )
        login_btn.click()
        input("请在浏览器中完成登陆操作后，按Enter继续...")
        config_and_play(driver)
        input("操作完成。按Enter退出...")
    except Exception as e:
        print(f"启动过程中出错：{e}")
    finally:
        if driver:
            driver.quit()


if __name__ == '__main__':
    # 获取MAC地址，并转为字符串
    mac_address = uuid.getnode()
    mac_str = str(mac_address)
    print("检测MAC：", mac_str)
    result = check(mac_str)
    if result:
        print("验证通过，即将开始执行。")
        start()
    else:
        print("MAC验证未通过或无权限。")