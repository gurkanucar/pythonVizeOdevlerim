from tkinter import *
from tkinter import messagebox as tkMessageBox
import sqlite3
import os.path

#baglanti kurma
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "data.db")
baglanti = sqlite3.connect(db_path)

#pencere oluşturma
pencere = Tk()
pencere.title("Gürkan UÇAR")
pencere.geometry("1460x690")

#Veri tabanından verileri getir
def Getir():
    #listboxlari temizle
    lb1.delete(0,END)
    lb2.delete(0,END)
    lb3.delete(0,END)
    for kayıt in baglanti.execute("SELECT * FROM Ogrenciler"):
        lb1.insert(END, kayıt[0] + ' ' + kayıt[1] + ' ' + kayıt[2])
    for kayıt in baglanti.execute("SELECT * FROM Dersler"):
        lb2.insert(END, kayıt[0] + ' ' + kayıt[1] )
    for kayıt in baglanti.execute("SELECT * FROM Notlar"):
        lb3.insert(END, kayıt[0] + ' ' + kayıt[1] + ' ' + kayıt[2]+ ' ' + kayıt[3])

#Veri tabanına ekleme yap
# tablo 1 ise solFrame
# tablo 2 ise ortaFrame
# tablo 3 ise sagFrame
def Ekleme(tablo):
    if(tablo == 1):
        if( len(e1.get())!=0 and len(e2.get())!=0 and len(e3.get())!=0):
            baglanti.execute("INSERT INTO Ogrenciler VALUES(?,?,?)",
                            [e1.get(), e2.get(), e3.get()])
            baglanti.commit()
        else:
            tkMessageBox.showwarning("UYARI !","Boş alan bırakamazsınız !")

    elif(tablo == 2):
        if (len(e4.get()) != 0 and len(e5.get()) != 0):
            baglanti.execute("INSERT INTO Dersler VALUES(?,?)",
                            [e4.get(), e5.get()])
            baglanti.commit()
        else:
            tkMessageBox.showwarning("UYARI !","Boş alan bırakamazsınız !")

    elif(tablo == 3):
        if (len(e6.get()) != 0 and len(e7.get()) != 0):
            baglanti.execute("INSERT INTO Notlar VALUES(?,?,?,?)",
                        [ lb1.get(ACTIVE).split(' ')[0], lb2.get(ACTIVE).split(' ')[0], e6.get(), e7.get()])
            baglanti.commit()
        else:
            tkMessageBox.showwarning("UYARI !","Boş alan bırakamazsınız !")

    #textboxlari sıfırlama
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    e4.delete(0,END)
    e5.delete(0,END)
    e6.delete(0,END)
    e7.delete(0,END)
    #işlemden sonra verileri çağırma
    Getir()

#Veri tabanından veri sil
def Silme(tablo):
    if tablo == 1:
        if tkMessageBox.askyesno("UYARI", "Seçili Kayıtları silmek istediğinize emin misiniz?"):
            sel = lb1.curselection()
            for index in sel[::-1]:
                baglanti.execute("DELETE FROM Ogrenciler WHERE OgrNo=?",
                            [lb1.get(index).split(' ')[0]])
                baglanti.commit()

    if tablo == 2:
        if tkMessageBox.askyesno("UYARI", "Seçili Kayıtları silmek istediğinize emin misiniz?"):
            sel = lb2.curselection()
            for index in sel[::-1]:
                baglanti.execute("DELETE FROM Dersler WHERE DersKodu=?",
                                 [lb2.get(index).split(' ')[0]])
                baglanti.commit()
    if tablo == 3:
        if tkMessageBox.askyesno("UYARI", "Seçili Kayıtları silmek istediğinize emin misiniz?"):
            sel = lb3.curselection()
            for index in sel[::-1]:
                baglanti.execute("DELETE FROM Notlar WHERE OgrNo=? AND DersKodu=?",
                                [lb3.get(index).split(' ')[0],lb3.get(index).split(' ')[1]])
                baglanti.commit()

    #işlemden sonra verileri çağırma
    Getir()


#Öğrenci ekleme kısmı
solKisim = Frame(width=450,height=670,relief=RIDGE, bd=10)
solKisim.place(x=10,y=10)
label = Label(solKisim,text="ÖGRENCİLER",font=("Calibri",30))
label.place(x=80,y=0)
label = Label(solKisim,text="OgrNo: ",font=("Calibri",15))
label.place(x=10,y=80)
label = Label(solKisim,text="     Adı: ",font=("Calibri",15))
label.place(x=10,y=130)
label = Label(solKisim,text="Soyadı: ",font=("Calibri",15))
label.place(x=10,y=180)
e1 = Entry(solKisim,font=("Calibri",15))
e1.place(x=150,y=80)
e2 = Entry(solKisim,font=("Calibri",15))
e2.place(x=150,y=130)
e3 = Entry(solKisim,font=("Calibri",15))
e3.place(x=150,y=180)
# parametreli fonksiyon için command= lambda: Ekleme(1) dedim
btn1 =  Button(solKisim,text="Ekle",font=("Calibri",15), width=25, command= lambda: Ekleme(1))
btn1.place(x=50,y=230)
lb1 = Listbox(solKisim, font="Calibri", selectmode="extended",width=40,exportselection=0)
lb1.place(x=10,y=300)
btn2 =  Button(solKisim,text="Seçili Olanları Sil",font=("Calibri",15), width=30, command= lambda: Silme(1))
btn2.place(x=20,y=580)

#Ders ekleme kısmı
ortaKisim = Frame(width=450,height=670,relief=RIDGE,  borderwidth = 10)
ortaKisim.place(x=505,y=10)
label = Label(ortaKisim,text="DERSLER",font=("Calibri",30))
label.place(x=130,y=0)
label = Label(ortaKisim,text="Ders Kodu: ",font=("Calibri",15))
label.place(x=0,y=80)
label = Label(ortaKisim,text=" Ders Adı: ",font=("Calibri",15))
label.place(x=0,y=130)
e4 = Entry(ortaKisim,font=("Calibri",15))
e4.place(x=150,y=80)
e5 = Entry(ortaKisim,font=("Calibri",15))
e5.place(x=150,y=130)
btn3 =  Button(ortaKisim,text="     Ekle     ",font=("Calibri",15), width=25, command= lambda: Ekleme(2))
btn3.place(x=50,y=230)
lb2 = Listbox(ortaKisim, font="Calibri", selectmode="extended",width=40,exportselection=0)
lb2.place(x=10,y=300)
btn4 =  Button(ortaKisim,text="Seçili Olanları Sil",font=("Calibri",15), width=30, command= lambda: Silme(2))
btn4.place(x=20,y=580)

#Not ekleme kısmı
sagKisim = Frame(width=450,height=670,relief=RIDGE, bd=10)
sagKisim.place(x=1000,y=10)
label = Label(sagKisim,text="NOTLAR",font=("Calibri",30))
label.place(x=130,y=0)
label = Label(sagKisim,text=" Vize Notu: ",font=("Calibri",15))
label.place(x=10,y=80)
label = Label(sagKisim,text=" Final Notu: ",font=("Calibri",15))
label.place(x=10,y=130)
e6 = Entry(sagKisim,font=("Calibri",15))
e6.place(x=150,y=80)
e7 = Entry(sagKisim,font=("Calibri",15))
e7.place(x=150,y=130)
btn5 =  Button(sagKisim,text="     Ekle     ",font=("Calibri",15), width=25, command= lambda: Ekleme(3))
btn5.place(x=50,y=230)
lb3 = Listbox(sagKisim, font="Calibri",width=40, selectmode="extended")
lb3.place(x=10,y=300)
btn6 =  Button(sagKisim,text="Seçili Olanları Sil",font=("Calibri",15), width=30, command= lambda: Silme(3))
btn6.place(x=20,y=580)

#veritabanındaki veriler listeleniyor
Getir()

pencere.mainloop()