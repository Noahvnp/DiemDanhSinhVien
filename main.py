from tkinter import*
from tkinter import ttk
from turtle import st
from typing import List
from PIL import Image, ImageTk
from pathlib import Path
import os
from time import strftime
from datetime import datetime
import unicodecsv as csv
import mysql.connector  
from tkinter import messagebox
import cv2
import numpy as np

from student import Student
from attendance import Attendance

parent_path = Path(__file__).parent
image_path = (parent_path / "./assets/images/logo_ctu.png").resolve()

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Hệ thống điểm danh sinh viên")
        
        img = Image.open(image_path)
        img = img.resize((200,200), Image.ANTIALIAS)
        self.photoImg = ImageTk.PhotoImage(img)
        
        logo_lbl = Label(self.root, image=self.photoImg)
        logo_lbl.place(x=10, y=10, width=200, height=200)
        
        title_lbl1 = Label(self.root, text="HỆ THỐNG ĐIỂM DANH",
                          fg="darkgreen", font =('times new roman', 48, ' bold '))
        title_lbl1.place(x=420, y=50, width= 800, height=70)
        
        title_lbl2 = Label(self.root, text="GIAO BÀI TẬP SINH VIÊN",
                          fg="darkgreen", font =('times new roman', 48, ' bold '))
        title_lbl2.place(x=420, y=150, width= 800, height=70)
        
        
        student_btn = Button(self.root, cursor="hand2", text ="Quản lý sinh viên",command=self.student_manager, fg ="white", bg ="teal",
					  activebackground = "blue", font =('times new roman', 18, ' bold '))
        student_btn.place(x = 130, y = 300, width = 300, height = 70)
        
        face_detect_btn = Button(self.root, cursor="hand2", text ="Nhận diện sinh viên", command=self.face_recog, fg ="white", bg ="teal",
					  activebackground = "blue", font =('times new roman', 18, ' bold '))
        face_detect_btn.place(x = 600, y = 300, width = 300, height = 70)
        
        attend_btn = Button(self.root, cursor="hand2", text ="Điểm danh sinh viên", command=self.attendance_manager, fg ="white", bg ="teal",
					  activebackground = "blue", font =('times new roman', 18, ' bold '))
        attend_btn.place(x = 1070, y = 300, width = 300, height = 70)
        
        train_data_btn = Button(self.root, cursor="hand2", text ="Train Data",command=self.train_classifier, fg ="white", bg ="teal",
					  activebackground = "blue", font =('times new roman', 18, ' bold '))
        train_data_btn.place(x = 130, y = 500, width = 300, height = 70)
        
        photo_btn = Button(self.root, cursor="hand2", text ="Kho dữ liệu",command=self.open_img_path, fg ="white", bg ="teal",
					  activebackground = "blue", font =('times new roman', 18, ' bold '))
        photo_btn.place(x = 600, y = 500, width = 300, height = 70)
        
        exit_btn = Button(self.root, cursor="hand2", text ="Thoát", command=root.destroy, fg ="white", bg ="teal",
					  activebackground = "blue", font =('times new roman', 18, ' bold '))
        exit_btn.place(x = 1070, y = 500, width = 300, height = 70)
           
    def student_manager(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)
        
    def attendance_manager(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)
    
    def open_img_path(self):
        os.startfile("data")
        
    def train_classifier(self):
        data_dir = ("data")
        imagePaths = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]
        
        faces = []
        ids = []
        
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L') # Gray scale image
            faceNp = np.array(faceImg, 'uint8')
            
            id = int(imagePath.split('\\')[1].split('.')[1])
            faces.append(faceNp)
            ids.append(id)
            
            cv2.imshow("Training Image", faceNp)
            cv2.waitKey(1) == 13
        
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(faces, np.array(ids))
        
        if not os.path.exists('recognizer'):
            os.makedirs('recognizer')
        recognizer.save('recognizer/TrainingData.yml')
        cv2.destroyAllWindows()
        messagebox.showinfo("Thành công", "Hoàn tất train dữ liệu!")
    
    def mark_attendance(self, studentId, name, department):
        with open("DsDiemDanh.csv", "r+", newline="\n", encoding='utf-16') as csvFile:
            myDataList = csvFile.readlines()
            name_list = []
            for line in myDataList:
                entry = line.split((","))
                name_list.append(entry[0])
            if((studentId not in name_list) and (name not in name_list) and (department not in name_list)):
                now = datetime.now()
                day = now.strftime("%d-%m-%Y")
                hour = now.strftime("%H:%M:%S")
                print(day, hour)
                csvFile.writelines(f"\n{studentId},{name},{department},{day},{hour},Hiện diện")
    
    def face_recog(self):
        def draw_boundray(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
            font = cv2.FONT_HERSHEY_COMPLEX
            
            coord = []
            
            for(x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 3)
                id, predict = clf.predict(gray_image[y:y+h, x:x+w])
                confidence = int((100*(1-predict/300)))
                
                conn = mysql.connector.connect(host="localhost", user="root", password="123456", database="face_recognizer")
                my_cursor = conn.cursor()
                
                id_new = 'B' + str(id)
                
                sql = "SELECT name FROM student WHERE studentId=%s"
                val = (id_new,)
                my_cursor.execute(sql, val)
                name = my_cursor.fetchone()
                name = "+".join(name)
                
                sql = "SELECT studentId FROM student WHERE studentId=%s"
                val = (id_new,)
                my_cursor.execute(sql, val)
                mssv = my_cursor.fetchone()
                mssv = "+".join(mssv)
                
                sql = "SELECT department FROM student WHERE studentId=%s"
                val = (id_new,)
                my_cursor.execute(sql, val)
                department = my_cursor.fetchone()
                department = "+".join(department)
                
                if confidence > 77:
                    cv2.putText(img, f"{mssv}", (x, y-55), font, 0.8, (255,255,255), 3)
                    cv2.putText(img, f"{name}", (x, y-30), font, 0.8, (255,255,255), 3)
                    self.mark_attendance(mssv, name, department)
                else:
                    cv2.rectangle(img,(x, y), (x+w, y+h), (0,255,0), 3)  
                    cv2.putText(img, "Unknown Face", (x, y-5), font, 0.8, (255,255,255), 3)

                coord = [x, y, w, y]
            
            return coord
        
        def recognize(img, clf, faceCascade):
            coord = draw_boundray(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
            return img
        
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("recognizer\TrainingData.yml")
        
        cam = cv2.VideoCapture(0)
        while True:
            ret, img = cam.read()
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Nhận diện khuôn mặt", img)
            
            if (cv2.waitKey(1) == 13 or cv2.waitKey(1)== ord('q')):
                break
        cam.release()
        cv2.destroyAllWindows()
            
if __name__ == "__main__":
    root = Tk()
    main = Face_Recognition_System(root)
    root.mainloop()