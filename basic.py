import redis, requests
from configparser import ConfigParser

class Basic(object):
  def __init__(self):
    cfg = ConfigParser()
    cfg.read('config.ini')
    redis_host = cfg.get('redis', 'host')
    redis_port = cfg.get('redis', 'port')
    redis_db = cfg.get('redis', 'db')
    # cfg.sections()
    self.rds = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db,decode_responses=True)
    self.__appId = cfg.get('wechat', 'app_id')
    self.__appSecret = cfg.get('wechat', 'app_secret')
    self.__accessToken = ''
      
  def __real_get_access_token(self):
    accessTokenKey = 'wechatAccessToken'
    accessToken = self.rds.get(accessTokenKey)
    if not accessToken:
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.__appId}&secret={self.__appSecret}"
        res = requests.get(url).json()
        accessToken = res.get('access_token', False)
        if accessToken:
            expiresIn = res.get('expires_in', 7000)
            self.rds.setex(accessTokenKey, expiresIn - 200, accessToken)
    self.__accessToken = accessToken

  def get_access_token(self):
    self.__real_get_access_token()
    return self.__accessToken
