# 引入请求库
import requests
# 请求链接
url='https://movie.douban.com/subject/24284175/comments?status=P'
# 请求头参数
hd={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}
res=requests.get(url,headers=hd)
print(res.status_code)
print(res.headers)
print(res.encoding)
print(res.text)
# print(res.json())
# print(res.content)