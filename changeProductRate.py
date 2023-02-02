import mysql.connector
from tkinter import * 
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
        self.cr.execute("update products set pricesell = ceiling(pricesell/%s*%s/1000.0)*1000 where 1=1",(self.oldrateentry.get(),self.newrateentry.get()))
        self.cn.commit()
        self.clearEntries()
    def clearEntries(self):
        self.oldrateentry.delete(0,END)
        self.newrateentry.delete(0,END)
        self.status.pack()
    def showWindow(self):
        root = Tk()
        root.title("Change Product Price USD RATE")
        width = 300 
        height= 200 
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = (sw / 2) - (width / 2)
        y = (sh / 2) - (height / 2)
        root.geometry("%dx%d+%d+%d"%(width,height,x,y))
        self.cr.execute("select oldrate from oldrate order by id desc limit 1")
        oldstoredrate = self.cr.fetchall()
        self.oldratelbl = Label(root,text = f"Old Rate ",font=21)
        self.oldrateentry = Entry(root,font=21)
        self.oldrateentry.insert(0,oldstoredrate)
        self.newratelbl = Label(root,text = f"New Rate ",font=21)
        self.newrateentry = Entry(root,font=21)
        changebtn  = Button(root,text = "Change Prices",command=self.changeRate)
        self.status = Label(root,text = "Change Success",fg="green")
        self.oldratelbl.pack()
        self.oldrateentry.pack()
        self.newratelbl.pack()
        self.newrateentry.pack()
        changebtn.pack()

        root.mainloop()

if __name__ == "__main__":
    app = lbprate()