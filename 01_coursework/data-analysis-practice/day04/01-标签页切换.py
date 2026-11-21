# 导入要使用的库
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
# 创建driver对象
driver=webdriver.Chrome()
# 访问页面
url='https://17k.com'
driver.get(url)
# iframe切换
# 获取//*[@id="header_login_user"]/a[1]
login=driver.find_element(By.XPATH,'//*[@id="header_login_user"]/a[1]')
login.click()
# 切换
# 获取iframe标签   /html/body/div[21]/div/div[1]/iframe
iframe=driver.find_element(By.XPATH,'/html/body/div[21]/div/div[1]/iframe')
driver.switch_to.frame(iframe)
# 获取账号一栏信息
zhanghao=driver.find_element(By.CLASS_NAME,'user').find_element(By.TAG_NAME,'input')
print(zhanghao)
zhanghao.send_keys('123456789')




# window切换
# current=driver.current_url
# wh=driver.window_handles
# print('点击之前',current,wh)
# time.sleep(2)
# # 获取排行榜
# paihangbang=driver.find_element(By.XPATH,'/html/body/div[2]/div/a[2]')
# # 点击进入排行榜页面
# paihangbang.click()
# time.sleep(2)
# current2=driver.current_url
# wh2=driver.window_handles
# print('点击之后切换之前',current2,wh2)
# # 切换
# driver.switch_to.window(wh2[-1])
# current3=driver.current_url
# wh3=driver.window_handles
# print('切换之后',current3,wh3)
# # 获取书籍信息的ul   BOX
# info=driver.find_element(By.CLASS_NAME,'BOX')
# print(info.text)