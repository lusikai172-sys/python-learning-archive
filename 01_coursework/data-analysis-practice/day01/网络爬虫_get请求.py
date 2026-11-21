
import requests

# 请求链接
url = 'https://movie.douban.com/subject/24284175/comments?status=P'


#res=requests.get(url)
#print(res)
#结果返回418状态码，418表示网页的反爬程序返回，需要补充headers参数

#请求头参数
hd={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/123'
}

res=requests.get(url,headers=hd)
print(res)
print(res.status_code)
print(res.headers)
print(res.encoding)
print(res.text)
#print(res.json()) #运行报错，此网站无动态数据
print(res.content)