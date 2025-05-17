import uuid

if __name__ == '__main__':
    mac_address = uuid.getnode()
    print(mac_address)
    input("请复制MAC地地址")