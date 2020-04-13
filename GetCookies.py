from selenium import webdriver
import time
import json

driver = webdriver.Chrome()
driver.get('https://store.steampowered.com/')
time.sleep(40)

with open('cookies.json', 'w' ) as cookief:
    cookief.write(json.dumps(driver.get_cookies()))

driver.close()