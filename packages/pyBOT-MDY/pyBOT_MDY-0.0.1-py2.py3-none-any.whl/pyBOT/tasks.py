#http://uploaded.net/file/dw1gn48u
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class sisactValidator:
    def __init__(self):
        self.driver = webdriver.Ie() 
        self.driver.capabilities["se:ieOptions"]["nativeEvents"] = False
        self.driver.capabilities["se:ieOptions"]["requireWindowFocus"] = True    
        
    def hover():
        self.element = driver.find_element_by_id("HM_Item1_3")
        self.hov = ActionChains(driver).move_to_element(element)
        self.hov.perform()
    
    def runTask(self):    
        self.driver.get("http://intranetsisact/sisact/Index.aspx")
        self.driver.set_window_rect(0,0,800,600)
        self.driver.switch_to.frame(driver.find_element_by_name("main"))
        self.driver.find_element_by_id("imgIngresar").click()
        self.driver.find_element_by_id("HM_Item1_3").click()
        self.driver.find_element_by_id("HM_Item1_3_1").click()
        self.driver.switch_to.frame(driver.find_element_by_name("iframeBody"))
        self.driver.find_element_by_id("txtNroDocumento").clear()
        self.driver.find_element_by_id("txtNroDocumento").send_keys("43788490") # 43788490 43687188
        self.select = Select(driver.find_element_by_id("ddlTipoDocumento"))
        self.select.select_by_visible_text("DNI")
        self.driver.find_element_by_id("btnConsultar").click()