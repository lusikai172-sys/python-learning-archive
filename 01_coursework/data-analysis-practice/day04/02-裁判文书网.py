# 说明：登录账号、密码与 Cookie 涉及个人凭据，已移除明文，改为从环境变量读取。
# 运行前先设置：SITE_LOGIN_NAME / SITE_LOGIN_PWD / SITE_COOKIE
import os
# 导入库
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
# 访问的链接
url='https://wenshu.court.gov.cn/website/wenshu/181029CR4M5A62CH/index.html'
# 创建driver实例对象
driver=webdriver.Chrome()
# 访问网站
driver.get(url)
# 窗口最大化
driver.maximize_window()
time.sleep(2)
# 获取登录按钮   //*[@id="loginLi"]/a
login_tag=driver.find_element(By.XPATH,'//*[@id="loginLi"]/a')
# 点击登录
login_tag.click()
time.sleep(10)
# 点击后刷新一下页面
driver.refresh()
time.sleep(10)
# 切换到iframe窗口
driver.switch_to.frame("contentIframe")
time.sleep(10)
# 获取账号输入框   //*[@id="root"]/div/form/div/div[1]/div/div/div/input
username=driver.find_element(By.XPATH,'//*[@id="root"]/div/form/div/div[1]/div/div/div/input')
# 获取密码输入框  //*[@id="root"]/div/form/div/div[2]/div/div/div/input
password=driver.find_element(By.XPATH,'//*[@id="root"]/div/form/div/div[2]/div/div/div/input')
# 获取登录按钮   //*[@id="root"]/div/form/div/div[3]/span
login_in=driver.find_element(By.XPATH,'//*[@id="root"]/div/form/div/div[3]/span')
username.send_keys(os.environ.get("SITE_LOGIN_NAME", ""))
time.sleep(2)
password.send_keys(os.environ.get("SITE_LOGIN_PWD", ""))
time.sleep(2)
login_in.click()
time.sleep(2)
wh=driver.window_handles
driver.switch_to.window(wh[-1])
# 获取高级检索
gaojijiansuo=driver.find_element(By.XPATH,'//*[@id="_view_1540966814000"]/div/div[1]/div[1]')
gaojijiansuo.click()
time.sleep(2)
fayuanVal=driver.find_element(By.ID,'s2')
# cprqStart   cprqEnd     开始日期和结束日期
startTime=driver.find_element(By.ID,'cprqStart')
endTime=driver.find_element(By.ID,'cprqEnd')
fayuanVal.send_keys('晋州市人民法院')
startTime.send_keys('2024-03-01')
endTime.send_keys('2024-05-09')
# searchBtn
sousuo=driver.find_element(By.ID,'searchBtn')
sousuo.click()
wh=driver.window_handles
driver.switch_to.window(wh[-1])

# 获取数量判断是否有文书   //*[@id="_view_1545184311000"]/div[1]/div[2]/span
page_num=driver.find_element(By.XPATH,'//*[@id="_view_1545184311000"]/div[1]/div[2]/span')
if page_num.text !='0':
#     获取数据   LM_list
    all_info=driver.find_elements(By.CLASS_NAME,'LM_list')
    for info in all_info:
        name=info.find_element(By.TAG_NAME,'h4')
        print(name.text)



time.sleep(3333)


