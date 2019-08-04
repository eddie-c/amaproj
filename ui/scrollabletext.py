#coding:utf-8
import tkinter as Tkinter

class ScrollableTextFrame(Tkinter.Frame):
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)
        # self.grid(row=0, column=0, sticky="nsew")
        self.createFrame()

    def getTextView(self):
        return self.textview

    def createFrame(self):
        label_frame_top = Tkinter.LabelFrame(self)
        # label_frame_top.pack()

        label_frame_center = Tkinter.LabelFrame(self)
        label_frame_center.pack(fill="x")

        lfc_field_1 = Tkinter.LabelFrame(label_frame_center)
        lfc_field_1.pack(fill="x")

        # self.lfc_field_1_l = Tkinter.Label(lfc_field_1, text="文件路径：", width=10)
        # self.lfc_field_1_l.pack(fill="y", expand=0, side=Tkinter.LEFT)

        self.lfc_field_1_b = Tkinter.Button(lfc_field_1, text="清除：", width=10, height=1, command=self.clearText)
        self.lfc_field_1_b.pack(fill="none", expand=0, side=Tkinter.RIGHT, anchor=Tkinter.SE)

        ##########文本框与滚动条
        self.lfc_field_1_t_sv = Tkinter.Scrollbar(lfc_field_1, orient=Tkinter.VERTICAL)  # 文本框-竖向滚动条
        # self.lfc_field_1_t_sh = Tkinter.Scrollbar(lfc_field_1, orient=Tkinter.HORIZONTAL)  # 文本框-横向滚动条

        # self.textview = Tkinter.Text(lfc_field_1, height=15, yscrollcommand=self.lfc_field_1_t_sv.set,
        #                              xscrollcommand=self.lfc_field_1_t_sh.set, wrap='none')  # 设置滚动条-不换行
        # 滚动事件
        self.textview = Tkinter.Text(lfc_field_1, height=15, yscrollcommand=self.lfc_field_1_t_sv.set)
        self.lfc_field_1_t_sv.config(command=self.textview.yview)
        # self.lfc_field_1_t_sh.config(command=self.textview.xview)

        # 布局
        self.lfc_field_1_t_sv.pack(fill="y", expand=0, side=Tkinter.RIGHT, anchor=Tkinter.N)
        # self.lfc_field_1_t_sh.pack(fill="x", expand=0, side=Tkinter.BOTTOM, anchor=Tkinter.N)
        self.textview.pack(fill="x", expand=1, side=Tkinter.LEFT)

        # 绑定事件
        self.textview.bind("<Control-Key-a>", self.selectText)
        self.textview.bind("<Control-Key-A>", self.selectText)

        ##########文本框与滚动条end



        label_frame_bottom = Tkinter.LabelFrame(self)
        # label_frame_bottom.pack()

        pass

        # 文本全选

    def selectText(self, event):
        self.textview.tag_add(Tkinter.SEL, "1.0", Tkinter.END)
        # self.lfc_field_1_t.mark_set(Tkinter.INSERT, "1.0")
        # self.lfc_field_1_t.see(Tkinter.INSERT)
        return 'break'  # 为什么要return 'break'

    # 文本清空
    def clearText(self):
        self.textview.delete(0.0, Tkinter.END)