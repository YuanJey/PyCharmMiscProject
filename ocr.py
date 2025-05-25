import requests
from ddddocr import DdddOcr

import pytesseract
from PIL import Image
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
if __name__ == '__main__':
    print("验证码识别结果：", get_code())