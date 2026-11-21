# requests  proxies参数设置代理
import requests

proxie={
    'http':'http://127.0.0.1:8080',
    'https':'https://115.236.55.186:10100'
}
# 代理ip的传输协议必须和请求链接的传输协议保持一致
try:
    res=requests.get('https://www.baidu.com/',proxies=proxie)
    print(res.status_code)
    print(res.text)
except requests.exceptions.RequestException as e:
    print('请求失败:',e)