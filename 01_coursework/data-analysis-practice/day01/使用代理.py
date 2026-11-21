#requests proxies参数设置代理
import requests

proxie={
    'http':'http://117.160.250.134:8089'
}
res=requests.get('http://www.baidu.com',proxies=proxie)
print(res.status_code)
print(res.text)