from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import lxml.html

caps = DesiredCapabilities.INTERNETEXPLORER
caps['ignoreProtectedModeSettings'] = True

"""
http://intranetsiacpost/siacpost-frontend
http://intranetsiac/siacpre-frontend
http://intranetsisact/sisact/Index.aspx
3216

TIM\E322330
booperaciones124*

TIM\E330976
Lct*53856421
"""
#driver = webdriver.Ie(capabilities=caps) 
driver = webdriver.Ie() 
driver.capabilities["se:ieOptions"]["nativeEvents"] = False
driver.capabilities["se:ieOptions"]["requireWindowFocus"] = True
#driver.set_window_rect(0,0,800,600)
def hover():
    element = driver.find_element_by_id("HM_Item1_3")
    hov = ActionChains(driver).move_to_element(element)
    hov.perform()
driver.get("http://intranetsisact/sisact/Index.aspx")
#driver.set_window_rect(0,0,800,600)
driver.switch_to.frame(driver.find_element_by_name("main"))
driver.find_element_by_id("imgIngresar").click()
driver.find_element_by_id("HM_Item1_3").click()
driver.find_element_by_id("HM_Item1_3_1").click()
driver.switch_to.frame(driver.find_element_by_name("iframeBody"))
driver.find_element_by_id("txtNroDocumento").clear()
driver.find_element_by_id("txtNroDocumento").send_keys("43788490") # 43788490 43687188
select = Select(driver.find_element_by_id("ddlTipoDocumento"))
select.select_by_visible_text("DNI")
driver.find_element_by_id("btnConsultar").click()

def q():
    driver.close()
    exit


headerTable = []
def printTableRows(attribute, criteria, search = ''):
    root = lxml.html.fromstring(driver.page_source)
    firstIter = True

    for row in root.xpath('.//table[@%s="%s"]//tr' % (attribute, criteria)): #dgLista
        if firstIter:
            global headerTable
            headerTable = row[0]
            print(row[0])
            firstIter = False
        cells = row.xpath('.//td/text()')
        print(cells)
        dict_value = {'0th': cells[0], '1st': cells[1], '2nd': cells[2], '3rd': cells[3]}

		
def Enable_Protected_Mode():
    # SECURITY ZONES ARE AS FOLLOWS:
    # 0 is the Local Machine zone
    # 1 is the Intranet zone
    # 2 is the Trusted Sites zone
    # 3 is the Internet zone
    # 4 is the Restricted Sites zone
    # CHANGING THE SUBKEY VALUE "2500" TO DWORD 0 ENABLES PROTECTED MODE FOR THAT ZONE.
    # IN THE CODE BELOW THAT VALUE IS WITHIN THE "SetValueEx" FUNCTION AT THE END AFTER "REG_DWORD".
    #os.system("taskkill /F /IM iexplore.exe")
    try:
        keyVal = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\1'
        key = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
        SetValueEx(key, "2500", 0, REG_DWORD, 0)
        print("enabled protected mode")
    except Exception:
        print("failed to enable protected mode")