import re
# print(re.match('Hello,World','Hello,WOrld'))
# print(re.search('e.*?$','hello worldello world'))
# print(re.fullmatch('e.*?$','hello world'))



# re.findall(pattern,string,flags=0)
'''
pattern  正则表达式
string   待匹配字符串
flags    标志，如：是否区分大小写
n,m  可选参数，指定字符串的起始位置n和结束位置m
'''
# pattern.findall(string,n,m)
res=re.findall('\D+','12a33v8bcjhf34h4')
print(res)
patter=re.compile('\D+')
res=patter.findall('12a33v8bcjhf34h4',0,5)
print(res)
