from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymongo
import time

cnx = pymongo.MongoClient()
db = cnx["selenium"]
tbl = db["customers"]

driver = webdriver.Firefox()
driver.get("http://paginasblancas.pe/")
driver.find_element_by_xpath("//a[@data-target='address']").click()
driver.find_element_by_name("street").send_keys("carlos izaguirre")
driver.find_element_by_name("streetNumber").send_keys("2")
#driver.find_element_by_id("aLocality").send_keys(u"los olivos\ue007")
driver.find_element_by_id("aLocality").send_keys(u"los olivos")
#search.send_keys(u'\ue007')
#selenium.keyPress("id="","\\13");
#1\N{U+E007}2\N{U+E007}3
#1\n2\n3
driver.find_element_by_id("btnSrchAddress").click()
#driver.find_element_by_xpath("//a[@data-target='address']") #name address phone ddni /(/*[@id]")
#pag = driver.find_elements_by_xpath("//ul[@class='m-results-pagination']")
#lis = driver.find_elements_by_css_selector("ul.m-results-pagination li")
#qPages = 1
_round = 0
existPages = True
def q():
    driver.close()

def insertCustomer(c):
    #tbl.insert_one({'name':c[0], 'address':c[2], 'city': c[4], 'phone': c[8], 'script': c})
    tbl.insert_one({'name':c[0], 'address':c[1], 'city': c[2], 'phone': c[3], 'script': c[4]})

def search():
    items = driver.find_elements_by_css_selector("li.m-results-business")
    time.sleep(2)
    lis = driver.find_elements_by_css_selector("ul.m-results-pagination li")
    qPages = len(lis)
    for i in items:
        scriptContent = i.find_element_by_tag_name("script").get_attribute("innerHTML")
        #"""
        s = i.find_element_by_tag_name("script")
        nombre = i.find_element_by_css_selector("h3 a").text
        direccion = i.find_element_by_xpath(".//span[@itemprop='streetAddress']").text
        ciudad = i.find_element_by_xpath(".//span[@itemprop='addressLocality']").text
        telefono = i.find_element_by_css_selector("div.m-button--results-business--see-phone").get_attribute("onclick").split(",")[1].strip()[:-1]
        #"""
        i = scriptContent.index("[")+1
        f = scriptContent.index("]")
        data = scriptContent[i:f].replace("'","").split(",")
        data = [nombre, direccion, ciudad, telefono, data]
        #data = scriptContent[i:f].replace("'","").encode("iso8859-1","ignore").decode("iso8859-1").split(",")

        insertCustomer(data)
    print("qPages: %d \n" % qPages)
    lastPage = lis[qPages-1]
    #print("qPages: %d \n" % lastPage)
    global existPages
    if lastPage.get_attribute("class") != "is-active":
        lastPage.click()
    else:
        existPages = False

    print(existPages)
    #is-active
    #last



while existPages:
    search()
q()

#script = "return $(\"td:contains('{}')\").length".format(text="Silver")
#count = driver.execute_script(script)
#count =  driver.find_elements_by_xpath("//td[text()='Silver']")
#search_button = self.driver.find_element(By.XPATH, './/*[@id="nav-search"]/form/div[2]/div/input').click()
#var xpath = "a[text()='SearchingText']";
#var matchingElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
#var xpath = "a[contains(text(),'Searching')]";
