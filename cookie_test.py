import  requests

def cookie_test():
    url = "https://www.amazon.co.uk/"
    req = requests.session()
    headers = {
            "Connection":"keep-alive",
            "Pragma":"no-cache",
            "Cache-Control":"no-cache",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.8"
    }
    req.get(url,headers=headers)
    print req.cookies.get("session-id")
    req.request()
if __name__=="__main__":
    cookie_test()