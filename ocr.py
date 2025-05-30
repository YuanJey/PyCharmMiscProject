import time

import requests
import seleniumwire.webdriver
from ddddocr import DdddOcr
from seleniumwire import webdriver

def get_code():
    session = requests.Session()
    response = session.get('https://sc.yuanda.biz/admin/login/checkVerify.html')
    with open('captcha.png', 'wb') as f:
        f.write(response.content)
    ocr = DdddOcr()
    with open('captcha.png', 'rb') as f:
        img_bytes = f.read()
    return ocr.classification(img_bytes)
    # gimg = Image.open('./captcha.png')
    # text = pytesseract.image_to_string(gimg, config='--psm 6 -c tessedit_char_whitelist=0123456789')
    # return text.strip()

def get_captcha_code_from_selenium(url, img_xpath, api_key):
    driver = webdriver.Chrome()
    # 配置 webdriver（这里以 Chrome 为例）
    # driver = webdriver.Chrome()  # 你需要提前安装chromedriver或配置环境变量
    driver.get(url)

    # 等待页面加载，或者等待验证码元素出现
    time.sleep(3)

    # 获取验证码图片URL（可以通过元素的src属性）
    captcha_img_element = driver.find_element_by_xpath(img_xpath)
    captcha_src = captcha_img_element.get_attribute('src')
    print('验证码图片URL:', captcha_src)

    # 下载验证码图片
    response = requests.get(captcha_src)
    if response.status_code != 200:
        print("验证码图片下载失败")
        driver.quit()
        return None
    image_bytes = response.content

    # 关闭浏览器
    # driver.quit()

    # 上传到2Captcha
    files = {'file': ('captcha.png', image_bytes)}
    data = {
        'key': api_key,
        'method': 'post',
        'json': 1
    }
    upload_response = requests.post(
        'https://2captcha.com/in.php',
        data=data,
        files=files
    )
    upload_result = upload_response.json()

    if upload_result['status'] != 1:
        print('上传验证码失败:', upload_result['request'])
        return None

    captcha_id = upload_result['request']
    print('上传成功，任务ID:', captcha_id)

    # 轮询等待识别结果
    fetch_url = f'https://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1'
    for i in range(20):
        time.sleep(5)
        res_response = requests.get(fetch_url)
        res_json = res_response.json()
        if res_json['status'] == 1:
            print('识别结果:', res_json['request'])
            return res_json['request']
        elif res_json['request'] == 'CAPCHA_NOT_READY':
            print('验证码还在识别中，等待中...')
        else:
            print('识别失败:', res_json['request'])
            return None
    print('超时未获得识别结果')
    return None

def get_captcha_image_by_request(target_url, request_url, api_key):
    # 配置 selenium-wire webdriver
    driver = webdriver.Chrome()

    # 打开目标网页
    driver.get(target_url)
    time.sleep(5)  # 等待页面加载和请求发出

    # 等待网络请求（最多等待一定时间）
    captcha_response = None
    max_wait = 15  # 最多等待15秒
    start_time = time.time()

    while time.time() - start_time < max_wait:
        # 遍历捕获的请求
        for request in driver.requests:
            if request.response and request.url == request_url:
                # 发现目标请求
                captcha_response = request.response
                break
        if captcha_response:
            break
        time.sleep(1)

    if not captcha_response:
        print('没有捕获到目标验证码请求')
        driver.quit()
        return None

    # 获取请求的内容（内容可能是图片二进制或html）
    body_bytes = captcha_response.body

    # 如果是图片二进制
    # 直接上传到2Captcha
    files = {'file': ('captcha.png', body_bytes)}
    data = {
        'key': api_key,
        'method': 'post',
        'json': 1
    }
    upload_response = requests.post(
        'https://2captcha.com/in.php',
        data=data,
        files=files
    )
    upload_result = upload_response.json()

    if upload_result['status'] != 1:
        print('上传验证码失败:', upload_result['request'])
        driver.quit()
        return None

    captcha_id = upload_result['request']
    print('上传成功，任务ID:', captcha_id)

    # 轮询识别结果
    fetch_url = f'https://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1'
    for _ in range(20):
        time.sleep(5)
        res_response = requests.get(fetch_url)
        res_json = res_response.json()
        if res_json['status'] == 1:
            print('识别结果:', res_json['request'])
            driver.quit()
            return res_json['request']
        elif res_json['request'] == 'CAPCHA_NOT_READY':
            print('验证码还在识别中，等待中...')
        else:
            print('识别失败:', res_json['request'])
            driver.quit()
            return None
    print('超时未获得识别结果')
    driver.quit()
    return None
if __name__ == '__main__':
    # print("验证码识别结果：", get_code())
    # 使用示例

    # url = 'https://sc.yuanda.biz/jingdian/User/index.html'
    # img_xpath = '//*[@id="veriimg"]'  # 你验证码图片的xpath
    # api_key = '4f7fe23e7cd68680a6b320982be0a1c9'
    # code = get_captcha_code_from_selenium(url, img_xpath, api_key)
    # print('验证码内容:', code)
    url = 'https://sc.yuanda.biz/jingdian/User/index.html'
    request_url = 'https://sc.yuanda.biz/admin/login/checkVerify.html'
    api_key = '4f7fe23e7cd68680a6b320982be0a1c9'
    code = get_captcha_image_by_request(url, request_url, api_key)
    print('验证码:', code)