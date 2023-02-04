import mysql.connector
from tkinter import * 
from tkinter import ttk
class lbprate :
    def __init__(self):
        self.createConnection() 
        self.createOldratetable()
        self.showWindow()

    def createConnection(self):
        self.cn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "softarispos"
        )
        self.cr = self.cn.cursor()
    def createOldratetable(self):
        self.cr.execute("""
            CREATE TABLE IF NOT EXISTS `oldrate` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `oldrate` int(11) DEFAULT NULL,
            PRIMARY KEY (`id`)
            )""")
        self.cn.commit()
    def changeRate(self):
        self.cr.execute("insert into oldrate (oldrate) values (%s)",(self.newrateentry.get(),))
        self.cn.commit()
        self.cr.execute("update products set pricesell = ceiling(pricesell/%s*%s/1000.0)*1000 where category =%s",(self.oldrateentry.get(),self.newrateentry.get(),self.chosencategid.get()))
        self.cn.commit()
        self.clearEntries()
    def changeRateCategories(self):
        self.cr.execute("insert into oldrate (oldrate) values (%s)",(self.newrateentrycateg.get(),))
        self.cn.commit()
        self.cr.execute("update products set pricesell = ceiling(pricesell/%s*%s/1000.0)*1000 where 1=1",(self.oldrateentrycateg.get(),self.newrateentrycateg.get()))
        self.cn.commit()
    def clearEntrieschangeRateCategories(self):
        self.oldrateentrycateg.delete(0,END)
        self.newrateentrycateg.delete(0,END)
        self.status.pack()
    def clearEntries(self):
        self.oldrateentry.delete(0,END)
        self.newrateentry.delete(0,END)
        self.status.pack()
    def showWindow(self):
        root = Tk()
        root.title("Change Product Price USD RATE")
        width = 600 
        height= 500 
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = (sw / 2) - (width / 2)
        y = (sh / 2) - (height / 2)
        root.geometry("%dx%d+%d+%d"%(width,height,x,y))
        tab_control = ttk.Notebook(root)
        tab1 = Frame(tab_control)
        tab_control.add(tab1, text='By Categories')
        tab2 = Frame(tab_control)
        tab_control.add(tab2, text='Change All ')
        tab_control.pack( fill='both')
        self.cr.execute("select oldrate from oldrate order by id desc limit 1")
        oldstoredrate = self.cr.fetchall()
        self.oldratelbl = Label(tab1,text = f"Old Rate ",font=21)
        self.oldrateentry = Entry(tab1,font=21)
        self.oldrateentry.insert(0,oldstoredrate)
        self.newratelbl = Label(tab1,text = f"New Rate ",font=21)
        self.newrateentry = Entry(tab1,font=21)
        changebtn  = Button(tab1,text = "Change Prices",command=self.changeRate)
        self.status = Label(tab1,text = "Change Success",fg="green")
        lbl = Label(tab1,text = "Choose Category to Change Rate")
        lbl.pack()
        container = Frame(tab1)
        canvas = Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )  
        canvas.create_window((200, 0), window=scrollable_frame, anchor="center")
        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        labelfr = LabelFrame(scrollable_frame,text = "Categories")
        labelfr.pack()
        self.cr.execute("select * from categories")
        self.chosencategid = StringVar("")
        self.chosencategid.set("test")
        for x in self.cr.fetchall():
            rd = Radiobutton(labelfr,text= f"{x[1]}",variable=self.chosencategid,value=x[0])
            rd.pack(anchor="w")
        self.oldratelbl.pack()
        self.oldrateentry.pack()
        self.newratelbl.pack()
        self.newrateentry.pack()
        changebtn.pack()
        ## Tab Two widgets
        self.cr.execute("select oldrate from oldrate order by id desc limit 1")
        oldstoredrate = self.cr.fetchall()
        self.oldratelblcateg = Label(tab2,text = f"Old Rate ",font=21)
        self.oldrateentrycateg = Entry(tab2,font=21)
        self.oldrateentrycateg.insert(0,oldstoredrate)
        self.newratelblcateg = Label(tab2,text = f"New Rate ",font=21)
        self.newrateentrycateg = Entry(tab2,font=21)
        changebtn  = Button(tab2,text = "Change Prices",command=self.changeRateCategories)
        self.status = Label(tab2,text = "Change Success",fg="green")
        self.oldratelblcateg.pack()
        self.oldrateentrycateg.pack()
        self.newratelblcateg.pack()
        self.newrateentrycateg.pack()
        changebtn.pack()




        root.mainloop()

if __name__ == "__main__":
    app = lbprate()