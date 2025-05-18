
import time
import uuid
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver=webdriver.Chrome()


def login():
    driver.get('https://sc.yuanda.info/')
    # 点击登录
    login_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div//ul//li//a[text()="登录"]'))
    )
    login_btn.click()
    input("登陆完成后，按Enter继续...")
if __name__ == '__main__':
    wait = WebDriverWait(driver, 4)
    login()
    driver.get('https://sc.yuanda.info/pg/234.html')
    # 等待“立即购买”按钮出现并点击
    icon_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cart-buy > a.buy-btn'))
    )
    icon_element.click()
    # 找“找人代付”并点击
    pay_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'alipay'))
    )
    driver.execute_script("arguments[0].click();", pay_button)

    # 点击结算按钮
    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'jiesuan'))
    )
    # 使用JavaScript点击
    driver.execute_script("arguments[0].click();", submit_btn)