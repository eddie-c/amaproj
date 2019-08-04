#__coding=utf8__
import  requests
import  requests.sessions
from bs4 import BeautifulSoup
from global_tools import GlobalTools
from search import get_link_by_asin
from comment_hendler import CommentHandler
from get_fba import get_fba
import time
import xlrd
from xlutils.copy import copy
import tkinter.messagebox as messagebox
import multiprocessing
import os
import brotli
import logging
import traceback
from tkinter import *


class amazon(object):
    def __init__(self,queue,asin,countrycode):
        self.queue = queue
        self.countrycode = countrycode
        self.baseurl = GlobalTools.getBaseurlFromCountrycode(countrycode)
        self.headers = GlobalTools.getHeaders()
        self.asin = asin
        self.url = get_link_by_asin(asin,self.baseurl)
        #if can't get a normal page ,can't use this kind of url to get a price and shop name
        #the second link look like this : http://www.amazon.de/gp/offer-listing/B01N52QW8A/ref=dp_olp_0?ie=UTF8&condition=all
        self.second_url = ""
        self.normal_situation = True
        self.unnormal_price = ""
        self.unnormal_shop = ""
        self.resultmap = {}
        self.result = []
        self.us_reviews_need_adjust = False

    def prerequest(self):
        queue = self.queue
        queue.put("prerequest")
        print("prerequest")
        GlobalTools.setbaseurl(self.baseurl)
        res = requests.get(self.url, headers=self.headers)
        self.res = res

        html = GlobalTools.getResponseContent(self.res)

        if html.find(id="add-to-cart-button") is None:
            if html.find(id="availability") is not None:
                # print "text" + html.find(id="availability").text
                url = self.baseurl + html.find(id="availability").find("a").get('href')
                self.second_url = url
                res = requests.get(url, headers=GlobalTools.getHeaders())
                html = GlobalTools.getResponseContent(res)

                try:
                    price = html.find(class_="olpOfferPrice").text.strip()
                    self.unnormal_price = price
                    print(price)
                    shop = html.find(class_="olpSellerName").text
                    self.unnormal_shop = shop
                    print(shop)
                except:
                    traceback.print_exc()
                self.normal_situation = False
                return False
        return True


    def parse(self,sheet,currrow):
        queue = self.queue
        self.result = [currrow]
        print("")
        queue.put(u"商品链接")
        queue.put(self.url)
        print("商品链接:")
        print(self.url)

        self.html = GlobalTools.getResponseContent(self.res)

        self.geturl()
        self.getprice()
        self.getshopname()
        self.getbrand()
        self.getfirstavailable()
        self.getranking()
        self.getqa()
        self.getCategory()
        self.getstars()
        self.getreviewcount()
        self.getgoodreviewvote()
        #美国的reviewcount是在getgoodreviewvote中统计出来的，所以要重新计算一下
        # if self.countrycode=="us":
            # self.adjustreviewcount()
        if self.us_reviews_need_adjust:
            self.getusviewcount()

        self.getfba()
        print(self.resultmap)
        return self.getresult()
        # return self.result

    def getresult(self):
        resultmap = self.resultmap
        result = self.result
        result.append(resultmap['url'])
        result.append(resultmap['price'])
        result.append(resultmap['shop'])
        result.append(resultmap['brand'])
        result.append(resultmap['first_available'])
        result.append(resultmap['qa'])
        result.append(resultmap['stars'])
        result.append(resultmap['positivereviewcount'])
        result.append(resultmap['negtivereviewcount'])
        result.append(resultmap['positivereviewvote'])
        result.append(resultmap['fba'])
        result.append(resultmap['first_level_menu'])
        result.append(resultmap['second_level_menu'])
        result.append(resultmap['ranking'])
        return result

    def adjustreviewcount(self):
        self.resultmap['positivereviewcount'] = self.comment_handler.getUsPositiveReviewCount()
        self.resultmap['negtivereviewcount'] = self.reviewCount - self.resultmap['positivereviewcount']

    def geturl(self):
        self.resultmap['url'] = self.url

    def getbrand(self):
        try:
            brand = self.html.find(id="brand").text.strip()
        except:
            brand = ""

        self.resultmap['brand'] = brand
        self.queue.put("brand:"+brand)

    def getprice(self):
        html = self.html
        price = html.find(id="priceblock_ourprice")
        if price is None:
            price = html.find(id="priceblock_dealprice")
        if price is None:
            price = html.find(id="priceblock_saleprice")
        if price is None:
            price = html.find(id="olp_feature_div")

        if self.normal_situation is False:
            self.resultmap['price'] = self.unnormal_price
        else:
            self.resultmap['price'] = price.text.strip()
        self.queue.put("price:"+self.resultmap['price'])
    def getfirstavailable(self):
        if self.countrycode=="us":
            if "Date First Available" in self.html.find(id="productDetails_detailBullets_sections1").find_all("th")[-1].text:
                first_available = self.html.find(id="productDetails_detailBullets_sections1").find_all("td")[-1]
            else:
                self.resultmap['first_available'] = ""
                return
        else:
            first_available = self.html.find(attrs={"class": "date-first-available"}).find(attrs={"class": "value"})
        self.resultmap['first_available'] = first_available.text.strip()
        self.queue.put("first_available:" + self.resultmap['first_available'])

    def getshopname(self):
        html = self.html
        try:
            shop = html.find(id="merchant-info").find('a')
            self.resultmap['shop'] = shop.text.strip()
        except:
            self.resultmap['shop'] = self.unnormal_shop

        self.queue.put("shop:" + self.resultmap['shop'])

    def getqa(self):
        try:
            if self.countrycode == "jp":
                qa = self.html.find(id="askATFLink").text.strip().split(u"人")[0]
            else:
                qa = self.html.find(id="askATFLink").text.strip().split()[0]
        except:
            qa = "0"
        self.resultmap['qa'] = qa
        self.queue.put("qa:" + self.resultmap['qa'])

    def getstars(self):
        try:
            if self.countrycode == "jp":
                stars = self.html.find(id="acrPopover").find('a').find('span').text.split()[1]
            else:
                stars = self.html.find(id="acrPopover").find('a').find('span').text.split()[0]
        except:
            stars = "no reviews"
        self.resultmap['stars'] = stars
        self.queue.put("stars:" + self.resultmap['stars'])

    def getusviewcount(self):
        asin = self.asin
        url = "https://www.amazon.com/product-reviews/"+asin+"/ref=acr_dpx_see_all?ie=UTF8&showViewpoints=1"
        res = requests.get(url,headers = GlobalTools.getHeaders())
        html = GlobalTools.getResponseContent(res)
        viewpoints = html.find_all(id=re.compile("viewpoint-"))
        if len(viewpoints)>0:
            try:
                positive = viewpoints[0].find_all(attrs={"data-reftag":"cm_cr_arp_d_viewpnt_lft"})[0].text
                self.resultmap['positivereviewcount'] = int(positive.split("positive")[0].split("all")[1].strip())
            except:
                pass
        if len(viewpoints)>1:
            try:
                negtive = viewpoints[1].find_all(attrs={"data-reftag":"cm_cr_arp_d_viewpnt_rgt"})[0].text
                self.resultmap['negtivereviewcount'] = int(negtive.split("critical")[0].split("all")[1].strip())
            except:
                pass
        print(viewpoints)

    def getreviewcount(self):
        html = self.html
        scoretable = html.find(id='histogramTable')
        rows = scoretable.find_all('tr', attrs={'class': 'a-histogram-row'})
        starcount = []

        if self.countrycode == "us":
            reviewText = html.find(id="acrCustomerReviewText")
            if reviewText != None:
                reviewCount = int(reviewText.text.split()[0].replace(",",""))
            else:
                reviewCount = 0

            self.reviewCount = reviewCount
            # if reviewCount == 0:
            #     positivecount = 0
            #     negtivecount = 0

            for i in range(0, len(rows)):
                try:
                    starcount.append(
                        int(rows[i].find('a', attrs={'class': 'histogram-review-count'}).text.split('%')[0]))
                except:
                    starcount.append(0)
            print(starcount)
            if starcount[0] + starcount[1] == 0:
                negtivecount = reviewCount
                positivecount = 0
            elif starcount[2] + starcount[3] + starcount[4] == 0:
                positivecount = reviewCount
                negtivecount = 0
            else:
                positivecount = reviewCount * (starcount[0] + starcount[1]) / 100 + 1
                negtivecount = reviewCount * (starcount[2] + starcount[3] + starcount[4]) / 100 + 1
                self.us_reviews_need_adjust = True

        else:
            for i in range(0, len(rows)):
                try:
                    starcount.append(int(rows[i].find_all('a')[2].text))
                except:
                    starcount.append(0)
            positivecount = starcount[0] + starcount[1]
            negtivecount = starcount[2] + starcount[3] + starcount[4]

        self.resultmap['positivereviewcount'] = positivecount
        self.resultmap['negtivereviewcount'] = negtivecount
        self.queue.put("positivereviewcount:" + str(self.resultmap['positivereviewcount']))
        self.queue.put("negtivereviewcount:" + str(self.resultmap['negtivereviewcount']))
    def getgoodreviewvote(self):
        self.parse_comment(self.asin, self.resultmap['positivereviewcount'], self.resultmap['negtivereviewcount'])

    def getranking(self):
        if self.countrycode == "us":
            addtional_info_items = self.html.find(id="productDetails_detailBullets_sections1").find_all("tr")
            for tr in addtional_info_items:
                if "Best Sellers Rank" in tr.find("th").text:
                    rank = tr.find("td").find_all("span")[0]
                    break
        else:
            rank = self.html.find(id="SalesRank").find("td", class_="value")

        if rank is not None:
            if self.countrycode != "us":
                rankul = rank.find("ul")

                rankitems = rank.find("ul").find_all("li")
                itemtext = ""
                for item in rankitems:
                    itemtext += ''.join(item.stripped_strings)+"\n"
                print("itemtext:")
                print(itemtext)
                rankul.decompose()
                ranktext = rank.text.strip()+"\n"+itemtext
                print("rank text:")
                print(rank.text.strip()+"\n"+itemtext)
            else:
                rankitems = rank.find_all("span")
                ranktext = ""
                for item in rankitems:
                    ranktext += "".join(item.stripped_strings) + "\n"

        countrySepMap = {
            "uk":"#",
            "us":"#",
            "fr":u"n°",
            "it":"n.",
            "de":"Nr.",
            "jp":u"位"
        }
        # rank = self.html.find(id="SalesRank")
        #
        # if rank is not None:
        #     out = re.sub(r"\s{2,}", " ", rank.text)
        #     s1 = out.split(countrySepMap[self.countrycode])
        #     for i in range(1, len(s1)):
        #         s1[i] = countrySepMap[self.countrycode] + s1[i]
        #     ranktext = "\n".join(s1)
        # else:
        #     ranktext = ""

        self.resultmap['ranking'] = ranktext
        # 在这里添加分类：
        if ranktext != "":
            if self.countrycode == "uk":
                self.resultmap['first_level_menu'] = ranktext.split("(")[0].split("in")[1]
            if self.countrycode == "jp":
                self.resultmap['first_level_menu'] = ranktext.split("-")[0]
            if self.countrycode == "de":
                self.resultmap['first_level_menu'] = ranktext.split("(")[0].split("in")[1]
            if self.countrycode == "fr":
                self.resultmap['first_level_menu'] = ranktext.split("(")[0].split("en")[1]
            if self.countrycode == "it":
                self.resultmap['first_level_menu'] = ranktext.split("(")[0].split("in")[1]
            if self.countrycode == "us":
                self.resultmap['first_level_menu'] = ranktext.split("(")[0].split("in")[1]
        self.queue.put("ranking:" + self.resultmap['ranking'])

    def getCategory(self):
        try:
            #商品有时没有分类，这时先在这里取为空""，在下面回去分类排名的时候，取第一分类
            menu_levels = self.html.find(id="wayfinding-breadcrumbs_feature_div").find_all(attrs={"class":"a-list-item"})
            count = len(menu_levels)
            self.resultmap['first_level_menu'] = GlobalTools.removeBlankChars(menu_levels[0].text)
            if count>=3:
                self.resultmap['second_level_menu'] = GlobalTools.removeBlankChars(menu_levels[2].text)
        except:
            pass

    def parse_comment(self, asin,positive_count,negtive_count):
        comment_handler = CommentHandler(asin,positive_count,negtive_count)
        #美国站点需要用到此变量
        self.comment_handler = comment_handler
        comment_handler.getPositiveCommentsInfo()
        print(u"好评点赞数：")
        positive_vote = comment_handler.get_positive_votes()
        self.resultmap['positivereviewvote'] = positive_vote
        self.queue.put("positivereviewvote:" + str(self.resultmap['positivereviewvote']))

    def getfba(self):
        print(u"库存：")
        try:
            self.resultmap['fba'] = get_fba(self.url,self.countrycode)
        except:
            traceback.print_exc()
            self.resultmap['fba'] = u"获取库存超时，请手动获取"
        self.queue.put("fba:" + self.resultmap['fba'])

def fun(queue,product,countrycode,currrow,sheet):
    amazonobj = amazon(queue,product,countrycode)
    amazonobj.prerequest()
    result = amazonobj.parse(sheet,currrow)
    return result

def main(queue,countrycode):
    if not os.path.isfile(GlobalTools.getExcelFile(countrycode)):
        # messagebox.showerror("error", u"请将uk.xls放到和amazon.exe相同目录下")
        queue.put(u"ERROR:请将"+countrycode+u".xls放到和amazon.exe相同目录下")
        exit(0)

    products = []
    rb = xlrd.open_workbook(GlobalTools.getExcelFile(countrycode))
    try:
        sheet = rb.sheet_by_name("asin")
        count = sheet.nrows
        for i in range(0, count):
            print(sheet.cell_value(i, 0))
            products.append(sheet.cell_value(i, 0))
    except:
        # messagebox.showerror("error", u"uk.xls中必须包含名字为asin的sheet")
        queue.put(u"ERROR:请将" + countrycode + u".xls放到和amazon.exe相同目录下")
        exit(0)
    print("copy")
    wb = copy(rb)
    sheet = wb.add_sheet(time.strftime(u"%m-%d_%H-%M", time.localtime(time.time())))
    # 写头部标题：
    tableheaders = GlobalTools.get_table_header()
    row = 0
    col = 0
    for item in tableheaders:
        sheet.write(row, col, item)
        col += 1

    pool = multiprocessing.Pool(processes=5)

    currrow = 1
    results = []

    for product in products:
        results.append(pool.apply_async(fun, (queue,product, countrycode, currrow, sheet, )))
        currrow += 1

    pool.close()
    pool.join()
    # for res in results:
    #     # try:
    #     print res.get()
    #     # except:
    #     #     pass


    for result in results:
        try:
            row = result.get()
            currrow = row[0]
            print("currrow:" + str(currrow))
            col = 0
            for i in range(1, len(row)):
                sheet.write(currrow, col, row[i])
                col += 1
        except:
            pass
    try:
        wb.save(GlobalTools.getExcelFile(countrycode))
    except:
        queue.put(u"ERROR:保存文件失败，运行时，请不要打开站点对应的xls文件")
        exit(0)
    queue.put("finish.")

def single_thread_main():
    if not os.path.isfile("d:/de.xls"):
        messagebox.showerror("error",u"请将uk.xls放到和amazon.exe相同目录下")
        exit(0)

    products = []

    rb = xlrd.open_workbook("d:/de.xls")

    try:
        sheet = rb.sheet_by_name("asin")
        count = sheet.nrows
        for i in range(0,count):
            print(sheet.cell_value(i,0))
            products.append(sheet.cell_value(i,0))
    except:
        messagebox.showerror("error", u"uk.xls中必须包含名字为asin的sheet")
        exit(0)
    wb = copy(rb)
    sheet = wb.add_sheet(time.strftime(u"%m-%d_%H-%M",time.localtime(time.time())))
    #写头部标题：
    tableheaders = GlobalTools.get_table_header()
    row = 0
    col = 0
    for item in tableheaders:
        sheet.write(row,col,item)
        col += 1

    currrow = 1

    for product in products:
        amazonobj = amazon(product)
        amazonobj.prerequest()
        result = amazonobj.parse(sheet,currrow)
        currrow += 1
        try:
            wb.save("d:/de.xls")
        except:
            messagebox.showerror("error", u"保存文件失败，运行时，请不要打开uk.xls文件")
        # except:
        #     continue

if __name__=="__main__":
    # if sys.platform.startswith('win'):
    #     # First define a modified version of Popen.
    #     class _Popen(forking.Popen):
    #         def __init__(self, *args, **kw):
    #             if hasattr(sys, 'frozen'):
    #                 # We have to set original _MEIPASS2 value from sys._MEIPASS
    #                 # to get --onefile mode working.
    #                 os.putenv('_MEIPASS2', sys._MEIPASS)
    #             try:
    #                 super(_Popen, self).__init__(*args, **kw)
    #             finally:
    #                 if hasattr(sys, 'frozen'):
    #                     # On some platforms (e.g. AIX) 'os.unsetenv()' is not
    #                     # available. In those cases we cannot delete the variable
    #                     # but only set it to the empty string. The bootloader
    #                     # can handle this case.
    #                     if hasattr(os, 'unsetenv'):
    #                         os.unsetenv('_MEIPASS2')
    #                     else:
    #                         os.putenv('_MEIPASS2', '')
    #
    #
    #     # Second override 'Popen' class with our modified version.
    #     forking.Popen = _Popen
    multiprocessing.freeze_support()
    # main()
    single_thread_main()

