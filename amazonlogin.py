#coding:utf-8
import tkinter
import requests
from global_tools import GlobalTools
import urllib
import json
from amazonframe import *

class LoginFrame():
    def __init__(self,master):
        root = master

        frame_top = Frame(width=300, height=300)
        label2 = Label(frame_top, text="欢迎使用易讯亚马逊信息获取工具")
        label2.grid(row=0)
        # titlelabel = Label(frame_top,text="asdf",image=image)
        # titlelabel.grid(row=0)
        frame_bottom = Frame(width=300,height=300)
        namelabel = Label(frame_bottom,text="用户名")
        passlebel = Label(frame_bottom, text="密码")

        self.unameentry = Entry(frame_bottom)
        self.upasyentry = Entry(frame_bottom, show="*")

        frame_top.grid(row=0, padx=2, pady=5,columnspan=2)
        frame_bottom.grid(rowspan=3, columnspan=2)

        namelabel.grid(row=1, column=0)
        passlebel.grid(row=2, column=0)
        self.unameentry.grid(row=1, column=1)
        self.upasyentry.grid(row=2, column=1)

        loginButton = Button(frame_bottom,text="登录",command=self.dologin).grid(row=3,columnspan=2)

    def dologin(self):
        uname = self.unameentry.get()
        upass = self.upasyentry.get()
        url = "http://lotfun.cn:8080/login.php"

        data = {
            "username":uname,
            "password":upass
        }


        # data2 = urllib.quote(data)
        data2 = json.dumps(data)
        payload = "username=%s&password=%s" %(uname,upass)
        headers = {
            "Connection":"keep-alive",
            "Connection":"Transfer-Encoding",
            "Host":"lotfun.cn:8080",
            "Pragma":"no-cache",
            "Content-Type":"application/x-www-form-urlencoded",
            "Cache-Control":"no-cache",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36" ,
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Cookie":"__atuvc=9%7C38%2C4%7C39%2C0%7C40%2C2%7C41; language=en-gb; currency=USD; _octo=GH1.1.1342976522.1513921130; _ga=GA1.2.1184963840.1513921130; OCSESSID=5f4e9bd0066a65ae672a3d7e5b; PHPSESSID=0627bb6b2391a09f2f49753c2863b846"
        }
        res = requests.post(url=url,headers=headers,data=payload)

        print(res.text)
        self.getMainFrame()
    def getMainFrame(self):
        root.withdraw()
        root.destroy()
        root2 = Tk()
        client = ThreadedClient(root2)
        root2.mainloop()

if __name__=="__main__":
    root=Tk()
    guilogin = LoginFrame(root)
    root.mainloop()
    # root2 = Tk()
    # client = ThreadedClient(root2)
    # root2.mainloop()
