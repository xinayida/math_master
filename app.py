import hashlib
import time
from ai import get_response
from flask import Flask, jsonify, request, make_response
from werkzeug.middleware.proxy_fix import ProxyFix
import xml.etree.ElementTree as ET
from config import setup_log, config
from ai import get_mathpix_response

WX_TOKEN = 'math'

app = Flask(__name__)
app.config.from_object(config)
setup_log("testing")  #使用日志

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)


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
        app.logger.info(f"fromUser {fromUser} msgType {msgType}")
        if msgType == 'text':
            content = xml.find('Content').text
            app.logger.info(f"content: {content}")
            return reply_text(
                fromUser, toUser, get_response(
                    fromUser, content))
        elif msgType == 'image':
            picUrl = xml.find('PicUrl').text
            # result = get_mathpix_response(picUrl)
            print("picUrl", picUrl)
            return reply_text(fromUser, toUser, picUrl)
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

@app.route('/hello')
def hello():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0',port=5000)