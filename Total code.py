from tkinter import *
from tkinter import messagebox
import tkinter as tk
import mysql.connector
import cv2
from PIL import Image, ImageTk
from tkinter import ttk #themed tk
import pandas as pd
import random as r


def open_main_application():
    
    def Excel():
        try:
            conn = mysql.connector.connect(host='localhost', username='root', password='123', database='management')
            my_cursor = conn.cursor()
            
            # Retrieve the IDs of the visible rows
            visible_ids = [criminal_table.item(item)['values'][0] for item in criminal_table.get_children()]
    
            # Create a query to select only the visible rows
            query = 'SELECT * FROM criminal WHERE Case_id IN ({})'.format(','.join(['%s']*len(visible_ids)))
            my_cursor.execute(query, visible_ids)
            data = my_cursor.fetchall()
            conn.close()

            # Convert the fetched data to a DataFrame
            df = pd.DataFrame(data, columns=['Case_id', 'Criminal_no', 'Criminal_name', 'Nick_name', 'arrest_date',
                                          'dateOfcrime', 'address', 'age', 'occupation', 'BirthMark', 'crimeType',
                                          'fatherName', 'gender', 'wanted'])
    
            # Save data to Excel
            l=[]
            n=r.randint(1,1000000)
            s=""
            if n not in l:
                l.append(n)
                excel_file = "criminal"+str(n)+".xlsx"
            df.to_excel(excel_file, index=False)#index - index column of the DataFrame is not written to the Excel file
            messagebox.showinfo('Successful', 'Data exported to Excel successfully.')
            
        except Exception as es:
            messagebox.showerror('Error', f'Due to {str(es)}')

    def add_data():
        
        if var_case_id.get() == "":
             messagebox.showerror('Error', 'All fields are required')
        else:
            try:
                conn = mysql.connector.connect(host='localhost', username='root', password='123', database='management')
                my_cursor = conn.cursor()
                my_cursor.execute('insert into criminal values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                              (var_case_id.get(), var_criminal_no.get(), var_name.get(), var_nickname.get(),
                               var_arrest_date.get(), var_date_of_crime.get(), var_address.get(), var_age.get(),
                               var_occupation.get(), var_birthMark.get(), var_crime_type.get(), var_father_name.get(),
                               var_gender.get(), var_wanted.get()))
                conn.commit()
                fetch_data()
                clear_data()
                conn.close()
                messagebox.showinfo('Successful', 'Criminal record has been added')
                
            except Exception as es:
                messagebox.showerror('Error', f'Due to {str(es)}')

    def fetch_data():
        
        try:
            conn = mysql.connector.connect(host='localhost', username='root', password='123', database='management')
            my_cursor = conn.cursor()
            my_cursor.execute('select * from criminal')
            data = my_cursor.fetchall()
            if len(data) != 0:
                criminal_table.delete(*criminal_table.get_children())
                for i in data:
                    criminal_table.insert('', END, values=i)
            conn.commit()
            conn.close()
            
        except Exception as es:
            messagebox.showerror('Error', f'Due to {str(es)}')

    def get_cursor(event=""):
        
        cursor_row = criminal_table.focus()
        content = criminal_table.item(cursor_row)
        data = content['values']
        var_case_id.set(data[0])
        var_criminal_no.set(data[1])
        var_name.set(data[2])
        var_nickname.set(data[3])
        var_arrest_date.set(data[4])
        var_date_of_crime.set(data[5])
        var_address.set(data[6])
        var_age.set(data[7])
        var_occupation.set(data[8])
        var_birthMark.set(data[9])
        var_crime_type.set(data[10])
        var_father_name.set(data[11])
        var_gender.set(data[12])
        var_wanted.set(data[13])

    def update_data():
        
        if var_case_id.get() == "":
            messagebox.showerror('Error', 'All fields are required')
        else:
            try:
                update = messagebox.askyesno('Update', "Are you sure you want to update this record?")
                if update > 0:
                    conn = mysql.connector.connect(host='localhost', username='root', password='123', database='management')
                    my_cursor = conn.cursor()
                    my_cursor.execute('update criminal set Criminal_no=%s, Criminal_name=%s, Nick_name=%s, arrest_date=%s, dateOfcrime=%s, address=%s, age=%s, occupation=%s, BirthMark=%s, crimeType=%s, fatherName=%s, gender=%s, wanted=%s where Case_id=%s',
                                  (var_criminal_no.get(), var_name.get(), var_nickname.get(), var_arrest_date.get(),
                                   var_date_of_crime.get(), var_address.get(), var_age.get(), var_occupation.get(),
                                   var_birthMark.get(), var_crime_type.get(), var_father_name.get(), var_gender.get(),
                                   var_wanted.get(), var_case_id.get()))
                else:
                    if not update:
                        return
                conn.commit()
                fetch_data()
                clear_data()
                conn.close()
                messagebox.showinfo('Successful', 'Criminal record has been updated')
                
            except Exception as es:
                messagebox.showerror('Error', f'Due to {str(es)}')

    def delete_data():
        if var_case_id.get() == "":
             messagebox.showerror('Error', 'All fields are required')
        else:
            try:
                delete = messagebox.askyesno('Delete', "Are you sure you want to delete this record?")
                if delete > 0:
                    conn = mysql.connector.connect(host='localhost', username='root', password='123', database='management')
                    my_cursor = conn.cursor()
                    sql = "DELETE FROM criminal WHERE Case_id=%s"
                    value = (var_case_id.get(),)
                    my_cursor.execute(sql, value)
                else:
                    if not delete:
                        return
                conn.commit()
                fetch_data()
                clear_data()
                conn.close()
                messagebox.showinfo('Successful', 'Criminal record has been deleted')
                
            except Exception as es:
                messagebox.showerror('Error', f'Due to {str(es)}')

    def clear_data():
        
        var_case_id.set("")
        var_criminal_no.set("")
        var_name.set("")
        var_nickname.set("")
        var_arrest_date.set("")
        var_date_of_crime.set("")
        var_address.set("")
        var_age.set("")
        var_occupation.set("")
        var_birthMark.set("")
        var_crime_type.set("")
        var_father_name.set("")
        var_gender.set("")
        var_wanted.set("")

    def search_data():
        
        if var_com_search.get() == "":
            messagebox.showerror('Error', 'All fields are required')
        else:
            try:
                conn = mysql.connector.connect(host='localhost', username='root', password='123', database='management')
                my_cursor = conn.cursor()
                search_column = var_com_search.get()
                search_value = var_search.get()
                query = f"SELECT * FROM criminal WHERE {search_column} LIKE '%{search_value}%'"
                my_cursor.execute(query)
                rows = my_cursor.fetchall()
                if len(rows) != 0:
                    criminal_table.delete(*criminal_table.get_children())
                    for i in rows:
                        criminal_table.insert('', END, values=i)
                else:
                    criminal_table.delete(*criminal_table.get_children())
                conn.commit()
                conn.close()
                
            except Exception as es:
                messagebox.showerror('Error', f'Due to {str(es)}')
        
    top=tk.Toplevel()
    top.geometry('1530x790+0+0')#relx and rely
    top.title('CRIMINAL MANAGEMENT SYSTEM')

    var_case_id = StringVar()
    var_criminal_no = StringVar()
    var_name = StringVar()
    var_nickname = StringVar()
    var_arrest_date = StringVar()
    var_date_of_crime = StringVar()
    var_address = StringVar()
    var_age = StringVar()
    var_occupation = StringVar()
    var_birthMark = StringVar()
    var_crime_type = StringVar()
    var_father_name = StringVar()
    var_gender = StringVar()
    var_wanted = StringVar()

    lbl_title = Label(top, text='CRIMINAL MANAGEMENT SYSTEM SOFTWARE', font=('times new roman', 35, 'bold'), bg='black', fg='gold')
    lbl_title.place(x=-95, y=0, width=1530, height=70)

    # Image Frame
    img_frame = Frame(top, bd=2, relief=RIDGE, bg='white')
    img_frame.place(x=0, y=70, width=1530, height=130)


    #1st Image
    img1 = Image.open('5.png')
    img1 = img1.resize((350, 150))
    photo1 = ImageTk.PhotoImage(img1)
    img1_label = Label(img_frame, image=photo1)
    img1_label.place(x=0, y=0, width=350, height=150)

    # 2nd Image
    img2 = Image.open('2.png')
    img2 = img2.resize((350, 150))
    photo2 = ImageTk.PhotoImage(img2)
    img2 = Label(img_frame, image=photo2)
    img2.place(x=350, y=0, width=350, height=150)

    # 3rd Image
    img3 = Image.open('3.png')
    img3 = img3.resize((350, 150))
    photo3 = ImageTk.PhotoImage(img3)
    img3 = Label(img_frame, image=photo3)
    img3.place(x=700, y=0, width=350, height=150)

    # 4rd Image
    img4 = Image.open('4.png')
    img4 = img4.resize((350, 150))
    photo4 = ImageTk.PhotoImage(img4)
    img4 = Label(img_frame, image=photo4)
    img4.place(x=1050, y=0, width=350, height=150)

    # Main Frame
    Main_frame = Frame(top, bd=2, relief=RIDGE, bg='white')
    Main_frame.place(x=10, y=200, width=1500, height=560)

    # Upper Frame
    upper_frame = LabelFrame(Main_frame, bd=2, relief=RIDGE, text='Criminal Information', font=('times new roman', 11, 'bold'), fg='red', bg='white')
    upper_frame.place(x=10, y=10, width=1480, height=180)

    # NCR Logo
    img_logo = Image.open('ncr_logo.png')
    img_logo = img_logo.resize((350, 150))
    photo_logo = ImageTk.PhotoImage(img_logo)
    logo = Label(upper_frame, image=photo_logo)
    logo.place(x=950, y=0, width=350, height=150)

   # Labels and Entries
    
    # Case ID
    caseid = Label(upper_frame, text='Case ID:', font=('arial', 11, 'bold'), bg='white')
    caseid.grid(row=0, column=0, padx=2, sticky=W)

    caseentry = ttk.Entry(upper_frame, textvariable=var_case_id, width=22, font=('arial', 11, 'bold'))
    caseentry.grid(row=0, column=1, padx=2, sticky=W)

    # Criminal No
    lbl_criminal_no = Label(upper_frame, text='Criminal No:', font=('arial', 11, 'bold'), bg='white')
    lbl_criminal_no.grid(row=0, column=2, padx=2, sticky=W)

    txt_criminal_no = ttk.Entry(upper_frame, textvariable=var_criminal_no, width=22, font=('arial', 11, 'bold'))
    txt_criminal_no.grid(row=0, column=3, padx=2, sticky=W)

    # Criminal Name
    lbl_name = Label(upper_frame, text='Criminal Name:', font=('arial', 11, 'bold'), bg='white')
    lbl_name.grid(row=1, column=0, padx=2, sticky=W)

    txt_name = ttk.Entry(upper_frame, textvariable=var_name, width=22, font=('arial', 11, 'bold'))
    txt_name.grid(row=1, column=1, padx=2, sticky=W)

    # Nickname
    lbl_nickname = Label(upper_frame, text='Nickname:', font=('arial', 11, 'bold'), bg='white')
    lbl_nickname.grid(row=1, column=2, padx=2, sticky=W)

    txt_nickname = ttk.Entry(upper_frame, textvariable=var_nickname, width=22, font=('arial', 11, 'bold'))
    txt_nickname.grid(row=1, column=3, padx=2, sticky=W)

    # Arrest Date
    lbl_arrest_date = Label(upper_frame, text='Arrest Date:', font=('arial', 11, 'bold'), bg='white')
    lbl_arrest_date.grid(row=2, column=0, padx=2, sticky=W)

    txt_arrest_date = ttk.Entry(upper_frame, textvariable=var_arrest_date, width=22, font=('arial', 11, 'bold'))
    txt_arrest_date.grid(row=2, column=1, padx=2, sticky=W)

    # Date of Crime
    lbl_date_of_crime = Label(upper_frame, text='Date of Crime:', font=('arial', 11, 'bold'), bg='white')
    lbl_date_of_crime.grid(row=2, column=2, padx=2, sticky=W)

    txt_date_of_crime = ttk.Entry(upper_frame, textvariable=var_date_of_crime, width=22, font=('arial', 11, 'bold'))
    txt_date_of_crime.grid(row=2, column=3, padx=2, sticky=W)

    # Address
    lbl_address = Label(upper_frame, text='Address:', font=('arial', 11, 'bold'), bg='white')
    lbl_address.grid(row=3, column=0, padx=2, sticky=W)

    txt_address = ttk.Entry(upper_frame, textvariable=var_address, width=22, font=('arial', 11, 'bold'))
    txt_address.grid(row=3, column=1, padx=2, sticky=W)

    # Age
    lbl_age = Label(upper_frame, text='Age:', font=('arial', 11, 'bold'), bg='white')
    lbl_age.grid(row=3, column=2, padx=2, sticky=W)

    txt_age = ttk.Entry(upper_frame, textvariable=var_age, width=22, font=('arial', 11, 'bold'))
    txt_age.grid(row=3, column=3, padx=2, sticky=W)

    # Occupation
    lbl_occupation = Label(upper_frame, text='Occupation:', font=('arial', 11, 'bold'), bg='white')
    lbl_occupation.grid(row=4, column=0, padx=2, sticky=W)
    
    txt_occupation = ttk.Entry(upper_frame, textvariable=var_occupation, width=22, font=('arial', 11, 'bold'))
    txt_occupation.grid(row=4, column=1, padx=2, sticky=W)

    # Birth Mark
    lbl_birthMark = Label(upper_frame, text='Birth Mark:', font=('arial', 11, 'bold'), bg='white')
    lbl_birthMark.grid(row=4, column=2, padx=2, sticky=W)

    txt_birthMark = ttk.Entry(upper_frame, textvariable=var_birthMark, width=22, font=('arial', 11, 'bold'))
    txt_birthMark.grid(row=4, column=3, padx=2, sticky=W)

    # Crime Type
    lbl_crime_type = Label(upper_frame, text='Crime Type:', font=('arial', 11, 'bold'), bg='white')
    lbl_crime_type.grid(row=0, column=4, padx=2, sticky=W)

    txt_crime_type = ttk.Entry(upper_frame, textvariable=var_crime_type, width=22, font=('arial', 11, 'bold'))
    txt_crime_type.grid(row=0, column=5, padx=2, sticky=W)

    # Father Name
    lbl_father_name = Label(upper_frame, text='Father Name:', font=('arial', 11, 'bold'), bg='white')
    lbl_father_name.grid(row=1, column=4, padx=2, sticky=W)

    txt_father_name = ttk.Entry(upper_frame, textvariable=var_father_name, width=22, font=('arial', 11, 'bold'))
    txt_father_name.grid(row=1, column=5, padx=2, sticky=W)

    # Gender
    lbl_gender = Label(upper_frame, text='Gender:', font=('arial', 11, 'bold'), bg='white')
    lbl_gender.grid(row=2, column=4, padx=2, sticky=W)

    combo_gender = ttk.Combobox(upper_frame, textvariable=var_gender, font=('arial', 11, 'bold'), width=20, state='readonly')
    combo_gender['value'] = ('Male', 'Female')
    combo_gender.current(0)
    combo_gender.grid(row=2, column=5, padx=2, sticky=W)

    # Most Wanted
    lbl_wanted = Label(upper_frame, text='Most Wanted:', font=('arial', 11, 'bold'), bg='white')
    lbl_wanted.grid(row=3, column=4, padx=2, sticky=W)

    combo_wanted = ttk.Combobox(upper_frame, textvariable=var_wanted, font=('arial', 11, 'bold'), width=20, state='readonly')
    combo_wanted['value'] = ('Yes', 'No')
    combo_wanted.current(0)
    combo_wanted.grid(row=3, column=5, padx=2, sticky=W)

    # Buttons
    btn_add = Button(upper_frame, text='Record Save', command=add_data, font=('arial', 13, 'bold'), width=14, bg='blue', fg='white')
    btn_add.place(x=10, y=125, width=130, height=30)

    btn_update = Button(upper_frame, text='Update', command=update_data, font=('arial', 13, 'bold'), width=14, bg='blue', fg='white')
    btn_update.place(x=150, y=125, width=130, height=30)

    btn_delete = Button(upper_frame, text='Delete', command=delete_data, font=('arial', 13, 'bold'), width=14, bg='blue', fg='white')
    btn_delete.place(x=290, y=125, width=130, height=30)

    btn_clear = Button(upper_frame, text='Clear', command=clear_data, font=('arial', 13, 'bold'), width=14, bg='blue', fg='white')
    btn_clear.place(x=430, y=125, width=130, height=30)

    btn_excel = Button(upper_frame, text='Excel', command=Excel, font=('arial', 13, 'bold'), width=14, bg='blue', fg='white')
    btn_excel.place(x=570, y=125, width=130, height=30)

    btn_exit = Button(upper_frame, text='Exit',command=top.destroy, font=('arial', 13, 'bold'), width=14, bg='blue', fg='white')
    btn_exit.place(x=710, y=125, width=130, height=30)

    # Down Frame
    down_frame = LabelFrame(Main_frame, bd=2, relief=RIDGE, text='Criminal Information Table', font=('times new roman', 11, 'bold'), fg='red', bg='white')
    down_frame.place(x=10, y=200, width=1480, height=270)

    # Search Frame
    search_frame = LabelFrame(down_frame, bd=2, relief=RIDGE, text='Search Criminal Record', font=('times new roman', 11, 'bold'), fg='red', bg='white')
    search_frame.place(x=0, y=0, width=1470, height=60)

    search_by = Label(search_frame, text='Search By:', font=('arial', 11, 'bold'), bg='red', fg='white')
    search_by.grid(row=0, column=0, padx=5, sticky=W)

    var_com_search = StringVar()
    combo_search_box = ttk.Combobox(search_frame, textvariable=var_com_search, font=('arial', 11, 'bold'), width=18, state='readonly')
    combo_search_box['value'] = ('Select Option', 'Case_id', 'Criminal_no','Arrest_Date')
    combo_search_box.current(0)
    combo_search_box.grid(row=0, column=1, padx=5, sticky=W)

    var_search = StringVar()
    txt_search = ttk.Entry(search_frame, textvariable=var_search, width=18, font=('arial', 11, 'bold'))
    txt_search.grid(row=0, column=2, padx=5)

    btn_search = Button(search_frame, text='Search', command=search_data, font=('arial', 13, 'bold'), width=14, bg='blue', fg='white')
    btn_search.grid(row=0, column=3, padx=5)

    btn_show_all = Button(search_frame, text='Show All', command=fetch_data, font=('arial', 13, 'bold'), width=14, bg='blue', fg='white')
    btn_show_all.grid(row=0, column=4, padx=5)

    # Table Frame
    table_frame = Frame(down_frame, bd=2, relief=RIDGE)
    table_frame.place(x=0, y=60, width=1470, height=170)

    scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
    scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

    criminal_table = ttk.Treeview(table_frame, column=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)

    scroll_x.config(command=criminal_table.xview)
    scroll_y.config(command=criminal_table.yview)

    criminal_table.heading('1', text='Case ID')
    criminal_table.heading('2', text='Crime Number')
    criminal_table.heading('3', text='Criminal Name')
    criminal_table.heading('4', text='Nickname')
    criminal_table.heading('5', text='Arrest Date')
    criminal_table.heading('6', text='Date of Crime')
    criminal_table.heading('7', text='Address')
    criminal_table.heading('8', text='Age')
    criminal_table.heading('9', text='Occupation')
    criminal_table.heading('10', text='BirthMark')
    criminal_table.heading('11', text='Crime Type')
    criminal_table.heading('12', text='Father Name')
    criminal_table.heading('13', text='Gender')
    criminal_table.heading('14', text='Wanted')

    criminal_table['show'] = 'headings'

    criminal_table.column('1', width=100)
    criminal_table.column('2', width=100)
    criminal_table.column('3', width=100)
    criminal_table.column('4', width=100)
    criminal_table.column('5', width=100)
    criminal_table.column('6', width=100)
    criminal_table.column('7', width=100)
    criminal_table.column('8', width=100)
    criminal_table.column('9', width=100)
    criminal_table.column('10', width=100)
    criminal_table.column('11', width=100)
    criminal_table.column('12', width=100)
    criminal_table.column('13', width=100)
    criminal_table.column('14', width=100)
    criminal_table.pack(fill=BOTH, expand=1)

    fetch_data()
    root.mainloop()

def clearTxt():
    
    username_entry.delete(0,END)
    password_entry.delete(0,END)
            
def login():
    global new_root
    username = username_entry.get()
    password = password_entry.get()
    if check_credentials(username, password):
        username_entry.delete(0,END)
        password_entry.delete(0,END)
        open_main_application()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def check_credentials(username, password):
    
    # Connect to MySQL database
    conn = mysql.connector.connect(host='localhost', user='root', password='123', database='management')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login WHERE userid=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

def play_video():
    
    cap = cv2.VideoCapture('123.mp4')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scale = min(800/width, 600/height)
    new_width = int(width * scale)
    new_height = int(height * scale)

    def update_frame():
        
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (new_width, new_height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
            root.after(10, update_frame)
        else:
            cap.release()
            root.after(2000, destroy_video_player)  # Wait 2 seconds before destroying the video player window

    update_frame()
        
def destroy_video_player():
    
    root.destroy()

    # Create a new root window
    new_root = tk.Tk()
    new_root.title("Indian RPG")
    new_root.geometry("1000x500")

    # Set background image
    bg_image = Image.open("1.png")  
    bg_image = bg_image.resize((1000, 500), Image.LANCZOS)  
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a canvas with the background image
    canvas = tk.Canvas(new_root, width=1000, height=1000)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)

    # Create a frame for the login interface
    login_frame = Frame(new_root, bg="black", width=300, height=150)
    login_frame.place(x=700, y=300)  

    # Username label and entry
    username_label = Label(login_frame, text="Username:", bg="black", fg="white")
    username_label.place(x=20, y=20)

    global username_entry
    username_entry = Entry(login_frame)
    username_entry.place(x=120, y=20)
    username_entry.focus_set()

    # Password label and entry
    password_label = Label(login_frame, text="Password:", bg="black", fg="white")
    password_label.place(x=20, y=60)

    global password_entry
    password_entry = Entry(login_frame, show="*")
    password_entry.place(x=120, y=60)

    # Login button
    login_button = Button(login_frame, text="Login", command=login,font=('arial', 13, 'bold'),width=7)
    login_button.place(x=120, y=100)

    # Clear button
    Clear_button = Button(login_frame, text="Clear", command=clearTxt,font=('arial', 13, 'bold'),width=7)
    Clear_button.place(x=210, y=100)
    new_root.mainloop()

root = tk.Tk()
root.title("International SPD Records")
root.geometry("800x600")

label = tk.Label(root)
label.pack()

play_video()

root.mainloop()
