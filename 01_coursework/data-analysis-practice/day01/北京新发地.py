import requests
import csv
url='http://www.xinfadi.com.cn/getPriceData.html'
#请求头参数
hd={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/123'
}
formData={
'limit':'',
'current':'',
'pubDateStartTime':'',
'pubDateEndTime':'',
'prodPcatid':'',
'prodCatid':'',
'prodName':''
}
#在Payload里面查询传递表单信息，空的也要传

res=requests.post(url,headers=hd,data=formData)
print(res.json())  #拿到的数据为字典，通过key查value
#print(res.text)
info_list=res.json()['list']  #想要的数据在Preview里面的list
file_obj=open('北京新发地.csv','w',encoding='utf-8',newline='')
csv_obj=csv.writer(file_obj)
for i in info_list:
    #print(i['prodName'])  #拿到所有菜品的名字
    #print(i)  #此时输出的数据均是以字典的形式给出
    #print(i['prodName'],i['lowPrice'],i['highPrice'],i['avgPrice'])
    csv_obj.writerow([i['prodName'],i['lowPrice'],i['highPrice'],i['avgPrice']])



'''
保存数据 open()
   文件地址
   ./ 当前目录
   ../ 上一级
   /  下一级
   直接写文件名默认保存在当前目录
操作符
w  先清空在写入
r 读取
a  追加写入
rb  二进制读取
wb   二进制先清空在写入
ab   二进制追加写入
'''

# file_obj=open('test.txt','w')   #如果没有这个文件，就自行创建
# file_obj.write('hello world')   #在当前目录下创建
# file_obj.close()
#
# #其他方法 with
# with open('test.txt','w',encoding='utf-8') as f:
#     f.write('你好！')
#
# #创建表格文件
# import csv
# file_obj=open('测试表格.csv','w',encoding='utf-8',newline='')
# csv_obj=csv.writer(file_obj)
# csv_obj.writerow([1,2,3,4])
# csv_obj.writerow([1,2,3,4])
# csv_obj.writerow([1,2,3,4])
#此时输出结果有空行，所以在上面添加newline
#若打开表格工具是office版，需要将encoding='utf-8-sig'

