#__coding=utf8__
import  requests
import  requests.sessions
from bs4 import BeautifulSoup
from global_tools import GlobalTools
from search import get_link_by_asin
from comment_hendler import CommentHandler
from get_fba import get_fba
import re
import os
import time
import xlwt
import xlrd
from xlutils.copy import copy
import sys
import io
import tkMessageBox as messagebox
import multiprocessing
import os
import sys
import  traceback
import brotli

# Module multiprocessing is organized differently in Python 3.4+
try:
    # Python 3.4+
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking



class amazon(object):
    def __init__(self, asin=None, url=None):
        self.baseurl = "https://www.amazon.co.uk"
        try:
            self.url = get_link_by_asin(asin,self.baseurl)
        except:
            traceback.print_exc()
        self.headers = GlobalTools.getHeaders()
        self.asin = asin
        self.second_url = ""
        self.normal_situation = True
        self.unnormal_price = ""
        self.unnormal_shop = ""


    def prerequest(self):
        GlobalTools.setbaseurl(self.baseurl)
        res = requests.get(self.url, headers=self.headers)
        # print "url:"+res
        self.res = res

        html = GlobalTools.getResponseContent(self.res)

        if html.find(id="add-to-cart-button") is None:
            if html.find(id="availability") is not None:
                print "text" + html.find(id="availability").text
                url = self.baseurl + html.find(id="availability").find("a").get('href')
                self.second_url = url
                res = requests.get(url, headers=GlobalTools.getHeaders())
                html = GlobalTools.getResponseContent(res)

                try:
                    price = html.find(class_="olpOfferPrice").text.strip()
                    self.unnormal_price = price
                    print price
                    shop = html.find(class_="olpSellerName").text
                    self.unnormal_shop = shop
                    print shop
                except:
                    traceback.print_exc()
                self.normal_situation = False
                return False
        return True


    def parse(self,sheet,currrow):
        result = [currrow]
        second_level_menu = None


        # tmp = open("tmp2.html", "w+")
        # if self.res.headers['Content-Encoding'] == "br":
        #     tmp.write(brotli.decompress(self.res.content))
        # else:
        #     tmp.write(self.res.content)
        # tmp.close()

        html = GlobalTools.getResponseContent(self.res)
        price = html.find(id="priceblock_ourprice")
        if price is None:
            price = html.find(id="priceblock_saleprice")
        if price is None:
            price = html.find(id="olp_feature_div")

        try:
            shop = html.find(id="merchant-info").find('a')
        except:
            pass
        brand = html.find(id="brand")
        first_available = html.find(attrs={"class":"date-first-available"}).find(attrs={"class":"value"})
        reviewCount = html.find(id="averageCustomerReviewCount")
        averageRating = html.find(id="averageCustomerReviewRating")

        rank = html.find(id="SalesRank")

        print "rank contents:"
        print rank.contents[1].contents

        if rank is not None:
            out = re.sub(r"\s{2,}", " ", rank.text)

            s1 = out.split("#")
            for i in range(1, len(s1)):
                s1[i] = "#" + s1[i]
            ranktext = "\n".join(s1)
        else:
            ranktext = ""

        try:
            qa = html.find(id="askATFLink").text.strip().split()[0]
        except:
            qa = "0"


        try:
            #商品有时没有分类，这时先在这里取为空""，在下面回去分类排名的时候，取第一分类
            menu_levels = html.find(id="wayfinding-breadcrumbs_feature_div").find_all(attrs={"class":"a-list-item"})
            count = len(menu_levels)
            if count>=3:
                first_level_menu = menu_levels[0].text
                second_level_menu = menu_levels[2].text
            elif count>=1:
                first_level_menu = menu_levels[0].text
        except:
            pass

        print u"商品链接:"
        print self.url
        result.append(self.url)
        # print u"价格:"
        # print price.text.strip().encode('utf-8')
        if self.normal_situation is False:
            result.append(self.unnormal_price)
        else:
            result.append(price.text.strip())
        # print u"店铺名称"
        # print shop.text.strip().encode('utf-8')
        try:
            result.append(shop.text.strip())
        except:
            result.append(self.unnormal_shop)
        # print u"商标:"
        # print brand.text.strip().encode('utf-8')
        try:
            result.append(brand.text.strip())
        except:
            result.append("")
        # print u"上架时间"
        # print first_available.text.strip()
        result.append(first_available.text.strip())
        #print reviewCount.text.strip()
        #print averageRating.text.strip()
        # print u"QA:"
        # print qa
        result.append(qa)
        #print "stars:"
        try:
            stars = html.find(id="acrPopover").find('a').find('span').text.split()[0]
        except:
            stars = "no reviews"
        #print "starts:"
        print stars
        result.append(stars)
        # print u"一级分类，二级分类:"
        # print first_level_menu.strip()
        # print second_level_menu.strip()
        # print u"排名:"
        # print ranktext.encode('utf-8')
        #print html.find('a',attrs={'class':'5star','class':'histogram-review-count'})
        scoretable = html.find(id='histogramTable')
        rows = scoretable.find_all('tr',attrs={'class':'a-histogram-row'})
        # fivestar = int(rows[0].find('a', attrs={'class': 'histogram-review-count'}).text)
        # fourstar = int(rows[1].find('a',attrs={'class':'histogram-review-count'}).text)
        # threestar = int(rows[2].find('a',attrs={'class':'histogram-review-count'}).text)
        # twostar = int(rows[3].find('a', attrs={'class':'histogram-review-count'}).text)
        # onestar = int(rows[4].find('a', attrs={'class':'histogram-review-count'}).text)
        starcount = []
#**********************************************************************************************************************
        for i in range(0, len(rows)):
            try:
                starcount.append(int(rows[i].find('a', attrs={'class': 'histogram-review-count'}).text))
            except:
                starcount.append(0)
        # positivecount = fivestar+fourstar
        # negtivecount = threestar+twostar+onestar
        positivecount = starcount[0]+starcount[1]
        negtivecount = starcount[2]+starcount[3]+starcount[4]
        print u"好评："
        print positivecount
        result.append(positivecount)
        print u"差评："
        print negtivecount
        result.append(negtivecount)
        #href = html.find(id="dp-summary-see-all-reviews").get("href")
        #href = self.baseurl + href
        #self.parse_comment(href)
        self.parse_comment(self.asin, positivecount, negtivecount, result)
        print u"库存："
        try:
            result.append(get_fba(self.url,"uk"))
        except:
            traceback.print_exc()
            result.append(u"获取库存超时，请手动获取")
        #-------------savedata-------------
#        self.save_data(result)
        result.append(first_level_menu.strip())
        result.append(second_level_menu.strip())
        result.append(ranktext)
        return result
        # col = 0
        # for item in result:
        #     sheet.write(currrow,col,item)
        #     col+=1


    def parse_comment(self, asin,positive_count,negtive_count,result):
        comment_handler = CommentHandler(asin,positive_count,negtive_count)
        comment_handler.getPositiveCommentsInfo()
        print u"好评点赞数："
        postive_vote = comment_handler.get_positive_votes()
        result.append(postive_vote)

def fun(product,currrow,sheet,wb):

    amazonobj = amazon(product)
    # link = get_link_by_asin
    amazonobj.prerequest()
    try:
        result = amazonobj.parse(sheet,currrow)
    except:
        traceback.print_exc()

    return result

def main():

    if not os.path.isfile(GlobalTools.getExcelFile("uk")):
        messagebox.showerror("error",u"请将uk.xls放到和amazon.exe相同目录下")
        exit(0)

    products = []

    rb = xlrd.open_workbook(GlobalTools.getExcelFile("uk"))

    try:
        sheet = rb.sheet_by_name("asin")
        count = sheet.nrows
        for i in range(0,count):
            print sheet.cell_value(i,0)
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

    pool = multiprocessing.Pool(processes=5)

    currrow = 1
    results = []

    for product in products:
        results.append(pool.apply_async(fun,(product,currrow,sheet,wb,)))
        currrow+=1

    pool.close()
    pool.join()
    for res in results:
        try:
            print res.get()
        except:
            pass
    print "finish."

    for result in results:
        try:
            row = result.get()
            currrow = row[0]
            print "currrow:"+str(currrow)
            col = 0
            for i in range(1,len(row)):
                sheet.write(currrow, col, row[i])
                col+=1
        except:
            pass

    try:
        wb.save(GlobalTools.getExcelFile("uk"))
    except:
        messagebox.showerror("error", u"保存文件失败，运行时，请不要打开uk.xls文件")



if __name__=="__main__":
    if sys.platform.startswith('win'):
        # First define a modified version of Popen.
        class _Popen(forking.Popen):
            def __init__(self, *args, **kw):
                if hasattr(sys, 'frozen'):
                    # We have to set original _MEIPASS2 value from sys._MEIPASS
                    # to get --onefile mode working.
                    os.putenv('_MEIPASS2', sys._MEIPASS)
                try:
                    super(_Popen, self).__init__(*args, **kw)
                finally:
                    if hasattr(sys, 'frozen'):
                        # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                        # available. In those cases we cannot delete the variable
                        # but only set it to the empty string. The bootloader
                        # can handle this case.
                        if hasattr(os, 'unsetenv'):
                            os.unsetenv('_MEIPASS2')
                        else:
                            os.putenv('_MEIPASS2', '')


        # Second override 'Popen' class with our modified version.
        forking.Popen = _Popen
    multiprocessing.freeze_support()
    main()

