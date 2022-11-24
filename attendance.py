import imp
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector  

import os
import csv
import numpy as np
from pathlib import Path
from tkinter import filedialog

parent_path = Path(__file__).parent
image_path = (parent_path / "./assets/images/logo_ctu.png").resolve()

mydata = []

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Hệ thống điểm danh sinh viên")
        
        img = Image.open(image_path)
        img = img.resize((200,200), Image.ANTIALIAS)
        self.photoImg = ImageTk.PhotoImage(img)
        
        logo_lbl = Label(self.root, image=self.photoImg)
        logo_lbl.place(x=10, y=10, width=200, height=200)
        
        title_lbl = Label(self.root, text="ĐIỂM DANH SINH VIÊN",
                          fg="darkgreen", font =('times new roman', 48, ' bold '))
        title_lbl.place(x=380, y=80, width= 840, height=80)
        
        
         # Main Frame
        main_frame = Frame(background="coral", bd=2)
        main_frame.place(x=20, y=220, width=1480, height=550)  
        
        # Main Layout
        Left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Thông tin điểm danh", font =('times new roman', 16, ' bold '))
        Left_frame.place(x=10, y=5, width=720, height=530)
        
        attendance_detail_frame = LabelFrame(Left_frame, bd=2, relief=RIDGE, text="Thông tin sinh viên", font =('times new roman', 15, ' bold '))
        attendance_detail_frame.place(x=10, y=10, width=700, height=480)
        
        attendanceId_lbl = Label(attendance_detail_frame, text="ID Phòng:", font =('times new roman', 11, 'bold'))
        attendanceId_lbl.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        attendanceId_entry = ttk.Entry(attendance_detail_frame, width=20, font =('times new roman', 11, 'bold'))
        attendanceId_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        
        studentId_lbl = Label(attendance_detail_frame, text="MSSV:", font =('times new roman', 11, 'bold'))
        studentId_lbl.grid(row=0, column=2, padx=10, pady=10, sticky=W)

        studentId_entry = ttk.Entry(attendance_detail_frame, width=20, font =('times new roman', 11, 'bold'))
        studentId_entry.grid(row=0, column=3, padx=10, pady=10, sticky=W)
        
        studentName_lbl = Label(attendance_detail_frame, text="Họ Tên:", font =('times new roman', 11, 'bold'))
        studentName_lbl.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        studentName_entry = ttk.Entry(attendance_detail_frame, width=20, font =('times new roman', 11, 'bold'))
        studentName_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        
        department_lbl = Label(attendance_detail_frame, text="Chuyên Ngành:", font =('times new roman', 11, 'bold'))
        department_lbl.grid(row=1, column=2, padx=10, pady=10, sticky=W)

        department_entry = ttk.Entry(attendance_detail_frame, width=20, font =('times new roman', 11, 'bold'))
        department_entry.grid(row=1, column=3, padx=10, pady=10, sticky=W)
        
        time_lbl = Label(attendance_detail_frame, text="Thời Gian:", font =('times new roman', 11, 'bold'))
        time_lbl.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        time_entry = ttk.Entry(attendance_detail_frame, width=20, font =('times new roman', 11, 'bold'))
        time_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W)
        
        date_lbl = Label(attendance_detail_frame, text="Ngày:", font =('times new roman', 11, 'bold'))
        date_lbl.grid(row=2, column=2, padx=10, pady=10, sticky=W)

        date_entry = ttk.Entry(attendance_detail_frame, width=20, font =('times new roman', 11, 'bold'))
        date_entry.grid(row=2, column=3, padx=10, pady=10, sticky=W)
        
        attendance_status_cbb = Label(attendance_detail_frame, text="Trạng Thái:", font =('times new roman', 11, 'bold'))
        attendance_status_cbb.grid(row=3, column=0, padx=10, pady=10, sticky=W)
        
        attendance_status_cbb = ttk.Combobox(attendance_detail_frame, font =('times new roman', 11, 'bold'), state="readonly", width=20)
        attendance_status_cbb["values"] = ("Chọn trạng thái", "Hiện diện", "Vắng", "Vào muộn")
        attendance_status_cbb.current(0)
        attendance_status_cbb.grid(row=3, column=1, padx=10, pady=10, sticky=W)
        
         # Buttons Frame
        btn_frame = Frame(attendance_detail_frame, relief=RIDGE)
        btn_frame.place(x=0, y=300, width=680, height=60)
        
        save_btn = Button(btn_frame, text="Import CSV", command=self.importCSV, width=16, font =('times new roman', 11, ' bold '), bg='teal', fg="white")
        save_btn.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        
        update_btn = Button(btn_frame, text="Export CSV", command=self.exportCSV, width=16, font =('times new roman', 11, ' bold '), bg='teal', fg="white")
        update_btn.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        
        delete_btn = Button(btn_frame, text="Cập nhật", width=16, font =('times new roman', 11, ' bold '), bg='teal', fg="white")
        delete_btn.grid(row=0, column=2, padx=10, pady=10, sticky=W)
        
        reset_btn = Button(btn_frame, text="Reset", width=16, font =('times new roman', 11, ' bold '), bg='teal', fg="white")
        reset_btn.grid(row=0, column=3, padx=10, pady=10, sticky=W)
        
        # Children layout in Right_frame
        Right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Bảng điểm danh", font =('times new roman', 16, ' bold '))
        Right_frame.place(x=740, y=5, width=720, height=530)
        
        Table_frame = Frame(Right_frame, bd=2, relief=RIDGE)
        Table_frame.place(x=10, y=10, width=700, height=480)
        
        scroll_x = ttk.Scrollbar(Table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Table_frame, orient=VERTICAL)
        
        columns=("studentID","name","department","time","date","attendanceStatus")
        self.attendanceReportTable = ttk.Treeview(Table_frame, columns=columns, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.attendanceReportTable.xview)
        scroll_y.config(command=self.attendanceReportTable.yview)
        
        # self.attendanceReportTable.heading("attendanceID", text="ID phòng")
        self.attendanceReportTable.heading("studentID", text="MSSV")
        self.attendanceReportTable.heading("name", text="Họ Tên")
        self.attendanceReportTable.heading("department", text="Chuyên Ngành")
        self.attendanceReportTable.heading("time", text="Thời Gian")
        self.attendanceReportTable.heading("date", text="Ngày")
        self.attendanceReportTable.heading("attendanceStatus", text="Trạng Thái")
                                           
        # self.attendanceReportTable.column("attendanceID", width=100)
        self.attendanceReportTable.column("studentID", width=100)
        self.attendanceReportTable.column("name", width=100)
        self.attendanceReportTable.column("department", width=100)
        self.attendanceReportTable.column("time", width=100)
        self.attendanceReportTable.column("date", width=100)
        self.attendanceReportTable.column("attendanceStatus", width=100)      
        
        self.attendanceReportTable["show"]="headings"
        
        self.attendanceReportTable.pack(fill=BOTH, expand=1)

    def fetchData(self, rows):
        self.attendanceReportTable.delete(*self.attendanceReportTable.get_children())
        for i in rows:
            self.attendanceReportTable.insert("",END, values=i)
                    
        
    def importCSV(self):
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File", "*csv"),("ALL File", "*.*")), parent=self.root)
        with open(fln, 'r', encoding='utf-16') as myfile:
            csvread = csv.reader((line.replace('\0','') for line in myfile), delimiter=",")
            for i in csvread:
                print(i)
                mydata.append(i)
                print(mydata)
            self.fetchData(mydata)
    
    
    def exportCSV(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("Dữ liệu rỗng", "Không có dữ liệu để xuất!", parent=self.root)
                return False
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File", "*csv"),("ALL File", "*.*")), parent=self.root)
            with open(fln, mode="w",newline="", encoding='utf-16') as myfile:
                exp_write = csv.writer(myfile, delimiter=",")
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("Xuất dữ liệu", "Xuất dữ liệu thành công: " + os.path.basename(fln))
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"{str(e)}", parent=self.root) 
                
                
if __name__ == "__main__":
    root = Tk()
    app = Attendance(root)
    root.mainloop()