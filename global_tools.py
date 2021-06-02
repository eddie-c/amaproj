#coding:utf-8
import random
import tkinter.messagebox as messagebox
from bs4 import BeautifulSoup
import brotli
import re

class GlobalTools(object):

    baseurl = ""

    @classmethod
    def setbaseurl(cls,baseurl):
        cls.baseurl = baseurl

    @classmethod
    def getLoginUrl(cls):
        return "http://127.0.0.1:63342/amazonphp7/login.php"

    @classmethod
    def getbaseurl(cls):
        return cls.baseurl

    @classmethod
    def getUserAgent(cls):
        user_agents = [
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        ]
        return random.choice(user_agents)

    @classmethod
    def getHeaders(cls):
        headers = {
            "Connection":"keep-alive",
            "Connection":"Transfer-Encoding",
            "Pragma":"no-cache",
            "Content-Type":"text/html;charset=UTF-8",
            # "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Cache-Control":"no-cache",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent": cls.getUserAgent(),
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Content-Encoding":"br",
            "Cookie":"""session-id=262-8263593-8680131; ubid-acbuk=259-6381954-9508758; lc-acbuk=en_GB; x-acbuk="G3?sdNJvonWxm?OgngVrbTBXRGhXcPkYp?Y6?u9cDfOuKKd95UL2s7opXa?J8nvV"; at-acbuk=Atza|IwEBIMwzF8p5bjpf4qQa0qbeCR1bfiymF59JcMieXE8CT52vV_HA0ld3HjbFa46IQg9YAeA1jt9AjWYfKq5rsf2ilwKIPtpnkwJXwhsb4WDkSLcAXZP7bwkFBJBVy21v_MPivDeWk4FPgaeRmAR8ic9bg52FMJCDjhXUSiVTs4wnEpfEER8amFxcooiTPjqE2JSUeSD9SevMalgLhdawpl_HfPlt; sess-at-acbuk="XplVpZ8Nj/rc3t8XPchLE89tsfXtabeGDK4RdtX5GE8="; sst-acbuk=Sst1|PQFmWD2PZmdj1dwrP_ZmBBkYCdlBhzSWxqqqFQR26atTgH9xad4jh8_CthlcHqRdUfC-t2r-5fRR3gnrcWgdW43FCsJzZXnMXSwNjvpDQthHaaS3w_v-TuCnXXeMpqDKw7-zvzUMD8GPmlM_ZkWnHXAcMJalSo0EcdW9W2Fl7dEhJOX3mj-2AfmlypGvsePmQE9NTbyV9LDh0dqq2uiNMrPuiYfHcHBeNojM0VgJMEZdMfXvs6CcdVQ97Y_jPWcvNf-LDLtkirPFp5vmmjwSvsHiu_SLwkijBGLePzpX0AADHm8; i18n-prefs=GBP; session-token="iT6S2+wNqWY4m15ihTdWKDDcbAPiPXaEq4PHUr9Kdi8HVDBJLcaY0xv9S57gJc4BOpu/f8amTUNqcY1lJYE4UAYG6in8Tif0rEUH6d+xUkCWwgOFkp7Yb1fJodsPi+Yxgvjm7VFj5Z6jTCPLPmQ4rik5KAK2/BHtOR1JvsdEU03WkLDlSKlqO2wiym2BKxa8okb1tiiOMeYu2Sh09PTrmg=="; session-id-time=2082758401l; csm-hit=tb:G1XJ01DT0S9NEX1SJMMZ+s-G1XJ01DT0S9NEX1SJMMZ|1622614501276&t:1622614501276&adb:adblk_no"""
        }
        return headers

    @classmethod
    def setCookie(cls,cookies):
        cls.cookies = cookies

    @classmethod
    def getCookie(cls):
        return cls.cookies

    @classmethod
    def getMarketplaceID(cls):
        return "A1F83G8C2ARO7P"

    @classmethod
    def getExcelFile(cls,countrycode):
        # return "./uk.xls"
        # return "./"+countrycode+".xls"
        return "/Users/eddie/PycharmProjects/amaproj/"+countrycode+".xls"


    @classmethod
    def getimgsavepath(cls, asin, extrainfo):
        return "./imgs/"+asin+"_"+extrainfo+".png"

    @classmethod
    def getSearchShopProductsUrl(cls):
        return "https://www.amazon.co.uk/sp/ajax/products"

    # def getSavePath(self):
    #     return "./uk.xls"

    @classmethod
    def get_table_header(self):
        return [u"商品链接",u"价格",u"店铺名称",u"商标",u"上架时间",u"QA:",u"STARS",u"好评",u"差评",u"好评点赞数",u"库存",u"一级分类",u"二级分类",u"排名"]

    @classmethod
    def get_search_products_pagesize(cls):
        return 12

    @classmethod
    def showMessage(cls,title,message):
        messagebox.askyesno(title, message)

    @classmethod
    def showerror(cls,title,message):
        messagebox.showerror(title,message)

    @classmethod
    def getResponseContent(cls,res):
        # html = ""
        if res.headers['Content-Encoding'] == "br":
            html = BeautifulSoup(brotli.decompress(res.content), "lxml")
        else:
            html = BeautifulSoup(res.content, "lxml")
        return html

    @classmethod
    def removeBlankChars(cls,txt):
        out = re.sub(r"\s{2,}", " ", txt)
        return out

    @classmethod
    def getBaseurlFromCountrycode(cls,countrycode):
        countrycodemap = {
            "us":"https://www.amazon.com",
            "uk":"https://www.amazon.co.uk",
            "de":"https://www.amazon.de",
            "fr":"https://www.amazon.fr",
            "it":"https://www.amazon.it",
            "jp":"https://www.amazon.co.jp"
        }

        return countrycodemap[countrycode]

if __name__=="__main__":
    txt = "\n\n this is o ...hhaha \n\n    "
    print(GlobalTools.removeBlankChars(txt))
