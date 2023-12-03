import hashlib
import uvicorn
import requests
import json
import redis
from typing import Union
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from Plugins.WechatMessage import parse_xml, Message
from starlette.responses import RedirectResponse, HTMLResponse, Response
from starlette.staticfiles import StaticFiles
from configparser import ConfigParser
from basic import Basic


# https://github.com/vastsa/Wechat-Fastapi

app = FastAPI(title="Wechat Memos", version='1',)
# 读取配置文件
cfg = ConfigParser()
cfg.read('config.ini')
# cfg.sections()
# appId = cfg.get('wechat', 'app_id')
# appSecret = cfg.get('wechat', 'app_secret')
token = cfg.get('wechat', 'token')
memos_open_api = cfg.get('memos', 'open_api')
memos_access_token = cfg.get('memos', 'access_token')
redis_host = cfg.get('redis', 'host')
redis_port = cfg.get('redis', 'port')
redis_db = cfg.get('redis', 'db')
# print(memos_open_api,redis_host,redis_port)
# print(token, Basic().get_access_token())

rds = redis.StrictRedis(host=redis_host, port=redis_port,
                        db=redis_db, decode_responses=True)

# def getAccessToken(appId, appSecret):
#     accessTokenKey = 'wechatAccessToken'
#     accessToken = rds.get(accessTokenKey)
#     if not accessToken:
#         url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appId}&secret={appSecret}"
#         res = requests.get(url).json()
#         accessToken = res.get('access_token', False)
#         if accessToken:
#             expiresIn = res.get('expires_in', 7000)
#             rds.setex(accessTokenKey, expiresIn - 200, accessToken)
#     return accessToken

# getAccessToken(appId, appSecret)


# 后台api允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get("/wechat")
def wechat(signature: str, echostr: int, timestamp: str, nonce: str):
    try:
        list = [token, timestamp, nonce]
        list.sort()
        # map函数在Python 2.x 返回列表，Python 3.x 返回迭代器。update函数在老版本中可以用字符串，在3.5版本中必须用字节了。
        s = list[0]+list[1]+list[2]
        sha1 = hashlib.sha1()
        sha1.update(bytes(s, "utf8"))
        hashcode = sha1.hexdigest()
        print("handle/GET func: hashcode, signature: ", hashcode, signature)
        if hashcode == signature:
            return echostr
        else:
            return ""
    except Exception as e:
        print(e)
        return e


@app.post("/wechat")
async def wechat_post(request: Request, signature: str, timestamp: str, nonce: str, openid: str):
    try:
        rec_msg = parse_xml(await request.body())
        to_user = rec_msg.FromUserName
        from_user = rec_msg.ToUserName

        memo = ''
        if rec_msg.MsgType == 'text':
            # 文字类型
            memo = rec_msg.Content
        elif rec_msg.MsgType == 'voice':
            # 语音类型
            memo = rec_msg.Recognition
        elif rec_msg.MsgType == 'event':
            return Response(Message(to_user, from_user, '欢迎您的关注').send(), media_type="application/xml")

        open_id_key = f'wechat:open_id:{to_user}'
        if memo == '绑定':
            # 将发信人的open_id存储下来
            rds.set(open_id_key, to_user)
            return Response(Message(to_user, from_user, '绑定成功，可以向 memos 中发消息了').send(), media_type="application/xml")
        elif memo != '' and rds.get(open_id_key):
            # print(rds.get(open_id_key))
            memoJson = json.dumps({"content": memo})
            res = requests.post(
                url=memos_open_api,
                headers={
                    "Content-type": "application/json",
                    "Authorization": "Bearer "+memos_access_token
                },
                data=memoJson
            ).json()
            # print(memo, res)
            if res.get('data', None) != None:
                responseMsg = "Memo保存成功"
            else:
                responseMsg = "Memo保存失败 原因"+res
            return Response(Message(to_user, from_user, responseMsg).send(), media_type="application/xml")
        else:
            return HTMLResponse('success')
    except:
        return HTMLResponse('success')
