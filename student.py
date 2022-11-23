from sys import prefix
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from turtle import st
from PIL import Image, ImageTk
import mysql.connector  
import cv2
from pathlib import Path

from sklearn.linear_model import Ridge

parent_path = Path(__file__).parent
image_path = (parent_path / "./assets/images/logo_ctu.png").resolve()

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Hệ thống điểm danh sinh viên")
        
        # ----------- Variables -----------
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_sesmester = StringVar()
        self.var_studentID = StringVar()
        self.var_name = StringVar()
        self.var_department = StringVar()
        self.var_classID = StringVar()
        self.var_email = StringVar()
        self.var_DoB = StringVar()
        self.var_gender = StringVar()
        self.var_imagePath = StringVar()
        
        
        img = Image.open(image_path)
        img = img.resize((200,200), Image.ANTIALIAS)
        self.photoImg = ImageTk.PhotoImage(img)
        
        logo_lbl = Label(self.root, image=self.photoImg)
        logo_lbl.place(x=10, y=10, width=200, height=200)
        
        title_lbl = Label(self.root, text="QUẢN LÝ SINH VIÊN",
                          fg="darkgreen", font =('times new roman', 48, ' bold '))
        title_lbl.place(x=480, y=80, width= 640, height=80)
        
        # Main Frame
        main_frame = Frame(background="coral", bd=2)
        main_frame.place(x=20, y=220, width=1480, height=550)  
        
        # Main Layout
        Left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Thông tin sinh viên", font =('times new roman', 16, ' bold '))
        Left_frame.place(x=10, y=5, width=720, height=530)
        
        # Children layout in Left_frame
        
        # ---------- Start of Current Course ----------
        Current_course_frame = LabelFrame(Left_frame, bd=2, relief=RIDGE, text="Thông tin môn học", font =('times new roman', 15, ' bold '))
        Current_course_frame.place(x=10, y=10, width=700, height=140)
        
        # departments - chuyên ngành
        dep_lbl = Label(Current_course_frame, text="Chuyên Ngành", font =('times new roman', 11, 'bold'))
        dep_lbl.grid(row=0, column=0, padx=10, sticky=W)
        
        dep_cbb = ttk.Combobox(Current_course_frame, textvariable=self.var_department, font =('times new roman', 11, 'bold'), state="readonly", width=20)
        dep_cbb["values"] = ("Chọn Chuyên ngành", "Công nghệ thông tin", "Tin học ứng dụng", "Hệ thống thông tin", "Kỹ thuật phần mềm", "Khoa học máy tính")
        dep_cbb.current(0)
        dep_cbb.grid(row=0, column=1, padx=2, pady=10, sticky=W)
        
        # Course - Học phần
        course_lbl = Label(Current_course_frame, text="Học phần", font =('times new roman', 11, 'bold'))
        course_lbl.grid(row=0, column=2, padx=10, sticky=W)
        
        course_cbb = ttk.Combobox(Current_course_frame, textvariable=self.var_course, font =('times new roman', 11, 'bold'), state="readonly", width=20)
        course_cbb["values"] = ("Chọn Học phần", "Công nghệ Web", "Lập trình căn bản", "Lập trình hướng đối tượng", "Trí tuệ nhân tạo")
        course_cbb.current(0)
        course_cbb.grid(row=0, column=3, padx=2, pady=10, sticky=W)
                
        # Year - Năm học
        year_lbl = Label(Current_course_frame, text="Năm học", font =('times new roman', 11, 'bold'))
        year_lbl.grid(row=1, column=0, padx=10, sticky=W)
        
        year_cbb = ttk.Combobox(Current_course_frame, textvariable=self.var_year, font =('times new roman', 11, 'bold'), state="readonly", width=20)
        year_cbb["values"] = ("Chọn Năm học", "2021-2022", "2022-2023", "2023-2024")
        year_cbb.current(0)
        year_cbb.grid(row=1, column=1, padx=2, pady=10, sticky=W)
        
        # Sesmester - Học kì
        sesmester_lbl = Label(Current_course_frame, text="Học kì", font =('times new roman', 11, 'bold'))
        sesmester_lbl.grid(row=1, column=2, padx=10, sticky=W)
        
        sesmester_cbb = ttk.Combobox(Current_course_frame,textvariable=self.var_sesmester, font =('times new roman', 11, 'bold'), state="readonly", width=20)
        sesmester_cbb["values"] = ("Chọn Học kì", "Học kì 1", "Học kì 2", "Học kì hè")
        sesmester_cbb.current(0)
        sesmester_cbb.grid(row=1, column=3, padx=2, pady=10, sticky=W)
        # ---------- End of Current Course ----------
        
         
        # ---------- Start of Class Student ----------
        Class_student_frame = LabelFrame(Left_frame, bd=2, relief=RIDGE, text="Thông tin sinh viên", font =('times new roman', 15, ' bold '))
        Class_student_frame.place(x=10, y=160, width=700, height=330)
        
        studentId_lbl = Label(Class_student_frame, text="MSSV:", font =('times new roman', 11, 'bold'))
        studentId_lbl.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        studentId_entry = ttk.Entry(Class_student_frame,textvariable=self.var_studentID, width=20, font =('times new roman', 11, 'bold'))
        studentId_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        
        studentName_lbl = Label(Class_student_frame, text="Họ Tên:", font =('times new roman', 11, 'bold'))
        studentName_lbl.grid(row=0, column=2, padx=10, pady=10, sticky=W)

        studentName_entry = ttk.Entry(Class_student_frame,textvariable=self.var_name, width=20, font =('times new roman', 11, 'bold'))
        studentName_entry.grid(row=0, column=3, padx=10, pady=10, sticky=W)
        
        studentClassId_lbl = Label(Class_student_frame, text="Lớp:", font =('times new roman', 11, 'bold'))
        studentClassId_lbl.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        studentClassId_entry = ttk.Entry(Class_student_frame,textvariable=self.var_classID, width=20, font =('times new roman', 11, 'bold'))
        studentClassId_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        
        studentEmail_lbl = Label(Class_student_frame, text="Email:", font =('times new roman', 11, 'bold'))
        studentEmail_lbl.grid(row=1, column=2, padx=10, pady=10, sticky=W)

        studentEmail_entry = ttk.Entry(Class_student_frame,textvariable=self.var_email, width=20, font =('times new roman', 11, 'bold'))
        studentEmail_entry.grid(row=1, column=3, padx=10, pady=10, sticky=W)
        
        studentDOB_lbl = Label(Class_student_frame, text="Ngày sinh:", font =('times new roman', 11, 'bold'))
        studentDOB_lbl.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        studentDOB_entry = ttk.Entry(Class_student_frame,textvariable=self.var_DoB, width=20, font =('times new roman', 11, 'bold'))
        studentDOB_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W)
        
        studentGender_lbl = Label(Class_student_frame, text="Giới tính:", font =('times new roman', 11, 'bold'))
        studentGender_lbl.grid(row=2, column=2, padx=10, pady=10, sticky=W)

        # studentGender_entry = ttk.Entry(Class_student_frame,textvariable=self.var_gender, width=20, font =('times new roman', 11, 'bold'))
        # studentGender_entry.grid(row=2, column=3, padx=10, pady=10, sticky=W)
        
        studentGender_cbb = ttk.Combobox(Class_student_frame, textvariable=self.var_gender, font =('times new roman', 11, 'bold'), state="readonly", width=20)
        studentGender_cbb["values"] = ("Chọn giới tính", "Nam", "Nu")
        studentGender_cbb.current(0)
        studentGender_cbb.grid(row=2, column=3, padx=10, pady=10, sticky=W)
        
        
        # Radio buttons
        self.var_radio1 = StringVar()
        take_photo_check_btn = ttk.Radiobutton(Class_student_frame, variable=self.var_radio1, text="Take Photo Sample", value="Yes")
        take_photo_check_btn.grid(row=3, column=0)
        
        no_photo_check_btn = ttk.Radiobutton(Class_student_frame, variable=self.var_radio1, text="No Photo Sample", value="No")
        no_photo_check_btn.grid(row=3, column=1)
        
        # Buttons Frame
        btn_frame = Frame(Class_student_frame, relief=RIDGE)
        btn_frame.place(x=0, y=180, width=680, height=60)
        
        save_btn = Button(btn_frame, text="Thêm", command=self.add_data, width=16, font =('times new roman', 11, ' bold '), bg='teal', fg="white")
        save_btn.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        
        update_btn = Button(btn_frame, text="Cập nhật", command=self.update_data, width=16, font =('times new roman', 11, ' bold '), bg='teal', fg="white")
        update_btn.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        
        delete_btn = Button(btn_frame, text="Xoá", command=self.delete_data, width=16, font =('times new roman', 11, ' bold '), bg='teal', fg="white")
        delete_btn.grid(row=0, column=2, padx=10, pady=10, sticky=W)
        
        reset_btn = Button(btn_frame, text="Reset", command=self.reset_data, width=16, font =('times new roman', 11, ' bold '), bg='teal', fg="white")
        reset_btn.grid(row=0, column=3, padx=10, pady=10, sticky=W)
        
        
        btn_frame1 = Frame(Class_student_frame, relief=RIDGE)
        btn_frame1.place(x=0, y=230, width=680, height=60)
        
        take_photo_btn = Button(btn_frame1, command=self.generate_dataset, text="Take Photo Sample", width=35, font =('times new roman', 11, ' bold '), bg='teal', fg="white")
        take_photo_btn.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        
        update_photo_btn = Button(btn_frame1, text="Update Photo Sample", width=35, font =('times new roman', 11, ' bold '), bg='teal', fg="white")
        update_photo_btn.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        
        # Children layout in Right_frame
        Right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Chi tiết sinh viên", font =('times new roman', 16, ' bold '))
        Right_frame.place(x=740, y=5, width=720, height=530)
        
        # -------------- Start of Searh Frame --------------
        Search_frame = LabelFrame(Right_frame, bd=2, relief=RIDGE, text="Tìm kiếm", font =('times new roman', 15, ' bold '))
        Search_frame.place(x=10, y=10, width=700, height=120)
        
        search_lbl = Label(Search_frame, text="Tìm kiếm bằng:", width=20,font =('times new roman', 13, ' bold '), bg='red', fg='white')
        search_lbl.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        
        search_cbb = ttk.Combobox(Search_frame, font =('times new roman', 11, 'bold'), state="readonly", width=20)
        search_cbb["values"] = ("MSSV", "Họ Tên",)
        search_cbb.current(0)
        search_cbb.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        
        show_all_btn = Button(Search_frame, width=20, text="Hiển thị tất cả", font =('times new roman', 11, ' bold '), bg='teal', fg="white")
        show_all_btn.grid(row=0, column=2, padx=5, pady=5)
        
        Search_frame1 = Frame(Search_frame, relief=RIDGE)
        Search_frame1.place(x=0, y=40, width=680, height=40)
        
        search_entry = ttk.Entry(Search_frame1,width=42, font =('times new roman', 13, 'bold'))
        search_entry.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        
        search_btn = Button(Search_frame1, text="Tìm", width=20, font =('times new roman', 11, ' bold '), bg='teal', fg="white")
        search_btn.grid(row=0, column=1, padx=10, pady=5)
        # -------------- End of Searh Frame --------------
        
        
        # -------------- Start of Table Frame --------------
        Table_frame = Frame(Right_frame, bd=2, relief=RIDGE)
        Table_frame.place(x=10, y=140, width=700, height=350)
        
        scroll_x = ttk.Scrollbar(Table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Table_frame, orient=VERTICAL)
        
        columns=("course","year","sesmester","studentID","name","department","classID","email","DoB","gender","imagePath")
        self.student_table = ttk.Treeview(Table_frame, columns=columns, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)
        
        self.student_table.heading("course", text="Học Phần")
        self.student_table.heading("year", text="Năm Học")
        self.student_table.heading("sesmester", text="Học Kì")  
        self.student_table.heading("studentID", text="MSSV")
        self.student_table.heading("name", text="Họ Tên")
        self.student_table.heading("department", text="Chuyên Ngành")
        self.student_table.heading("classID", text="Lớp")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("DoB", text="Ngày Sinh")
        self.student_table.heading("gender", text="Giới Tính")
        self.student_table.heading("imagePath", text="Hình Ảnh")
        
        self.student_table.column("course", width=100)
        self.student_table.column("year", width=80)
        self.student_table.column("sesmester", width=60)        
        self.student_table.column("studentID", width=60)
        self.student_table.column("name", width=140)
        self.student_table.column("department", width=120)
        self.student_table.column("classID", width=60)
        self.student_table.column("email", width=100)
        self.student_table.column("DoB", width=100)
        self.student_table.column("gender", width=60)
        self.student_table.column("imagePath", width=100)
        
        self.student_table["show"]="headings"
        
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

    # Thêm sinh viên vào CSDL
    def add_data(self):
        if self.var_department.get() == "Chọn Chuyên Ngành" or self.var_name.get() == "" or self.var_studentID == "":
            messagebox.showerror("Lỗi", "Hãy điền đầy đủ thông tin!", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="123456", database="face_recognizer")
                my_cursor = conn.cursor()
                sql = "insert into student values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_sesmester.get(),
                        self.var_studentID.get(),
                        self.var_name.get(),
                        self.var_department.get(),
                        self.var_classID.get(),
                        self.var_email.get(),
                        self.var_DoB.get(),
                        self.var_gender.get(),
                        self.var_radio1.get()
                    )
                my_cursor.execute(sql, val)
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Thành công", "Đã lưu thông tin sinh viên.", parent=self.root)
            except Exception as e:
                messagebox.showerror("Có lỗi xảy ra", f"{str(e)}", parent=self.root)
             
    # Đổ thông tin sinh viên trong CSDL ra bảng student_table
    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="123456", database="face_recognizer")
        my_cursor = conn.cursor()
        
        sql = "SELECT * FROM student"
        my_cursor.execute(sql)
        
        data = my_cursor.fetchall()
        if (len(data)) != 0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data: 
                self.student_table.insert("", END, values=i)
            conn.commit()
        conn.close()
    
    # Bắt sự kiện nhấn vào 1 row trong student_table thì xuất ra dữ liệu sinh viên đó
    def get_cursor(self, event):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]
        
        self.var_course.set(data[0]),
        self.var_year.set(data[1]),
        self.var_sesmester.set(data[2]),
        self.var_studentID.set(data[3]),
        self.var_name.set(data[4]),
        self.var_department.set(data[5]),
        self.var_classID.set(data[6]),
        self.var_email.set(data[7]),
        self.var_DoB.set(data[8]),
        self.var_gender.set(data[9]),
        self.var_radio1.set(data[10])
    
    # Cập nhật thông tin 1 sinh viên
    def update_data(self):
        if self.var_department.get() == "Chọn Chuyên Ngành" or self.var_name.get() == "" or self.var_studentID == "":
            messagebox.showerror("Lỗi", "Hãy điền đầy đủ thông tin!", parent=self.root)
        else:
            try:
                Update = messagebox.askyesno("Cập nhật", "Cập nhật lại thông tin sinh viên này?", parent=self.root)
                if Update > 0:
                    conn = mysql.connector.connect(host="localhost", user="root", password="123456", database="face_recognizer")
                    my_cursor = conn.cursor()
                    sql = "UPDATE student SET course=%s, year=%s, sesmester=%s, name=%s, department=%s, classId=%s, email=%s, DoB=%s, gender=%s, imagePath=%s where studentId=%s"
                    val = (
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_sesmester.get(),
                        self.var_name.get(),
                        self.var_department.get(), 
                        self.var_classID.get(),
                        self.var_email.get(),
                        self.var_DoB.get(),
                        self.var_gender.get(),
                        self.var_radio1.get(),
                        self.var_studentID.get()
                        )
                    print(type(self.var_studentID.get()))
                    my_cursor.execute(sql, val)
                else:
                    if not Update:
                        return
                conn.commit()
                messagebox.showinfo("Thành công", "Cập nhật sinh viên thành công!", parent=self.root) 
                self.fetch_data()
                conn.close()
                  
            except Exception as e:
                messagebox.showerror("Có lỗi xảy ra", f"{str(e)}", parent=self.root) 

    # Xoá 1 sinh viên
    def delete_data(self):
        if self.var_studentID.get() == "":
            messagebox.showerror("Có lỗi xảy ra", "Hãy điền MSSV!", parent=self.root) 
        else:
            try:
                Delete = messagebox.askyesno("Xoá sinh viên", "Bạn có chắc muốn xoá sinh viên này?", parent=self.root)
                if Delete > 0:
                    conn = mysql.connector.connect(host="localhost", user="root", password="123456", database="face_recognizer")
                    my_cursor = conn.cursor()
                    sql = "DELETE FROM student where studentId=%s"
                    val = (self.var_studentID.get(),)
                    my_cursor.execute(sql, val)
                else:
                    if not Delete:
                        return
                conn.commit()
                messagebox.showinfo("Thành công", "Xoá sinh viên thành công!", parent=self.root) 
                self.fetch_data()
                conn.close()
                  
            except Exception as e:
                messagebox.showerror("Có lỗi xảy ra", f"{str(e)}", parent=self.root) 

    # Reset lại dữ liệu về mặc định
    def reset_data(self):
        self.var_course.set("Chọn Học phần")
        self.var_year.set("Chọn Năm học")
        self.var_sesmester.set("Chọn Học kì")
        self.var_studentID.set("")
        self.var_name.set("")
        self.var_department.set("Chọn Chuyên ngành")
        self.var_classID.set("")
        self.var_email.set("")
        self.var_DoB.set("")
        self.var_gender.set("Chọn giới tính")
        self.var_radio1.set("")

    # Tạo dữ liệu khuôn mặt của sinh viên
    def generate_dataset(self):
        if self.var_department.get() == "Chọn Chuyên Ngành" or self.var_name.get() == "" or self.var_studentID == "":
            messagebox.showerror("Lỗi", "Hãy điền đầy đủ thông tin!", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="123456", database="face_recognizer")
                my_cursor = conn.cursor()
                sql = "SELECT * FROM student"
                my_cursor.execute(sql)
                my_results = my_cursor.fetchall()
                
                # count_id = 0
                # for i in my_results:
                #     count_id += 1
                student_id = self.var_studentID.get()
                print(self.var_studentID.get())
                    
                sql = "UPDATE student SET course=%s, year=%s, sesmester=%s, name=%s, department=%s, classId=%s, email=%s, DoB=%s, gender=%s, imagePath=%s where studentId=%s"
                val = (
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_sesmester.get(),
                        self.var_name.get(),
                        self.var_department.get(), 
                        self.var_classID.get(),
                        self.var_email.get(),
                        self.var_DoB.get(),
                        self.var_gender.get(),
                        self.var_radio1.get(),
                        self.var_studentID.get()
                        )
                my_cursor.execute(sql, val)
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                
                # -------------- Tạo dữ liệu khuôn mặt với thư viện open-cv2 --------------
                
                # Mở camera chính của máy với 0, cam phụ với số 1
                cam = cv2.VideoCapture(0)
        
                harcascadePath = "haarcascade_frontalface_default.xml"
                # Tạo phân lớp dựa trên tệp haarcascade.
                detector = cv2.CascadeClassifier(harcascadePath)
                # Initializing the sample number(No. of images) as 0
                sampleNum = 0
                while(True):
                    # Đọc video được quay bằng máy ảnh từng khung hình
                    ret, img = cam.read()
                    # Chuyển đổi hình ảnh qua thangg màu xám
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    
                    # It converts the images in different sizes
                    # (decreases by 1.3 times) and 5 specifies the
                    # number of times scaling happens
                    # Scaling factor = 1.3
                    # Minium neighbors = 5
                    faces = detector.detectMultiScale(gray, 1.3, 5)
                    
                    # Vòng lặp tạo 1 frame bao khuôn mặt
                    for (x, y, w, h) in faces:
                        # Specifying the coordinates of the image as well
                        # as color and thickness of the rectangle.	
                        # incrementing sample number for each image
                        cv2.rectangle(img, (x, y), (
                            x + w, y + h), (255, 0, 0), 2)
                        sampleNum = sampleNum + 1
                        # saving the captured face in the dataset folder
                        # TrainingImage as the image needs to be trained
                        # are saved in this folder
                        file_name_path = ''.join(["data/user.", str(student_id)[1:], ".", str(sampleNum), ".jpg"])
                        cv2.imwrite(file_name_path, img)
                        cv2.putText(img, "Count: "+str(sampleNum), (30,30), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 2)
                        cv2.imwrite(file_name_path, gray[y:y + h, x:x + w])
                        # display the frame that has been captured
                        # and drawn rectangle around it.
                        cv2.imshow('Cropped Face', img)
                    # wait for 100 milliseconds
                    if cv2.waitKey(100) & 0xFF == ord('q'):
                        break
                    # break if the sample number is more than 80
                    elif sampleNum>80:
                        break
                # releasing the resources
                cam.release()
                # closing all the windows
                cv2.destroyAllWindows()
                messagebox.showinfo("Kết quả", "Đã tạo xong tập dữ liệu")
                
            except Exception as e:
                messagebox.showerror("Có lỗi xảy ra", f"{str(e)}", parent=self.root) 
            
            
if __name__ == "__main__":
    root = Tk()
    app = Student(root)
    root.mainloop()