from Tkinter import *

class MenuFrame(object):
    def __init__(self,master):
        self.root = master
        frame = Frame(master)
        goodsinfo_bt = Button(frame,text="商品信息获取")
        comments_bt = Button(frame,text="评论信息获取")
        shop_info_bt = Button(frame,text="店铺信息获取")
        shop_track_bt = Button(frame,text="店铺跟踪")
        new_product_bt = Button(frame,text="店铺新品追踪")
        bad_reviews_bt = Button(frame,text="差评追踪")
        report_bt = Button(frame,text="报表")

    def show(self):
        pass

    def close(self,frame):
        root = self.root
        root.destroy()