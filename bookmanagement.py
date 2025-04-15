from tkinter import *
from tkinter import messagebox
import time
import sqlite3
from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedStyle
from PIL import ImageTk,Image
import customtkinter
import tkinter


#SQL DATABASE
conn = sqlite3.connect("Booksmanagement.db")
table_create_query = """CREATE TABLE IF NOT EXISTS Booksdetails(ISBN TEXT, Booktitle TEXT, Bookauthor TEXT, Publisher TEXT, Yearofpublish INT, Clasification TEXT, Issued TEXT)"""

try:
    conn.execute(table_create_query)
except sqlite3.Error as e:
    print(f"Error creating the table: {e}")

c = conn.cursor()

# resizing funtion
def on_resize(event):
    if root.state() == "normal":
        root.attributes('-zoomed', True)  # Maximize the window
    else:
        root.attributes('-zoomed', False)  # Restore the window

# clock functuion
def clock():
    date = time.strftime("\t\t %a %b %d       %H:%M:%S")
    datetimelabel.configure(text=f"{date}")
    datetimelabel.after(1000, clock)

# slider of the title
Issuedbook = "Not Issued"
Issuingbook = "Issued"
count=0
text=""
def slider():
    global text,count
    if count == len(s):
        count=0
        text=""
    text=text+s[count]
    heading.configure(text=text)
    count+=1
    heading.after(300,slider)

def search_book():
    conn = sqlite3.connect("Booksmanagement.db")
    cursor = conn.cursor()
    
    try:
        if searchentry.get() == "":
            messagebox.showerror("Error", "Please enter the book you are looking for.")
        else:
            cursor.execute("SELECT * FROM Booksdetails WHERE Booktitle = ? ",
                            (searchentry.get(),))
            tree.delete(*tree.get_children())
            bookspresent = cursor.fetchall()
            
            if not bookspresent:
                messagebox.showinfo("No Book Found", "No Book matching the search criteria.")
            else:
                for data in bookspresent:
                    tree.insert("", END, values=data)
    
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def update():
    global Issuingbook
    conn = sqlite3.connect("Booksmanagement.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Booksdetails SET Issued=? WHERE ISBN = ?", (Issuingbook, isbnissued_input))
    conn.commit()
    conn.close()    

def insert_data(isbninput, titleinput, authorinput, publisherinput, yearinput, clasificationinput):
    global Issuedbook
    conn = sqlite3.connect("Booksmanagement.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Booksdetails(ISBN, Booktitle, Bookauthor, Publisher, Yearofpublish, Clasification, Issued) VALUES(?,?,?,?,?,?,?)",
                   (isbninput, titleinput, authorinput, publisherinput, yearinput, clasificationinput, Issuedbook))
    conn.commit()
    conn.close()

def exists(isbnissued_input):
    conn = sqlite3.connect("Booksmanagement.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Booksdetails where ISBN = ?", (isbnissued_input,))
    results = cursor.fetchone()
    conn.close()
    return results[0] > 0

def exists(isbninput):
    conn = sqlite3.connect("Booksmanagement.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Booksdetails where ISBN = ?", (isbninput,))
    results = cursor.fetchone()
    conn.close()
    return results[0] > 0

def add_data():
    global isbninput
    isbninput = isbn.get()
    titleinput = title.get()
    authorinput = author.get()
    publisherinput = publisher.get()
    yearinput = year.get()
    clasificationinput = clasification.get()
    if not (isbninput and titleinput and authorinput and publisherinput and yearinput and clasificationinput):
        messagebox.showerror("Error", "Enter All details")
    elif exists(isbninput):
        messagebox.showerror("Error", "The book isbn already exists.")
    else:
        insert_data(isbninput, titleinput, authorinput, publisherinput, yearinput, clasificationinput)
        view_all()
        result=messagebox.askyesno("Confirm", "Book Data has been added, Do you want to clean the form?")   
        if result:
            clear_data()
        else:
            pass

def remove_data():
    selected_item = tree.selection()
    if selected_item:
        decision = messagebox.askquestion("", "Delete the selected data?")
        if decision == "yes":
            book_isbn = tree.item(selected_item, "values")[0]
            
            try:
                conn = sqlite3.connect("Booksmanagement.db")
                cursor = conn.cursor()
                
                # Assuming you have a table named 'students' with a 'reg_no' column to identify the student
                cursor.execute("DELETE FROM Booksdetails WHERE ISBN=?", (book_isbn,))
                conn.commit()
                
                cursor.close()
                conn.close()
                
                tree.delete(selected_item)  # Remove the selected item from the Treeview
                messagebox.showinfo("", "Successfully deleted")
            except sqlite3.Error as e:
                messagebox.showerror("", f"Error: {e}")
        else:
            return
    else:
        messagebox.showinfo("", "Please select a student from the Treeview.")


def clear_data():
    searchentry.delete(0, END)
    isbn.delete(0, END)
    title.delete(0, END)
    author.delete(0, END)
    publisher.delete(0, END)
    year.delete(0, END)
    clasification.delete(0, END)
    isbnissued.delete(0, END)
    titleissued.delete(0, END)
    issuedby.delete(0, END)
    issuedto.delete(0, END)
    when.delete(0, END)
    duration.delete(0, END)
    tree.delete(*tree.get_children())

# fetching data from database before viewing it
def fetch_alldata():
    conn = sqlite3.connect("Booksmanagement.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Booksdetails")
    books = cursor.fetchall()
    conn.close()
    return books

# Viewing the database ---- all items 
def view_all():
    books=fetch_alldata()
    tree.delete(*tree.get_children())
    for student in books:
        tree.insert("", END, values=student)

def dispatch_book():
    global isbnissued_input
    isbnissued_input = isbnissued.get()
    titleissued_input = titleissued.get()
    issuedby_input = issuedby.get()
    issuedto_input = issuedto.get()
    when_input = when.get()
    duration_input = duration.get()
    if not (isbnissued_input and titleissued_input and issuedby_input and issuedto_input and when_input and duration_input):
        messagebox.showerror("Error", "Enter all Details")
# add an elif function if the book is assigned it should tell me that.
    elif exists(isbnissued_input):
        update()
        view_all()
        result=messagebox.askyesno("Confirm", "Book Data has been issued, Do you want to clean the form?")   
        if result:
            clear_data()
        else:
            pass
    else:
        messagebox.showerror("Error", "The book isbn does not exists in our archives.")        

#def return_book():

#def fetch_issued():

#def fetch_present():

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.title("LIBRARY MANAGEMENT SYSTEM")
root.geometry("1500x740") # Geometry adjust to the screen coordinates
root.resizable(TRUE,TRUE)
root.bind('<Configure>', on_resize)
style = ThemedStyle(root)
style.set_theme("elegance")

# image in the background
img1=ImageTk.PhotoImage(Image.open("PYTHON/images/pattern.png"))
label1 = customtkinter.CTkLabel(master=root,image=img1)
label1.pack()


topframe = customtkinter.CTkFrame(master=label1, bg_color="grey20",fg_color="grey20", corner_radius=20)
topframe.place(x=0, relwidth=1.0)
topframe.pack_propagate(False)
topframe.configure(height=60)

s=" Library Management System"
heading=customtkinter.CTkLabel(master=topframe, text=s, fg_color="grey20",
              font=("times new roman",35,"bold"))
heading.pack(side=LEFT)
slider()

datetimelabel=customtkinter.CTkLabel(master=topframe, font=("times new roman", 20, "bold"), fg_color="grey20")
datetimelabel.pack(side=RIGHT, fill=BOTH)
clock()

search = customtkinter.CTkButton(master=topframe, text="Search", width=100,
                                height=20, corner_radius=6, compound="left", text_color="white",
                                fg_color="grey20", hover_color="#A4A4A4", command=search_book)
search.pack(side=RIGHT)

searchentry=customtkinter.CTkEntry(master=topframe, width=300, placeholder_text="Book Title.", height=40)
searchentry.pack(side=RIGHT)

titleframe = customtkinter.CTkFrame(master=label1, width=800, height=800, corner_radius=25)
titleframe.place(relx=0.1, rely=0.5, anchor=tkinter.CENTER)

headinglabel = customtkinter.CTkLabel(master=titleframe, text="Book Details", font=("times new roman", 30 , "bold"))
headinglabel.grid(row=0, column=0, columnspan=6)

isbn = customtkinter.CTkEntry(master=titleframe, width=300, placeholder_text="ISBN No.", height=40)
isbn.grid(row=1, column=0, padx=20, pady=20, columnspan=2)

title = customtkinter.CTkEntry(master=titleframe, width=300, placeholder_text="Book Title", height=40)
title.grid(row=2, column=0, padx=20, pady=20, columnspan=2) 

author = customtkinter.CTkEntry(master=titleframe, width=300, placeholder_text="Book Author", height=40)
author.grid(row=3, column=0, padx=20, pady=20, columnspan=2)  

publisher = customtkinter.CTkEntry(master=titleframe, width=300, placeholder_text="Publisher", height=40)
publisher.grid(row=4, column=0, padx=20, pady=20, columnspan=2) 

year = customtkinter.CTkEntry(master=titleframe, width=300, placeholder_text="Year of Publish", height=40)
year.grid(row=5, column=0, padx=20, pady=20, columnspan=2)

clasification = customtkinter.CTkEntry(master=titleframe, width=300, placeholder_text="Classification", height=40)
clasification.grid(row=6, column=0, padx=20, pady=20, columnspan=2)

save = customtkinter.CTkButton(master=titleframe, text="Save", width=100,
                                height=20, corner_radius=6, compound="left", text_color="black",
                                fg_color="white", hover_color="#A4A4A4", command=add_data)
save.grid(row=7, column=0, padx=5, pady=5)

deletebutton = customtkinter.CTkButton(master=titleframe, text="Delete", width=100,
                                height=20, corner_radius=6, compound="left", text_color="black",
                                fg_color="white", hover_color="#A4A4A4", command=remove_data)
deletebutton.grid(row=7, column=1, padx=5, pady=5)

view = customtkinter.CTkButton(master=titleframe, text="View All", width=100,
                                height=20, corner_radius=6, compound="left", text_color="black",
                                fg_color="white", hover_color="#A4A4A4", command=view_all)
view.grid(row=8, column=0, padx=5, pady=5)

clear = customtkinter.CTkButton(master=titleframe, text="Clear", width=100,
                                height=20, corner_radius=6, compound="left", text_color="black",
                                fg_color="white", hover_color="#A4A4A4", command=clear_data)
clear.grid(row=8, column=1, padx=5, pady=5)


tableframe = customtkinter.CTkFrame(master=label1, width=600, height=1200, corner_radius=25)
tableframe.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

treeframe = Frame(tableframe, bg="grey20", bd=12, relief=GROOVE)
treeframe.pack(fill=BOTH, expand=1)

scrollbary = Scrollbar(treeframe, orient=VERTICAL)
scrollbary.pack(side=RIGHT, fill=Y)

scrollbarx = Scrollbar(treeframe, orient=HORIZONTAL)
scrollbarx.pack(side=BOTTOM, fill=X)

tree=ttk.Treeview(treeframe, height=28, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set, 
                  columns=("ISBN", "Booktitle", "Bookauthor", "Publisher", "Yearofpublish", "Clasification", "Issued"))
tree.pack(fill=BOTH,expand=1)

scrollbary.config(command=tree.yview)
scrollbarx.config(command=tree.xview)

tree.column("#0", width=0, stretch=tk.NO)
tree.column("ISBN", anchor=tk.CENTER, width=150)
tree.column("Booktitle", anchor=tk.CENTER, width=150)
tree.column("Bookauthor", anchor=tk.CENTER, width=150)
tree.column("Publisher", anchor=tk.CENTER, width=150)
tree.column("Yearofpublish", anchor=tk.CENTER, width=150)
tree.column("Clasification", anchor=tk.CENTER, width=150)
tree.column("Issued", anchor=tk.CENTER, width=150)

tree.heading("ISBN", text="ISBN No.")
tree.heading("Booktitle", text="Book Title")
tree.heading("Bookauthor", text="Book Author")
tree.heading("Publisher", text="Publisher")
tree.heading("Yearofpublish", text="Year of Publish")
tree.heading("Clasification", text="Clasification")
tree.heading("Issued", text="Issued")

tree.config(show="headings")


issueframe = customtkinter.CTkFrame(master=label1, width=800, height=800, corner_radius=25)
issueframe.place(relx=0.9, rely=0.5, anchor=tkinter.CENTER)

headinglabel1 = customtkinter.CTkLabel(master=issueframe, text="Book Dispatch", font=("times new roman", 30 , "bold"))
headinglabel1.grid(row=0, column=0, columnspan=6)

isbnissued = customtkinter.CTkEntry(master=issueframe, width=300, placeholder_text="ISBN No. of issued book", height=40)
isbnissued.grid(row=1, column=0, padx=20, pady=20, columnspan=2)

titleissued = customtkinter.CTkEntry(master=issueframe, width=300, placeholder_text="Book Title of issued book", height=40)
titleissued.grid(row=2, column=0, padx=20, pady=20, columnspan=2) 

issuedby = customtkinter.CTkEntry(master=issueframe, width=300, placeholder_text="Book Issued by", height=40)
issuedby.grid(row=3, column=0, padx=20, pady=20, columnspan=2)  

issuedto = customtkinter.CTkEntry(master=issueframe, width=300, placeholder_text="Book Issued to", height=40)
issuedto.grid(row=4, column=0, padx=20, pady=20, columnspan=2) 

when = customtkinter.CTkEntry(master=issueframe, width=300, placeholder_text="Date Issued", height=40)
when.grid(row=5, column=0, padx=20, pady=20, columnspan=2)

duration = customtkinter.CTkEntry(master=issueframe, width=300, placeholder_text="Date of return", height=40)
duration.grid(row=6, column=0, padx=20, pady=20, columnspan=2)

dispatch = customtkinter.CTkButton(master=issueframe, text="Dispatch", width=100,
                                height=20, corner_radius=6, compound="left", text_color="black",
                                fg_color="white", hover_color="#A4A4A4", command=dispatch_book)
dispatch.grid(row=7, column=0, padx=5, pady=5)

returnbook = customtkinter.CTkButton(master=issueframe, text="Return", width=100,
                                height=20, corner_radius=6, compound="left", text_color="black",
                                fg_color="white", hover_color="#A4A4A4")
returnbook.grid(row=7, column=1, padx=5, pady=5)

issuedbooks = customtkinter.CTkButton(master=issueframe, text="Issued books", width=100,
                                height=20, corner_radius=6, compound="left", text_color="black",
                                fg_color="white", hover_color="#A4A4A4")
issuedbooks.grid(row=8, column=0, padx=5, pady=5)

presentbooks = customtkinter.CTkButton(master=issueframe, text="Present books", width=100,
                                height=20, corner_radius=6, compound="left", text_color="black",
                                fg_color="white", hover_color="#A4A4A4")
presentbooks.grid(row=8, column=1, padx=5, pady=5)


accessframe = customtkinter.CTkFrame(master=label1, width=800, height=800, corner_radius=25)
accessframe.place(relx=0.5, rely=0.88, anchor=tkinter.CENTER)

issuedbysearch = customtkinter.CTkEntry(master=accessframe, width=300, placeholder_text="Books Issued by", height=40)
issuedbysearch.grid(row=0, column=0, padx=20, pady=20)  

issuedtosearch = customtkinter.CTkEntry(master=accessframe, width=300, placeholder_text="Books Issued to", height=40)
issuedtosearch.grid(row=0, column=1, padx=20, pady=20) 

clasificationsearch = customtkinter.CTkEntry(master=accessframe, width=300, placeholder_text="Search for book classification", height=40)
clasificationsearch.grid(row=0, column=2, padx=20, pady=20) 

searchbook_detail= customtkinter.CTkButton(master=accessframe, text="Search", width=100,
                                height=20, corner_radius=6, compound="left", text_color="black",
                                fg_color="white", hover_color="#A4A4A4")
searchbook_detail.grid(row=0, column=3, padx=5, pady=5)

unreturned = customtkinter.CTkEntry(master=accessframe, width=300, placeholder_text="Unreturned Book", height=40)
unreturned.grid(row=1, column=0, padx=20, pady=20)  

lost = customtkinter.CTkEntry(master=accessframe, width=300, placeholder_text="Lost Book", height=40)
lost.grid(row=1, column=1, padx=20, pady=20) 

late = customtkinter.CTkEntry(master=accessframe, width=300, placeholder_text="Suspended for late return", height=40)
late.grid(row=1, column=2, padx=20, pady=20) 

updatebook_detail= customtkinter.CTkButton(master=accessframe, text="Update", width=100,
                                height=20, corner_radius=6, compound="left", text_color="black",
                                fg_color="white", hover_color="#A4A4A4")
updatebook_detail.grid(row=1, column=3, padx=5, pady=5)

lost_books = customtkinter.CTkButton(master=accessframe, text="Lost Books", width=100,
                                height=20, corner_radius=6, compound="left", text_color="black",
                                fg_color="white", hover_color="#A4A4A4")
lost_books.grid(row=3, column=0, padx=5, pady=5)

suspended= customtkinter.CTkButton(master=accessframe, text="Suspended Borrowers", width=100,
                                height=20, corner_radius=6, compound="left", text_color="black",
                                fg_color="white", hover_color="#A4A4A4")
suspended.grid(row=3, column=2, padx=5, pady=5)

root.mainloop()