import  global_tools
from global_tools import GlobalTools
from bs4 import BeautifulSoup
import requests
import brotli
import traceback
import json

class CommentHandler(object):
    def __init__(self,asin,positive_count,negtive_count,debug=False):
        self.debug = debug
        self.baseurl = GlobalTools.getbaseurl()
        self.asin = asin
        self.headers = GlobalTools.getHeaders()
        # self.positiveurl = self.baseurl+"/ss/customer-reviews/ajax/reviews/get/ref=cm_cr_arp_d_viewpnt_lft"
        self.positiveurl = self.baseurl+"/hz/reviews-render/ajax/reviews/get/ref=cm_cr_arp_d_viewpnt_lft"

        self.negtive_page_count = negtive_count/4+1
        self.positivecount = positive_count
        self.negtivecount = negtive_count
        self.positivevote = 0
        self.negtivevote = 0
        self.POSITIVE_VOTE_TYPE = 0
        self.NEGTIVE_VOTE_TYPE = 1

    def getPage(self,total):
        pass

    def getUsPositiveReviewCount(self):
        return self.positivecount

    def getPositiveCommentsInfo(self):

        data = {
            "sortBy":"",
            "reviewerType":"all_reviews",
            "formatType":"",
            "filterByStar":"",
            "pageNumber":"1",
            "filterByKeyword":"",
            "shouldAppend":"undefined",
            "deviceType":"desktop",
            "reftag":"cm_cr_getr_d_paging_btm_1",
            "pageSize":self.positivecount+self.negtivecount,
            "asin":self.asin,
            "scope":"reviewsAjax1"
        }
        print("positiveurl:"+self.positiveurl)
        print("data:")
        print(data)
        self.headers['Content-Type']='application/x-www-form-urlencoded;charset=UTF-8'
        res = requests.post(self.positiveurl,headers=self.headers,data=data)
        # print("content:"
        # print(res.content
        # tmp = open("tmp2.html", "w+")
        # tmp.write(brotli.decompress(res.content))
        # tmp.close()
        #print(res.text
        # text = brotli.decompress(res.content)
        comments = res.text.split("&&&")
        commentlist = []
        tmp_positivecount = 0
        for comment in comments:
            tmp = comment.strip("\n").strip()
            #commentlist.append(eval(comment.strip("\n")))
            if tmp!="":
                tmplist = eval(tmp)
                if(tmplist[0]=="append"):
                    print("comment:")
                    html = tmplist[2]
                    if "customer_review" not in html:
                        continue
                    try:
                        html = BeautifulSoup(html ,"lxml")
                        #a = html.find("div").get("id")
                    except:
                        pass
                        # print(html
                    # helpful = html.find(attrs={"data-hook": "helpful-vote-statement"})
                    #
                    # #helpful - vote - statement
                    # if helpful:
                    #     self.handle_votes(helpful.text,self.POSITIVE_VOTE_TYPE)
                    verifiedpur = html.find(attrs={"data-hook":"avp-badge"})
                    if verifiedpur is not None:
                        verified = "YES"
                    else:
                        verified = "NO"
                    print("verified :"+verified)
                    try:
                        stars = html.find(attrs={"data-hook":"review-star-rating"}).text
                    except:
                        continue
                    stars = str(stars.split(" ")[0])
                    print("stars:"+stars)
                    reviewdate = html.find(attrs={"data-hook":"review-date"})
                    print("review date:")
                    print(reviewdate)
                    # try:
                    comment_author = html.find('a',attrs={"class":"a-profile"})
                    print(comment_author['href'])
                    print(comment_author.text)
                    user_profile_url = self.baseurl+comment_author['href']

                    print("profile date:"+user_profile_url)
                    self.get_profile_info(user_profile_url)
                        # self.get_email(user_profile_url.split("/ref=")[0]+""+"/customer_email")
                    # except:
                    #     traceback.print_exc()
        self.positivecount = tmp_positivecount
        print("in comment handler:"+str(self.positivecount))
        #print(commentlist)

    def get_profile_info(self,url):
        "https://www.amazon.co.uk/gp/profile/amzn1.account.AHTYNWDHL6M2WCVS7LOUVFXBLLFQ/ref=cm_cr_getr_d_gw_btm?ie=UTF8"
        profileid = url.split("profile/")[1].split("/ref")[0]
        url = "https://www.amazon.co.uk/profilewidget/bio/"+profileid+"?view=visitor"
        print("in get_profile_info")
        headers = GlobalTools.getHeaders()
        headers['Cookie']='s_nr=1507517187408-New; s_vnum=1939517187408%26vn%3D1; s_dslv=1507517187409; x-acbde="6gxYYwpBpG20FBChzzu9sn?hypH9MpwKF0gVmk2LOxnYWw2uE@5B3Qh7Df?gkrXM"; at-acbde=Atza|IwEBIFPo-tRvBxygSgF8Ard63lJANpi78TG-8BUTC8ScSLLiUskUDIh0VMUwG_l8fsWqij5ArfksGmp6Ks52ZiYPS0bJeoDkACAtCZF6h3ePo0yqw9jdKVsq4edrTZPfLFYYYaRsbNyD2x09klSn7jKaU8Sn56Cr4VCIx_H8LObqLF2bX6Aq0EWW-O0PoBHgkdYI9iPhMo_2OHQjWuFAeinw0dU1M7X-SWBl2wB4FtzVXlQzarbwLjsHxXSaw2LwX3ENF6oCHOh73pPPnTX68JEedEkLu-sOSL2eZ5Whe7zJ2L76yyEzyjVXQpWbDdUqUP58MdLTNLfhCM5LkwWGmd7fuoLC1u7sZhBkJSA6oLQ0Q3kua5e8x0LfI3HfLZwC6qzrDJ6pheW0my98MFK4r9JaG85Z; sess-at-acbde="d7DXrZglD8+7+42k5qmlfFUxSpHJkUg8H1Dz17ZCU+U="; x-wl-uid=1WLJUGaYF93xUQuJRK3PCgsu0IJeaJoL7J/7XRaD4Men7E4FPUEro4vxW+rjyvLb9XCGGKFNM1yrtwZ9b9BK3yXkMKCav41q6XBiaxBqGmVWG1vMYfNxoP30XR5Otq5GKr5uenX7TA98=; session-token="1o+pNqOm6F7uZWrYdtDbU26LiB8ByJ40B64c+JFwPh3lkBt1MbUn+ha6qR3BaTgduMMVK1e1LjJ6pnoF+/r3c4PUBDfax7J+AGcgt2QiXkvMdVyLjyDowIQtWUbeHi6V4hfxIhgrYGcAyZ4x4keQvPaEHOW0v8t8akQV0nmi5sj1Jzu8pn162bmTw0XLP88olTMWGCWAeJlHGsXpCvyiS1VrFGHpgj2xSW3j5jdNi8DCjE4R7E+EqR+4BNFVQs+1KUR7bf9qBMWu3xT7DDe9KQ=="; session-id-time=2082754801l; session-id=261-5557160-1959728; ubid-acbde=258-5984155-0914160; csm-hit=0CP5W9ZYZNFE06XFCV0V+b-9KE07PDF4YD27JB8DFQQ|1509967781417'
        res = requests.get(url,headers=headers)
        # html = GlobalTools.getResponseContent(res)
        # htmltxt = html.text
        # s = htmltxt.split("window.CustomerProfileRootProps")[1].split("window.PageContext")[0].replace("=","").replace(";","").strip()
        # print(s)
        # s = s.decode(encoding="utf-8")
        s = res.text
        try:
            jsonobj = json.loads(s)
        except:
            tmp = open("tmp2.html","w+")
            tmp.write(s)
            tmp.close()
            exit(1)
        # name = jsonobj["nameHeaderData"]["name"]
        # print("name:"+name)
        reviewRank = jsonobj['topReviewerInfo']['rank']
        print(reviewRank)
        # email = jsonobj['bioData']['publicEmail']
        # print("email:")
        # print(email)
        # custid = jsonobj['customerId']
        # print("custid:"+custid)
        # tmp = open("tmp2.html", "w+")
        # if res.headers['Content-Encoding'] == "br":
        #     tmp.write(brotli.decompress(self.res.content))
        # else:
        #     tmp.write(res.content)
        # tmp.close()

    def get_email(self,url):
        print("******************")
        print("url:"+url)

        headers = GlobalTools.getHeaders()
        headers['X-Requested-With']='XMLHttpRequest'
        headers['Referer']='https://www.amazon.de/gp/profile/amzn1.account.AF3BW3DYKKEHMR4HSAFIQDM62QNQ/ref=cm_cr_getr_d_pdp?ie=UTF8'
        headers['Cookie']='s_nr=1507517187408-New; s_vnum=1939517187408%26vn%3D1; s_dslv=1507517187409; x-acbde="6gxYYwpBpG20FBChzzu9sn?hypH9MpwKF0gVmk2LOxnYWw2uE@5B3Qh7Df?gkrXM"; at-acbde=Atza|IwEBIFPo-tRvBxygSgF8Ard63lJANpi78TG-8BUTC8ScSLLiUskUDIh0VMUwG_l8fsWqij5ArfksGmp6Ks52ZiYPS0bJeoDkACAtCZF6h3ePo0yqw9jdKVsq4edrTZPfLFYYYaRsbNyD2x09klSn7jKaU8Sn56Cr4VCIx_H8LObqLF2bX6Aq0EWW-O0PoBHgkdYI9iPhMo_2OHQjWuFAeinw0dU1M7X-SWBl2wB4FtzVXlQzarbwLjsHxXSaw2LwX3ENF6oCHOh73pPPnTX68JEedEkLu-sOSL2eZ5Whe7zJ2L76yyEzyjVXQpWbDdUqUP58MdLTNLfhCM5LkwWGmd7fuoLC1u7sZhBkJSA6oLQ0Q3kua5e8x0LfI3HfLZwC6qzrDJ6pheW0my98MFK4r9JaG85Z; sess-at-acbde="d7DXrZglD8+7+42k5qmlfFUxSpHJkUg8H1Dz17ZCU+U="; x-wl-uid=1WLJUGaYF93xUQuJRK3PCgsu0IJeaJoL7J/7XRaD4Men7E4FPUEro4vxW+rjyvLb9XCGGKFNM1yrtwZ9b9BK3yXkMKCav41q6XBiaxBqGmVWG1vMYfNxoP30XR5Otq5GKr5uenX7TA98=; session-token="1o+pNqOm6F7uZWrYdtDbU26LiB8ByJ40B64c+JFwPh3lkBt1MbUn+ha6qR3BaTgduMMVK1e1LjJ6pnoF+/r3c4PUBDfax7J+AGcgt2QiXkvMdVyLjyDowIQtWUbeHi6V4hfxIhgrYGcAyZ4x4keQvPaEHOW0v8t8akQV0nmi5sj1Jzu8pn162bmTw0XLP88olTMWGCWAeJlHGsXpCvyiS1VrFGHpgj2xSW3j5jdNi8DCjE4R7E+EqR+4BNFVQs+1KUR7bf9qBMWu3xT7DDe9KQ=="; session-id-time=2082754801l; session-id=261-5557160-1959728; ubid-acbde=258-5984155-0914160; csm-hit=0CP5W9ZYZNFE06XFCV0V+b-9KE07PDF4YD27JB8DFQQ|1509967781417'
        res = requests.get(url,headers)
        print(res.status_code)
        html = GlobalTools.getResponseContent(res)
        print(html)
        print("******************")
        # print(html)


    def handle_votes(self,comment,votetype):
        comment = comment.strip()

        try:
            count = (int(comment.split(" ")[0]))
        except:
            if (comment.split(" ")[0] in ["One","Eine"]):
                count = 1
            else:
                count = 0
        if (votetype == self.POSITIVE_VOTE_TYPE):
            self.positivevote+=count
        else:
            self.negtivevote+=count

    def get_positive_votes(self):
        return self.positivevote

def main():
    ch = CommentHandler("B0742DRT5S",4,3,True)
    ch.getPositiveCommentsInfo()
    print(ch.get_positive_votes())

if __name__=="__main__":
    main()