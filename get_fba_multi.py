#--coding=utf8--
import traceback

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from global_tools import GlobalTools
from search import get_link_by_asin
from comment_hendler import CommentHandler
# from get_fba import get_fba
import re
import os
import time
import xlwt
import xlrd
from xlutils.copy import copy
import sys
import io
import tkinter.messagebox as messagebox
import multiprocessing
import os
import sys
import traceback
import brotli

# Module multiprocessing is organized differently in Python 3.4+
# try:
#     # Python 3.4+
#     if sys.platform.startswith('win'):
#         import multiprocessing.popen_spawn_win32 as forking
#     else:
#         import multiprocessing.popen_fork as forking
# except ImportError:
#     import multiprocessing.forking as forking

NORMAL_ADD_TO_CART = 1
ASIN = ""
# def need_proxy(driver,url):
#     driver.get(url)
#     if len(driver.find_elements_by_id("add-to-cart-button-ubb")) > 0:
#         return True
#     else:
#         return False

def link_to_other_page(driver,url):
    global ASIN
    ASIN = url.split("dp/")[1].split("/ref")[0]
    try:
        driver.get(url)
    except:
        driver.execute_script('window.stop()')

    # f = open("tmp3.html", "w+")
    # f.write(driver.page_source)
    # f.close()
    driver.save_screenshot("d:/" + ASIN + "_first.png")
    if len(driver.find_elements_by_id("add-to-cart-button")) > 0:
        driver.find_element_by_id("add-to-cart-button").click()
        return NORMAL_ADD_TO_CART
    if len(driver.find_elements_by_id("availability")) > 0:
        href = driver.find_element_by_id("availability").find_element_by_tag_name("a").get_attribute("href")
        print("href:"+href)
        return href
    return None


def init_driver(driver):
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)



def get_fba(queue,url,currrow,countrycode):
    result=[currrow]
    caps = dict(DesiredCapabilities.PHANTOMJS)
    caps["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 `(Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    caps["phantomjs.page.settings.loadImages"] = False
    queue.put("try to get phantomjs driver")
    driver = webdriver.PhantomJS(desired_capabilities=caps)
    # driver = webdriver.Chrome()
    queue.put("init driver")
    init_driver(driver)
    # queue.put("before link to other page")
    href = link_to_other_page(driver,url)
    # queue.put("after")
    print("ASIN:"+ASIN)
    result.append(ASIN)
    if href is not None and href != NORMAL_ADD_TO_CART:
        print("link to other page")
        queue.put("link to other page")
        try:
            driver.get(href)
        except:
            traceback.print_exc()
            # driver.save_screenshot("d:/" + ASIN + "_timeout.png")
            driver.save_screenshot("d:/" + ASIN + "_timeout.png")
            driver.execute_script('window.stop()')
        init_driver(driver)
        driver.save_screenshot(GlobalTools.getimgsavepath(ASIN,"add_to_cart"))
        try:
            driver.find_element_by_name("submit.addToCart").click()
        except:
            traceback.print_exc()
            driver.quit()
            return None

    elif href is None:
        queue.put("href is None")
        driver.save_screenshot("d:/"+ ASIN +"_activity.png")
        if len(driver.find_elements_by_xpath("//div[starts-with(@id,'dealCountdownTimer')]")) > 0:
            fba = u"活动中,请手动获取库存"
        else:
            fba = u"此产品需登录才能看到库存"
        print (fba)
        driver.quit()
        result.append(fba)
        return result

    try:
        queue.put("try click cart")
        driver.find_element_by_id("hlb-view-cart-announce").click()
    except:
        traceback.print_exc()
        return None
    queue.put("try click cart")
    sel = driver.find_element_by_name("quantity")
    Select(sel).select_by_value("10")
    driver.find_element_by_name("quantityBox").send_keys("999")
    #点击更新
    driver.find_element_by_xpath("//a[@data-action='update']").click()
    #get fba
    try:
        queue.put("saving screenshot")
        driver.save_screenshot("d:/" + ASIN + "_fba.png")
        text = driver.find_element_by_class_name("sc-quantity-update-message").text
        # print text
        if countrycode == "uk":
            if text.find("only") > 0:
                fba = text.split("only")[1].split("of")[0]
            elif text.find("limit") > 0:
                fba = "limit "+text.split("of")[1].split("per")[0]
        #us site ends with com
        if countrycode == "com":
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
        queue.put("fba:"+fba)
    except:
        traceback.print_exc()
        if driver.find_element_by_id("sc-subtotal-label-activecart") is not None and "999" in driver.find_element_by_id("sc-subtotal-label-activecart").text:
            fba = "999+"
        else:
            print("return None retry")
            return None
    result.append(fba)
    driver.get_screenshot_as_file("d:/4.png")
    driver.quit()
    return result

def fun(queue,link,currrow,countrycode):
    while True:
        queue.put("trying ")
        result = get_fba(queue,link,currrow,countrycode)
        if result is not None:
            queue.put("get fba success!")
            return result
        else:
            queue.put("get fba failed retring......")

def main(queue):
    if not os.path.isfile(GlobalTools.getExcelFile("fba")):
        queue.put("ERROR:"+u"请将fba.xls放到和amazon.exe相同目录下")
        exit(0)

    productlinks = []

    rb = xlrd.open_workbook(GlobalTools.getExcelFile("fba"))

    try:
        sheet = rb.sheet_by_index(0)
        count = sheet.nrows
        for i in range(0,count):
            print(sheet.cell_value(i,0))
            productlinks.append(sheet.cell_value(i,0))
    except:
        queue.put("ERROR:" + u"请保证文件包含商品链接")
        exit(0)

    wb = copy(rb)
    sheet = wb.add_sheet(time.strftime(u"%m-%d_%H-%M",time.localtime(time.time())))

    pool = multiprocessing.Pool(processes=5)

    currrow = 0
    results = []


    for link in productlinks:
        if link.strip() == "":
            currrow+=1
            continue
        countrycode = link.split("amazon.")[1].split(".")[-1].split('/')[0]
        results.append(pool.apply_async(fun,(queue,link,currrow,countrycode)))
        currrow+=1

    pool.close()
    pool.join()
    # for res in results:
    #     # try:
    #     print res.get()
    #     # except:
    #     #     pass
    # print "finish."

    tmpresult = []

    for result in results:
        try:
            row = result.get()
            tmpresult.append(row)
            currrow = row[0]
            print("currrow:"+str(currrow))
            col = 0
            for i in range(1,len(row)):
                sheet.write(currrow, col, row[i])
                col+=1
        except:
            pass

    try:
        wb.save(GlobalTools.getExcelFile("fba"))
    except:
        tmp = open("./tmp.txt","w+")
        for row in tmpresult:
            tmp.write(str(row)+"\n")
        queue.put("ERROR:"+u"保存文件失败，运行时，请不要打开fba.xls文件")

    queue.put("finish.")

if __name__=="__main__":
    main()