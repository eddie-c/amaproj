#--coding=utf8--
import requests
import traceback
import json
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from global_tools import GlobalTools
# from ippool import IpPool
NORMAL_ADD_TO_CART = 1
ASIN = ""


def link_to_other_page(driver,url):
    print(url)
    global ASIN
    ASIN = url.split("dp/")[1].split("/ref")[0]
    # url.split("dp%2F")[1].split("%2Fref")[0] # 可能斜杠/ 会被转换成%2F
    try:
        driver.get(url)
    except:
        driver.execute_script('window.stop()')

        driver.save_screenshot("d:/" + ASIN + "_first.png")

    if len(driver.find_elements_by_id("regularBuybox")) > 0:
        driver.find_element_by_id("regularBuybox").click()
        print("regular Buy Box")
        time.sleep(1)

    if len(driver.find_elements_by_id("add-to-cart-button")) > 0:
        while True:
            try:
                # driver.find_element_by_id("add-to-cart-button").click()
                driver.execute_script("document.getElementById('add-to-cart-button').click()")
                break
            except ElementClickInterceptedException:
                continue
        return NORMAL_ADD_TO_CART
    if len(driver.find_elements_by_id("availability")) > 0:
        href = driver.find_element_by_id("availability").find_element_by_tag_name("a").get_attribute("href")
        print("href:"+href)
        return href
    return None


def init_driver(driver):
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(5)
    driver.set_script_timeout(5)



def get_fba(url,countrycode):
    #caps = dict(DesiredCapabilities.PHANTOMJS)
    #caps["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 `(Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    #caps["phantomjs.page.settings.loadImages"] = False
    #driver = webdriver.PhantomJS(desired_capabilities=caps)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    #driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()
    init_driver(driver)
    href = link_to_other_page(driver,url)
    # href = GlobalTools.getBaseurlFromCountrycode(countrycode)+"/dp/"+asin+"/ref=redir_mobile_desktop"
    print("ASIN:"+ASIN)
    if href is not None and href != NORMAL_ADD_TO_CART:
        print("link to other page")
        try:
            driver.get(href)
        except:
            traceback.print_exc()
            driver.save_screenshot("d:/" + ASIN + "_timeout.png")
            driver.execute_script('window.stop()')
        init_driver(driver)
        driver.save_screenshot("d:/"+ASIN+"_add_to_cart.png")
        driver.find_element_by_name("submit.addToCart").click()

    elif href is None:
        driver.save_screenshot("d:/"+ ASIN +"_activity.png")
        if len(driver.find_elements_by_xpath("//div[starts-with(@id,'dealCountdownTimer')]")) > 0:
            fba = u"活动中,请手动获取库存"
        else:
            fba = u"此产品需登录才能看到库存"
        print(fba)
        driver.quit()
        return fba



    # if need_proxy(driver,url):
    #     driver.quit()
    #     service_args = [
    #         '--ignore-ssl-errors=true',
    #         '--cookies-file=test.cookies',
    #         '--disk-cache=true',
    #         '--local-to-remote-url-access=true',
    #         '--proxy='+IpPool.get_one(),
    #         '--proxy-type=https',
    #         '--proxy-auth=user:pass',
    #         '--web-security=false',
    #     ]
    #     driver = webdriver.PhantomJS(desired_capabilities=caps,service_args=service_args)
    #     init_driver(driver)

    # driver.get_screenshot_as_file("d:/uuu.png")
    driver.find_element_by_id("hlb-view-cart-announce").click()
    sel = driver.find_element_by_name("quantity")
    Select(sel).select_by_value("10")
    driver.find_element_by_name("quantityBox").send_keys("999")
    #点击更新
    driver.find_element_by_xpath("//a[@data-action='update']").click()
    try:
        WebDriverWait(driver,20).until(EC.invisibility_of_element_located(By.XPATH,"//a[@data-action='update']"))
        print("waiting 20")
    except:
        print("waiting timeout")
        driver.save_screenshot("d:/waiting_timeout.png")
        # driver.quit()
    #get fba
    try:
        driver.save_screenshot("d:/" + ASIN + "_fba.png")
        text = driver.find_element_by_class_name("sc-quantity-update-message").text
        # print text
        if countrycode == "uk":
            if text.find("only") > 0:
                fba = text.split("only")[1].split("of")[0]
            elif text.find("limit") > 0:
                fba = "limit "+text.split("of")[1].split("per")[0]
        if countrycode == "us":
            if text.find("only") > 0:
                fba = text.split("only")[1].split("of")[0]
            elif text.find("limit") > 0:
                fba = "limit "+text.split("of")[1].split("per")[0]
        if countrycode == "de":
            if text.find("pro Kunde") > 0:
                fba = "limit " + text.split("lediglich")[1].split("Exemplare")[0]
            elif text.find("nur") > 0:
                fba = text.split("Exemplare")[0].split("nur")[1]
        if countrycode == "fr":
            if text.find("uniquement disponibles") > 0:
                fba = text.split(":")[1].split(".")[0]
            elif text.find("par client") > 0:
                fba = "limit "+ text.split(":")[1].split(".")[0]
        if countrycode == "it":
            if text.find("articoli disponibili") > 0:
                fba = text.split("solo")[1].split("articoli")[0]
            elif text.find("per cliente") > 0:
                fba = "limit "+ text.split(":")[1].split(".")[0]
        if countrycode == "jp":
            if text.find(u"お取り扱い数") > 0:
                fba = text.split(u"お取り扱い数は")[1].split(u"点")[0]
            elif text.find(u"一人様") > 0:
                fba = "limit" + text.split(u"一人様")[1].split(u"点")[0]

        print("fba:===="+fba)
    except:
        traceback.print_exc()
        if driver.find_element_by_id("sc-subtotal-label-activecart") is not None:
            fba = "999+"
        else:
            fba = "can't get FBA, please try manually"

    driver.get_screenshot_as_file("d:/4.png")
    driver.quit()
    return fba

if __name__=="__main__":
    # url = "https://www.amazon.co.uk/Nestling%C2%AE-Rechargeable-Automatic-Charging-Wardrobe/dp/B014H76RSK/ref=pd_cart_cp_1_1?_encoding=UTF8&pd_rd_i=B014H76RSK&pd_rd_r=KV42DV8MY51SCGD2ZNA9&pd_rd_w=imDbc&pd_rd_wg=bHY6u&psc=1&refRID=KV42DV8MY51SCGD2ZNA9"
    url = "https://www.amazon.co.uk/dp/B0742DRT5S/ref=redir_mobile_desktop"
    fba = get_fba(url,"uk")
    print("fba:",fba)