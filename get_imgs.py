import requests
from bs4 import BeautifulSoup
from global_tools import GlobalTools
class ImgHandelr(object):
    def __init__(self,asin):
        self.asin = asin

    def get_product_images(self):
        for img in self.imgurls:
            res = requests.get(img,headers=GlobalTools.getHeaders())
            filename = self.asin+"_"+self.url.split("/")[-1]
            with(open(filename,"wb")) as f:
                f.write(res.content)
            f.close()

    def get_imgs_by_asin(self,asin):
        pass

    def get_imgs_by_product_url(self,url):
        res = requests.get(url)
        html = GlobalTools.getResponseContent(res)
        html.find(id="main-image-container").find("ul")

    def get_img_by_url(self,imgurl):
        pass

    def get_imgs_by_urls(self,imgurls):
        for url in imgurls:
            self.get_img_by_url(url)

def main():
    imghandler = ImgHandelr("")
if __name__=="__main__":
    main()
