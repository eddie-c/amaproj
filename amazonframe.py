#coding:utf-8
import tkinter, threading
import queue as oriQueue
import multiprocessing
from multiprocessing import Manager
from tkinter import *
import amazon
from ui.scrollabletext import ScrollableTextFrame
from tkinter import ttk
from global_vars import GlobalVars
import get_fba_multi
import tkinter.messagebox as messagebox
import amazon_comments
class GuiPart(object):

    def __init__(self,master,queue,endCommand):
        self.baseinfothread = None
        self.queue=queue
        self.master = master
        master.title("Amazon_TCO")
        master.geometry('800x600')
        root = master

        topframe = Frame(root)
        topframe.pack(side=TOP, padx=10, pady=10, fill=BOTH)
        Label(topframe, text=u"TCO amazon市调工具").pack(side=LEFT)

        sitechoiceframe = Frame(root)
        sitechoiceframe.pack(padx=10, pady=10, fill=BOTH)

        Label(sitechoiceframe, text=u"选择站点").pack(side=LEFT)
        siteSelected = tkinter.StringVar(root)
        siteSelected.set(u"英国")
        self.sitechoice = ttk.Combobox(sitechoiceframe, textvariable=siteSelected,values=[u"英国", u"美国", u"德国", u"法国", u"意大利", u"日本"])

        self.sites = {u"英国":"uk",u"美国":"us",u"德国":"de",u"法国":"fr",u"意大利":"it",u"日本":"jp"}
        self.sitechoice["state"] = "readonly"
        self.sitechoice.pack()

        bottomframe = Frame(root)
        bottomframe.pack(padx=10, pady=10, fill=Y)
        self.baseinfoButton = Button(bottomframe, text=u"获取商品信息", command=self.runbaseinfoThread)
        # baseinfoButton.bind('<Button-1>',getbaseinfo)
        self.baseinfoButton.pack(side=LEFT)
        self.fbaButton = Button(bottomframe, text=u"获取库存", command=self.rungetfbaThread)
        self.fbaButton.pack(fill=X)

        self.commentsButton = Button(bottomframe,text=u"获取评论信息", command=self.rungetcommentsinfo)
        self.commentsButton.pack(fill=X)
        self.outputframe = ScrollableTextFrame(root)
        self.outputframe.pack()

        # Button(master,text='Done',command=endCommand).pack()

    def getoutputframe(self):
        return self.outputframe.getTextView()

    def runbaseinfoThread(self):
        countrycode = self.sites[self.sitechoice.get()]
        print("countrycode:"+countrycode)
        target = amazon.main
        th = threading.Thread(target=target,args=(self.queue,countrycode,))
        th.start()

    def rungetfbaThread(self):
        target = get_fba_multi.main
        th = threading.Thread(target=target,args=(self.queue,))
        th.start()

    def rungetcommentsinfo(self):
        countrycode = self.sites[self.sitechoice.get()]
        target = amazon_comments.main
        th = threading.Thread(target=target,args=(self.queue,countrycode,))
        th.start()

    def processIncoming(self):
        while self.queue.qsize():
            try:
                msg=self.queue.get(0)
                if msg.startswith("ERROR:"):
                    messagebox.showerror("ERROR",msg.split("ERROR:")[1])
                # else:
                if  msg == "finish.":
                    messagebox.showinfo("Info",msg)
                self.outputframe.getTextView().insert(END,msg+"\n")
                self.outputframe.getTextView().see(END)
            except oriQueue.Empty:
                pass

class ThreadedClient():
    def __init__(self,master):
        self.master=master
        self.queue=Manager().Queue()
        # GuiPart.setmainframe(master)

        # print GuiPart.getmainframe()
        self.gui=GuiPart(master,self.queue,self.endApplication)
        # GuiPart.maingui = master
        gvars = GlobalVars(master)
        # GlobalVars.mainframe = master
        self.running=True
        # self.thread1=threading.Thread()
        # self.thread1.start()
        self.periodicCall()

    def periodicCall(self):
        self.master.after(200,self.periodicCall)
        self.gui.processIncoming()
        # if not self.running:
        #     self.master.destroy()

    # def workerThread1(self):
    #     #self.ott=Tkinter.Tk()
    #     #self.ott.mainloop()
    #     while self.running:
    #         time.sleep(rand.random()*1.5)
    #         msg=rand.random()
    #         self.queue.put(msg)
    def endApplication(self):
        self.running=False

if __name__=="__main__":
    multiprocessing.freeze_support()
    root=Tk()
    client=ThreadedClient(root)
    root.mainloop()
