# 引入需要使用的库
import requests
import csv
# 请求的接口链接
url='http://www.xinfadi.com.cn/getPriceData.html'
# 头部信息
hd={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}
# 创建文件对象
file_obj=open('北京新发地.csv','a',encoding='utf-8',newline='')
# 创建csv文件对象
csv_obj=csv.writer(file_obj)
# 表单信息
for current in range(10):
    formData = {
        'limit': 20,
        'current': current+1,
        'pubDateStartTime': '',
        'pubDateEndTime': '',
        'prodPcatid': '',
        'prodCatid': '',
        'prodName': ''
    }
    # 构造请求
    res=requests.post(url,headers=hd,data=formData)
    print(res.json())
    # 提取数据
    info_list=res.json()['list']
    for i in info_list:
        # print(i['prodName'],i['lowPrice'],i['highPrice'],i['avgPrice'])
        # 写入csv文件内容
        csv_obj.writerow([i['prodName'],i['lowPrice'],i['highPrice'],i['avgPrice']])


'''
 保存数据   open()
    文件地址 
       ./  当前目录
       ../  上一级
       /    下一级
       直接写文件名默认保存在当前目录
    操作符
        w    先清空再写入
        r      读取
        a       追加写入
        rb  二进制读取
        wb  二进制先清空再写入
        ab  二进制追加写入
'''

# file_obj=open('test.txt','w')
# file_obj.write('hello world')
# file_obj.close()
#
# with open('test.txt','w',encoding='utf-8') as f:
#     f.write('你好，世界')
#
# import csv
# file_obj=open('测试表格.csv','w',encoding='utf-8-sig',newline='')
# csv_obj=csv.writer(file_obj)
# csv_obj.writerow([1,2,3])
# csv_obj.writerow([1,2,3])
# csv_obj.writerow([1,2,3])