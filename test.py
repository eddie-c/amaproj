import requests
from selenium import webdriver
import time
import re
import json

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8;",
    # "cookie": "session-id=257-6148668-6321746; i18n-prefs=GBP; ubid-acbuk=257-8856236-4543129; session-id-time=2082758401l; x-wl-uid=1E3xTGFjbbBu/u03NTEDX9na+747rpOq7ZDxEOvumD5UltvaLaNF4pZHTqBbLn9fgTcN6t4VEFGE=; session-token=5AAtC+m8BGxFw6IflPOSWxHpTsgZwPqsdVjtHRMhW4zdAXQZJa/EY1QdvxGk051KR8xx5n8IIwxmYkOHoWBrTCBKJue8ZhFP6BGx9hbQg1/rnQBckdKuIxjOw/OgKnMoVcKRb09+HlfPvXykz5O9q8ragOg/PjDwuBFTqnvvLKVOB5Wz1UcyzXl0ehUecDyPg+kcLbHW2pc58ybEJGGjYo05mwhPD6Fc2TlUunxIw6sle+6SrCRgA51ikXuIcd6bjantWLiZj18=; csm-hit=tb:RTR9T3XM284ZA8JEF3K4+s-TBJR43MW3RD2P2V8H0WV|1563193419563&t:1563193419563&adb:adblk_no",
    "origin": "https://www.amazon.co.uk",
    "referer": "https://www.amazon.co.uk/gp/cart/view.html/ref=lh_cart",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.90 Chrome/75.0.3770.90 Safari/537.36",
    "x-aui-view": "Desktop",
    "x-requested-with": "XMLHttpRequest"
}

def gotocartpage():
    url = "https://www.amazon.co.uk/gp/cart/view.html?ref_=nav_cart"
    session = requests.session()
    res = session.post(url,headers=headers)
    pass

def getRequestId():
    html = open("a.txt","r").read()
    p = re.search(r"var opts =(.*?);", html, flags=re.DOTALL + re.MULTILINE)
    json.(p.group(1))
    pass

def view_html():
    url = "https://www.amazon.co.uk/gp/cart/view.html?ref_=nav_cart"
    global headers
    res = requests.post(url,headers=headers)
    print(res.text)

def getfba():
# ch = webdriver.Chrome()
    url = "https://www.amazon.co.uk/gp/cart/ajax-update.html/ref=ox_sc_update_quantity_1%7C1%7C999"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8;",
        "cookie": "session-id=257-6148668-6321746; i18n-prefs=GBP; ubid-acbuk=257-8856236-4543129; session-id-time=2082758401l; x-wl-uid=1E3xTGFjbbBu/u03NTEDX9na+747rpOq7ZDxEOvumD5UltvaLaNF4pZHTqBbLn9fgTcN6t4VEFGE=; session-token=5AAtC+m8BGxFw6IflPOSWxHpTsgZwPqsdVjtHRMhW4zdAXQZJa/EY1QdvxGk051KR8xx5n8IIwxmYkOHoWBrTCBKJue8ZhFP6BGx9hbQg1/rnQBckdKuIxjOw/OgKnMoVcKRb09+HlfPvXykz5O9q8ragOg/PjDwuBFTqnvvLKVOB5Wz1UcyzXl0ehUecDyPg+kcLbHW2pc58ybEJGGjYo05mwhPD6Fc2TlUunxIw6sle+6SrCRgA51ikXuIcd6bjantWLiZj18=; csm-hit=tb:RTR9T3XM284ZA8JEF3K4+s-TBJR43MW3RD2P2V8H0WV|1563193419563&t:1563193419563&adb:adblk_no",
        "origin": "https://www.amazon.co.uk",
        "referer": "https://www.amazon.co.uk/gp/cart/view.html/ref=lh_cart",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.90 Chrome/75.0.3770.90 Safari/537.36",
        "x-aui-view": "Desktop",
        "x-requested-with": "XMLHttpRequest"
    }
    data = {
        # "hasMoreItems": "0",
        "timeStamp": 1563262177,
        "token": "gHmEHM5DWA7bCx4C3siEjFDzgHdhPUHmCJK8xFIAAAAJAAAAAF0tfOFyYXcAAAAA",
        "requestID": "B8YJQ25KSVJBTB62E5J5",
        # "activeItems": "C64ad9644-3c3c-4d0a-b7e4-3a665b03ae9e|1|0|1|17.99|||0||",
        "addressId":"",
        "addressZip":"",
        # "closeAddonUpsell": "1",
        # "flcExpanded": "0",
        "quantity.C64ad9644-3c3c-4d0a-b7e4-3a665b03ae9e": "999",
        "pageAction": "update-quantity",
        "submit.update-quantity.C64ad9644-3c3c-4d0a-b7e4-3a665b03ae9e": "1",
        # "displayedSavedItemNum": "0",
        "actionItemID": "C64ad9644-3c3c-4d0a-b7e4-3a665b03ae9e",
        "actionType": "update-quantity",
        "asin": "B07QBMJW6W",
        "encodedOffering": "K4yBXL%2BNCuX2sjFiOvyf4w8H8srfUCcoXLk8QopkWkpVEyzG4ICuYqskHKlK5wiTnl1SZNEgBpyun%2BaX58UWYvrCmVqQm7%2BBhF5airueyDVCCjT1qB3gtKsAOcBCVLl5lxLpvY6cvENBT%2F7lrCYYv4%2F36YZn7ZWm",
    }
    res = requests.post(url=url,headers=headers,data=data)
    print(res.text)

if __name__=="__main__":
    # getfba()
    # view_html()
    getRequestId()
    # gotocartpage()