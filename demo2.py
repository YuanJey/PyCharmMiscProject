from seleniumwire import webdriver  # 使用 seleniumwire 替代原生 selenium

if __name__ == '__main__':
    driver = webdriver.Chrome()
    try:
        driver.get('https://sc.yuanda.biz/jingdian/User/index.html')

        # 等待任意请求完成（可以替换为具体的 URL 正则匹配）
        driver.wait_for_request('.*', timeout=10)

        # 遍历所有捕获的请求
        for request in driver.requests:
            if request.response:
                print(f"Method: {request.method}")
                print(f"URL: {request.url}")
                print(f"Status Code: {request.response.status_code}")
                try:
                    print(f"Response Body: {request.response.body.decode()}")
                except UnicodeDecodeError:
                    print("Response Body: 无法解码二进制内容")
                print("---")
    finally:
        driver.quit()
