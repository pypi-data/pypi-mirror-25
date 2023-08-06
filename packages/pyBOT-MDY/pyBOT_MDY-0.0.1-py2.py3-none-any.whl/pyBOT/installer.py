#https://chromedriver.storage.googleapis.com/2.9/chromedriver_win32.zip
#https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-win32.zip
#http://selenium-release.storage.googleapis.com/3.4/IEDriverServer_Win32_3.4.0.zip
#http://selenium-release.storage.googleapis.com/3.4/IEDriverServer_x64_3.4.0.zip

#http://selenium-release.storage.googleapis.com/index.html?path=3.4/

#driver = webdriver.Chrome(executable_path="/path/to/chromedriver")
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
"""
from selenium import webdriver

fp = webdriver.FirefoxProfile()

fp.add_extension(extension='firebug-1.8.4.xpi')
fp.set_preference("extensions.firebug.currentVersion", "1.8.4") #Avoid startup screen
browser = webdriver.Firefox(firefox_profile=fp) #"""

"""
from selenium import webdriver

driver = webdriver.Firefox()
driver.get('http://www.python.org/')
driver.save_screenshot('screenshot.png')
driver.quit()#"""
