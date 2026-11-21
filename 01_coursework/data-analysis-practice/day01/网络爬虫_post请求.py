# 说明：登录账号、密码与 Cookie 涉及个人凭据，已移除明文，改为从环境变量读取。
# 运行前先设置：SITE_LOGIN_NAME / SITE_LOGIN_PWD / SITE_COOKIE
import os
import requests
login_url='https://passport.17k.com/ck/user/login'
#设置请求头
hd={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'cookie': os.environ.get("SITE_COOKIE", ""),
}
#准备登录表单
formData={
    'loginName': os.environ.get("SITE_LOGIN_NAME", ""),
    'password2': os.environ.get("SITE_LOGIN_PWD", "")
}
#发送post请求进行登录
res=requests.post(login_url,data=formData,headers=hd)
print(res.headers)
cookie_list=res.headers['Set-Cookie'].split(';')
for i in cookie_list:
    if 'accessToken' in i:
        cookie=i
url='https://user.17k.com/ck/author2/shelf?page=1&appKey=2406394919'
# # # 请求头参数
hd2={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'cookie':cookie
}
res=requests.get(url,headers=hd)
print(res.json())