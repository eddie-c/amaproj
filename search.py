from global_tools import GlobalTools
import requests
from bs4 import BeautifulSoup
import brotli
import logging
import traceback

def get_link_by_asin(asin,baseurl):
    headers = GlobalTools.getHeaders()
    # url = baseurl+"/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="+str(asin)
    url = baseurl + "/s?k="+asin+"&ref=nb_sb_noss_2"

    print("get url:"+url)

    res = requests.get(url,headers=headers)
    #
    print("res:headers:")
    print(res.headers)
    if res.headers['Content-Encoding'] == "br":
        html = BeautifulSoup(brotli.decompress(res.content),"lxml")
        with open("searchasin.html", "w") as f:
            f.write(brotli.decompress(res.content).decode("utf-8"))
    else:
        html = BeautifulSoup(res.content,"lxml")
        with open("searchasin.html", "w") as f:
            f.write(res.content.decode("utf-8"))

    # tmp = open("tmp2.html","w")
    # if res.headers['Content-Encoding'] == "br":
    #     tmp.write(brotli.decompress(res.content))
    # else:
    #     tmp.write(res.content.decode("utf-8"))
    # tmp.close()
    #
    # link = html.find_all(class_="s-search-results")[1].find_all('a',attrs={'class':'a-text-normal'})[0]
    # link = link.get('href')
    # link = link.split("&qid")[0]
    # print("link:"+baseurl+link)
    #
    # return baseurl+link
    # return baseurl + "/dp/" + asin +"/ref=redir_mobile_desktop"
    t = html.find_all(class_="s-search-results")[1]
    productslink = t.find_all("a")
    for item in productslink:
        if "/dp/"+asin in item.get('href'):
            return baseurl+(item.get('href').split("&qid")[0])
if __name__=="__main__":
    ret = get_link_by_asin('B0742DRT5S',"http://www.amazon.co.uk")
    print(ret)