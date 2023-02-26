import requests,json
from basic import Basic

class Menu(object):
    def __init__(self):
        self.uri = "https://api.weixin.qq.com"
    
    # 创建菜单
    def create(self, data, accessToken):
        createUrl = f"{self.uri}/cgi-bin/menu/create?access_token={accessToken}"
        # python3 中 str 就是 unicode
        if isinstance(data, str):
            data = data.encode("utf-8")
        res = requests.post(createUrl, data=data).json()
        print(res)


if __name__ == '__main__':
    myMenu = Menu()
    postJson = """
    {
        "button":
        [
            {
                "type": "click",
                "name": "开发指引",
                "key":  "mpGuide"
            },
            {
                "name": "公众平台",
                "sub_button":
                [
                    {
                        "type": "view",
                        "name": "更新公告",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "接口权限说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "返回码说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
                    }
                ]
            },
            {
                "type": "media_id",
                "name": "旅行",
                "media_id": "z2zOokJvlzCXXNhSjF46gdx6rSghwX2xOD5GUV9nbX4"
            }]
    }
    """
    accessToken = Basic().get_access_token()
    print(accessToken)
    myMenu.create(postJson, accessToken)




