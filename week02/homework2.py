from selenium import webdriver
import time

url = 'https://shimo.im'

try:
    with webdriver.Chrome() as chrome:
        chrome.get(url)
        login_button = chrome.find_element_by_xpath("//div[@class='entries']/a[2]")
        login_button.click()

        chrome.find_element_by_xpath("//div[@class='input']/input[@name='mobileOrEmail']").send_keys("13691203452")
        chrome.find_element_by_xpath("//div[@class='input']/input[@name='password']").send_keys("5j0878ok")
        chrome.find_element_by_xpath("//div[@class='StyledLogin-sc-2oZUsG bZrWhJ']/div/button").click()
        time.sleep(5)
except:
    raise


