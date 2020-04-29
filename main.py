from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 " \
     "Safari/537.36 "
options = webdriver.ChromeOptions()
options.add_argument('user-agent=' + UA)
prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', options=options)
driver.get("https://steamdb.info/upcoming/free")
driver.maximize_window()
time.sleep(4)

# 获取游戏名字

i = 1
game_name_lt = []  # 名字列表
game_id_lt = []
while True:
    try:
        data_appid = driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div[4]/table[1]/tbody/tr[" + str(i) + "]").get_attribute(
            "data-appid")
        game_id_lt.append(data_appid)
        game_name_location = driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div[4]/table[1]/tbody/tr[" + str(i) + "]/td[2]/a/b")
        ActionChains(driver).move_to_element(game_name_location).perform()  # 元素显示受jQuery控制 添加鼠标事件
        time.sleep(1)
        js = "return document.querySelector('#js-hover-app-" + str(data_appid) + " > h4').textContent"  # 返回隐藏元素的值即正确游戏名
        game_name = driver.execute_script(js)
        game_name_lt.append(game_name)
        i += 1
    except:
        break

# 获取对应游戏的现有状态 (仅保存状态为Keep的游戏序号并对应上述 game_name_lt)

j = 1
k = 0
game_type_lt = []  # 状态列表

while True:
    try:
        game_type = driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div[3]/table[1]/tbody/tr[" + str(j) + "]/td[4]/b").get_attribute(
            "innerHTML")  # 仅状态为keep时可以运行，否则进入下一个try语句
        game_type_lt.append(j - 1)  # 列表序号减1
        j += 1
        k += 1
    except:  # 嵌套try语句以避开状态为“Weekend”时抓取无法抓取图片导致的异常
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[3]/table[1]/tbody/tr[" + str(j) + "]/td[4]")
            j += 1
        except:
            break

# 筛选正确状态下的游戏

print("TotalGames:" + str(i))
print("Available：" + str(k))
print("Available Game's Name:")
available_game_lt = []
available_game_id_lt = []
for l in game_type_lt:
    print(game_id_lt[l])
    print(game_name_lt[l])
    available_game_lt.append(game_name_lt[l])
    available_game_id_lt.append(game_id_lt[l])

# 登录Steam

choice = input("cookie登录输入1，账号密码登录输入2")
if choice == "1":
    print("cookie登录")
    driver.get('https://store.steampowered.com/')
    driver.delete_all_cookies()

    with open('cookies.json', 'r') as cookief:
        cookieslist = json.load(cookief)

    for item in cookieslist:
        driver.add_cookie(
            {"domain": ".steampowered.com",
             'name': item['name'],
             'value': item['value'],
             'path': '/',
             'expires': None}
        )
    driver.refresh()
    print('Login Successful!')
elif choice == "2":
    print("账号密码登录")
    driver.get("https://store.steampowered.com/login/?redir=&redir_ssl=1")
    UserName = input("输入用户名:")
    PassWord = input("输入密码:")
    driver.find_element_by_xpath('//*[@id="input_username"]').send_keys(UserName)
    driver.find_element_by_xpath('//*[@id="input_password"]').send_keys(PassWord)
    driver.find_element_by_xpath('//*[@id="login_btn_signin"]/button').click()

    if driver.find_element_by_xpath('//*[@id="twofactorcode_entry"]'):
        VerificationCode = input("输入手机令牌:")
        driver.find_element_by_xpath('//*[@id="twofactorcode_entry"]').send_keys(VerificationCode)
        driver.find_element_by_xpath('//*[@id="login_twofactorauth_buttonset_entercode"]/div[1]').click()
        time.sleep(10)
        driver.refresh()
        print('Login Successful!')
    else:
        driver.refresh()
        print('Login Successful!')

# 检索游戏并获取
Num = len(available_game_lt)
temp = 0
while temp < Num:
    try:
        driver.get('https://store.steampowered.com/app/'+str(available_game_id_lt[temp])+'/'+str(available_game_lt[temp]))
        # driver.find_element_by_xpath('//*[@id="store_nav_search_term"]').send_keys(games)   输入搜索框
        # driver.find_element_by_xpath('//*[@id="store_search_link"]/img').click()   点击搜索按钮
        # time.sleep(2)
        # driver.find_element_by_xpath('//*[@id="search_resultsRows"]/a[1]/div[2]').click()   进入当前游戏页面
        time.sleep(2)
        js1 = 'document.querySelector("#game_area_purchase > div.game_area_purchase_game_wrapper > div > div.game_purchase_action > div > div.btn_addtocart > a > span").click()'
        time.sleep(2)
        driver.execute_script(js1)  # 执行添加至账户
        driver.get('https://store.steampowered.com/')
        print("Get " + available_game_lt[temp] + " Succeed")
        temp += 1
    except:
        CurrentGame = driver.find_element_by_xpath(
            '/html/body/div[1]/div[7]/div[4]/div[1]/div[2]/div[2]/div[2]/div/div[3]').get_attribute("innerHTML")
        if available_game_lt[temp] != CurrentGame:
            print("未找到相关游戏")
        print("Failed to get " + available_game_lt[temp])
        temp += 1
