SteamFreeGames
==============

有什么用？
--------------
1.从Steamdb的游戏限免资讯界面(https://steamdb.info/upcoming/free/)获得当日免费信息 <br>
2.仅筛选可以永久免费游玩的游戏 <br>
3.自动登录你的steam，检索这些游戏并领取 <br>

应该如何使用？
--------------
1.正确安装Python3以上版本及其第三方库Selenium，并正确安装Chrome对应版本的ChromeDriver <br>
2.采用两种登录方式(Cookie登录和普通账密登录) <br>

普通账密登录 (推荐无安全令时使用)
--------------
1.直接运行  *main.py*  等待数据获取完成控制台输入"2"选择此登录方式, <br>根据控制台中的提示输入 账号 密码 (若有手机安全令也需要输入) <br>
2.等待成功提示 <br>

Cookie登录 (推荐有安全令时使用)
--------------
1.先运行  *GetCookies.py*  并且正确登录Steam获得Cookie信息，将会保存在Cookies.json中 (若有手机安全令也需要输入) <br>
2.再运行  *main.py*    等待数据获取完成控制台输入"1"选择此登录方式 <br>
3.等待成功提示 <br>

提示
-------------
1.*main.py*  运行时鼠标不要置于浏览器页面上，会导致鼠标事件暂停报错 <br>
2.此程序全部由  Selenium  编写，运行速度较慢，请耐心等待 <br>
3.执行 *GetCookies.py*  请在40s内正确登录账号 <br>
