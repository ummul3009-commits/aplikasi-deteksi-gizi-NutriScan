import tkinter as tk                       #Library GUI utama
from tkinter import filedialog, messagebox #Dialog file & popup pesan
from PIL import Image, ImageTk             #Mengolah dan menampilkan gambar
import json                                #Membaca & menyimpan data JSON
import subprocess                          #Menjalankan file Python lain      
import sys                                 #Akses interpreter Python
from datetime import datetime              #Mengambil tanggal & waktu 
import os                                  #Operasi file & folder

os.makedirs("dataset", exist_ok=True)    #Memastikan folder dataset ada

# Inisialisasi file JSON jika belum ada
if not os.path.exists("dataset/riwayat.json"):
    with open("dataset/riwayat.json", "w", encoding="utf-8") as f:        #kalau belum ada, maka folder akan dibuat oleh perintah ini
        json.dump([], f)

# Load data gizi dan rekomendasi
with open("dataset/gizi.json", encoding="utf-8") as f:                     #Dari folder dataset di file gizi.json
    gizi_data = json.load(f)

with open("dataset/rekomendasi.json", encoding="utf-8") as f:                #Dari folder dataset di file rekomendasi.json
    rekom_data = json.load(f)

# Load riwayat data makanan yang pernah di deteksi
FILE_RIWAYAT = "dataset/riwayat.json"                                         #Dari folder dataset di file riwayat.json
with open(FILE_RIWAYAT, "r", encoding="utf-8") as f:                         #membaca riwayat dari file riwayat.json
    riwayat = json.load(f)

# =====CLASS untuk LOGIN PAGE =====
class LoginPage(tk.Frame):                                                                                                    #Membuat halaman baru bernama LoginPage.
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)                                                                                    #Inisialisasi LoginPage sebagai Frame Tkinter
        self.controller = controller                                                                                #Menyimpan controller (App) agar bisa berpindah halaman
        
        # Menyimpan path (lokasi) file gambar background untuk halaman login
        self.image_path = "bg-button/Loginbg.png"
        try:
            self.original_image = Image.open(self.image_path)                                                                      #Membuka file gambar background menggunakan PIL dan disimpan dalam variabel original_image
        except FileNotFoundError:
            messagebox.showerror("Error", "Loginbg.png tidak ditemukan!")                                                         #Jika file gambar tidak ditemukan: Menampilkan pesan error ke pengguna
            self.controller.root.destroy()
            return
        
        # Membuat canvas sebagai layer utama untuk background dan konten login
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        # Frame sebagai container form login (tampilan kotak putih di tengah)
        self.frame = tk.Frame(self, bg="white", bd=5)
        
        # Label dan input untuk username
        tk.Label(self.frame, text="Username:", bg="white").pack(pady=10, padx=40)
        self.entry_username = tk.Entry(self.frame)
        self.entry_username.pack(pady=5, padx=40, fill='x')
        
        # Label dan input untuk password
        tk.Label(self.frame, text="Password:", bg="white").pack(pady=10, padx=40)
        self.entry_password = tk.Entry(self.frame, show="*")#(karakter disembunyikan)
        self.entry_password.pack(pady=5, padx=40, fill='x')
        
        #Tombol login yang memanggil fungsi login saat diklik
        tk.Button(self.frame, text="Login", command=self.login).pack(pady=20, padx=40, fill='x')
        
        self.login_window_id = self.canvas.create_window(250, 200, window=self.frame, anchor="center")                        #Menempatkan frame login ke dalam canvas
        self.canvas.bind('<Configure>', self.resize_bg)                                                                          #Mengatur ulang background dan posisi form saat ukuran window berubah
    
     #MENGATUR UKURAN BACKGROUND   
    def resize_bg(self, event):
        # Mengambil ukuran canvas terbaru saat window di-resize
        new_width = event.width
        new_height = event.height
        # Resize gambar background agar sesuai ukuran window
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        # Konversi gambar PIL ke format yang bisa digunakan Tkinter
        self.bg_photo = ImageTk.PhotoImage(resized_image)
        self.canvas.delete("background")                                                                               #Menghapus background lama agar tidak menumpuk
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw", tags="background")                             #Menampilkan background baru di pojok kiri atas canvas
        self.canvas.coords(self.login_window_id, new_width // 2, new_height // 2)                                         #Menampilkan background baru di pojok kiri atas canvas
        self.canvas.tag_lower("background")                                                                               #Menurunkan layer background agar berada di belakang widget lain
    
    def login(self):
        messagebox.showinfo("Sukses", "Login berhasil!")                                                                     #Menurunkan layer background agar berada di belakang widget lain
        self.controller.show_frame(HomePage)                                                                             #Berpindah ke halaman Home tanpa membuat window baru

# =====CLASS untuk HOME PAGE =====
class HomePage(tk.Frame):                                                                                                      #Membuat halaman baru bernama HomePage.
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)                                                                                         #Inisialisasi HomePage sebagai Frame Tkinter
        self.controller = controller                                                                                                #Menyimpan controller (App) agar bisa berpindah halaman
        self.configure(bg="#B6E7A7")                                                                                                #kode mengatur warna (hijau pastel) untuk background HomePage
        
        # HEADER (Bagian atas halaman)
        header = tk.Frame(self, bg="#B6E7A7")                                                                                      #kode mengatur warna (hijau pastel) untuk background Header
        header.pack(fill="x", pady=20)                                                                                                   #Melebar ke samping, beri jarak atas-bawah
        tk.Label(header, text="Welcome in NutriScan!", font=("Arial", 22, "bold"), bg="#B6E7A7", fg="white").pack()                            #Judul aplikasi di header
        # CONTENT (Isi utama halaman)
        content = tk.Frame(self, bg="#B6E7A7")                                                                                                         #kode mengatur warna (hijau pastel) untuk background content
        content.pack(expand=True)
        # CARD SCAN FOOD
        scan_card = tk.Frame(content, bg="white", width=250, height=220, relief="raised", bd=2)                                                          #Frame background putih dengan lebar 250 dam tinggi 220
        scan_card.grid(row=0, column=0, padx=40)
        scan_card.pack_propagate(False)#Mengunci ukuran frame
        # Judul card "Scan Food"
        tk.Label(scan_card, text="Scan Food", font=("Arial", 14, "bold"), bg="white").pack(pady=20)
        tk.Label(scan_card, text="Deteksi makanan\nberdasarkan foto", bg="white").pack()                                                                   #Deskripsi penjelasan singkat fungsi card
        # Tombol "Scan Food" ketika di klik akan menuju halaman deteksi
        tk.Button(scan_card, text="Scan Food", bg="#8B5A2B", fg="white", width=15,
                  command=lambda: self.controller.show_frame(DetectorPage)).pack(pady=20)                                                                              #Perintah saat tombol diklik,maka pindah halaman ke DetectorPage
        # CARD STORAGE (Riwayat Deteksi)
        storage_card = tk.Frame(content, bg="white", width=250, height=220, relief="raised", bd=2)                                                     #Frame background putih dengan lebar 250 dam tinggi 220
        storage_card.grid(row=0, column=1, padx=40)
        storage_card.pack_propagate(False)#Menjaga ukuran card tetap
        # Judul card "Storage"
        tk.Label(storage_card, text="Storage", font=("Arial", 14, "bold"), bg="white").pack(pady=20)
        tk.Label(storage_card, text="Lihat riwayat\nhasil deteksi", bg="white").pack()                                                          #Deskripsi penjelasan singkat fungsi card
        # Tombol "Storage" 
        tk.Button(storage_card, text="Storage", bg="#8B5A2B", fg="white", width=15,
                  command=lambda: self.controller.show_frame(StoragePage)).pack(pady=20)                                                              #Perintah saat tombol diklik,maka pindah halaman ke DetectorPage
        # Tombol "Logout"
        tk.Button(self, text="Logout", bg="red", fg="white", width=10,
                  command=lambda: self.controller.show_frame(LoginPage)).pack(pady=10)                                                           #Perintah saat tombol diklik,maka pindah halaman ke LOginPage

# =====CLASS untuk DETECTOR PAGE =====================
class DetectorPage(tk.Frame):                                                                                                       #Membuat halaman baru bernama DetectorPage.
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)                                                                                                  #Inisialisasi DetectorPage sebagai Frame Tkinter
        self.controller = controller                                                                                                     #Menyimpan controller (App) agar bisa berpindah halaman
        # UNTUK MEMBUAT SCROLLBAR
        self.canvas = tk.Canvas(self)                                                                                                   #Canvas digunakan agar halaman bisa di-scroll
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)                                                        #Scrollbar vertikal untuk menggeser isi Canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)                                                                                          #Menghubungkan Canvas dengan Scrollbar
        scrollbar.pack(side="right", fill="y")                                                                                            #Menempatkan Scrollbar di kanan memenuhi dari atas kebawah
        self.canvas.pack(side="left", fill="both", expand=True)                                                                            #Menempatkan Canvas di kiri dan memenuhi layar
        # UNTUK ISI CANVAS
        self.content = tk.Frame(self.canvas)                                                                                                         #Frame utama untuk menampung seluruh isi halaman (dimasukkan ke Canvas)
        self.window_id = self.canvas.create_window((0, 0), window=self.content, anchor="n")                                                              #Memasukkan Frame ke dalam Canvas sebagai window,dengan posisi awal titik kiri atas
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.window_id, width=e.width))                                                 #Otomatis menyesuaikan lebar Frame selalu sama dengan lebar Canvas
        self.content.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))                                          #Mengatur area scroll Canvas sesuai ukuran isi Frame
        # VARIABEL PILIHAN MAKANAN
        self.selected_food = tk.StringVar(value="Pilih makanan")                                                                      #Variabel untuk menyimpan makanan yang dipilih
        self.main_img_label = None                                                                                                               #Label gambar utama (awal None, diisi setelah upload)
        self.image_path = None        
        # MEMBUAT HEADER
        header = tk.Frame(self.content)                                                                                                           #Membuat Frame khusus header
        header.pack(fill="x", pady=10)                                                                                                          #menampilkan widget header melebar horizontal (kiri–kanan),dengan jarak atas bawah 10
        # TOMBOL BACK
        tk.Button(header, text="← Back", command=lambda: self.controller.show_frame(HomePage)).pack(anchor="w", padx=10)                            #Perintah Back baru akan jalan jika tombol di klik,kembali ke HomePage 
        #JUDUL HALAMAN
        tk.Label(header, text="Aplikasi Deteksi Kandungan Gizi", font=("Arial", 16, "bold")).pack()
        # TOMBOL UPLOAD GAMBAR
        self.upload_btn = tk.Button(self.content, text="Upload Foto", command=self.upload_image, width=25)
        self.upload_btn.pack(pady=5)
        # Dropdown pilihan makanan pilihan user
        self.option_menu = tk.OptionMenu(self.content, self.selected_food, *gizi_data.keys())                                                                         #Berdasarkan semua pilihan yang ada di file gizi.json,otomatis jadi isi dropdown
        self.option_menu.pack(pady=5)
        # TOMBOL DETEKSI GIZI
        self.detect_btn = tk.Button(self.content, text="Deteksi", command=self.detect_food,
                                    bg="green", fg="white", width=25)
        self.detect_btn.pack(pady=10)
    
    #FUNGSI UPLOAD IMAGE
    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])                                                                         #Membuka dialog untuk memilih file gambar dengan beberapa tipe file(lebih direkomendasikan memilih dari folder imagefood)
        if not path:#Jika user membatalkan pemilihan file
            return
        
        self.image_path = path   #Simpan path gambar untuk digunakan fungsi lain
        
        img = Image.open(path).resize((220, 220)) #Buka dan resize gambar agar sesuai tampilan
        img_tk = ImageTk.PhotoImage(img) #Konversi gambar ke format Tkinter
        
        if self.main_img_label is None: #Cek apakah label gambar sudah ada
            self.main_img_label = tk.Label(self.content, image=img_tk) #Jika ini upload pertama,maka Membuat Label baru dengan Isi label adalah gambar
            self.main_img_label.image = img_tk #simpan referensi gambar
            self.main_img_label.pack(pady=10) #Menampilkan gambar di layar
        else:
            self.main_img_label.config(image=img_tk)# Jika sudah ada gambar, cukup ganti gambarnya
            self.main_img_label.image = img_tk #simpan referensi gambar
        
        self.auto_detect_from_filename() #Deteksi otomatis makanan dari nama file gambar
    
    #FUNGS AUTO DETECT FROM FILENAME
    def auto_detect_from_filename(self):
        if not self.image_path: #Cek apakah gambar sudah di-upload
            return #Kalau belum ada gambar maka fungsi langsung berhenti
        
        filename = os.path.basename(self.image_path).lower()                                                                                     #Ambil nama file gambar saja (tanpa path folder) dan ubah ke huruf kecil
        filename = filename.replace(" ", "").replace("-", "").replace("_", "")                                                                                 #Menghilangkan spasi, tanda minus, dan underscore agar format seragam
        # Loop semua nama makanan pada data gizi
        for food in gizi_data.keys():
            key = food.replace("_", "").lower() #Menyesuaikan nama makanan dari dataset
            #Mencocokkan nama file dengan data makanan
            if key in filename:
                self.selected_food.set(food)#Maka Set dropdown secara otomatis
                return #Hentikan loop setelah ketemu
    
    #FUNGSI SIMPAN RIWAYAT
    def simpan_riwayat(self, food):
        global riwayat #Mengakses variabel global riwayat
        # Membuat data riwayat baru
        data_baru = {
            "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M"),#Menyimpan tanggal dan waktu deteksi
            "makanan": food,#Menyimpan nama makanan yang dideteksi
            "gizi": gizi_data[food],#Menyimpan data gizi dari file gizi.json
            "rekomendasi": [r["food_name"] for r in rekom_data.get(food, {}).get("rekomendasi", [])]                                                                   #Menyimpan daftar nama makanan rekomendasi
        }
        # Menambahkan data baru ke list riwayat
        riwayat.append(data_baru)
        with open(FILE_RIWAYAT, "w", encoding="utf-8") as f: #Membuka file riwayat.json dan menulis ulang isi file(memperbarui)
            json.dump(riwayat, f, indent=4) #simpan Python list ke file JSON
            
    #FUNGSI DETECT FOOD untuk dipanggil saat tombol “Deteksi” ditekan
    def detect_food(self):
        food = self.selected_food.get()#Mengambil nilai makanan yang dipilih dari OptionMenu
        # Validasi jika user belum memilih makanan
        if food == "Pilih makanan":
            messagebox.showwarning("Peringatan", "makanan yang anda upload tidak tersedia di dataset. silahkan klik menu yang ada di tombol 'pilih makanan'")                                    #Memberikan pop up pemberitahuan
            return #Menghentikan eksekusi fungsi
        # Menghapus widget hasil deteksi sebelumnya
        for w in self.content.winfo_children():
            #Menentukan widget yang TIDAK dihapus untuk menjaga agar header, gambar, dan tombol utama tidak terhapus
            if w not in [self.content.winfo_children()[0], self.main_img_label,
                         self.upload_btn, self.option_menu, self.detect_btn]:
                w.destroy()#Menghapus widget yang tidak diperlukan
                
        # Frame untuk menampilkan informasi gizi makanan
        gizi_frame = tk.Frame(self.content) 
        gizi_frame.pack(pady=10)
        # Judul gizi berdasarkan makanan yang dipilih
        tk.Label(gizi_frame, text=f"Gizi {food.replace('_',' ').title()}",
                 font=("Arial", 12, "bold")).pack()
        # Menampilkan detail gizi (kalori, protein, dll) berdasarkan file gizi.json
        for k, v in gizi_data[food].items():
            tk.Label(gizi_frame, text=f"{k} : {v}").pack(anchor="w")#menampilkan key:value rata kiri
            
        # Frame untuk menampilkan rekomendasi makanan
        rekom_frame = tk.Frame(self.content)
        rekom_frame.pack(pady=20)
        # Judul bagian rekomendasi
        tk.Label(rekom_frame, text="Rekomendasi Makanan",
                 font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=10, pady=5)
        
        # Menampilkan daftar rekomendasi makanan dalam bentuk kartu
        for i, r in enumerate(rekom_data.get(food, {}).get("rekomendasi", [])):
            card = tk.Frame(rekom_frame, bd=1, relief="solid", padx=10, pady=10)#Membuat kartu (card) untuk satu rekomendasi makanan
            card.grid(row=1, column=i, padx=10)#Agar kartu sejajar
            # Menampilkan gambar dari folder imagerecomendation jika tersedia,berdasarkan nama picture di file rekomendasi.json
            try:
                img = Image.open(r["picture"]).resize((110, 110))#Membuka gambar dari path di JSON dan meresize ke ukuran 110x110 px
                img_tk = ImageTk.PhotoImage(img)#Mengubah gambar PIL ke format Tkinter
                lbl = tk.Label(card, image=img_tk)
                lbl.image = img_tk #mencegah gambar hilang
                lbl.pack()
            except:
                tk.Label(card, text="Gambar\nTidak Ada").pack() #Jika Gambar Tidak Ada,maka akan diganti dengan teks 
            # Menampilkan nama makanan rekomendasi dan menghilangkan format underscore
            tk.Label(card, text=r["food_name"].replace("_"," ").title(),
                     font=("Arial", 10, "bold")).pack()
            # Menampilkan detail tambahan (selain nama dan gambar)
            for k, v in r.items():
                if k not in ["food_name", "picture"]:
                    tk.Label(card, text=f"{k}: {v}").pack(anchor="w")#Menampilkan data gizi berdasarkan file rekomendas.json
        # Menyimpan hasil deteksi ke riwayat
        self.simpan_riwayat(food)
        messagebox.showinfo("Berhasil", "Hasil deteksi tersimpan di Storage")#Memunculkan pop up pemberitahuan 

# =====CLASS untuk STORAGE PAGE =====
class StoragePage(tk.Frame):#Membuat halaman baru bernama StoragePage.
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #Inisialisasi DetectorPage sebagai Frame Tkinter
        self.controller = controller #Menyimpan controller (App) agar bisa berpindah halaman
        # UNTUK MEMBUAT SCROLLBAR
        self.canvas = tk.Canvas(self) #Canvas digunakan agar halaman bisa di-scroll
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)#Scrollbar vertikal untuk menggeser isi Canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)#Menghubungkan Canvas dengan Scrollbar
        scrollbar.pack(side="right", fill="y")#Menempatkan Scrollbar di kanan memenuhi dari atas kebawah
        self.canvas.pack(side="left", fill="both", expand=True)#Menempatkan Canvas di kiri dan memenuhi layar
        # UNTUK ISI CANVAS
        self.content = tk.Frame(self.canvas)#Frame utama untuk menampung seluruh isi halaman (dimasukkan ke Canvas)
        self.window_id = self.canvas.create_window((0, 0), window=self.content, anchor="n")#Memasukkan Frame ke dalam Canvas sebagai window,dengan posisi awal titik kiri atas
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.window_id, width=e.width))#Otomatis menyesuaikan lebar Frame selalu sama dengan lebar Canvas
        self.content.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))#Mengatur area scroll Canvas sesuai ukuran isi Frame
        # HEADER HALAMAN STORAGE
        header = tk.Frame(self.content)
        header.pack(fill="x", pady=10)
        # Tombol kembali ke HomePage
        tk.Button(header, text="← Back", command=lambda: self.controller.show_frame(HomePage)).pack(anchor="w", padx=10)#Perintah Back baru akan jalan jika tombol di klik,kembali ke HomePage 
        # Judul halaman "Riwayat Deteksi Makanan"
        tk.Label(header, text="Riwayat Deteksi Makanan",
                 font=("Arial", 16, "bold")).pack()
        # Tombol untuk menghapus seluruh riwayat
        tk.Button(header, text="Hapus Semua Riwayat", bg="red", fg="white",
                  command=self.hapus_semua).pack(pady=5)
        
        self.load_riwayat()#Memperbarui data riwayat
        
    #FUNGSI LOAD RIWAYAT
    def load_riwayat(self):
        global riwayat #Mengakses variabel global riwayat
        
        # Hapus semua widget lama kecuali header (refresh tampilan)
        for w in self.content.winfo_children():
            if w != self.content.winfo_children()[0]:
                w.destroy()
        # Jika belum ada riwayat,maka akan muncul popup notifikasi
        if not riwayat:
            tk.Label(self.content, text="Belum ada riwayat.", font=("Arial", 12)).pack(pady=30)
        else:
            # Loop setiap data riwayat dengan membuat card riwayat
            for i, item in enumerate(riwayat):
                card = tk.Frame(self.content, bd=1, relief="solid", padx=10, pady=10)
                card.pack(fill="x", padx=20, pady=10)
                # Judul card (tanggal + nama makanan)
                tk.Label(card, text=f"{item['tanggal']} - {item['makanan'].replace('_',' ').title()}",
                         font=("Arial", 12, "bold")).pack(anchor="w")
                # Menggabungkan data gizi menjadi satu baris teks
                gizi_text = ", ".join([f"{k}:{v}" for k, v in item["gizi"].items()])
                tk.Label(card, text=f"Gizi: {gizi_text}",
                         wraplength=800, justify="left").pack(anchor="w", pady=5)
                # Menampilkan rekomendasi jika ada
                if item["rekomendasi"]:
                    tk.Label(card, text="Rekomendasi: " + ", ".join(item["rekomendasi"]),
                             fg="green").pack(anchor="w")
                # Tombol hapus riwayat per item
                tk.Button(card, text="Hapus Riwayat Ini", bg="gray", fg="white",
                          command=lambda idx=i: self.hapus_satu(idx)).pack(anchor="e", pady=5)#Menyimpan index saat ini
                
    #FUNGSI HAPUS SATU
    def hapus_satu(self, index):
        global riwayat #mengakses global riwayat
        if not messagebox.askyesno("Konfirmasi", "Hapus riwayat ini?"):#Memunculkan popup konfirmasi sebelum menghapus satu data riwayat
            return
        del riwayat[index] #Menghapus data riwayat berdasarkan index
        with open(FILE_RIWAYAT, "w", encoding="utf-8") as f: #Menulis perubahan ke file JSON
            json.dump(riwayat, f, indent=4) #Menyimpan perubahan ke file JSON
        self.load_riwayat()#Memperbarui riwayat
        
    #FUNGSI HAPUS SEMUA
    def hapus_semua(self):
        global riwayat #mengakses global riwayat
        if not messagebox.askyesno("Konfirmasi", "Hapus SEMUA riwayat?"):#Memunculkan popup konfirmasi sebelum menghapus satu data riwayat
            return
        riwayat = []#Kosongkan semua data riwayat
        with open(FILE_RIWAYAT, "w", encoding="utf-8") as f: #Menulis perubahan ke file JSON
            json.dump(riwayat, f, indent=4) #Menyimpan perubahan ke file JSON
        self.load_riwayat()#Memperbarui riwayat

# =====CLASS untuk MAIN APP =====
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self) #Inisialisasi aplikasi dengan memanggil constructor dari tk.Tk
        self.title("Healthy Life")#Judul window
        self.geometry("900x700")#Ukuran window lebar x tinggi
        
        # Container untuk semua halaman
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        # Konfigurasi grid responsif agar halaman dapat menyesuaikan ukuran window
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}#Menyimpan semua halaman dalam dictionary
        for F in (LoginPage, HomePage, DetectorPage, StoragePage): #Membuat semua halaman aplikasi
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew") #Mengisi seluruh area container
        
        self.show_frame(LoginPage) #Menampilkan halaman awal
    #FUNGSI SHOW FRAME
    def show_frame(self, cont):
        frame = self.frames[cont]#Ambil halaman yang ingin ditampilkan
        #JIKA HALAMAN STORAGE, REFRESH DATA
        if cont == StoragePage:
            frame.load_riwayat()

        frame.tkraise()#Menampilkan halaman ke layar

# Menjalankan aplikasi hanya jika file ini dijalankan langsung
if __name__ == "__main__":
    app = App() #Membuat instance aplikasi utama
    app.mainloop() #Menjalankan event loop Tkinter agar aplikasi tetap aktif