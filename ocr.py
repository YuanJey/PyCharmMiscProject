import requests
from ddddocr import DdddOcr


def get_code():
    session = requests.Session()
    response = session.get('https://sc.yuanda.biz/admin/login/checkVerify.html')
    with open('captcha.png', 'wb') as f:
        f.write(response.content)
    ocr = DdddOcr()
    with open('captcha.png', 'rb') as f:
        img_bytes = f.read()
    return ocr.classification(img_bytes)
if __name__ == '__main__':
    print("验证码识别结果：", get_code())