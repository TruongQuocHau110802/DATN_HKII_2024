#----------------------------import thu vien & Load model face_recognition
import numpy as np
import facenet
import detect_face
import os
import pickle
from PIL import Image
import tensorflow.compat.v1 as tf
modeldir = './model/20180402-114759.pb'
classifier_filename = './class/classifier.pkl'
npy='./npy'
train_img="./data_face"
with tf.Graph().as_default():
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
    with sess.as_default():
        pnet, rnet, onet = detect_face.create_mtcnn(sess, npy)
        minsize = 30  # minimum size of face
        threshold = [0.7,0.8,0.8]  # three steps's threshold
        factor = 0.75  #0.709 for 1200x900 # scale factor
        margin = 44
        image_size = 182
        input_image_size = 160
        facenet.load_model(modeldir)
        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
        embedding_size = embeddings.get_shape()[1]
        classifier_filename_exp = os.path.expanduser(classifier_filename)
        with open(classifier_filename_exp, 'rb') as infile:
            (model, class_names) = pickle.load(infile,encoding='latin1')
#----------------------------import thu vien can thiet
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from tkinter.messagebox import *
from datetime import datetime
from PIL import Image, ImageTk
import hashlib
import gspread
import re
import cv2
import os
import calendar
#----------------------------import thu vien & load model object_detection
from ultralytics import YOLO
model_yolo = YOLO('model/best_object.pt')
#----------------------------Bien khoi tao ban dau
dic_check = {}
check_id = ''
on_GUI_camera = 0
record = 0
output1 = 0
output2 = 0
running = 0
time = 0
show_time = ''
index_loading = 0
status = 0
file =''
warning1 = 0
warning2 = 0
on_notice = 0
scale = 5
zoom1 = 10
zoom2 = 10
list1 = [10,9,8,7,6,5,4,3,2,1]
list2 = ['0% - Minimum','10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90% - Maximum']
list3 = ['0% - 最低限度','10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90% - 最大限度']
button_zoom1 = 0
button_zoom2 = 0
#---------------------------- Đoi ngon ngu
List_Languages = ['Tiếng Việt','中国人']
language = 0
#----------------------------Lay du lieu nguoi dung tu gg sheet
key = gspread.service_account('key/keyggsheet.json')
open = key.open_by_key('1h_vghHolUw0BlphHb8sxSs2BuDyXGvQlBz7W-6B8A9g')
def insert_gg_sheet():
    global dic_check
    data = open.sheet1.get_all_values()
    for i in data:
        dic_check[i[1]] = [i[3],i[2]]
insert_gg_sheet()
#----------------------------Giao dien chinh
def GUI2_supervisor():
    global dic_check,check_id
    GUI2 = Tk()
    GUI2.title('Supervisor')
    GUI2.configure(bg = 'white')
    GUI2.wm_iconbitmap("img/camera.ico")
    screenWidth = GUI2.winfo_screenwidth()
    screenHeight = GUI2.winfo_screenheight()
    width_gui2 = 1295
    height_gui2 = 520
    x = int(screenWidth/2 - width_gui2/2) #left
    y =  int(screenHeight/2 - height_gui2/2) #top
    GUI2.geometry('%dx%d+%d+%d'%(width_gui2,height_gui2,x, y))
    GUI2.resizable(False, False)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#----------------------------
    w1 = LabelFrame(GUI2,width= 315, height= 150)#info
    w2 = LabelFrame(GUI2,width= 333, height= 150)#button
    w4 = LabelFrame(GUI2, width= 647, height= 150)#button
    w6 = LabelFrame(GUI2,bg = 'white', width= 1295, height= 370)
    w1.place(x = 0, y = 370)
    w2.place(x = 315, y = 370)
    w4.place(x = 648, y = 370)
    w6.place(x = 0, y = 0)
#----------------------------Chuc nang doi mat khau
    def change_pw_f():
        clear_widget()
        w8 = LabelFrame(w6,bg = 'white', width= 495, height= 360)
        w8.place(x = 400, y= 3)
        #an/hien mat khau
        def show_pw_1():
            if o_pw_value.cget('show') == '*':
                o_pw_value.config(show = '')
            else:
                o_pw_value.config(show = '*')
        def show_pw_2():
            if n_pw_value.cget('show') == '*':
                n_pw_value.config(show = '')
            else:
                n_pw_value.config(show = '*')
        def show_pw_3():
            if n_pw_confirm_value.cget('show') == '*':
                n_pw_confirm_value.config(show = '')
            else:
                n_pw_confirm_value.config(show = '*')
        #xoa mat khau da nhap  
        def quit_f():
            list = [o_pw_value,n_pw_value,n_pw_confirm_value]
            for i in list:
                i.delete(0,END)
                i.insert(0,'')
        #kiem tra du lieu duoc nhap vao de doi mat khau
        def get_data_change_pw():
            list_convert = [o_pw_value.get(),n_pw_value.get(),n_pw_confirm_value.get()]
            list_converted = []
            for i in list_convert:
                j = hashlib.md5(i.encode('utf-8')).hexdigest()
                list_converted.append(j)
            ####    
            if dic_check[check_id][0] != list_converted[0]:
                if list_converted[0] == 'd41d8cd98f00b204e9800998ecf8427e':
                    if language == 0:
                        showwarning('Warning','Bạn chưa nhập mật khẩu cũ!')
                    else:
                        showwarning('警告','您还没有输入旧密码!')
                else:
                    if language == 0:
                        showwarning('Warning','Mật khẩu hiện tại của bạn sai. Vui lòng nhập lại!')  
                    else:
                        showwarning('警告','您当前的密码不正确. 请重新输入!')
            elif dic_check[check_id][0] == list_converted[0]: #mat khau cu đung
                if list_converted[1] == dic_check[check_id][0]:
                    if language == 0:
                        showwarning('Warning','Mật khẩu mới trùng mật khẩu cũ. Vui lòng nhập lại!')
                    else:
                        showwarning('警告','新密码与旧密码一致. 请重新输入!')    
                elif list_converted[1] != list_converted[2]:
                    if list_converted[2] == 'd41d8cd98f00b204e9800998ecf8427e':
                        if language == 0:
                            showwarning('Warning','Bạn chưa xác nhận mật khẩu mới!')
                        else:
                            showwarning('警告','您还没有确认您的新密码!')              
                    else:
                        if language == 0:
                            showwarning('Warning','Mật khẩu xác nhận sai. Vui lòng nhập lại!')
                        else:
                            showwarning('警告','密码确认错误. 请重新输入!')
                elif list_converted[1] == list_converted[2]:
                    if len(n_pw_value.get()) >= 8:
                        numbers = re.findall('[0-9]+', n_pw_value.get())
                        lowercase_letters = re.findall('[a-z]+', n_pw_value.get())
                        uppercase_letters = re.findall('[A-Z]+', n_pw_value.get())
                        special_characters = re.findall('[^a-zA-Z0-9]+', n_pw_value.get())
                        if len(numbers) and len(lowercase_letters) and len(uppercase_letters) and len(special_characters) >= 1:
                            global open
                            cell = open.sheet1.find(f'{check_id}')
                            row = cell.row
                            update = open.sheet1.update_cell(row,4,f'{list_converted[2]}')
                            insert_gg_sheet()
                            if language == 0:
                                showwarning('Notice','Đổi mật khẩu thành công. Hãy đăng nhập lại!')
                            else:
                                showwarning('注意','密码修改成功. 请重新登录!')
                            quit_GUI2()
                        else:
                            listvietnamese = ['Thiếu chữ số', 'Thiếu chữ thường', 'Thiếu chữ in', 'Thiếu kí tự đặc biệt']
                            listchinese = ['缺少数字', '缺少小写字母', '缺少大写字母', '缺少特殊字符']
                            text = ''
                            rate = 0
                            if language == 0:
                                if len(numbers) < 1:
                                    text = text + listvietnamese[0] 
                                    rate = 1  
                                if len(lowercase_letters) < 1:
                                    if rate == 0:
                                        text = text + listvietnamese[1]
                                    else:
                                        text = text +'. ' + listvietnamese[1]
                                    rate = 1
                                if len(uppercase_letters) < 1:
                                    if rate == 0:
                                        text = text + listvietnamese[2]
                                    else:
                                        text = text +'. ' + listvietnamese[2]
                                    rate = 1 
                                if len(special_characters) < 1:
                                    if rate == 0:
                                        text = text + listvietnamese[3]
                                    else:
                                        text = text +'. '+ listvietnamese[3]
                                    rate = 1
                                showwarning('Warning',f'{text}. Vui lòng nhập lại!')
                            else:
                                if len(numbers) < 1:
                                    text = text + listchinese[0] 
                                    rate = 1  
                                if len(lowercase_letters) < 1:
                                    if rate == 0:
                                        text = text + listchinese[1]
                                    else:
                                        text = text +'. ' + listchinese[1]
                                    rate = 1
                                if len(uppercase_letters) < 1:
                                    if rate == 0:
                                        text = text + listchinese[2]
                                    else:
                                        text = text +'. ' + listchinese[2]
                                    rate = 1 
                                if len(special_characters) < 1:
                                    if rate == 0:
                                        text = text + listchinese[3]
                                    else:
                                        text = text +'. '+ listchinese[3]
                                    rate = 1
                                showwarning('警告',f'{text}. 请重新输入!')
                    elif n_pw_value.get() == '':
                        if language == 0:
                            showwarning('Warning','Bạn chưa nhập mật khẩu mới!')
                        else:
                            showwarning('警告','您还没有输入新密码!')    
                    else:
                        if language == 0:
                            showwarning('Warning','Mật khẩu mới chưa đủ 8 kí tự. Vui lòng nhập lại!')
                        else:
                            showwarning('警告','新密码长度少于 8 个字符. 请重新输入!')              
#----------------------------
        if language == 0:
            c1 = Label(w8,text = 'Đổi mật khẩu',font = ('Arial', 23, 'bold'), fg = '#57a1f8', bg = 'white' ).place(x = 148 , y = 20)

            o_pw = Label(w8,text = "Mật khẩu hiện tại:",font = ('Arial', 12),bg = 'white').place(x = 80 , y = 70)
            o_pw_value = Entry(w8, font = ('Arial', 12),width = 19, show ='*',relief=RIDGE)
            o_pw_value.place( x = 80, y = 100)

            n_pw = Label(w8,text = "Mật khẩu mới:",font = ('Arial', 12),bg = 'white').place(x = 80 , y = 130)
            n_pw_value = Entry(w8, font = ('Arial', 12),width = 19, show ='*',relief=RIDGE)
            n_pw_value.place( x = 80, y = 160)

            note = Label(w8,text='Hãy sử dụng ít nhất 8 kí tự bao gồm chữ số,   \nchữ thường, chữ in và kí tự đặc biệt (!,@,#,...)',fg = 'red',font = ('Arial', 12),bg = 'white').place(x = 80, y = 190)

            n_pw_confirm = Label(w8,text = "Xác nhận mật khẩu mới:",font = ('Arial', 12),bg = 'white').place(x = 80 , y = 230)
            n_pw_confirm_value = Entry(w8, font = ('Arial', 12),width = 19, show ='*',relief=RIDGE)
            n_pw_confirm_value.place( x = 80, y = 260)

            save = Button(w8,text = "Lưu thay đổi",font = ('Arial', 12),width = 10, bd = 0,bg= '#1e90ff', fg = 'white', command=get_data_change_pw).place(x = 100 , y = 300)
            quit = Button(w8,text = "Hủy bỏ"      ,font = ('Arial', 12),width = 10, bd = 0,command=quit_f).place(x = 280 , y = 300)

            show_pw1  = Checkbutton(w8, text= 'Hiện mật khẩu', font = ('Arial', 12),bg = 'white', activebackground= 'white', command=show_pw_1).place( x = 280, y = 100 )
            show_pw2  = Checkbutton(w8, text= 'Hiện mật khẩu', font = ('Arial', 12),bg = 'white', activebackground= 'white', command=show_pw_2).place( x = 280, y = 160 )
            show_pw3  = Checkbutton(w8, text= 'Hiện mật khẩu', font = ('Arial', 12),bg = 'white', activebackground= 'white', command=show_pw_3).place( x = 280, y = 260 )
        else:
            c1 = Label(w8,text = '更改密码',font = ('Arial', 23, 'bold'), fg = '#57a1f8', bg = 'white' ).place(x = 180 , y = 20)
            o_pw = Label(w8,text = "当前密码:",font = ('Arial', 12),bg = 'white').place(x = 80 , y = 70)
            o_pw_value = Entry(w8, font = ('Arial', 12),width = 19, show ='*',relief=RIDGE)
            o_pw_value.place( x = 80, y = 100)

            n_pw = Label(w8,text = "新密码:",font = ('Arial', 12),bg = 'white').place(x = 80 , y = 130)
            n_pw_value = Entry(w8, font = ('Arial', 12),width = 19, show ='*',relief=RIDGE)
            n_pw_value.place( x = 80, y = 160)

            note = Label(w8,text='请使用至少 8 个字符, 包括数字, 小写字母,\n大写字母和特殊字符 (!,@,#,...)                   ',fg = 'red',font = ('Arial', 12),bg = 'white').place(x = 80, y = 190)

            n_pw_confirm = Label(w8,text = "确认新密码:",font = ('Arial', 12),bg = 'white').place(x = 80 , y = 230)
            n_pw_confirm_value = Entry(w8, font = ('Arial', 12),width = 19, show ='*',relief=RIDGE)
            n_pw_confirm_value.place( x = 80, y = 260)

            save = Button(w8,text = "保存更改",font = ('Arial', 12),width = 10, bd = 0,bg= '#1e90ff', fg = 'white', command=get_data_change_pw).place(x = 100 , y = 300)
            quit = Button(w8,text = "取消"      ,font = ('Arial', 12),width = 10, bd = 0,command=quit_f).place(x = 280 , y = 300)

            show_pw1  = Checkbutton(w8, text= '显示密码', font = ('Arial', 12),bg = 'white', activebackground= 'white', command=show_pw_1).place( x = 280, y = 100 )
            show_pw2  = Checkbutton(w8, text= '显示密码', font = ('Arial', 12),bg = 'white', activebackground= 'white', command=show_pw_2).place( x = 280, y = 160 )
            show_pw3  = Checkbutton(w8, text= '显示密码', font = ('Arial', 12),bg = 'white', activebackground= 'white', command=show_pw_3).place( x = 280, y = 260 )
#---------------------------Chuc nang thong bao
    def notice_f():
        clear_widget()
        w7 = LabelFrame(w6,bg = 'white', width= 480, height= 365)
        w8 = LabelFrame(w6,bg = 'white', width= 810, height= 365)
        w7.place(x = 0, y = 0)
        w8.place(x = 480, y = 0)
        w9 = LabelFrame(w7)
        w9.place(x = 2, y = 60)
        if language == 0:
            l1 = Label(w7,text = 'Thông báo',font = ('Arial', 23, 'bold'), fg = '#57a1f8', bg = 'white' ).place(x = 157 , y = 5)
        else:
            l1 = Label(w7,text = '通知',font = ('Arial', 23, 'bold'), fg = '#57a1f8', bg = 'white' ).place(x = 204 , y = 5)
#---------------------------
        style = ttk.Style()
        style.theme_use("default")
        style.configure("mystyle.Treeview.Heading", font=('Arial', 13))
        scroll = Scrollbar(w9)
        scroll.pack(side=RIGHT, fill=Y)
        table = ttk.Treeview(w9,show='headings',height = 10,style="mystyle.Treeview",yscrollcommand = scroll.set)
        table['columns'] = ('1','2','3')
        table.column('1', width=50,minwidth = 50)
        table.column('2', width=200,minwidth = 200)
        table.column('3', width=200,minwidth = 200)
        if language == 0:
            table.heading('1',text = 'STT')
            table.heading('2',text = 'Máy ảnh 1')
            table.heading('3',text = 'Máy ảnh 2')
        else:
            table.heading('1',text = 'STT')
            table.heading('2',text = '相机 1')
            table.heading('3',text = '相机 2')
        table.pack()
        scroll.config(command=table.yview)
        #Lay du lieu
        input_data_table = './record/image/' #duong dan
        def data():
            global today, previous_day
            previous_day_f()
            directory = os.listdir(input_data_table)
            list1 = []
            list2 = []
            list3 = []
            for item in directory:
                    if item[:8] == today or item[:8] == previous_day: #lay du lieu 2 days lien ke
                        if item[-6:-4] == 'c1':
                            list1.append(item)
                        else:
                            list2.append(item)
            for c1 in list1:
                for c2 in list2:
                    if c1[:15] == c2[:15]:
                        list3.append([c1,c2])
            #insert du lieu vao table
            STT = 1
            for x in list3:
                table.insert('',END,values=(STT,x[0],x[1]))
                STT +=1
#---------------------------
        def item_selected(event): #chon file
            global file,status
            status = 0
            clear_w8()
            if language == 0:
                l2.config(text = 'Máy ảnh 1')
            else:
                l2.config(text = '相机 1')
            for selected_item in table.selection():
                item = table.item(selected_item)
                file = item['values']
                open_file()
        table.bind('<<TreeviewSelect>>', item_selected)
#---------------------------
        def open_file():# mo file & hien thi 
            global file,status
            clear_w8()
            if status == 0:
                openfile = Image.open(input_data_table + file[1])
            else:
                openfile = Image.open(input_data_table + file[2])
            n_openfile = openfile.resize((640,360), Image.Resampling.LANCZOS)
            showfile = ImageTk.PhotoImage(n_openfile)
            show = Label(w8,image = showfile,bd = 0,bg = 'white')
            show.place(x=85,y=0)
            mainloop()
        def clear_w8():
            if len(w8.winfo_children()) != 0:
                for widget in w8.winfo_children():
                    widget.destroy()   
        def reset():
            global file
            file =''
            for record in table.get_children():
                table.delete(record)
            data()
            clear_w8()
        def delete():
            global file
            if file == '':
                pass
            else:
                if language == 0:
                    ask = askokcancel('Asking','Bạn chắc chắn sẽ xóa ảnh vừa chọn chứ?')
                else:
                    ask = askokcancel('询问','您确定要删除刚刚选择的照片吗 ?')
                if ask == True:
                    if os.path.isfile(input_data_table + file[1]) and os.path.isfile(input_data_table + file[2]):
                        os.remove(input_data_table + file[1])
                        os.remove(input_data_table + file[2])
                        for record in table.get_children():
                            table.delete(record)
                        data()
                        clear_w8()
                        file = '' 
                        if language == 0:
                            showinfo('Notice','Đã xóa ảnh!')
                        else:
                            showinfo('注意','照片已删除 !')
                else:
                    pass         
        def next_file(): 
            global status
            if file == '':
                pass
            else:
                if language == 0:
                    l2.config(text = 'Máy ảnh 2')
                else:
                    l2.config(text = '相机 2')
                status = 1
                open_file()
        def back_file():
            global status
            if file =='':
                pass
            else:
                if language == 0:
                    l2.config(text = 'Máy ảnh 1')
                else:
                    l2.config(text = '相机 1')
                status = 0
                open_file()
        def today_search():
            global today, previous_day
            previous_day_f()
            clear_w8()
            directory = os.listdir(input_data_table)
            list1 = []
            list2 = []
            list3 = []
            for record in table.get_children():
                table.delete(record)
            for item in directory:
                    if item[:8] == today:
                        if item[-6:-4] == 'c1':
                            list1.append(item)
                        else:
                            list2.append(item)
            for c1 in list1:
                for c2 in list2:
                    if c1[:15] == c2[:15]:
                        list3.append([c1,c2])
            STT = 1
            for x in list3:
                table.insert('',END,values=(STT,x[0],x[1]))
                STT +=1
        def previousday_search():
            global today, previous_day
            previous_day_f()
            clear_w8()
            for record in table.get_children():
                table.delete(record)
            directory = os.listdir(input_data_table)
            list1 = []
            list2 = []
            list3 = []
            for item in directory:
                    if item[:8] == previous_day:
                        if item[-6:-4] == 'c1':
                            list1.append(item)
                        else:
                            list2.append(item)
            for c1 in list1:
                for c2 in list2:
                    if c1[:15] == c2[:15]:
                        list3.append([c1,c2])
            STT = 1
            for x in list3:
                table.insert('',END,values=(STT,x[0],x[1]))
                STT +=1
#---------------------------      
        img_next = PhotoImage(file = 'img/next_icon.png')
        img_back = PhotoImage(file = 'img/back_icon.png')
        if language == 0:
            today = Button(w7,text = "Hôm nay",font = ('Arial', 12), bd = 0,width = 10,command=today_search).place(x =55 , y = 295)
            previousday = Button(w7,text = "Hôm qua",font = ('Arial', 12), bd = 0,width = 10,command=previousday_search).place(x =55 , y = 325)

            delete = Button(w7,text = "Xóa",font = ('Arial', 12), bd = 0,width = 10,bg= '#1e90ff', fg = 'white', command=delete).place(x =153 , y = 295)
            reset = Button(w7,text = "Quay lại",font = ('Arial', 12), bd = 0,width = 10 ,command=reset).place(x = 153 , y = 325)
            l2 = Label(w7,text = 'Máy ảnh 1',font = ('Arial', 12), bg = 'white')
            l2.place(x=326,y=312)

            next = Button(w7,compound="left",image = img_next,activebackground='white',width = 24,font = ('Arial', 12), bd = 0,bg ='white',command=next_file).place(x = 400 , y = 310)
            back = Button(w7,compound="left",image = img_back,activebackground='white',width = 24,font = ('Arial', 12), bd = 0,bg ='white',command=back_file).place(x = 300 , y = 310)
        else:
            today = Button(w7,text = "今天",font = ('Arial', 12), bd = 0,width = 10,command=today_search).place(x =55 , y = 295)
            previousday = Button(w7,text = "昨天",font = ('Arial', 12), bd = 0,width = 10,command=previousday_search).place(x =55 , y = 325)

            delete = Button(w7,text = "删除照片",font = ('Arial', 12), bd = 0,width = 10,bg= '#1e90ff', fg = 'white', command=delete).place(x =153 , y = 295)
            reset = Button(w7,text = "返回",font = ('Arial', 12), bd = 0,width = 10 ,command=reset).place(x = 153 , y = 325)
            l2 = Label(w7,text = '相机 1',font = ('Arial', 12), bg = 'white')
            l2.place(x=340,y=312)

            next = Button(w7,compound="left",image = img_next,activebackground='white',width = 24,font = ('Arial', 12), bd = 0,bg ='white',command=next_file).place(x = 400 , y = 310)
            back = Button(w7,compound="left",image = img_back,activebackground='white',width = 24,font = ('Arial', 12), bd = 0,bg ='white',command=back_file).place(x = 300 , y = 310)         
        data()
        mainloop()
#---------------------------
    def previous_day_f():
        global today, previous_day
        today = datetime.now().strftime('%Y%m%d')
        month1 = ['05','07','10','12']#=>thang30d
        month2 = ['02','04','06','08','09','11']# =>31d
        day = today[-2:]
        month = today[4:6]
        year = today[:4]
        if day == '01' and month == '01':
            previous_day = f'{int(year) - 1}'+ '12'+ '31'
        elif calendar.isleap(int(year)) == True:
            if day == '01' and month == '03':
                previous_day = year + '02' + '29'
            elif day == '01' and month in month1:
                previous_month = int(month) - 1
                previous_day = year + '{:02d}'.format(previous_month) + '30'
            elif day == '01' and month in month2:
                previous_month = int(month) - 1
                previous_day = year + '{:02d}'.format(previous_month) + '31'
            else:
                previous_day = year + month + '{:02d}'.format(int(day) - 1)
        elif calendar.isleap(int(year)) == False:
            if day == '01' and month == '03':
                previous_day = year + '02' + '28'
            elif day == '01' and month in month1:
                previous_month = int(month) - 1
                previous_day = year + '{:02d}'.format(previous_month) + '30'
            elif day == '01' and month == '09':
                previous_month = int(month) - 1
                previous_day = year + '{:02d}'.format(previous_month) + '31'
            else:
                previous_day = year + month + '{:02d}'.format(int(day) - 1)   
    def notice_of_camera():
        global today, previous_day,on_notice
        if on_notice == 1:
            previous_day_f()
            l1 = Label(w4)
            l1.place(x = 60, y = 60)
            input_data_table = './record/image/' #duong dan
            directory = os.listdir(input_data_table)
            list = []
            for item in directory:
                    if item[:8] == today or item[:8] == previous_day: #lay du lieu 2 days lien ke
                        list.append(item)
            if len(list) != 0:
                if language == 0:
                    l1.config(text = 'Hãy kiểm tra thông báo!',font = ('Arial', 12))
                else:
                    l1.config(text = '          请查看通知!      ',font = ('Arial', 12))
            w4.after(10000,notice_of_camera)
#---------------------------Chuc nang may anh
    def camera_f():
        clear_widget()
        if language == 0:
            l1 = Label(w4, text = 'Chọn Camera USB/ Camera IP',font = ('Arial', 12,'bold'),fg= '#1e90ff')
            l1.place( x=350, y= 10)
            l2 = Label(w4, text = 'Máy ảnh 1:',font = ('Arial', 12)).place( x=310, y= 40)
            e1 = Entry(w4, font = ('Arial', 12),width = 25)
            e1.place(x = 400, y = 40)
            l3 = Label(w4, text = 'Máy ảnh 2:',font = ('Arial', 12)).place( x=310, y= 70)
            e2 = Entry(w4, font = ('Arial', 12),width = 25)
            e2.place(x = 400, y = 70)
        else:
            l1 = Label(w4, text = '选择 Camera USB/ Camera IP',font = ('Arial', 12,'bold'),fg= '#1e90ff')
            l1.place( x=350, y= 10)
            l2 = Label(w4, text = '相机 1:',font = ('Arial', 12)).place( x=340, y= 40)
            e1 = Entry(w4, font = ('Arial', 12),width = 25)
            e1.place(x = 400, y = 40)
            l3 = Label(w4, text = '相机 2:',font = ('Arial', 12)).place( x=340, y= 70)
            e2 = Entry(w4, font = ('Arial', 12),width = 25)
            e2.place(x = 400, y = 70)
#---------------------------
        def access_f():
            global option1, option2, on_GUI_camera
            option1 = e1.get()
            option2 = e2.get()
            camera1_ok = 0
            camera2_ok = 0
            if len(option1) == 1:
                check1 = re.findall('[0-9]+', option1) #phong tru truong hop nguoi dung nhap nham chu cai
                if check1 == []:
                    if language == 0:
                        showwarning('Warning',"Cú pháp 'Camera USB1' sai. Hãy nhập số!")
                    else:
                        showwarning('警告',"'Camera USB1' 语法错误. 请输入号码!")
                else:                  
                    option1 = int(option1)
                    camera1_ok = 1
            else:
                camera1_ok = 1

            if len(option2) == 1:
                check2 = re.findall('[0-9]+', option2)
                if check2 == []:
                    if language == 0:
                        showwarning('Warning',"Cú pháp 'Camera USB2' sai. Hãy nhập số!")
                    else:
                        showwarning('警告',"'Camera USB2' 语法错误. 请输入号码!")
                else:                  
                    option2 = int(option2)
                    camera2_ok = 1
            else:
                camera2_ok = 1

            if option1 == '' or option2 == '':
                if language == 0:
                    showwarning('Warning','Chọn đủ 2 máy ảnh!')
                else:
                    showwarning('警告','选择 2 个相机！')                  
            elif camera1_ok == 1 and camera2_ok == 1:
                on_GUI_camera = 1
                on_GUI_camera_f()
                access.destroy()
                e1.destroy()
                e2.destroy()
                if language == 0:
                    l1.config(text = 'Phóng to/ Thu nhỏ')
                    l1.place(x = 370, y = 10)
                else:
                    l1.config(text = '放大/ 缩小')
                    l1.place(x = 405, y = 10)
                    
                def zoom_in_1_f():
                    global zoom1
                    if zoom1 in [10,9,8,7,6,5,4,3,2]:
                        zoom1 -=1
                        if zoom1 in list1:
                            i = list1.index(zoom1)
                            if language == 0:
                                percent_1.config(text = f'{list2[i]}')
                            else:
                                percent_1.config(text = f'{list3[i]}')       
                def zoom_out_1_f():
                    global zoom1
                    if zoom1 in [1,2,3,4,5,6,7,8,9]:
                        zoom1 +=1
                        if zoom1 in list1:
                            i = list1.index(zoom1)
                            if language == 0:
                                percent_1.config(text = f'{list2[i]}')
                            else:
                                percent_1.config(text = f'{list3[i]}')

                def zoom_in_2_f():
                    global zoom2
                    if zoom2 in [10,9,8,7,6,5,4,3,2]:
                        zoom2 -=1
                        if zoom2 in list1:
                            i = list1.index(zoom2)
                            if language == 0:
                                percent_2.config(text = f'{list2[i]}')
                            else:
                                percent_2.config(text = f'{list3[i]}')       
                def zoom_out_2_f():
                    global zoom2
                    if zoom2 in [1,2,3,4,5,6,7,8,9]:
                        zoom2 +=1
                        if zoom2 in list1:
                            i = list1.index(zoom2)
                            if language == 0:
                                percent_2.config(text = f'{list2[i]}')
                            else:
                                percent_2.config(text = f'{list3[i]}')                  
                #[10 ,9   ,8   ,7   ,6   ,5   ,4   ,3   ,2   ,   1]
                #[0% , 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%]
                            
                img_zoom_in = PhotoImage(file = 'img/zoomin_icon.png')
                img_zoom_out = PhotoImage(file = 'img/zoomout_icon.png')
                if language == 0:
                    percent_1 = Label(w4,text = '0% - Minimum',font = ('Arial', 12))
                    percent_2 = Label(w4,text = '0% - Minimum',font = ('Arial', 12))
                else:
                    percent_1 = Label(w4,text = '0% - 最低限度',font = ('Arial', 12))
                    percent_2 = Label(w4,text = '0% - 最低限度',font = ('Arial', 12))

                percent_1.place(x = 490, y = 40)
                zoom_in_1 = Button(w4,compound="left",image = img_zoom_in,width = 25,font = ('Arial', 12), bd = 0,command=zoom_in_1_f)
                zoom_in_1.place(x = 450 , y = 40)
                zoom_out_1 = Button(w4,compound="left",image = img_zoom_out,width = 25,font = ('Arial', 12), bd = 0, command=zoom_out_1_f)
                zoom_out_1.place(x = 410 , y = 40)
                
                percent_2.place(x = 490, y = 70)
                zoom_in_2 = Button(w4,compound="left",image = img_zoom_in,width = 25,font = ('Arial', 12), bd = 0,command=zoom_in_2_f)
                zoom_in_2.place(x = 450 , y = 70)
                zoom_out_2 = Button(w4,compound="left",image = img_zoom_out,width = 25,font = ('Arial', 12), bd = 0, command=zoom_out_2_f)
                zoom_out_2.place(x = 410 , y = 70)
                if button_zoom1 == 1:
                    zoom_in_1.config(state=DISABLED)
                    zoom_out_1.config(state=DISABLED)
                if button_zoom2 == 1:
                    zoom_in_2.config(state=DISABLED)
                    zoom_out_2.config(state=DISABLED)
                mainloop()
         
        def on_GUI_camera_f():
            if on_GUI_camera ==1:
                global video1,video2,record,on_notice
                on_notice = 1
                width = 640
                height = 360
                
                video1 = cv2.VideoCapture(option1)
                video1.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
                video1.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                video1.set(cv2.CAP_PROP_FPS, 30)

                video2 = cv2.VideoCapture(option2)
                video2.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
                video2.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                video2.set(cv2.CAP_PROP_FPS, 30)

                w3 = LabelFrame(w6,bg = 'white', width= 645, height= 365)#camera1
                w5 = LabelFrame(w6,bg = 'white', width= 645, height= 365)#camera2

                w3.place(x = 0, y = 0)
                w5.place(x = 645, y = 0)
                cam1 = Label(w3,bd = 0,bg = 'white')
                cam1.place(x = 0, y = 0)
                cam2 = Label(w5,bd = 0,bg = 'white')
                cam2.place(x = 0, y = 0) 
                def open_camera1_2_f():
                    global record, output1,output2,frame1,frame2,button_zoom1, button_zoom2
                    sucess1, frame1 = video1.read()
                    sucess2, frame2 = video2.read()
                    if sucess1 == True:

                        centerX_original = int(frame1.shape[1]/2)
                        centerY_original = int(frame1.shape[0]/2)
                        xmin_original = centerX_original - 320
                        xmax_original = centerX_original + 320
                        ymin_original = centerY_original - 180
                        ymax_original = centerY_original + 180
                        frame1 = frame1[ymin_original:ymax_original,xmin_original:xmax_original]

                        radiusY = int(scale*height/100)
                        radiusX =  int(scale*width/100)
                        centerX = int(width/2)
                        centerY = int(height/2)

                        xmin = centerX - zoom1*radiusX
                        xmax = centerX + zoom1*radiusX
                        ymin = centerY - zoom1*radiusY
                        ymax = centerY + zoom1*radiusY

                        frame1 = frame1[ymin:ymax,xmin:xmax]
                        frame1 = cv2.resize(frame1, (width, height))

                        if record == 1:
                            output1.write(frame1)
                        cv2.putText(frame1,'Camrera 1',(0 ,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)
                        face_recognition()
                        opencv_image1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB) 
                        captured_image1 = Image.fromarray(opencv_image1) 
                        photo_image1 = ImageTk.PhotoImage(image = captured_image1)
                        cam1.photo_image = photo_image1
                        cam1.configure(image=photo_image1)
                    else:
                        cam1.config(text = 'No Video',font = ('Arial', 23),fg= '#1e90ff')
                        cam1.place(x = 257,y = 162)
                        button_zoom1 = 1
                    if sucess2 == True:

                        centerX_original = int(frame2.shape[1]/2)
                        centerY_original = int(frame2.shape[0]/2)
                        xmin_original = centerX_original - 320
                        xmax_original = centerX_original + 320
                        ymin_original = centerY_original - 180
                        ymax_original = centerY_original + 180
                        frame2 = frame2[ymin_original:ymax_original,xmin_original:xmax_original]

                        radiusY = int(scale*height/100)
                        radiusX =  int(scale*width/100)
                        centerX = int(width/2)
                        centerY = int(height/2)

                        xmin = centerX - zoom2*radiusX
                        xmax = centerX + zoom2*radiusX
                        ymin = centerY - zoom2*radiusY
                        ymax = centerY + zoom2*radiusY

                        frame2 = frame2[ymin:ymax,xmin:xmax]
                        frame2 = cv2.resize(frame2, (width, height))

                        if record == 1:
                            output2.write(frame2)
                        cv2.putText(frame2,'Camrera 2',(0 ,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)
                        object_detection()
                        opencv_image2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB) 
                        captured_image2 = Image.fromarray(opencv_image2) 
                        photo_image2 = ImageTk.PhotoImage(image = captured_image2)
                        cam2.photo_image2 = photo_image2
                        cam2.configure(image=photo_image2)
                    else:
                        cam2.config(text = 'No Video',font = ('Arial', 23),fg= '#1e90ff')
                        cam2.place(x= 257, y= 162)
                        button_zoom2 = 1

                    w6.after(1, open_camera1_2_f)
                def face_recognition():
                    global frame1,warning1
                    bounding_boxes, _ = detect_face.detect_face(frame1, minsize, pnet, rnet, onet, threshold, factor)
                    faceNum = bounding_boxes.shape[0]
                    if faceNum > 0:
                        det = bounding_boxes[:, 0:4]
                        img_size = np.asarray(frame1.shape)[0:2]
                        cropped = []
                        scaled = []
                        scaled_reshape = []
                        for i in range(faceNum):
                            emb_array = np.zeros((1, embedding_size))
                            xmin = int(det[i][0])
                            ymin = int(det[i][1])
                            xmax = int(det[i][2])
                            ymax = int(det[i][3])
                            try:
                                cropped.append(frame1[ymin:ymax, xmin:xmax,:])
                                cropped[i] = facenet.flip(cropped[i], False)
                                scaled.append(np.array(Image.fromarray(cropped[i]).resize((image_size, image_size))))
                                scaled[i] = cv2.resize(scaled[i], (input_image_size,input_image_size),
                                                        interpolation=cv2.INTER_CUBIC)
                                scaled[i] = facenet.prewhiten(scaled[i])
                                scaled_reshape.append(scaled[i].reshape(-1,input_image_size,input_image_size,3))
                                feed_dict = {images_placeholder: scaled_reshape[i], phase_train_placeholder: False}
                                emb_array[0, :] = sess.run(embeddings, feed_dict=feed_dict)
                                predictions = model.predict_proba(emb_array)
                                best_class_indices = np.argmax(predictions, axis=1)
                                best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]

                                if best_class_probabilities>0.9:
                                    result_names = class_names[best_class_indices[0]]
                                    if result_names == check_id:#nguoi duoc nhan dien voi do chinh xac cao va dang dung phan mem
                                        cv2.rectangle(frame1, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)    #boxing face
                                        cv2.putText(frame1, result_names + ' '+ str(round(best_class_probabilities[0], 2)) , (xmin,ymin-5),
                                                    cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (0, 255,255),1,1)
                                        warning1 = 1
                                    else:#nguoi duoc nhan dien do chinh xac cao nhung ko dang nhap phan mem
                                        cv2.rectangle(frame1, (xmin, ymin), (xmax, ymax), (0, 0, 255), 1)
                                        cv2.putText(frame1, "?", (xmin,ymin-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255,255),1,1)
                                        warning1 = 2                                       
                                else :#đo chinh xac chua cao
                                    cv2.rectangle(frame1, (xmin, ymin), (xmax, ymax), (0, 0, 255), 1)
                                    cv2.putText(frame1, "?", (xmin,ymin-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255,255),1,1)
                                    warning1 = 2
                            except:
                                print("error")
                    else:#khong co mat nguoi
                        warning1 = 3
                def object_detection():
                    global frame2,warning2
                    cv2.rectangle(frame2,(0,200),(639,359),(0,0,255),1)
                    results = model_yolo(frame2)
                    for result in results:
                        boxes = result.boxes.numpy()
                        name = result.names
                        for box in boxes:
                            x1 = int(box.xyxy[0][0])
                            y1 = int(box.xyxy[0][1])
                            x2 = int(box.xyxy[0][2])
                            y2 = int(box.xyxy[0][3])
                            if y2 >= 200:
                                if box.conf[0] >= 0.8:
                                    cv2.putText(frame2,name[box.cls[0]]+ ' ' + str(round(box.conf[0],2)),(x1 ,y1 - 5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0, 255,255),1)
                                    cv2.rectangle(frame2,(x1,y1),(x2,y2),(0,0,255),1)
                                    cap_img()
                                else:
                                    cv2.putText(frame2,'?',(x1 ,y1 - 5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,255),1)
                                    cv2.rectangle(frame2,(x1,y1),(x2,y2),(0,0,255),1)
                                warning2 = 1

                def cap_img():
                    global warning1, warning2, frame1, frame2
                    if warning2 == 1 and warning1 == 1:#antoan
                        pass
                    elif warning2 == 1 and warning1 ==2:#cokegian
                        time_cap()
                    elif warning2 == 1 and warning1 == 3:#khongthaymat
                        time_cap()
                def time_cap():
                    global frame1,frame2,warning1, warning2
                    path = './record/image/' #duong dan den thu muc luu hinh chup
                    directory = os.listdir(path)
                    begin_cap = datetime.now().strftime('%Y%m%d_%H%M%S')
                    if len(directory)==0:
                        cv2.imwrite(f'{path}{begin_cap}_c1.jpg',frame1)
                        cv2.imwrite(f'{path}{begin_cap}_c2.jpg',frame2)
                    else:
                        twofile = directory[-2:]
                        hour_ago = int(twofile[0][9:11])
                        hour = int(begin_cap[9:11])
                        minute_ago = int(twofile[0][11:13])
                        minute = int(begin_cap[11:13])
                        second_ago = int(twofile[0][13:15])
                        second = int(begin_cap[13:15])
                        total_second_ago = hour_ago*60*60 + minute_ago*60 + second_ago
                        total_second = hour*60*60 + minute*60 + second
                        tolerance = abs(total_second - total_second_ago)
                        if tolerance >= 10:#sau 10s moi chup tiep
                            cv2.imwrite(f'{path}{begin_cap}_c1.jpg',frame1)
                            cv2.imwrite(f'{path}{begin_cap}_c2.jpg',frame2)
                    warning1 = 0
                    warning2 = 0
                def record_f():
                    global record,output1,output2,show_time,running, button_zoom1, button_zoom2
                    path = './record/video'
                    record = 1
                    running = 1
                    begin_record = datetime.now().strftime('%Y%m%d_%H%M%S')
                    folders = os.listdir(path)
                    if begin_record[:8] not in folders:
                        folder = os.mkdir(f'{path}/{begin_record[:8]}')
                    fourcc = cv2.VideoWriter_fourcc(*'avc1')
                    if button_zoom1 == 0:
                        output1 = cv2.VideoWriter(f'{path}/{begin_record[:8]}/{begin_record}_c1.avi', fourcc, 3.0, (640,  360))
                    if button_zoom2 == 0:
                        output2 = cv2.VideoWriter(f'{path}/{begin_record[:8]}/{begin_record}_c2.avi', fourcc, 3.0, (640,  360))
                    if language == 0:
                        show_time = Label(w4, text = 'Đang ghi: 00:00:00',font = ('Arial', 12), fg = 'red')
                        show_time.place(x = 75, y =100)
                    else:
                        show_time = Label(w4, text = '记录图像: 00:00:00',font = ('Arial', 12), fg = 'red')
                        show_time.place(x = 75, y =100)
                    update_time() 
                def save_record_f():
                    global record, output1,output2,running, time, show_time
                    if record == 1:
                        record = 0
                        output1 = 0
                        output2 = 0
                        running = 0
                        time = 0
                        show_time.destroy()
                        if language == 0:
                            showinfo('Notice','Đã lưu lại đoạn ghi hình!')
                        else:
                            showinfo('注意','录音已保存 !')        
                def update_time():
                    global time, running,show_time
                    if running == 1:
                        time +=1
                        minute = time//60
                        second = time%60
                        hour = minute//60
                        minute = minute%60
                        if hour == 24:
                            save_record_f()
                        if language == 0:
                            show_time.config(text = 'Đang ghi: {:02d}:{:02d}:{:02d}'.format(hour,minute,second))
                        else:
                            show_time.config(text = '记录图像: {:02d}:{:02d}:{:02d}'.format(hour,minute,second))
                        show_time.after(1000,update_time)

                open_camera1_2_f()
                notice_of_camera()

                if language == 0:
                    record_v = Button(w4,text = "Ghi hình",font = ('Arial', 12),width = 10, bd = 0,bg= '#1e90ff', fg = 'white', command= record_f)
                    record_v.place(x = 30 , y = 10)
                    save_v = Button(w4,text = "Lưu",font = ('Arial', 12),width = 10, bd = 0,bg= '#1e90ff', fg = 'white',command= save_record_f)
                    save_v.place(x = 160 , y = 10)
                else:
                    record_v = Button(w4,text = "记录",font = ('Arial', 12),width = 10, bd = 0,bg= '#1e90ff', fg = 'white', command= record_f)
                    record_v.place(x = 30 , y = 10)
                    save_v = Button(w4,text = "节省",font = ('Arial', 12),width = 10, bd = 0,bg= '#1e90ff', fg = 'white',command= save_record_f)
                    save_v.place(x = 160 , y = 10)

                if button_zoom1 == 1 and button_zoom2 == 1:#vo hieu hoa nut ghi hinh & luu khi 2 camera khong ket noi
                    record_v.config(state=DISABLED)
                    save_v.config(state=DISABLED)

        if language == 0:
             access = Button(w4,text = "Truy cập",font = ('Arial', 12),width = 10, bd = 0,bg= '#1e90ff', fg = 'white',command=access_f)
        else:
            access = Button(w4,text = "使用权",font = ('Arial', 12),width = 10, bd = 0,bg= '#1e90ff', fg = 'white',command=access_f)
        access.place(x = 400 , y = 110)     
#---------------------------Chuc nang thoat ung dung
    def exit_f():
        GUI2.destroy()   
    #Huy bo giao dien chinh & quay lai giao dien dang nhap
    def quit_GUI2():
        GUI2.destroy()
        GUI1_login()
    #Huy tab cu
    def clear_widget():
        global on_GUI_camera,video1, video2,status, file, warning1, warning2,on_notice,output1,output2,record,time,show_time, zoom1, zoom2, button_zoom1, button_zoom2
        warning1 = 0
        warning2 = 0
        on_notice = 0
        status = 0
        file = ''
        zoom1 = 10
        zoom2 = 10
        button_zoom1 = 0
        button_zoom2 = 0
        if record == 1:
            output1 = 0
            output2 = 0
            record = 0
            time = 0
            show_time.destroy()
            showinfo('Notice','Đã lưu lại đoạn ghi hình!')
        if on_GUI_camera == 1:
            video1.release()
            video2.release()
            on_GUI_camera = 0
            
        if len(w4.winfo_children()) != 0:
            for widget in w4.winfo_children():
                widget.destroy()

        if len(w6.winfo_children()) != 0:
            for widget in w6.winfo_children():
                widget.destroy()
#----------------------------
    if language == 0:
        time_now = Label(w1,text = f'Thời gian đăng nhập: {now}',font = ('Arial', 12)).place(x = 0 , y = 10)
        name = Label(w1,text = f'Người thao tác: {dic_check[check_id][1]}',font = ('Arial', 12)).place(x = 0 , y = 40)
        id = Label(w1,text = f'Mã thẻ: {check_id}',font = ('Arial', 12)).place(x = 0 , y = 70)
    else:
        time_now = Label(w1,text = f'登录时间: {now}',font = ('Arial', 12)).place(x = 0 , y = 10)
        name = Label(w1,text = f'用户: {dic_check[check_id][1]}',font = ('Arial', 12)).place(x = 0 , y = 40)
        id = Label(w1,text = f'员工卡代码: {check_id}',font = ('Arial', 12)).place(x = 0 , y = 70)

    img_change = PhotoImage(file="img/change_icon.png")
    img_notice = PhotoImage(file="img/notice_icon.png")
    img_camera = PhotoImage(file="img/camera_icon.png")
    img_exit = PhotoImage(file="img/exit_icon.png")
    if language == 0:
        change = Button(w2, image=img_change,compound="left", text = " Đổi mật khẩu",font = ('Arial', 16),width = 160, bd = 0,command = change_pw_f ).place(x = 0, y = 0)
        notice = Button( w2,image=img_notice,compound="left",text = " Thông báo    ",font = ('Arial', 16),width = 160, bd = 0,command=notice_f).place(x = 165 , y = 0)
        camera = Button(w2,image=img_camera,compound="left", text = " Máy ảnh       ",font = ('Arial', 16),width = 160, bd = 0, command=camera_f).place(x = 0 , y = 36)
        exit = Button(w2,image=img_exit,compound="left", text = " Thoát           ",font = ('Arial', 16),width = 160, bd = 0, command=exit_f).place(x = 165 , y = 36)
    else:
        change = Button(w2, image=img_change,compound="left", text = " 更改密码    ",font = ('Arial', 16),width = 160, bd = 0,command = change_pw_f ).place(x = 0, y = 0)
        notice = Button( w2,image=img_notice,compound="left",text = " 通知           ",font = ('Arial', 16),width = 160, bd = 0,command=notice_f).place(x = 165 , y = 0)
        camera = Button(w2,image=img_camera,compound="left", text = " 相机           ",font = ('Arial', 16),width = 160, bd = 0, command=camera_f).place(x = 0 , y = 36)
        exit = Button(w2,image=img_exit,compound="left", text = " 出口           ",font = ('Arial', 16),width = 160, bd = 0, command=exit_f).place(x = 165 , y = 36)
    GUI2.mainloop()
#----------------------------Giao dien dang nhap
def GUI1_login():
    GUI1 = Tk()
    GUI1.title('Login')
    GUI1.configure(bg = 'white')
    GUI1.wm_iconbitmap("img/login.ico")
    screenWidth = GUI1.winfo_screenwidth()
    screenHeight = GUI1.winfo_screenheight()
    width_gui1 = 500
    height_gui1 = 250
    x = int(screenWidth/2 - width_gui1/2) #left
    y =  int(screenHeight/2 - height_gui1/2) #top
    GUI1.geometry('%dx%d+%d+%d'%(width_gui1,height_gui1,x, y))
    GUI1.resizable(False,False)
    #an/hien mat khau
    def show_password():
        if pw_value.cget('show') == '*':
            pw_value.config(show = '')
        else:
            pw_value.config(show = '*')
    #Chuyen ngon ngu
    def language_f():
        global language
        if c1.get() == List_Languages[0]:
            language = 0
        else:
            language = 1
    #kiem tra du lieu duoc nhap vao
    def check_user():
        global dic_check,check_id
        language_f()
        check_id = str(id_value.get())
        check_pw = str(pw_value.get())
        if check_pw != '':
           check_pw = hashlib.md5(check_pw.encode('utf-8')).hexdigest()
        if check_id == '' and check_pw != '':
            showinfo('Notice','Vui lòng nhập mã thẻ!')
        elif check_id != '' and check_pw == '':
            showinfo('Notice','Vui lòng nhập mật khẩu!')
        elif check_id == '' and check_pw == '':
            showinfo('Notice','Vui lòng nhập đầy đủ mã thẻ và mật khẩu!')
        else:
            if check_id in dic_check and check_pw == dic_check[check_id][0]:
                for widget in GUI1.winfo_children():
                    widget.destroy()
                #giao dien xin chao user
                i2 = Label(GUI1, image = img1, bg = 'white').place(x = 5, y = 40)
                width_canvas = 335
                height_canvas = 245
                c1 = Canvas(bg = 'white', highlightthickness=0, width=width_canvas, height=height_canvas)
                c1.place(x = 160, y = 0)
                if language == 0:
                    hello_text = Label(c1, text = f'Xin chào {dic_check[check_id][1]}', font = ('Arial', 15, 'bold'), bg = 'white')
                else:
                    hello_text = Label(c1, text = f'你好 {dic_check[check_id][1]}', font = ('Arial', 15, 'bold'), bg = 'white')
                hello_text.place(x = 0, y = 0)
                #Căn giua doan text
                c1.update()
                label_width = hello_text.winfo_width()
                label_height = hello_text.winfo_height()
                label_x = int((width_canvas - label_width) / 2)
                label_y = int((height_canvas - label_height) / 2)
                hello_text.place( x = label_x, y = label_y)
                #Hieu ung loading
                load = Progressbar(length=500,orient='horizontal',mode='determinate')
                load.place(x=0,y=228)
                def next_GUI():
                    global index_loading
                    if index_loading <= 10:
                        load['value'] = 10*index_loading
                        index_loading += 1
                        load.after(300,next_GUI)
                    else:
                        index_loading = 0
                        GUI1.destroy()
                        GUI2_supervisor()
                next_GUI()
            elif check_id in dic_check and check_pw != dic_check[check_id][0]:
                showwarning('Warning','Mật khẩu sai. Vui lòng nhập lại!')
            elif check_id not in dic_check:
                showwarning('Warning','Mã thẻ sai. Vui lòng kiểm tra lại mã thẻ hoặc bạn chưa cấp phép sử dụng!')
    #Huy bo giao dien dang nhap
    def quit_GUI1():
        GUI1.destroy()
#----------------------------
    img1 = PhotoImage(file = 'img\img1.png')
    i1 = Label(GUI1, image = img1, bg = 'white').place(x = 20, y = 40)

    c1 = ttk.Combobox(GUI1, values = List_Languages,width=10,font = ('Arial', 12))
    c1.set(List_Languages[0])
    c1.place(x = 340, y = 55)

    h1 = Label(GUI1, text = 'Đăng nhập', font = ('Arial', 23, 'bold'), fg = '#57a1f8', bg = 'white' ).place( x = 250, y = 5)
    h2 = Label(GUI1, text = 'Quên mật khẩu? \nLiên hệ IT: 082 452 0894', font = ('Arial', 12), bg = 'white' ).place( x = 10, y = 190)
    id = Label(GUI1,text = "Mã thẻ:",font = ('Arial', 12),bg = 'white').place(x = 210 , y = 90)
    pw = Label(GUI1,text = "Mật khẩu:",font = ('Arial', 12),bg = 'white').place(x = 210 , y = 140)

    id_value = Entry(font = ('Arial', 12),width = 19,border = 0)
    pw_value = Entry(font = ('Arial', 12),width = 19, border = 0, show ='*')
    id_value.place(x = 280 , y = 90)
    pw_value.place(x = 280 , y = 140)

    line1 = Frame(GUI1, width = 170, height = 2, bg = 'black').place(x = 280, y = 110)
    line2 = Frame(GUI1, width = 170, height = 2, bg = 'black').place(x = 280, y = 160)

    show_pw  = Checkbutton(GUI1, text= 'Hiện mật khẩu', font = ('Arial', 12),bg = 'white', activebackground= 'white', command= show_password).place( x = 210, y = 170 )
    login = Button(GUI1,text = "Đăng nhập",font = ('Arial', 12),width = 10,bg = '#57a1f8',fg = 'white' ,command = check_user, bd = 0,activebackground = 'skyblue').place(x = 210 , y = 200)
    exit = Button(GUI1,text = "Thoát",font = ('Arial', 12),width = 10,command = quit_GUI1, bd = 0,activebackground= 'white').place(x = 355 , y = 200)
    GUI1.mainloop()
#----------------------------
GUI1_login()
#GUI2_supervisor()
