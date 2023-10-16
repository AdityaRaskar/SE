import tkinter as tk
import time
from tkinter import *
import pandas
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3
import csv
from PIL import Image,ImageTk
from tkinter import filedialog, messagebox



# from PIL import ImageTk, Image


# function to define database
def Database():
    global conn, cursor
    # creating student database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # creating STUD_REGISTRATION table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS STUD_REGISTRATION ( STU_NAME TEXT, STU_MIS INTEGER, STU_CONTACT INTEGER, STU_EMAIL TEXT, STU_BRANCH TEXT, STU_CGPA FLOAT  , STU_CATEGORY TEXT , STU_CITY TEXT)")



# defining function to access data from SQLite database
def DisplayData(tree):
    # open database
    Database()
    # clear current data

    # global tree
    # tree = ttk.Treeview()

    tree.delete(*tree.get_children())
    # select query
    cursor = conn.execute("SELECT * FROM STUD_REGISTRATION")
    # fetch all data from database
    fetch = cursor.fetchall()
    # loop for displaying all data in GUI
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # self.shared_data = {'Balance':tk.IntVar()}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # for F in (StartPage, MenuPage, AddPage, DataPage, SettingsPage):
        for F in (StartPage, MenuPage, AddPage, DataPage):  #aditya
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()




class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='black')
        self.controller = controller

        self.controller.title('STUDENT MANAGEMENT SYSTEM')
        self.controller.state('zoomed')


        # ========================================================================
        # ============================background image============================
        # ========================================================================
        self.bg_frame = Image.open('Images\\background1.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')


        # ====== Login Frame =========================
        self.lgn_frame = Frame(self, bg='#040405', width=950, height=600)
        self.lgn_frame.place(x=300, y=70)

        # ========================================================================
        # ========================================================
        # ========================================================================
        self.txt = "WELCOME TO STUDENT MANAGEMENT SYSTEM"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#040405",
                             fg='white',
                             bd=5,
                             relief=FLAT)
        self.heading.place(x=95, y=30)

        # ========================================================================
        # ============ Left Side Image ================================================
        # ========================================================================
        self.side_image = Image.open('Images\\vector.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # ========================================================================
        # ============ Sign In Image =============================================
        # ========================================================================
        self.sign_in_image = Image.open('Images\\hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=130)

        # ========================================================================
        # ============ Sign In label =============================================
        # ========================================================================
        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="#040405", fg="white",
                                    font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)

        # ========================================================================
        # ============================username====================================
        # ========================================================================
        self.username_label = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        username=StringVar()
        self.username_entry = Entry(self.lgn_frame, highlightthickness=0,textvariable=username, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"), insertbackground = '#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        # ===== Username icon =========
        self.username_icon = Image.open('Images\\username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)





        # ************************************************************************

        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        # Create user table if it doesn't exist
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
        self.conn.commit()

        # Check if user table is empty
        self.cursor.execute("SELECT COUNT(*) FROM users")
        count = self.cursor.fetchone()[0]
        if count == 0:
            # Insert default username and password as 'admin' into the user table
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin'))
            self.conn.commit()

        # **********************************************************

        def check_password():
            entered_username = self.username_entry.get()
            entered_password = self.password_entry.get()

            # Query the user table to check if the entered credentials are valid
            self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                                (entered_username, entered_password))
            user = self.cursor.fetchone()

            if user:
                self.password_entry.delete(0, tk.END)
                self.username_entry.delete(0, tk.END)
                self.controller.show_frame('MenuPage')
            else:
                messagebox.showwarning("Error", "Incorrect Credentials")



        self.lgn_button = Image.open('Images\\btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.login = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2',command=check_password, activebackground='#3047ff', fg='white')
        self.login.place(x=20, y=10)




        # ========================================================================
        # ============================password====================================
        # ========================================================================
        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        password=StringVar()
        self.password_entry = Entry(self.lgn_frame,textvariable=password, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)
        # ======== Password icon ================
        self.password_icon = Image.open('images\\password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)
        # ========= show/hide password ==================================================================
        self.show_image = ImageTk.PhotoImage \
            (file='Images\\show.png')

        self.hide_image = ImageTk.PhotoImage \
            (file='Images\\hide.png')

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')


class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#21252b')
        self.controller = controller



        title_frame = tk.Frame(self , border=1, bg="#282c34")
        title_frame.place(x=20, y=20, relwidth=0.97)


        # Title Label
        title_label = tk.Label(title_frame, text="STUDENT MANAGEMENT SYSTEM", font="Arial 47 bold",
                                foreground='#22d3fe' , bg="#282c34")
        title_label.pack()



        time_frame = tk.Frame(self , border=1, bg="#21252b")
        time_frame.place(x=20, y=120, relwidth=0.97,height=100)

        # Date and Time Label
        date_string = time.strftime("%a,%d/%b/%y")
        time_string = time.strftime("%I:%M %p")
        date_label = tk.Label(time_frame, text=date_string, font="Arial 20 bold" ,foreground='#22d3fe' , bg="#21252b")
        date_label.pack(side='top')
        time_label = tk.Label(time_frame, text=time_string, font="Arial 20 bold",foreground='#22d3fe' , bg="#21252b")
        time_label.pack(side='top')

        # creating label for main menu
        sec_frame = tk.Frame(self , border=1, bg="#21252b")
        sec_frame.place(x=20, y=220, relwidth=0.97)

        self.main_menu_label = tk.Label(sec_frame,
                                   text=' SELECT ANY OPTION ',
                                   font=('orbitron', 25),
                                   fg='white',
                                   bg='#21252b')
        self.main_menu_label.pack()

        self.left_frame = tk.Frame(self, bg='#21252b',width=1240,height=350)
        # self.left_frame.pack(fill='both', expand=True)
        self.left_frame.place(x=150,y=300)

        # function for going in Add page
        def AddPage():
            controller.show_frame('AddPage')

        def on_enter(event):
            self.AddPage_button.config(cursor="hand2")

        def on_leave(event):
            self.AddPage_button.config(cursor="")


        # creating button for Add info
        self.add_img = tk.PhotoImage(file='Images/add.png')
        # clear_btn = tk.Button(apw_frame2, image=self.clear_btn_img, bd=0,
        self.AddPage_button = tk.Button(self.left_frame,
                                   # text='New Student',
                                   command=AddPage,
                                   relief='raised',
                                   bd=0,background='#21252b',
                                   image=self.add_img,
                                   activebackground='#21252b'
                                   )
        self.AddPage_button.place(x=50, y=45)

        self.AddPage_button.bind("<Enter>", on_enter)
        self.AddPage_button.bind("<Leave>", on_leave)

        # function for going in Search page
        def Data():
            controller.show_frame('DataPage')

        def on_enter(event):
            self.Data_button.config(cursor="hand2")

        def on_leave(event):
            self.Data_button.config(cursor="")
        # creating button for Search
        self.Data_img = tk.PhotoImage(file='Images/data.png')

        self.Data_button = tk.Button(self.left_frame,
                                  # text='Search',
                                  command=Data,
                                  relief='raised',
                                  bd=0,background='#21252b',
                                  image=self.Data_img,
                                  activebackground='#21252b'
                                  )
        self.Data_button.place(x=350, y=45)
        self.Data_button.bind("<Enter>", on_enter)
        self.Data_button.bind("<Leave>", on_leave)


        # function for going in Delete page
        def Settings():
            controller.show_frame('SettingsPage')

        def on_enter(event):
            self.Settings_button.config(cursor="hand2")

        def on_leave(event):
            self.Settings_button.config(cursor="")
        # creating button for delete
        self.Settings_img = tk.PhotoImage(file='Images/settings.png')

        self.Settings_button = tk.Button(self.left_frame,
                                command=Settings,
                                relief='raised',
                                bd=0,
                                image=self.Settings_img,
                                background='#21252b',
                                activebackground='#21252b'
                                )
        self.Settings_button.place(x=650, y=45)
        self.Settings_button.bind("<Enter>", on_enter)
        self.Settings_button.bind("<Leave>", on_leave)





        # function for exiting the current page and goin to previous page
        def exit():
            controller.show_frame('StartPage')

        def on_enter(event):
            self.exit_button.config(cursor="hand2")

        def on_leave(event):
            self.exit_button.config(cursor="")
        self.exit_img = tk.PhotoImage(file='Images/exit.png')

        self.exit_button = tk.Button(self.left_frame,
                                # text='Exit',
                                command=exit,
                                relief='raised',
                                bd=0, image=self.exit_img,
                                background='#21252b',
                                activebackground='#21252b'
                                )
        self.exit_button.place(x=950, y=45)
        self.exit_button.bind("<Enter>", on_enter)
        self.exit_button.bind("<Leave>", on_leave)

        self.bottom_frame = tk.Frame(self, relief='raised', bd=3)
        self.bottom_frame.pack(fill='x', side='bottom')

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(self.bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()


class AddPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#1e2324')
        self.controller = controller

        title_frame = tk.Frame(self , border=1, bg="#282c34")
        title_frame.place(x=20, y=20, relwidth=0.98)


        # Back Button

        def back():
            controller.show_frame('MenuPage')

        def on_enter(event):
            back_btn.config(cursor="hand2")

        def on_leave(event):
            back_btn.config(cursor="")

        self.back_btn_img = tk.PhotoImage(file='images/back_button.png')
        back_btn = tk.Button(title_frame, image=self.back_btn_img, bd=0,
                             bg="#282c34", activebackground="#282c34",command=back)
        back_btn.place(relwidth=0.15, relheight=1)


        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)

        # Title Label
        title_label = tk.Label(title_frame, text="ADD STUDENT", font="Arial 60 bold",
                                foreground='#22d3fe' , bg="#282c34")
        title_label.pack()
        # Date and Time Label
        date_string = time.strftime("%a,%d/%b/%y")
        time_string = time.strftime("%I:%M %p")
        date_label = tk.Label(title_frame, text=date_string, font="Arial 18 bold" ,foreground='#22d3fe' , bg="#282c34")
        date_label.place(x=1280, y=15)
        time_label = tk.Label(title_frame, text=time_string, font="Arial 18 bold",foreground='#22d3fe' , bg="#282c34")
        time_label.place(x=1280, y=50)

        left_frame = tk.Frame(self, border=1, bg='#282c34')
        left_frame.place(x=20, y=130, width=1200, height=600)
        # Create the right frame
        right_frame = tk.Frame(self, border=1, bg="#282c34")
        right_frame.place(x=1240, y=130, width=275, height=600)

        name = tk.StringVar()
        mis = tk.StringVar()
        contact = tk.StringVar()
        email = tk.StringVar()
        branch = tk.StringVar()
        cgpa = tk.StringVar()
        category = tk.StringVar()
        city = tk.StringVar()

        # function to insert data into database
        def register():
            Database()
            # getting form data
            name1 = name.get()
            mis1 = mis.get()
            con1 = contact.get()
            email1 = email.get()
            branch1 = branch.get()
            cgpa1 = cgpa.get()
            category1 = category.get()
            city1 = city.get()
            # DisplayData(tree)

            def isnumeric(value):
                try:
                    float(value)
                    return True
                except ValueError:
                    return False
            # applying empty validation
            if name1 == '' or mis1 == '' or con1 == '' or email1 == '' or cgpa1 == '' or branch1 == '' or category1 == '' or city1 == "":
                tkMessageBox.showinfo("Warning", "fill the empty field!!!")
            else:
                if not mis1.isdigit() or not con1.isdigit() or not isnumeric(cgpa1):
                    tkMessageBox.showinfo("Error", "Please enter numeric data for MIS, contact, and CGPA!")
                else:
                    # execute query
                    conn.execute('INSERT INTO STUD_REGISTRATION (STU_NAME, STU_MIS, STU_CONTACT, STU_EMAIL, STU_BRANCH, STU_CGPA, STU_CATEGORY, STU_CITY) \
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                                 (name1, mis1, con1, email1, branch1, cgpa1, category1, city1))

                    conn.commit()
                    tkMessageBox.showinfo("Message", "Stored successfully")

                    reset()
                    conn.close()







        self.name_label = tk.Label(left_frame, text="Name  ", font="Arial 17 bold",background="#282c34", foreground='#4eacfe').place(x=25, y=20)
        self.name_entry = tk.Entry(left_frame,  textvariable=name,  font="Arial 17 ",
                                           bg="#282c34", fg="white", bd=0,width=30).place(x=25, y=55)
        line_label_half = tk.Label(left_frame, text=("_") * (70),
                                   bg="#282c34", fg="white", bd=0)
        line_label_half.place(x=24, y=80)




        self.mis_label = tk.Label(left_frame, text="MIS ", font="Arial 17 bold",background="#282c34", foreground='#4eacfe').place(x=715, y=25)
        self.mis_entry = tk.Entry(left_frame,  textvariable=mis, font="Arial 17 ",
                                           bg="#282c34", fg="white", bd=0,width=30).place(x=715, y=55)
        line_label_half = tk.Label(left_frame, text=("_") * (70),
                                   bg="#282c34", fg="white", bd=0)
        line_label_half.place(x=714, y=80)

        self.Contact_label = tk.Label(left_frame, text="Contact No.", font="Arial 17 bold",background="#282c34", foreground='#4eacfe').place(
            x=25, y=160)
        self.Contact_label = tk.Entry(left_frame, textvariable=contact, font="Arial 17 ",
                                           bg="#282c34", fg="white", bd=0,width=30).place(x=25, y=195)
        line_label_half = tk.Label(left_frame, text=("_") * (70),
                                   bg="#282c34", fg="white", bd=0)
        line_label_half.place(x=24, y=220)



        self.email_label = tk.Label(left_frame, text="Email ", font="Arial 17 bold",background="#282c34", foreground='#4eacfe').place(x=715,
                                                                                                              y=160)
        self.email_entry = tk.Entry(left_frame, textvariable=email, font="Arial 17 ",
                                           bg="#282c34", fg="white", bd=0,width=30).place(x=715, y=195)
        line_label_half = tk.Label(left_frame, text=("_") * (70),
                                   bg="#282c34", fg="white", bd=0)
        line_label_half.place(x=714, y=220)



        self.branch_label = tk.Label(left_frame, text="Branch  ", font="Arial 17 bold",background="#282c34", foreground='#4eacfe').place(x=25,
                                                                                                                 y=280)
        self.branch_entry = tk.Entry(left_frame, textvariable=branch,font="Arial 17 ",
                                           bg="#282c34", fg="white", bd=0,width=30).place(x=25, y=315)
        line_label_half = tk.Label(left_frame, text=("_") * (70),
                                   bg="#282c34", fg="white", bd=0)
        line_label_half.place(x=24, y=340)



        self.cgpa_label = tk.Label(left_frame, text="CGPA ", font="Arial 17 bold",background="#282c34", foreground='#4eacfe').place(x=715, y=280)
        self.cgpa_entry = tk.Entry(left_frame,  textvariable=cgpa, font="Arial 17 ",
                                           bg="#282c34", fg="white", bd=0,width=30).place(x=715, y=315)
        line_label_half = tk.Label(left_frame, text=("_") * (70),
                                   bg="#282c34", fg="white", bd=0)
        line_label_half.place(x=714, y=340)




        self.category_label = tk.Label(left_frame, text="Categpry ",  font="Arial 17 bold",background="#282c34", foreground='#4eacfe').place(
            x=25, y=410)
        self.category_label = tk.Entry(left_frame, textvariable=category,font="Arial 17 ",
                                           bg="#282c34", fg="white", bd=0,width=30).place(x=25, y=445)
        line_label_half = tk.Label(left_frame, text=("_") * (70),
                                   bg="#282c34", fg="white", bd=0)
        line_label_half.place(x=24, y=470)



        self.city_label = tk.Label(left_frame, text="City ",  font="Arial 17 bold",background="#282c34", foreground='#4eacfe').place(x=715, y=410)
        self.city_entry = tk.Entry(left_frame,  textvariable=city,font="Arial 17 ",
                                           bg="#282c34", fg="white", bd=0,width=30).place(x=715, y=445)
        line_label_half = tk.Label(left_frame, text=("_") * (70),
                                   bg="#282c34", fg="white", bd=0)
        line_label_half.place(x=714, y=470)


        # -------------------------------------------------------------

        self.sub = tk.PhotoImage(file='Images/addprod_button2.png')

        def on_enter(event):
            submit_button.config(cursor="hand2")

        def on_leave(event):
            submit_button.config(cursor="")


        submit_button = tk.Button(right_frame,
                                  relief='groove',
                                  bd=0,
                                  command=register,
                                  image=self.sub,
                                  bg='#2a2f30',
                                  activebackground='#2a2f30' )
        submit_button.pack(side=TOP, pady=15)

        submit_button.bind("<Enter>", on_enter)
        submit_button.bind("<Leave>", on_leave)
        def reset():

            name.set("")
            contact.set("")
            email.set("")
            mis.set("")
            city.set("")
            category.set("")
            cgpa.set("")
            branch.set("")

        self.res_img = tk.PhotoImage(file='Images/res2.png')

        def on_enter(event):
            res_button.config(cursor="hand2")

        def on_leave(event):
            res_button.config(cursor="")
        res_button = tk.Button(right_frame,
                               # text='Reset',
                               command=reset,
                               relief='groove',
                               bd=0,
                               image=self.res_img,
                               # width=25,height=2,
                               bg='#2a2f30',
                               activebackground='#2a2f30')
        res_button.pack(side=TOP, pady=15)
        res_button.bind("<Enter>", on_enter)
        res_button.bind("<Leave>", on_leave)


        self.bottom_frame = tk.Frame(self, bg="#2a2f30",relief='raised', bd=3)
        self.bottom_frame.pack(fill='x', side='bottom')

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(self.bottom_frame,bg='#2a2f30', font=('orbitron', 12))
        time_label.pack(side='right')

        tick()


class DataPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#18191c')
        self.controller = controller

        title_frame = tk.Frame(self, border=1, bg="#282c34")
        title_frame.place(x=18, y=10, relwidth=0.98,height=90)

        # Back Button

        def back():
            controller.show_frame('MenuPage')

        self.back_btn_img = tk.PhotoImage(file='images/back_button.png')
        back_btn = tk.Button(title_frame, image=self.back_btn_img, bd=0,
                             bg="#282c34", activebackground="#282c34", command=back)
        back_btn.place(relwidth=0.15, relheight=1)
        # Title Label
        title_label = tk.Label(title_frame, text="DATA MANAGEMENT", font="Arial 60 bold",
                               foreground='#22d3fe', bg="#282c34")
        title_label.pack()
        # Date and Time Label
        date_string = time.strftime("%a,%d/%b/%y")
        time_string = time.strftime("%I:%M %p")
        date_label = tk.Label(title_frame, text=date_string, font="Arial 18 bold", foreground='#22d3fe', bg="#282c34")
        date_label.place(x=1280, y=15)
        time_label = tk.Label(title_frame, text=time_string, font="Arial 18 bold", foreground='#22d3fe', bg="#282c34")
        time_label.place(x=1280, y=50)


        left_frame = tk.Frame(self, border=1, bg='#282c34')
        left_frame.place(x=18, y=110, width=360, height=680)
        # Create the right frame
        right_frame = tk.Frame(self, border=1, bg="#282c34")
        right_frame.place(x=395, y=110, width=1120, height=680)



        def reset():
            search_var.set("")

        search_option_label = Label(left_frame, text="Search By: ", font=('Arial bold', 10), bg="#282c34", fg='white',
                                    width=10)
        search_option_label.place(x=30, y=5)


        # Define the list of search options
        search_options = ["NAME", "MIS", "CONTACT", "EMAIL", "BRANCH", "CGPA", "CATEGORY", "CITY"]


        # Create search criteria menu
        search_option_var = tk.StringVar()
        search_option_menu = OptionMenu(left_frame, search_option_var, *search_options)
        search_option_menu.config(font=('verdana', 10), width=15, bg="#282c34", fg="white", highlightthickness=0,
                                  activebackground="#00e4ff")
        search_option_menu.place(x=120, y=10)

        # Create the search entry
        search_var = tk.StringVar()
        search_entry = Entry(left_frame, bg="#282c34", fg="white", textvariable=search_var, font=('verdana', 15),
                             width=20)
        search_entry.place(x=10, y=60)



        # function to search data

        def SearchRecord():
            # Open database
            Database()

            # Get the selected search option
            search_option = search_option_var.get()

            # Get the search text
            search_text = search_var.get()

            # Clear the current display data
            tree.delete(*tree.get_children())

            # Perform the search based on the selected option
            if search_option == "NAME":
                cursor = conn.execute("SELECT * FROM STUD_REGISTRATION WHERE STU_NAME LIKE ?",
                                      ('%' + str(search_text) + '%',))
            elif search_option == "MIS":
                cursor = conn.execute("SELECT * FROM STUD_REGISTRATION WHERE STU_MIS LIKE ?",
                                      ('%' + str(search_text) + '%',))
            elif search_option == "CONTACT":
                cursor = conn.execute("SELECT * FROM STUD_REGISTRATION WHERE STU_CONTACT LIKE ?",
                                      ('%' + str(search_text) + '%',))
            elif search_option == "EMAIL":
                cursor = conn.execute("SELECT * FROM STUD_REGISTRATION WHERE STU_EMAIL LIKE ?",
                                      ('%' + str(search_text) + '%',))
            elif search_option == "BRANCH":
                cursor = conn.execute("SELECT * FROM STUD_REGISTRATION WHERE STU_BRANCH LIKE ?",
                                      ('%' + str(search_text) + '%',))
            elif search_option == "CGPA":
                cursor = conn.execute("SELECT * FROM STUD_REGISTRATION WHERE STU_CGPA LIKE ?",
                                      ('%' + str(search_text) + '%',))
            elif search_option == "CATEGORY":
                cursor = conn.execute("SELECT * FROM STUD_REGISTRATION WHERE STU_CATEGORY LIKE ?",
                                      ('%' + str(search_text) + '%',))
            elif search_option == "CITY":
                cursor = conn.execute("SELECT * FROM STUD_REGISTRATION WHERE STU_CITY LIKE ?",
                                      ('%' + str(search_text) + '%',))

            # Fetch all matching records
            fetch = cursor.fetchall()

            # Loop for displaying all records into GUI
            for data in fetch:
                tree.insert('', 'end', values=data)

            cursor.close()
            conn.close()

        # creating search button
        self.srch_img = tk.PhotoImage(file='Images/search2.png')
        def on_enter(event):
            btn_search.config(cursor="hand2")

        def on_leave(event):
            btn_search.config(cursor="")
        btn_search = Button(left_frame,
                            image=self.srch_img,
                            command=SearchRecord,
                            # text="Search",
                            # command=SearchRecord,
                            relief=GROOVE, bd=0,
                            bg="#282c34", activebackground="#282c34"
                            )
        btn_search.place(x=300, y=60)
        btn_search.bind("<Enter>", on_enter)
        btn_search.bind("<Leave>", on_leave)

        # creating view button
        self.reset_img = tk.PhotoImage(file='Images/reset.png')

        def on_enter(event):
            reset_button.config(cursor="hand2")

        def on_leave(event):
            reset_button.config(cursor="")
        reset_button = tk.Button(left_frame,
                                 command=reset,
                                 relief='groove',
                                 image=self.reset_img,
                                 bd=0, bg="#282c34",
                                 activebackground='#282c34'
                                 )

        reset_button.place(x=65, y=150)
        reset_button.bind("<Enter>", on_enter)
        reset_button.bind("<Leave>", on_leave)



        # creating view button
        self.viewall_img = tk.PhotoImage(file='Images/view_all.png')

        def on_enter(event):
            viewaall_button.config(cursor="hand2")

        def on_leave(event):
            viewaall_button.config(cursor="")
        viewaall_button = tk.Button(left_frame,
                                 command=lambda: self.DisplayData(tree),
                                 relief='groove',
                                 image=self.viewall_img,
                                 bd=0, bg="#282c34",
                                 activebackground='#282c34'
                                 )
        viewaall_button.place(x=65, y=255)
        viewaall_button.bind("<Enter>", on_enter)
        viewaall_button.bind("<Leave>", on_leave)



        def Delete():
            # Open database
            Database()
            if not tree.selection():
                tkMessageBox.showwarning("Warning", "Select data to delete")
            else:
                result = tkMessageBox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                                  icon="warning")
                if result == 'yes':
                    curItem = tree.focus()
                    contents = tree.item(curItem)
                    selecteditem = contents['values']
                    tree.delete(curItem)
                    # Delete data from database
                    cursor = conn.execute("DELETE FROM STUD_REGISTRATION WHERE STU_MIS = ?", (selecteditem[1],))
                    conn.commit()
                    cursor.close()
                    conn.close()

        # def delete():
        self.del_img = tk.PhotoImage(file='Images/delete.png')
        def on_enter(event):
            del_button.config(cursor="hand2")


        def on_leave(event):
            del_button.config(cursor="")
        del_button = tk.Button(left_frame,
                               relief='groove',
                               image=self.del_img,
                               command=Delete,
                               bg='#282c34',
                               bd=0,
                               activebackground='#282c34'
                               )

        del_button.place(x=63, y=360)
        del_button.bind("<Enter>", on_enter)
        del_button.bind("<Leave>", on_leave)

# sanchit add export fxn/
def exportstudent():
            # Ask the user to provide a filename and location for the exported file
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")],
                                                     title="Save CSV File")

            # Check if the user canceled the save dialog
            if not file_path:
                return

            try:
                # Get the current displayed records in the Treeview widget
                selected_records = tree.get_children()

                if len(selected_records) == 0:
                    messagebox.showinfo("Info", "No records to export.")
                    return

                # Create empty lists for each column
                name, mis, contact, email, branch, cgpa,category,city = [], [], [], [], [], [], [], []

                # Extract data from each selected record
                for record_id in selected_records:
                    values = tree.item(record_id)["values"]
                    name.append(values[0])
                    mis.append(values[1])
                    contact.append(values[2])
                    email.append(values[3])
                    branch.append(values[4])
                    cgpa.append(values[5])
                    category.append(values[6])
                    city.append(values[7])


                # Create a DataFrame with the extracted data
                data = {"Name": name, "MIS": mis, "Contact": contact, "Email": email, "Branch": branch, "CGPA": cgpa,
                        "City": city, "Category": category}
                df = pandas.DataFrame(data)

                # Check if the user canceled the save dialog
                if file_path == "":
                    return

                # Save the DataFrame to a CSV file
                df.to_csv(file_path, index=False)

                messagebox.showinfo("Success", f"Student data is saved: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")



        self.exp_img = tk.PhotoImage(file='Images/export.png')

        def on_enter(event):
            exp_button.config(cursor="hand2")

        def on_leave(event):
            exp_button.config(cursor="")

        exp_button = tk.Button(left_frame,
                               relief='groove',
                               image=self.exp_img,
                               bg='#282c34',
                               bd=0,
                               command=exportstudent,
                               activebackground='#282c34'
                               )
        exp_button.place(x=62, y=470)
        exp_button.bind("<Enter>", on_enter)
        exp_button.bind("<Leave>", on_leav



        scrollbarx = Scrollbar(right_frame, orient=HORIZONTAL)
        scrollbary = Scrollbar(right_frame, orient=VERTICAL)
        # ================================================================================


        # Create a custom style for the Treeview widget
        style = ttk.Style()
        style.configure("Custom.Treeview", rowheight=30)

        tree = ttk.Treeview(right_frame, style="Custom.Treeview",
                            columns=("NAME", "MIS", "CONTACT", "EMAIL", "BRANCH", "CGPA", "CATEGORY","CITY"),
                            selectmode="extended", height=100, yscrollcommand=scrollbary.set,
                            xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)

        # setting headings for the columns
        tree.heading('NAME', text="NAME", anchor=W)
        tree.heading('MIS', text="MIS", anchor=W)
        tree.heading('CONTACT', text="CONTACT", anchor=W)
        tree.heading('EMAIL', text="EMAIL", anchor=W)
        tree.heading('BRANCH', text="BRANCH", anchor=W)
        tree.heading('CGPA', text="CGPA", anchor=W)
        tree.heading('CATEGORY', text="CATEGORY", anchor=W)
        tree.heading('CITY', text="CITY", anchor=W)
        # setting width of the columns
        tree.column('#0', stretch=NO, minwidth=0, width=200)
        tree.column('#1', stretch=NO, minwidth=0, width=150)
        tree.column('#2', stretch=NO, minwidth=0, width=150)
        tree.column('#3', stretch=NO, minwidth=0, width=150)
        tree.column('#4', stretch=NO, minwidth=0, width=120)
        tree.column('#5', stretch=NO, minwidth=0, width=120)
        tree.column('#6', stretch=NO, minwidth=0, width=120)
        tree.column('#7', stretch=NO, minwidth=0, width=120)

        tree.pack()
        DisplayData(tree)



    def DisplayData(self, tree):
        # Open database
        Database()
        # Clear current data
        tree.delete(*tree.get_children())
        # Select query
        cursor = conn.execute("SELECT * FROM STUD_REGISTRATION")
        # Fetch all data from database
        fetch = cursor.fetchall()
        # Loop for displaying all data in GUI
        for data in fetch:
            tree.insert('', 'end', values=data)
        cursor.close()
        conn.close()

    def SearchRecord(self):
        # open database
        Database()
        # DisplayData()
        # checking search text is empty or not
        search_var = tk.StringVar()
        if search_var.get() != "":
            # clearing current display data
            self.tree.delete(*self.tree.get_children())
            # select query with where clause
            cursor = conn.execute("SELECT * FROM STUD_REGISTRATION WHERE STU_MIS LIKE ?",
                                  ('%' + str(search_var.get()) + '%',))
            # fetch all matching records
            fetch = cursor.fetchall()
            # loop for displaying all records into GUI
            for data in fetch:
                self.tree.insert('', 'end', values=data)
            cursor.close()
            conn.close()


# class SettingsPage(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent, bg='#18191c')
#         self.controller = controller

#         # Establish database connection
#         self.conn = sqlite3.connect('database.db')
#         self.cursor = self.conn.cursor()


#         title_frame = tk.Frame(self , border=1, bg="#282c34")
#         title_frame.place(x=20, y=20, relwidth=0.97)


#         # Back Button

#         def back():
#             controller.show_frame('MenuPage')

#         def on_enter(event):
#             back_btn.config(cursor="hand2")

#         def on_leave(event):
#             back_btn.config(cursor="")

#         self.back_btn_img = tk.PhotoImage(file='images/back_button.png')
#         back_btn = tk.Button(title_frame, image=self.back_btn_img, bd=0,
#                              bg="#282c34", activebackground="#282c34",command=back)
#         back_btn.place(relwidth=0.15, relheight=1)


#         back_btn.bind("<Enter>", on_enter)
#         back_btn.bind("<Leave>", on_leave)


#         # Title Label
#         title_label = tk.Label(title_frame, text="SETTINGS", font="Arial 60 bold",
#                                 foreground='#22d3fe' , bg="#282c34")
#         title_label.pack()
#         # Date and Time Label
#         date_string = time.strftime("%a,%d/%b/%y")
#         time_string = time.strftime("%I:%M %p")
#         date_label = tk.Label(title_frame, text=date_string, font="Arial 18 bold" ,foreground='#22d3fe' , bg="#282c34")
#         date_label.place(x=1280, y=15)
#         time_label = tk.Label(title_frame, text=time_string, font="Arial 18 bold",foreground='#22d3fe' , bg="#282c34")
#         time_label.place(x=1280, y=50)

#         # ===============  Password Frame / Left Frame 1 =======================#



#         ch_pass_frame = tk.Frame(self, border=1,bg="#282c34")
#         ch_pass_frame.place(x=20, y=135,relwidth=0.97,height=300)



#         # Heading Label
#         heading_label = ttk.Label(ch_pass_frame, text="CHANGE USERNAME",
#                                   font="Arial 20 bold", foreground='#4eacfe',background="#282c34")
#         heading_label.pack(side='top', pady=25)
#         # Current username
#         current_username_label = ttk.Label(ch_pass_frame, text="Current Username",
#                                            font="Arial 17 bold",background="#282c34", foreground='#4eacfe')
#         current_username_label.place(x=250, y=100)  #
#         self.current_username_entry = tk.Entry(ch_pass_frame, font="Arial 17",
#                                                width=23, bg="#282c34", fg="white", bd=0)
#         self.current_username_entry.place(x=250, y=150)
#         # Adding line below entry widget to look modern
#         line_label_half = tk.Label(ch_pass_frame, text=("_") * (61),
#                                     bg="#282c34", fg="white", bd=0)
#         line_label_half.place(x=249, y=180)
#         # Binding Line label to focus on entry widget
#         line_label_half.bind("<Button-1>", lambda e: self.current_username_entry.focus_set())

#         # New username
#         new_username_label = ttk.Label(ch_pass_frame, text="New Username",
#                                        font="Arial 17 bold",background="#282c34", foreground='#4eacfe')
#         new_username_label.place(x=950, y=100)
#         self.new_username_entry = tk.Entry(ch_pass_frame, font="Arial 17 ",
#                                            bg="#282c34", fg="white", bd=0, width=23)
#         self.new_username_entry.place(x=950, y=150)
#         # Adding line below entry widget to look modern
#         line_label_half = tk.Label(ch_pass_frame, text=("_") * (61),
#                                     bg="#282c34", fg="white", bd=0)
#         line_label_half.place(x=949, y=180)
#         # Binding Line label to focus on entry widget
#         line_label_half.bind("<Button-1>", lambda e: self.new_username_entry.focus_set())

#         def change_username():
#             previous_username = self.current_username_entry.get()
#             new_username = self.new_username_entry.get()

#             # Check if the previous username matches the stored value
#             self.cursor.execute("SELECT username FROM users WHERE username = ?", (previous_username,))
#             result = self.cursor.fetchone()
#             if result is None:
#                 messagebox.showerror("Error", "Invalid previous username.")
#                 return

#             # Check if the new username already exists
#             self.cursor.execute("SELECT username FROM users WHERE username = ?", (new_username,))
#             result = self.cursor.fetchone()
#             if result is not None:
#                 messagebox.showerror("Error", "Username already exists. Please choose a different username.")
#                 return

#             # Update the username
#             self.cursor.execute("UPDATE users SET username = ? WHERE username = ?", (new_username, previous_username))
#             self.conn.commit()
#             messagebox.showinfo("Success", "Username changed successfully.")
#             self.current_username_entry.delete(0, tk.END)
#             self.new_username_entry.delete(0, tk.END)


#         self.changeuser_btn_img = tk.PhotoImage(file='images/changeuser_btn.png')
#         def on_enter(event):
#             self.change_username_button.config(cursor="hand2")

#         def on_leave(event):
#             self.change_username_button.config(cursor="")


#         self.change_username_button = tk.Button(ch_pass_frame, image=self.changeuser_btn_img,
#                                                 bd=0,  bg="#282c34", fg="white", activebackground="#282c34",command=change_username)
#         self.change_username_button.pack(side='bottom', pady=25)


#         self.change_username_button.bind("<Enter>", on_enter)
#         self.change_username_button.bind("<Leave>", on_leave)


#         # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#         ch_pass_frame2 = tk.Frame(self, border=1, bg="#282c34")
#         ch_pass_frame2.place(x=20, y=450, relwidth=0.97, height=300)

#         # Heading Label
#         heading_label = ttk.Label(ch_pass_frame2, text="CHANGE PASSWORD",
#                                   font="Arial 20 bold", foreground='#4eacfe',background="#282c34")
#         heading_label.pack(side='top', pady=15)
#         # Current Password
#         current_password_label = ttk.Label(ch_pass_frame2, text="Current Password",
#                                            font="Arial 17 bold", foreground='#4eacfe',background="#282c34")
#         current_password_label.place(x=250, y=100)
#         self.current_password_entry = tk.Entry(ch_pass_frame2, font="Arial 17 bold", show="*",
#                                                width=23, bg="#282c34", fg="white", bd=0)
#         self.current_password_entry.place(x=250, y=150)
#         # Adding line below entry widget to look modern
#         line_label_half = tk.Label(ch_pass_frame2, text=("_") * (61),
#                                     bg="#282c34", fg="white", bd=0)
#         line_label_half.place(x=249, y=180)
#         # Binding Line label to focus on entry widget
#         line_label_half.bind("<Button-1>", lambda e: self.current_password_entry.focus_set())

#         # New Password
#         new_password_label = ttk.Label(ch_pass_frame2, text="New Password",
#                                        font="Arial 17 bold",background="#282c34", foreground='#4eacfe')
#         new_password_label.place(x=950, y=100)
#         self.new_password_entry = tk.Entry(ch_pass_frame2, show="*", font="Arial 17 bold",
#                                            bg="#282c34", fg="white", bd=0, width=23)
#         self.new_password_entry.place(x=950, y=150)
#         # Adding line below entry widget to look modern
#         line_label_half = tk.Label(ch_pass_frame2, text=("_") * (61),
#                                     bg="#282c34", fg="white", bd=0)
#         line_label_half.place(x=949, y=180)
#         # Binding Line label to focus on entry widget
#         line_label_half.bind("<Button-1>", lambda e: self.new_password_entry.focus_set())
#         # Change Password Button
#         def change_password():
#             username = self.current_username_entry.get()
#             previous_password = self.current_password_entry.get()
#             new_password = self.new_password_entry.get()

#             # Check if the entered username matches the stored value
#             self.cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
#             result = self.cursor.fetchone()
#             if result is None:
#                 messagebox.showerror("Error", "Invalid username.")
#                 return

#             # Check if the previous password matches the stored value
#             self.cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
#             result = self.cursor.fetchone()
#             if result is None or result[0] != previous_password:
#                 messagebox.showerror("Error", "Invalid previous password.")
#                 return

#             # Check if the new password is the same as the previous password
#             if previous_password == new_password:
#                 messagebox.showerror("Error", "New password cannot be the same as the previous password.")
#                 return

#             # Update the password
#             self.cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
#             self.conn.commit()
#             messagebox.showinfo("Success", "Password changed successfully.")
#             self.current_password_entry.delete(0, tk.END)
#             self.new_password_entry.delete(0, tk.END)

#         self.changepass_btn_img = tk.PhotoImage(file='images/changepass_btn.png')

#         def on_enter(event):
#             self.change_password_button.config(cursor="hand2")

#         def on_leave(event):
#             self.change_password_button.config(cursor="")

#         self.change_password_button = tk.Button(ch_pass_frame2, image=self.changepass_btn_img,
#                                                 bd=0,  bg="#282c34", fg="white", activebackground="#282c34",command=change_password)
#         self.change_password_button.pack(side='bottom', pady=25)


#         self.change_password_button.bind("<Enter>", on_enter)
#         self.change_password_button.bind("<Leave>", on_leave)







if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
