import requests
import time
from selenium import webdriver


def get_code_from_url(image_url, api_key):
    # 获取验证码图片内容（二进制）
    response = requests.get(image_url)
    if response.status_code != 200:
        print("获取验证码图片失败")
        return None
    image_bytes = response.content

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

    # 轮询等待验证码识别结果
    fetch_url = f'https://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1'
    for i in range(20):  # 最多轮询20次
        time.sleep(5)  # 等待5秒
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
def get_code_from_path(image_path, api_key):
    # 读取本地图片内容（二进制）
    try:
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
    except FileNotFoundError:
        print("图片文件未找到")
        return None

    # 上传到2Captcha
    files = {'file': ('captcha.png', image_bytes)}
    data = {
        'key': api_key,
        'method': 'post',
        'json': 1
    }
    response = requests.post(
        'https://2captcha.com/in.php',
        data=data,
        files=files
    )
    upload_result = response.json()

    if upload_result['status'] != 1:
        print('上传验证码失败:', upload_result['request'])
        return None

    captcha_id = upload_result['request']
    print('上传成功，任务ID:', captcha_id)

    # 轮询等待验证码识别结果
    fetch_url = f'https://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1'
    for i in range(20):  # 最多轮询20次
        time.sleep(5)  # 等待5秒
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

if __name__ == '__main__':
    # 使用示例：
    api_key = '4f7fe23e7cd68680a6b320982be0a1c9'  # 替换成你的API密钥
    # url = 'https://sc.yuanda.biz/admin/login/checkVerify.html'
    # captcha_code = get_code_from_url(url, api_key)
    # if captcha_code:
    #     print('最终验证码为:', captcha_code)
    captcha_code=get_code_from_path('captcha.png',api_key)
    if captcha_code:
        print('最终验证码为:', captcha_code)