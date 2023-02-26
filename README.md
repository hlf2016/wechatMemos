## fastapi 简单对接 memos
### 权限十分有限 仅实现
- 语音识别记录
- 文字输入记录

## 配置
```
cp config.ini.example config.ini
```
- wechat
  - app_id 微信公众号 app_id
  - app_secret 微信公众号 app_id
  - token 微信公众号 验证服务器时 用到的 token

- memos
  - open_api memos 提交数据用的api 设置中查看

运行一个 redis 默认 6379 端口 
