from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
if __name__ == '__main__':
    driver.get('https://sc.yuanda.biz/jingdian/User/index.html')
    veriimg = driver.find_element(By.ID, 'veriimg')
    veriimg.screenshot('veriimg.png')
    # 关闭浏览器
    # driver.quit()
