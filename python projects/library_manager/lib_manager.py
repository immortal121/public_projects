from tkinter import *
from tkinter import ttk,messagebox
from ttkwidgets.autocomplete import AutocompleteEntry
from PIL import ImageTk, Image
import sqlite3
import os
import ssl
import smtplib
from email.message import EmailMessage 
from datetime import datetime, timedelta
# our class
file = "C:\\Users\\Rohith\\OneDrive\\Documents\\python_projects\\library_manager\\libdata.db"
# file2 = "libdata.db"
# conn = sqlite3.connect(file2)
licensetext = 'readme.txt'


############## Mail ######################
Hostmail = "iamyrohith@gmail.com"
Hostpassword = "qgdelibaicrtxrvu"
# Hostmail = "iamyrohith@gmail.com"
# Hostpassword = "qgdelibaicrtxrvu"
#CREATING CURSOR
# cursor = conn.cursor()
def sent_mail(mail,subject,body):
    if Hostmail != '' and Hostpassword != '':
        hemail = Hostmail
        hpassword = Hostpassword
        em = EmailMessage()
        em['From'] = hemail
        em['To'] = mail
        em['Subject'] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(hemail,hpassword)
            smtp.sendmail(hemail,mail,em.as_string())
    else:
        popup('Error','set Mail first')

def popup(var1,var,*data):
    if data == '':
        messagebox.showerror(var1,var)
    else:
        messagebox.showinfo(var1,var)
def start():
    try: 
        file_Found = os.path.exists(file)
        if file_Found == False:
            global cursor
            global conn
            file2 = "C:\\Users\\Rohith\\OneDrive\\Documents\\python_projects\\library_manager\\libdata.db"
            # file2 = "libdata.db"
            conn = sqlite3.connect(file2)
            licensetext = 'readme.txt'
            #CREATING CURSOR
            cursor = conn.cursor()
            
            # Creating tables
            student_table = """ CREATE TABLE STUDENTS (
            EMAIL VARCHAR(255) UNIQUE NOT NULL,
            TOTAL_NAME CHAR(50) NOT NULL,
            PHONE_NO CHAR(25),
            PIN VARCHAR(20) NOT NULL,
            CREATED_DATE  timestamp,
            DETAILS TEXT
            ); """
            Books_table = """
            CREATE TABLE BOOKS (
                BOOK_SNO VARCHAR(50) UNIQUE NOT NULL,
                BOOK_NAME VARCHAR(200) NOT NULL,
                AUTHOR VARCHAR(200) ,
                BRANCH VARCHAR(200),
                BOOK_QUANTITY INT,
                BOOK_PRICE INT,
                TAKEN_DATE  timestamp
            );
            """
            Books_Status_table = """
            CREATE TABLE BOOK_STATUS (
            BOOK_REFNO INT NOT NULL,
                BOOK_NAME VARCHAR(200) NOT NULL,
                STUDENT_NAME VARCHAR(200) NOT NULL,
                STUDENT_PIN VARCHAR(200) NOT NULL,
                updated_time timestamp
            );
            """
            cursor.execute(student_table)
            cursor.execute(Books_table)
            cursor.execute(Books_Status_table)
            conn.commit()
            
            print('created')
        else:
            file2 = "C:\\Users\\Rohith\\OneDrive\\Documents\\python_projects\\library_manager\\libdata.db"
            # file2 = "libdata.db"
            conn = sqlite3.connect(file2)
            licensetext = 'readme.txt'
            #CREATING CURSOR
            cursor = conn.cursor()

    except:
        print("Database Sqlite3.db not formed.")


class Book_Manager:
    # book_name = book_sno = auther = price = quantity = branch_name = book_branch = None

    def Add_book_lib(book_sno,book_name,auther,branch,quantity,price,timestamp):
        sql2 = """
        INSERT INTO BOOKS (BOOK_SNO, BOOK_NAME, AUTHOR,BRANCH,BOOK_QUANTITY,BOOK_PRICE,TAKEN_DATE) VALUES (?,?,?,?,?,?,?);
        """
        cursor.execute(sql2,(book_sno,book_name,auther,branch,quantity,price,timestamp))
        conn.commit()
    def delete_book_lib():
        pass

    def update_book_lib():
        pass

    def check_availabe_lib(quantity,id):
        # print(quantity)
        # print(id)
        # try:
        # sql12 = "SELECT * FROM BOOK_STATUS WHERE BOOK_REFNO = '{}' ;".format(id)
        # cursor.execute(sql12)
        # print(len(cursor.fetchall()))
        # quantity = quantity - len(cursor.fetchall())
        #     print(quantity)
        # except:
        #     quantity
        #     pass
        if quantity > 0:
            return 'Available'
        else:
            return 'UnAvailable'


class Student_Manger:

    def Add_student(email,name,phone,pin,created,details):
        email = str(email)
        name = str(name)
        phone = str(phone)
        pin = str(pin)
        created = str(created)
        details = str(details)
        sql = """
        INSERT INTO STUDENTS (EMAIL, TOTAL_NAME, PHONE_NO,PIN,CREATED_DATE,DETAILS) VALUES ( ?, ?, ?,?,?,?);
        
        """
        cursor.execute(sql,(email,name,phone,pin,created,details))
        conn.commit()

    def delete_student(email):
        sql = "DELETE from STUDENTS WHERE EMAIL = '{}'".format(email)
        cursor.execute(sql)

    # def update_student():
    #     sql = "UPDATE STUDENTS SET column1 = value1, column2 = value2 WHERE condition"
        


class Transcation_Manager:
    def Add_student_book(self,bookname,booksno,stdname,stdpin):
        sql1 = "SELECT * FROM BOOKS WHERE BOOK_SNO = '{}'".format(booksno)
        data1 = cursor.execute(sql1)
        lis = []
        for d in data1:
            lis.append(d[4])
        sql2 = "select * from STUDENTS where PIN = '{}' ".format(stdpin)
        data2 = cursor.execute(sql2)
        email = []
        for f in data2:
            email.append(f[0])
        email = email[0]
        
        sql = "SELECT * FROM BOOK_STATUS WHERE BOOK_REFNO = '{}'".format(booksno)
        data =cursor.execute(sql)
        ls = []
        for d in data:
            ls.append(d[2])
        if(len(ls) >= lis[0]):
            popup('BOOK ALREADY TAKEN ERROR','BOOK ALREADY TAKEN BY'+str(ls))
        else:
            popup('SUCCESSFULLY TAKEN','BOOK TAKEN LIMIT START TODAY')
            sql2 = """
            INSERT INTO BOOK_STATUS (BOOK_REFNO,BOOK_NAME,STUDENT_NAME,STUDENT_PIN,updated_time) VALUES ( ?, ?, ?,?,?);

            """

            cursor.execute(sql2,(booksno,bookname,stdname,stdpin,datetime.now()))
            
            conn.commit()
            sent_mail(email,"BOOK TAKEN","THANKS FOR TAKEING BOOK \nFROM LIBRARY LIMIT IS FOR\n'{}' today ".format(stdname))
            
        

    def Delete_student_book(self,booksno,stdpin):
        try:
            sql2 = "select * from STUDENTS where PIN = '{}' ".format(stdpin)
            data2 = cursor.execute(sql2)
            email = []
            for f in data2:
                email.append(f[0])
            email = email[0]
            sql1 = "SELECT * FROM BOOK_STATUS  WHERE STUDENT_PIN = '{}'AND BOOK_REFNO = '{}' ORDER BY updated_time LIMIT 1".format(stdpin,booksno)
            data = cursor.execute(sql1)
            
            list = []
            for d in data:
                list.append(d[4])
            if list[0] is not None:
                sql = "DELETE FROM BOOK_STATUS WHERE STUDENT_PIN = '{}'AND updated_time = '{}' ".format(stdpin,list[0])
            else:
                sql = "DELETE FROM BOOK_STATUS WHERE STUDENT_PIN = '{}'AND BOOK_REFNO = '{}' ".format(stdpin,booksno)
            cursor.execute(sql)
            popup('SUCCESSFULLY RETURNED ','BOOK RETURNED SUCCESSFULLY')
            conn.commit()
            body = """
            THANKS FOR RETURNING BOOK \nFROM LIBRARY SEE YOU SOON\n PIN :{}
            """.format(stdpin)
            sent_mail(email,"BOOK RETURNED",body)
          
        except:
            popup('BOOK IS NOT TAKEN AND NOT RETURNED ','BOOK IS NOT REGISTERED IN TAKEN LIST')

    def total_fee(self,booksno,stdpin):
        try:
            sql1 = "SELECT * FROM BOOK_STATUS  WHERE STUDENT_PIN = '{}'AND BOOK_REFNO = '{}' ORDER BY updated_time LIMIT 1".format(stdpin,booksno)
            data = cursor.execute(sql1)
            list = []
            for d in data:
                list.append(d[4])
            l = list[0]
            l = l[:10]
            format = '%Y-%m-%d'
            d = datetime.strptime(l,format)
                   
            # print(l) gives after date
            delta = d - datetime.now()
            difference = delta.days
            difference = difference+1
            # print(f'Difference is {difference} days')
            output = []
            if(difference <= 15):
                output = 'NO FEE'
            else:
                global perdayfee
                if (perdayfee in None):
                    perdayfee = 0
                
                fee = difference-15
                output = fee + perdayfee
            return output

            
        except:
            print('date exception in total fee' )
            
# class settings:
#     def start_on_boot():
#         pass
#     def login():
#         pass

#     def reset_password():
#         pass

#     def reset_username():
#         pass







def set_email(self,mail,password):
    Hostmail = mail
    Hostpassword = password
    popup('Success','Mail setup performed')
def backup():
        
    from pydrive.drive import GoogleDrive
    from pydrive.auth import GoogleAuth
    gauth = GoogleAuth()

    # Creates local webserver and auto
    # handles authentication.
    gauth.LocalWebserverAuth() 
    # auth_url = gauth.GetAuthUrl()   

    drive = GoogleDrive(gauth)
    try:
        # path = r"C:/Users/Rohith/OneDrive/Documents/python_projects/library_manager/libdata.db" 
        f = drive.CreateFile({'title':'libdata.db'})
        f.SetContentFile('libdata.db')
        f.Upload()
        abc = f['id']
        with open('libid.txt','w') as f:
            f.writelines(abc)
        popup('BACKUP','BACK UP SUCCESSFULL KEP LIBID.TXT FILE SAFE !!!!!!')
    except:
        popup('Error','Exception in RESTORE CONTACT DEVELOPER')

        

def restore():
    # f.Delete()
    from pydrive.drive import GoogleDrive
    from pydrive.auth import GoogleAuth
    gauth = GoogleAuth()

    # Creates local webserver and auto
    # handles authentication.
    gauth.LocalWebserverAuth() 
    # auth_url = gauth.GetAuthUrl()   
    try:
        drive = GoogleDrive(gauth)
        with open('libid.txt','r') as f:
            variable = f.read()
        f = drive.CreateFile({'id':variable})
        f.GetContentFile('libdata.db')
    except:
        popup('Error','Exception in RESTORE CONTACT DEVELOPER')
    # path = r"C:/Users/Rohith/OneDrive/Documents/python_projects/library_manager/libdata.db" 



def dele(arg):
    arg.destroy()

books_obj = Book_Manager#objective of book
def toggle_win():
    f1 = Frame(root, width=300, height=1000, bg='#12c4c0')
    f1.place(x=0, y=0)

    # buttons
    def bttn(x, y, text, bcolor, fcolor, cmd):

        def on_entera(e):
            myButton1['background'] = bcolor  # ffcc66
            myButton1['foreground'] = '#262626'  # 000d33

        def on_leavea(e):
            myButton1['background'] = fcolor
            myButton1['foreground'] = '#262626'

        myButton1 = Button(f1, text=text,
                           width=42,
                           height=2,
                           fg='#262626',
                           border=0,
                           bg=fcolor,
                           activeforeground='#262626',
                           activebackground=bcolor,
                           command=cmd)

        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x, y=y)

    bttn(0, 80, 'D A S H B O A R D', '#0f9d9a', '#12c4c0',
         lambda: screen_frame(60, 0, '#12c4c0', f1, 'dashboard'))
    bttn(0, 117, 'S T U D E N T', '#0f9d9a', '#12c4c0',
         lambda: screen_frame(60, 0, '#12c4c0', f1, 'student'))
    bttn(0, 154, 'B O O K S', '#0f9d9a', '#12c4c0',
         lambda: screen_frame(60, 0, '#12c4c0', f1, 'books'))
    bttn(0, 191, 'S E T T I N G S', '#0f9d9a', '#12c4c0',
         lambda: screen_frame(60, 0, '#12c4c0', f1, 'settings'))
    bttn(0, 261, 'A B O U T', '#0f9d9a', '#12c4c0',
         lambda: screen_frame(60, 0, '#12c4c0', f1, 'about'))

    global img2
    img2 = ImageTk.PhotoImage(Image.open("close.png"))

    Button(f1, image=img2, border=0, command=lambda: dele(f1),
           bg='#12c4c0', activebackground='#12c4c0').place(x=5, y=10)


def screen_frame(x, y, bg, frame, arg):
    try:
        dele(frame)
    except:
        # print(_ExceptionWithTraceback)
        # print('here exception')
        pass
    frame = Frame(root, width=width, height=height, bg=bg)
    frame.place(x=x, y=y)
    if arg == 'student':
        t = Transcation_Manager()
        # t.total_fee('bb114','20105-cm-013')
        dash_frame = Frame(frame, width=width, height=60, bg='#FFFFFF')
        dash_frame.grid()
        dash_frame1 = Frame(frame, width=width,
                            height=height, pady=10,padx=20, bg='#FFFFFF')
        dash_frame1.grid()
        # dash_frame2 = Frame(frame, width=width, height=height, bg='#FFFFFF')
        # dash_frame2.grid()
        Label(dash_frame, text='S T U D E N T ', font='25',
              bd=6, padx=3, pady=4, bg='#12c4c0').grid()
        # Create an instance of ttk
        style = ttk.Style()

        # Define Style for Notebook widget
        style.layout("Tab", [('Notebook.tab', {'sticky': 'nswe', 'children':
                                               [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                                                                      [('Notebook.label', {
                                                                        'side': 'top', 'sticky': ''})],
                                                                      })],
                                               })]
                     )

        # Use the Defined Style to remove the dashed line from Tabs
        style.configure("Tab", focuscolor=style.configure(".")
                        ["background"], padding=10, width=70)

        tabControl = ttk.Notebook(dash_frame1,)
        tab1 = Frame(tabControl, bg='#3C4048')
        tab2 = Frame(tabControl, bg='#3C4048')
        tab3 = Frame(tabControl, bg='#3C4048')
        # TAKE STUDENT BOOK
        tabControl.add(tab1, text='TAKE BOOK')
        # AND RETURN BOOK
        tabControl.add(tab2, text='RETURN BOOK')
        # STUDENT ADD

        tabControl.add(tab3, text='ADD STUDENT')
        #transactions
        studentvar = StringVar()
        studentpinvar = StringVar()
        booksno = StringVar()
        bookname = StringVar()
        estudentvar = StringVar()
        estudentpinvar = StringVar()
        ebooksno = StringVar()
        ebookname = StringVar()
        feeblock = StringVar()
        searchvar = StringVar()
        esearchvar = StringVar()
         # Adding combobox drop down list
        
        data = cursor.execute('SELECT * FROM STUDENTS;')
        
        lst = []
        for d in data:
            lst.append(d[3])
        dataa = cursor.execute('SELECT * FROM BOOKS;')
        slst = []
        for daa in dataa:
            slst.append(daa[0])
        
        def search(e):
            data = searchvar.get()
            # treeclear
            if data != '':
                for record in tree.get_children():
                    tree.delete(record)
                sql = "SELECT * FROM BOOKS WHERE BOOK_NAME like '%{}%'".format(data)
                # sql = "SELECT * FROM BOOKS WHERE BOOK_NAME LIKE '{}'".format(data)
                fetched = cursor.execute(sql)
                i = 1
                
                for d in fetched:
                    if d == '':
                        print('hello')
                        tree.insert("",'end',values = (i,d[0],d[1],'**','no','records ','are ' ,'there'))
                        break
                    else:
                        tree.insert("",'end',values = (i,d[0],d[1],d[2],d[3],d[4],d[5],books_obj.check_availabe_lib(d[4],d[0]))) 
                        i = i+1
              
                
            else:
                update_book()
        def esearch(e):
            data = esearchvar.get()
            # tre
            if data != "":
                for record in treee.get_children():
                    treee.delete(record)
              
                sql = "SELECT * FROM BOOK_STATUS WHERE BOOK_NAME LIKE '%{}%'".format(data)
                dataa = cursor.execute(sql)

                i = 1
              
                for d in dataa:                    
                   treee.insert("",'end',values = (i,d[0],d[1],d[2],d[3])) 
                   i = i+1
                   if d is None:
                        treee.insert("",'end',values = ('**','no','records ','are','there'))

            else:
                eupdate_book()
                       
            
        def clear():
                sudentpinentry.delete(0,END)
                ent.delete(0,END)
                booksnoentry.delete(0,END)
                booknameentry.delete(0,END)
        def eclear():
                esudentpinentry.delete(0,END)
                eent.delete(0,END)
                ebooksnoentry.delete(0,END)
                ebooknameentry.delete(0,END)
                fee.delete(0,END)
        def enterstudent():
            studentpin = studentpinvar.get().lower()
            studne = studentvar.get().lower()
            bookn = bookname.get().lower()
            books = booksno.get().lower()
            if(studentpin == ''):
                popup('validation error','STUDENT PIN MUST BE FILLED')
        
            elif(studne == ''):
                popup('validation error','STUDENT NAME MUST BE FILLED')

            elif(bookn == ''):
                popup('validation error','BOOK NAME MUST BE FILLED')

            elif(books == ''):
                popup('validation error','BOOKSNO MUST BE FILLED')
            else:
                clear()
                transcation = Transcation_Manager()
                transcation.Add_student_book(bookn,books,studne,studentpin)
                
            

        def removestudent():
            booksno = ebooksno.get()
            studentpin = estudentpinvar.get()
            fee = feeblock.get()
            if(booksno == ''):
                popup('validation error','STUDENT PIN MUST BE FILLED')
            elif(studentpin == ''):
                popup('validation error','STUDENT NAME MUST BE FILLED')
            elif(fee == 'None'):
                popup('validation error', 'This book is not registered')
            else:
                if(fee == 'NO FEE'):         
                    eclear()
                    transcation = Transcation_Manager()
                    transcation.Delete_student_book(booksno,studentpin)
                    
                else:
                    f = messagebox.askyesno("IS YOU PAID","ARE YOU PAID FEE ,FEE AMOUNT" + fee )
                    if(f):
                        eclear()
                        transcation = Transcation_Manager()
                        transcation.Delete_student_book(booksno,studentpin)
                        
                    else:
                        messagebox.showwarning('PAY FEE','PLEASE FEE')

        def filldatastudent(event):
            data = studentpinvar.get()
            data.lower()
            dat = cursor.execute("SELECT * FROM STUDENTS WHERE PIN = '{}'".format(data))
            for da in dat:
                studentvar.set(da[1])
                break
        def efilldatastudent(event):
      
            data = estudentpinvar.get()
            data.lower()
            dat = cursor.execute("SELECT * FROM STUDENTS WHERE PIN = '{}'".format(data))
            for da in dat:
                estudentvar.set(da[1])
                break
        def fillbook(event):
            data = booksno.get()
            data = data.lower()
            dat = cursor.execute("SELECT * FROM BOOKS WHERE BOOK_SNO = '{}'".format(data))
            for da in dat:
                bookname.set(da[1])
                break
        def efillbook(event):
            data = ebooksno.get()
            pin = estudentpinvar.get().lower()
            statu = ''
            def fee():
                t = Transcation_Manager()
                feee = t.total_fee(data,pin)
                feeblock.set(feee)
            if(pin == ''):
                statu = 'not'
                popup('validation error','STUDENT PIN MUST FILL MUST BE FILLED FIRST')
            if statu != 'not':
                data = data.lower()
                dat = cursor.execute("SELECT * FROM BOOKS WHERE BOOK_SNO = '{}'".format(data))
                
                for da in dat:
                    ebookname.set(da[1])
                    fee()
                
        ################# take book ##########
        Label(tab1,text='PIN NO',font="27",width=25, bg='#12c4c0').grid(row=1,column=2,padx=10,pady=10)
        sudentpinentry = AutocompleteEntry(tab1,width=30,font=27,completevalues=lst,textvariable=studentpinvar)
        sudentpinentry.grid(row=1,column=3,padx=10,pady=10)
        Label(tab1,text='STUDENT NAME',font="27",width=25, bg='#12c4c0').grid(row=2,column=2,padx=10,pady=10)
        ent=Entry(tab1,textvariable=studentvar,width=30,font=30,border=2)
        ent.grid(row=2,column=3,padx=10,pady=10)
     
        Label(tab1,text='BOOK SNO',font="27",width=25, bg='#12c4c0').grid(row=3,column=2,padx=10,pady=10)
        # booksnoentry =Entry(tab1,textvariable=booksno,width=30,font=30,border=2)
        booksnoentry = AutocompleteEntry(tab1,width=30,font=27,completevalues=slst,textvariable=booksno)
       
        booksnoentry.grid(row=3,column=3,padx=10,pady=10)
        Label(tab1,text='BOOK NAME',font="27",width=25, bg='#12c4c0').grid(row=4,column=2,padx=10,pady=10)
        booknameentry =Entry(tab1,textvariable=bookname,width=30,font=30,border=2)
        booknameentry.grid(row=4,column=3,padx=10,pady=10)
        Button(tab1,text="A D D  B O O K",font='27',command=enterstudent).grid(row=5,column=2,columnspan=2,padx=20,pady=10)
        sudentpinentry.bind('<Return>',filldatastudent)
        booksnoentry.bind('<Return>',fillbook)
        searchentry = Entry(tab1,textvariable=searchvar,width=30,font=30,border=2)
        searchentry.grid(row=6,column=2,padx=10,pady=10)
        searchentry.bind('<KeyRelease>',search)
        #return book#########################
        #*******this is return block
        
        Label(tab2,text='PIN NO',font="27",width=25, bg='#12c4c0').grid(row=1,column=2,padx=10,pady=10)
        esudentpinentry = AutocompleteEntry(tab2,width=30,font=27,completevalues=lst,textvariable=estudentpinvar)
        esudentpinentry.grid(row=1,column=3,padx=10,pady=10)
        Label(tab2,text='STUDENT NAME',font="27",width=25, bg='#12c4c0').grid(row=2,column=2,padx=120,pady=10)
        eent=Entry(tab2,textvariable=estudentvar,width=30,font=30,border=2)
        eent.grid(row=2,column=3,padx=10,pady=10)     
        Label(tab2,text='BOOK SNO',font="27",width=25, bg='#12c4c0').grid(row=3,column=2,padx=10,pady=10)
        ebooksnoentry = AutocompleteEntry(tab2,width=30,font=27,completevalues=slst,textvariable=ebooksno)
        ebooksnoentry.grid(row=3,column=3,padx=10,pady=10)
        Label(tab2,text='BOOK NAME',font="27",width=25, bg='#12c4c0').grid(row=4,column=2,padx=10,pady=10)
        ebooknameentry =Entry(tab2,textvariable=ebookname,width=30,font=30,border=2)
        ebooknameentry.grid(row=4,column=3,padx=10,pady=10)
        Label(tab2,text='FEE STATUS',font="27",width=25, bg='#12c4c0').grid(row=5,column=2,padx=10,pady=10)
        fee =Entry(tab2,textvariable=feeblock,width=30,font=30,border=2)
        fee.grid(row=5,column=3,padx=10,pady=10)
        Button(tab2,text="R E T U R N  B O O K",command=removestudent,font='30',width=30,padx=20).grid(row=6,column=2,columnspan=2,padx=7,pady=20)
        esudentpinentry.bind('<Return>',efilldatastudent)
        ebooksnoentry.bind('<Return>',efillbook)
        esearchentry = Entry(tab2,textvariable=esearchvar,width=30,font=30,border=2)
        esearchentry.grid(row=7,column=2,padx=10,pady=10)
        esearchentry.bind('<KeyRelease>',esearch)
        ###############################################################
        def update_book():
            global tree
            tree = ttk.Treeview(tab1,selectmode='browse')
            tree.grid(row=7,rowspan=15,column=1,columnspan=5,padx=15,sticky='nw')
            verscrlbar = ttk.Scrollbar(tab1,
                               orient ="vertical",command=tree.yview)
            verscrlbar.grid(row=9,rowspan=15,column=0)
            # Configuring treeview
            tree.configure(xscrollcommand = verscrlbar.set)
            
            # Defining number of columns
            tree["columns"] = ("1", "2", "3","4","5",'6','7','8')
    
            # Defining heading
            tree['show'] = 'headings'
            # Assigning the width and anchor to  the
            # respective columns
            tree.column("1", width = 52, anchor ='c')
            tree.column("2", width = 200, anchor ='c')
            tree.column("3", width = 200, anchor ='c')
            tree.column("4", width = 200, anchor ='c')
            tree.column("5", width = 160, anchor ='c')
            tree.column("6", width = 150, anchor ='c')
            tree.column("7", width = 150, anchor ='c')
            tree.column("8", width = 150, anchor ='c')
    
            # Asigning the heading names to the
            # repective columns
            tree.heading("1", text ="S NO",)
            tree.heading("2", text ="BOOK SERIAL NO",)
            tree.heading("3", text ="BOOK NAME")
            tree.heading("4", text ="AUTHOR")
            tree.heading("5", text ="BRANCH")
            tree.heading("6", text ="QUANTITY")
            tree.heading("7", text ="PRICE")
            tree.heading("8", text ="STATUS")
        
            i = 1
            data = cursor.execute('SELECT * FROM BOOKS ORDER BY TAKEN_DATE DESC LIMIT 0,30 ;')
            for d in data:
                tree.insert("",'end',values = (i,d[0],d[1],d[2],d[3],d[4],d[5],books_obj.check_availabe_lib(d[4],d[0]))) 
                i = i+1
        update_book()
        def eupdate_book():
            global treee
            treee = ttk.Treeview(tab2,selectmode='browse')
            treee.grid(row=8,rowspan=15,column=1,columnspan=5,padx=15,sticky='nw')
            verscrlbar = ttk.Scrollbar(tab2,
                               orient ="vertical",command=tree.yview)
            verscrlbar.grid(row=10,rowspan=15,column=0)
            # Configuring treeview
            treee.configure(xscrollcommand = verscrlbar.set)
            
            # Defining number of columns
            treee["columns"] = ("1", "2", "3","4","5")
    
            # Defining heading
            treee['show'] = 'headings'
            # Assigning the width and anchor to  the
            # respective columns
            treee.column("1", width = 150, anchor ='c')
            treee.column("2", width = 250, anchor ='c')
            treee.column("3", width = 300, anchor ='c')
            treee.column("4", width = 300, anchor ='c')
            treee.column("5", width = 250, anchor ='c')
    
    
            # Asigning the heading names to the
            # repective columns
            treee.heading("1", text ="S NO",)
            treee.heading("2", text ="BOOK SERIAL NO",)
            treee.heading("3", text ="BOOK NAME")
            treee.heading("4", text ="BOOK TAKEN BY ")
            treee.heading("5", text ="PIN")
          
        
            i = 1
            data = cursor.execute('SELECT * FROM BOOK_STATUS ORDER BY updated_time DESC LIMIT 0,30 ;')
            for d in data:
                treee.insert("",'end',values = (i,d[0],d[1],d[2],d[3])) 
                i = i+1
        eupdate_book()
        #control function
        def student():
            email = emailvar.get()
            email = email.lower()
            name = namevar.get() 
            phone = phonevar.get()
            pinno = pin.get()
            detail = details.get()
            error = ''
            def clear():
                emailentry.delete(0,END)
                nameentry.delete(0,END)
                phoneentry.delete(0,END)
                pinentry.delete(0,END)
                detailsvar.delete(0,END)
            if email == '':
                popup('validation error','email must be filled')
                error = 'error'
            if email != '' and pinno != '':
                sql = """
                SELECT * FROM STUDENTS WHERE EMAIL = ? OR PIN = ?
                """
                abc = cursor.execute(sql,(email,pinno))
                for a in abc:
                    if a[1] != '':
                        popup('validation error',a[0]+' email already taken')
                        popup('validation error',a[3]+' Pin already taken')
                        error = 'error'
                    else:
                        break

            if name == '':
                popup('validation error','Name must be filled')
                error = 'error'
            if phone == '':
                popup('validation error','phone must be filled')
                error = 'error'
            if pinno == '':
                popup('validation error','pin  must be filled')
                error = 'error'
            if detail == '':
                popup('validation error',"details must be filled")
                error = 'error'
            if error == '':
                student_obj = Student_Manger
                student_obj.Add_student(email,name,phone,pinno,datetime.now(),detail)
                popup('Sucess','Student added successfully','info')
                update()
                clear()
            else :
                pass

            
        # mail,name,phone,pin,created,details
        #tab1
        emailvar = StringVar()
        namevar = StringVar()
        phonevar = StringVar()
        pin = StringVar()
        details = StringVar()
        emailentry = Entry(tab3,textvariable=emailvar,width=30,font=30,border=2)
        nameentry = Entry(tab3,textvariable=namevar,width=30,font=30,border=2)
        phoneentry = Entry(tab3,textvariable=phonevar,width=30,font=30,border=2)
        pinentry = Entry(tab3,textvariable=pin,width=30,font=30,border=2)
        detailsvar = Entry(tab3,textvariable=details,width=30,font=30,border=2)
        # Label(tab3,text='',bg='#3C4048').grid(row=1,column=2,padx=50,pady=20)
        # Label(tab3,text='',bg='#3C4048').grid(row=1,column=3,padx=50,pady=20)
        Label(tab3,text='EMAIL',font="27",width=25, bg='#12c4c0').grid(row=1,column=2,padx=50,pady=10)
        emailentry.grid(row=1,column=3 ,padx=10,pady=10)
        Label(tab3,text='Name',font="27",width=25, bg='#12c4c0').grid(row=2,column=2 ,padx=10,pady=10)
        nameentry.grid(row=2,column=3 ,padx=20,pady=10)
        Label(tab3,text='Phone',font="27",width=25, bg='#12c4c0').grid(row=3,column= 2,padx=10,pady=10)
        phoneentry.grid(row=3,column=3 ,padx=20,pady=10)
        Label(tab3,text='PIN',font="27",width=25, bg='#12c4c0').grid(row=4,column=2 ,padx=10,pady=10)
        pinentry.grid(row=4,column=3 ,padx=20,pady=10)
        Label(tab3,text='DETAILS',font="27",width=25, bg='#12c4c0').grid(row=5,column=2 ,padx=10,pady=10)
        detailsvar.grid(row=5,column=3 ,padx=20,pady=10)
        Button(tab3,text="S U B M I T",command=student,font='27').grid(row=6,column=2,columnspan=2,padx=20,pady=10)
        #takebook block
        #return book
        # Label(tab2,text="return book").grid()
        tabControl.place(relx=0, rely=0)

        #display box
        def update():
            tree = ttk.Treeview(tab3,selectmode='browse')
            tree.grid(row=9,rowspan=10,column=1,columnspan=5,padx=15,sticky='nw')
            verscrlbar = ttk.Scrollbar(tab3,
                               orient ="vertical",command=tree.yview)
            verscrlbar.grid(row=9,rowspan=10,column=0)
            # Configuring treeview
            tree.configure(xscrollcommand = verscrlbar.set)
            
            # Defining number of columns
            tree["columns"] = ("1", "2", "3","4","5",'6')
    
            # Defining heading
            tree['show'] = 'headings'
            # Assigning the width and anchor to  the
            # respective columns
            tree.column("1", width = 92, anchor ='c')
            tree.column("2", width = 250, anchor ='c')
            tree.column("3", width = 250, anchor ='c')
            tree.column("4", width = 200, anchor ='c')
            tree.column("5", width = 200, anchor ='nw')
            tree.column("6", width = 300, anchor ='nw')
    
            # Asigning the heading names to the
            # repective columns
            tree.heading("1", text ="S NO",)
            tree.heading("2", text ="EMAIL",)
            tree.heading("3", text ="NAME")
            tree.heading("4", text ="PHONE")
            tree.heading("5", text ="PIN")
            tree.heading("6", text ="DETAILS")
        
            i = 1
            data = cursor.execute('SELECT * FROM STUDENTS ORDER BY CREATED_DATE DESC LIMIT 0,30 ;')
            for d in data:
                tree.insert("",'end',values = (i,d[0],d[1],d[2],d[3],d[5])) 
                i = i+1
        update()
        ttk.Style().configure("Treeview", background="#262626",foreground="white")
        ttk.Style().configure("Treeview.Heading", background="#12c4c0")
        #tab2

        #tab1

    elif arg == 'dashboard':
        # def lab():
        #     Label(dash_frame2, text='hello').pack()
        dash_frame = Frame(frame, width=width, height=60, bg='#12c4c0')
        dash_frame.pack()
        dash_frame1 = Frame(frame, width=frame.winfo_screenwidth(),
                            height=200, bd=10, pady=5, bg='#262626')
        dash_frame1.pack()
        dash_frame2 = Frame(frame, width=width, height=height, bg='#ffffff')
        dash_frame2.pack()
        Label(dash_frame, text='D A S H B O A R D', font='25',
              bd=6, padx=3, pady=4, bg='#12c4c0').pack()
        global stud_button_img,book_button,setting_button
        stud_button_img = PhotoImage(file='grad.png')
        book_button = PhotoImage(file='lib.png')
        setting_button = PhotoImage(file='set.png')
        Button(dash_frame1,image=book_button,compound='c',width=100,height=100, command=(lambda: call_any('books')),
               bg='#262626', activebackground='#12c4c0', fg='#ffff00').place(relx=0, rely=0, x=100, y=60)
        sut = Button(dash_frame1,image=stud_button_img,width=100,height=100, command=(lambda: call_any('student')),
               bg='#262626', activebackground='#12c4c0', fg='#ffff00').place(relx=0, rely=0, x=550, y=60)
        Button(dash_frame1, image=setting_button,compound=CENTER,width=100,height=100, command=(lambda: call_any('settings')),
               bg='#262626', activebackground='#12c4c0', fg='#ff0000').place(relx=0, rely=0, x=1000, y=60)

    elif arg == 'books':
        dash_frame = Frame(frame, width=width, height=60, bg='#12c4c0')
        dash_frame.pack()
        dash_frame1 = Frame(frame, width=width, height=height,
                            bd=10, pady=5, bg='#262626')
        dash_frame1.pack()
        Label(dash_frame, text='B O O K S', font='25',
              bd=6, padx=3, pady=4, bg='#12c4c0').pack()

        # Create an instance of ttk
        style = ttk.Style()

        # Define Style for Notebook widget
        style.layout("Tab", [('Notebook.tab', {'sticky': 'nswe', 'children':
                                               [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                                                                      [('Notebook.label', {
                                                                        'side': 'top', 'sticky': ''})],
                                                                      })],
                                               })]
                     )

        # Use the Defined Style to remove the dashed line from Tabs
        style.configure("Tab", focuscolor=style.configure(".")
                        ["background"], padding=10, width=110)

        tabControl = ttk.Notebook(dash_frame1)
        tab1 = Frame(tabControl, bg='#3C4048')
        tab2 = Frame(tabControl, bg='#3C4048')
        # SHOW BOOKS TAB
        tabControl.add(tab1, text='SHOW BOOKS')
        # ADD BOOKS TAB

        tabControl.add(tab2, text='ADD BOOK',)


        tabControl.place(relx=0, rely=0)
     
        #show books
        # Label(tab2, text='ADD BOOKS').grid(row=0, column=4, padx=10, pady=10,)
        def update_book():
            tree = ttk.Treeview(tab1,selectmode='browse')
            tree.grid(row=9,rowspan=15,column=1,columnspan=5,padx=15,sticky='nw')
            verscrlbar = ttk.Scrollbar(tab1,
                               orient ="vertical",command=tree.yview)
            verscrlbar.grid(row=9,rowspan=15,column=0)
            # Configuring treeview
            tree.configure(xscrollcommand = verscrlbar.set)
            
            # Defining number of columns
            tree["columns"] = ("1", "2", "3","4","5",'6','7','8')
    
            # Defining heading
            tree['show'] = 'headings'
            # Assigning the width and anchor to  the
            # respective columns
            tree.column("1", width = 52, anchor ='c')
            tree.column("2", width = 200, anchor ='c')
            tree.column("3", width = 200, anchor ='c')
            tree.column("4", width = 200, anchor ='c')
            tree.column("5", width = 160, anchor ='c')
            tree.column("6", width = 150, anchor ='c')
            tree.column("7", width = 150, anchor ='c')
            tree.column("8", width = 150, anchor ='c')
    
            # Asigning the heading names to the
            # repective columns
            tree.heading("1", text ="S NO",)
            tree.heading("2", text ="BOOK SERIAL NO",)
            tree.heading("3", text ="BOOK NAME")
            tree.heading("4", text ="AUTHOR")
            tree.heading("5", text ="BRANCH")
            tree.heading("6", text ="QUANTITY")
            tree.heading("7", text ="PRICE")
            tree.heading("8", text ="STATUS")
        
            i = 1
            data = cursor.execute('SELECT * FROM BOOKS ORDER BY TAKEN_DATE DESC LIMIT 0,30 ;')
            for d in data:
                tree.insert("",'end',values = (i,d[0],d[1],d[2],d[3],d[4],d[5],books_obj.check_availabe_lib(d[4],d[0]))) 
                i = i+1
        update_book()
        #add books
        booknamevar = StringVar()
        booksnovar = StringVar()
        authorvar = StringVar()
        branchvar = StringVar()
        quantityvar = IntVar(tab2,1)
        pricevar = StringVar()
        # Dictionary with options
        choices = { 'CM','CNNA','AIML','MECH','EEE','ECE','CIVIL'}
        branchvar.set('SELECT BRANCH') # set the default option

        #LABELS OF ADD BOOK
        
        popupMenu = OptionMenu(tab2, branchvar, *choices)

        # on change dropdown value
        
        def book():
            name = booknamevar.get()
            sno = booksnovar.get()
            price = pricevar.get()
            author = authorvar.get()
            quantity = quantityvar.get()
            branch = branchvar.get()
            error = ''
            def clear():
                booknameentry.delete(0,END)
                booksnoentry.delete(0,END)
                authorentry.delete(0,END)
                quantityentry.delete(0,END)
                priceentry.delete(0,END)
                branchvar.set('SELECT BRANCH')
            if name == '':
                popup('validation error','Name must be filled')
                error = 'error'
            if sno != '':
                sqla = """
                SELECT * FROM BOOKS WHERE BOOK_SNO = '{}'
                """.format(str(sno))
                dataabc = cursor.execute(sqla)
                for a in dataabc:
                    print(a[0])
                    if a[0] != '':
                        popup('validation error',a[0]+' Serial No already taken')
                        error = 'error'
                    else:
                        break
            if price == '':
                popup('validation error','Price must be filled')
                error = 'error'
            if quantity < 0:
                popup('validation error','Quantity must be Positive')
                error = 'error'
            if quantity == '':
                popup('validation error','Quantity  must be filled')
                error = 'error'
            if author == '':
                popup('validation error','Auther  must be filled')
                error = 'error'
            if branch == 'SELECT BRANCH':
                popup('validation error','Branch  must be select')
                error = 'error'
            if error == '':
                books_obj.Add_book_lib(sno,name,author,branch,quantity,price,datetime.now())
                popup('Sucess','Books added successfully')
                update_book()
                clear()
            
             
        # link function to change dropdown
        booknameentry = Entry(tab2,textvariable=booknamevar,width=30,font=30,border=2)
        booksnoentry = Entry(tab2,textvariable=booksnovar,width=30,font=30,border=2)
        authorentry = Entry(tab2,textvariable=authorvar,width=30,font=30,border=2)
        quantityentry = Entry(tab2,textvariable=quantityvar,width=30,font=30,border=2)
        priceentry = Entry(tab2,textvariable=pricevar,width=30,font=30,border=2)        
        Label(tab2,text='BOOK NAME',font="27",width=25, bg='#12c4c0').grid(row=1,column=1,padx=50,pady=10)
        booknameentry.grid(row=1,column=2 ,padx=10,pady=10)    
        Label(tab2,text='BOOK SNO',font="27",width=25, bg='#12c4c0').grid(row=1,column=3,padx=50,pady=10)
        booksnoentry.grid(row=1,column=4 ,padx=10,pady=10)    
        Label(tab2,text='AUTHOR',font="27",width=25, bg='#12c4c0').grid(row=2,column=1,padx=50,pady=10)
        authorentry.grid(row=2,column=2 ,padx=10,pady=10)    
        Label(tab2,text='BRANCH',font="27",width=25, bg='#12c4c0').grid(row=2,column=3,padx=50,pady=10)
        popupMenu.grid(row = 2, column =4,padx=50,pady=10)  
        Label(tab2,text='QUANTITY',font="27",width=25, bg='#12c4c0').grid(row=3,column=1,padx=50,pady=10)
        quantityentry.grid(row=3,column=2 ,padx=20,pady=10)    
        Label(tab2,text='PRICE',font="27",width=25, bg='#12c4c0').grid(row=3,column=3,padx=50,pady=10)
        priceentry.grid(row=3,column=4 ,padx=10,pady=10)
        Button(tab2,text="S U B M I T",command=book,font='27').grid(row=4,column=1,columnspan=4,padx=20,pady=10)

        ttk.Style().configure("Treeview", background="#262626",foreground="white")
        ttk.Style().configure("Treeview.Heading", background="#12c4c0")
    elif arg == 'settings':
        dash_frame = Frame(frame, width=width, height=60, bg='#ff00ff')
        dash_frame.pack()
        dash_frame1 = Frame(frame, width=frame.winfo_screenwidth(),
                            height=200, bd=10, pady=5, bg='#262626')
        dash_frame1.pack()
        dash_frame2 = Frame(frame, width=width, height=height, bg='#ffffff')
        dash_frame2.pack()
        Label(dash_frame, text='S E T T I N G S', font='25',
              bd=6, padx=3, pady=4, bg='#12c4c0').pack()
        gmailvar = StringVar()
        passvar = StringVar()
        def Askmail():
            search = Toplevel(dash_frame1)
            search.title('Gmail add')
            search.geometry('800x200')
           
            gmailentry = Entry(search,textvariable=gmailvar,width=30,font=30,border=2)
            passentry = Entry(search,textvariable=passvar,width=30,font=30,border=2)

            Label(search,text='GMAIL',font="27",width=25, bg='#12c4c0').grid(row=3,column=3,padx=50,pady=10)
            gmailentry.grid(row=3,column=4 ,padx=10,pady=10)
            Label(search,text='GMAIL APP PASSWORD',font="27",width=25, bg='#12c4c0').grid(row=4,column=3,padx=50,pady=10)
            passentry.grid(row=4,column=4 ,padx=10,pady=10)
            Button(search,text="A D D",command=(lambda: gmail(search)),font='27').grid(row=5,column=1,columnspan=4,padx=20,pady=10)
        def gmail(a):
            popup('success' , 'Added gmail sucessfully')
            Hostmail = gmailvar.get()
            Hostpassword = passvar.get()
            a.destroy()
            # Label(search,text='here entry').pack()


        Button(dash_frame1,text='ADD EMAIL',command=Askmail,padx=3,width=50,pady=4,bg='#262626').grid(row=2,column=2,columnspan=5,padx=480)
        Button(dash_frame1,text='BACK UP ',command=backup,width=50,padx=4,pady=4,bg='#262626').grid(row=4,column=2,columnspan=5,padx=480)
        Button(dash_frame1,text='RETORE',command=restore,padx=4,width=50,pady=4,bg='#262626').grid(row=6,column=2,columnspan=5,padx=480)

        book_obj = Book_Manager
    elif arg == 'about':
        dash_frame = Frame(frame, width=width, height=60, bg='#ff00ff')
        dash_frame.pack()
        dash_frame2 = Frame(frame, width=width, height=height, bg='#EAEAEA')
        dash_frame2.pack()
        Label(dash_frame, text='A B O U T', font='25',
              bd=6, padx=3, pady=4, bg='#12c4c0').pack()
        with open(licensetext, 'rt') as f:
            variable = f.read()  # dont forgot to change
        Label(dash_frame2, text=variable, font=1,
              justify=LEFT, pady=200, padx=400).pack(fill=BOTH)
    else:
        pass


def print_on(e):
    print('he')


def call_any(var):
    var = str(var)
    f1 = Frame(root, width=300, height=1000, bg='#12c4c0')
    f1.place(x=0, y=0)
    screen_frame(60, 0, '#12c4c0', f1, var)


# main code

root = Tk()
start()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.iconphoto(False,PhotoImage(file='library.ico'))
root.minsize(800, 400)
root.title('Lib manager(by rohith groups)')
root.configure(bg='#262626')

l1 = Label(root, text='ROHITH GROUPS', fg='white', bg='#262626')

l1.config(font=('Comic Sans MS', 60))
l1.pack(expand=True)
screen_frame(60, 0, '#12c4c0', None, 'dashboard')


img1 = ImageTk.PhotoImage(Image.open("open.png"))


Button(root, image=img1, command=toggle_win, border=0,
       bg='#262626', activebackground='#262626').place(x=5, y=10)


root.state('zoomed')

root.mainloop()
conn.commit()
conn.close() 