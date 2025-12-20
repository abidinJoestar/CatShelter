import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Kedi Barınağı Sistemi")
        self.root.geometry("600x650")
            
        # Arka plan rengini modern bir gri-mavi yapalım
        self.bg_color = "#cbeef7" 
        self.root.configure(bg=self.bg_color)

        # --- TTK STİL AYARLARI (Modern Görünümün Sırrı Burası) ---
        self.style = ttk.Style()
        self.style.theme_use('clam') # 'clam' teması renk değişimine daha açıktır

        # Yazı (Label) Stili
        self.style.configure("TLabel", background=self.bg_color, foreground="#2c3e50", font=("Segoe UI", 11))
        self.style.configure("Baslik.TLabel", font=("Segoe UI", 20, "bold"), foreground="#2c3e50")

        # Buton (Button) Stili
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=10, background="#4da5fd", foreground="white")
        self.style.map("TButton", background=[("active","#1abc9c")]) 

        # RadioButon Stili
        self.style.configure("TRadiobutton", background=self.bg_color, font=("Segoe UI", 10))

        # --- ORTA ÇERÇEVE ---
        # ttk.Frame yerine tk.Frame kullandım çünkü arka plan rengi vermek daha kolay
        self.center_frame = tk.Frame(self.root, bg=self.bg_color, width=320, height=500)
        self.center_frame.pack_propagate(False)
        self.center_frame.pack(expand=True)

        # --- LOGO / BAŞLIK ---
        # Not: style="Baslik.TLabel" diyerek yukarıda tanımladığımız stili çağırdık
        self.login_label = ttk.Label(self.center_frame, text="Sisteme Giriş", style="Baslik.TLabel")
        self.login_label.pack(pady=(40, 30))

        # --- KULLANICI ADI ---
        self.user_label = ttk.Label(self.center_frame, text="Kullanıcı Adı:")
        self.user_label.pack(fill="x", pady=(5, 0))
        
        self.user_entry = ttk.Entry(self.center_frame, font=("Segoe UI", 11))
        self.user_entry.pack(fill="x", pady=5, ipady=3) # ipady: kutuyu biraz şişirir, modern durur

        # --- ŞİFRE / TELEFON ---
        self.pass_label = ttk.Label(self.center_frame, text="Şifre:")
        self.pass_label.pack(fill="x", pady=(15, 0))
        
        self.pass_entry = ttk.Entry(self.center_frame, font=("Segoe UI", 11), show="*")
        self.pass_entry.pack(fill="x", pady=5, ipady=3)

        # --- ROL SEÇİMİ (SWITCH) ---
        self.role_var = tk.StringVar(value="personel")
        self.role_var.trace("w", self.arayuzu_guncelle)

        self.radio_frame = tk.Frame(self.center_frame, bg=self.bg_color)
        self.radio_frame.pack(pady=20)

        # ttk.Radiobutton kullanıyoruz
        self.rb_personel = ttk.Radiobutton(self.radio_frame, text="Personel / Vet", variable=self.role_var, value="personel")
        self.rb_personel.pack(side="left", padx=10)

        self.rb_customer = ttk.Radiobutton(self.radio_frame, text="Sahiplenen", variable=self.role_var, value="customer")
        self.rb_customer.pack(side="left", padx=10)

        # --- GİRİŞ BUTONU ---
        self.login_btn = ttk.Button(self.center_frame, text="GİRİŞ YAP", cursor="hand2", command=self.login_kontrol)
        self.login_btn.pack(fill="x", pady=30)

    # functions
    def arayuzu_guncelle(self, *args):
        # entryleri temizle
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)
        secilen = self.role_var.get()
        if secilen == "personel":
            self.user_label.config(text="Kullanıcı Adı:")
            self.pass_label.config(text="Şifre:")
            self.pass_entry.config(show="*")
            self.login_btn.config(text="PERSONEL GİRİŞİ")
        else:
            self.user_label.config(text="Ad Soyad:")
            self.pass_label.config(text="Telefon Numarası:")
            self.pass_entry.config(show="")
            self.login_btn.config(text="SORGULA / GİRİŞ")

    def login_kontrol(self):
        print(f"Giriş deneniyor: {self.user_entry.get()}")