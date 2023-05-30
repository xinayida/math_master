import requests
import uuid
import logging

def downloadImage(url):
    response = requests.get(url)
    # 生成一个随机的文件名
    # 生成随机字符串
    random_string = str(uuid.uuid4())
    random_filename = "./static/images/" +random_string

    # 将内容写入本地文件
    with open(random_filename, 'wb') as file:
        file.write(response.content)

    logging.info("文件已下载并保存为：" + random_filename)
    return random_filename