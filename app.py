import hashlib
import time
import multiprocessing
import threading
from ai import get_ai_explain, get_ai_title, get_mathpix_response
from flask import Flask, jsonify, request, make_response
# from werkzeug.middleware.proxy_fix import ProxyFix
import xml.etree.ElementTree as ET
from config import setup_log, config
import time
import logging
from notion import createPage, queryPage

WX_TOKEN = 'math'
DB_URL = "https://rocky-pufferfish-0c8.notion.site/72c8dc936632419dac502e5625d45805?v=b988da68a78943afa17c83173cf25b6a"
responseStr = f"稍后请在此网址查看解释:${DB_URL}"
app = Flask(__name__)
app.config.from_object(config)
setup_log()  #使用日志

# logging.info(f"appid ${app_id} app_key ${app_key}")

# app.wsgi_app = ProxyFix(
#     app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
# )

@app.route('/wechat_api/', methods=['GET', 'POST'])
# 定义路由地址请与URL后的保持一致
def wechat():
    if request.method == 'GET':
        token = WX_TOKEN
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        s = sorted([timestamp, nonce, token])
        # 字典排序
        s = ''.join(s)
        if hashlib.sha1(s.encode('utf-8')).hexdigest() == signature:
            # 判断请求来源，并对接受的请求转换为utf-8后进行sha1加密
            response = make_response(echostr)
            # response.headers['content-type'] = 'text' 
            return response
        else:
             return 'error', 403 
    else:
        xml = ET.fromstring(request.data)
        toUser = xml.find('ToUserName').text
        fromUser = xml.find('FromUserName').text
        msgType = xml.find("MsgType").text
        logging.info(f"fromUser {fromUser} msgType {msgType}")
        if msgType == 'text':
            content = xml.find('Content').text
            # logging.info(f"content: {content}")
            # result = get_ai_response(content)
            # return reply_text(fromUser, toUser, result)
            sideTask("",content)
            return reply_text(fromUser,toUser, responseStr)
        elif msgType == 'image':
            picUrl = xml.find('PicUrl').text
            # sideTask(picUrl, "")
            # return reply_text(fromUser, toUser, response)
            code, result = get_mathpix_response(picUrl)
            # logging.info("ocr: ", code, result)
            if(code == 200):
                sideTask(picUrl, result)
                response = f"LaTeX: \n{result}\n\n {responseStr}"
                return reply_text(fromUser, toUser, response)
            else:
                return reply_text(fromUser, toUser, result)
        else:
            return reply_text(fromUser, toUser, "嗯？我听不太懂")
        

def reply_text(to_user, from_user, content):
    reply = """
    <xml><ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    <FuncFlag>0</FuncFlag></xml>
    """
    response = make_response(reply % (to_user, from_user,
                                      str(int(time.time())), content))
    response.content_type = 'application/xml'
    return response

def sideTask(imageUrl, latex):
    p = multiprocessing.Process(target=postToNotion, args=(imageUrl, latex))
    p.start()
    # thread = threading.Thread(target=postToNotion, args=(imageUrl, latex))
    # thread.start()

##根据给出的公式，提取公式名称和公式解释，并post到Notion的Database
def postToNotion(imageUrl, latex):
    title = get_ai_title(latex)
    queryResult = queryPage(title)
    # 如果已经有这个公式则不需要重复添加
    if len(queryResult.get("results", [])) > 0:
        logging.info("duplicate latex")
        return
    explain = get_ai_explain(latex)
    createPage(image_url=imageUrl, title=title, latex=latex, explain=explain)

@app.route('/')
def hello():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0',port=5000)