import tkinter as tk
from tkinter import ttk

class CatShelterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cat Shelter Yönetim Sistemi")
        self.root.geometry("1000x600")
        
        # --- RENK PALETİ ---
        # Renkleri değişkenlere atayalım ki yönetmesi kolay olsun
        self.sidebar_bg = "#7ce1ff"   # Sol panel rengi
        self.main_bg = "#cbeef7"      # Ana içerik rengi
        self.btn_bg = "#4da5fd"       # Buton rengi
        self.btn_active = "#1abc9c"   # Buton üzerine gelince
        self.text_color = "#004f63"   # Yazı rengi

        # --- TTK STİL AYARLARI ---
        self.style = ttk.Style()
        self.style.theme_use('clam') # Renk değişimini destekleyen tema

        # 1. Sol Panel (Sidebar) Stili
        self.style.configure("Sidebar.TFrame", background=self.sidebar_bg)
        
        # 2. Ana Panel (Main) Stili
        self.style.configure("Main.TFrame", background=self.main_bg)

        # 3. Sol Paneldeki Başlık (Label) Stili
        self.style.configure("Title.TLabel", 
                             background=self.sidebar_bg, 
                             foreground="white", 
                             font=("Segoe UI", 16, "bold"))

        # 4. Menü Butonları Stili
        self.style.configure("Menu.TButton", 
                             font=("Segoe UI", 10, "bold"), 
                             background=self.btn_bg, 
                             foreground="white",
                             borderwidth=0,
                             focuscolor="none") # Tıklayınca oluşan kesikli çizgiyi kaldırır
        
        # Buton üzerine gelince (hover) renk değişimi
        self.style.map("Menu.TButton", 
                       background=[("active", self.btn_active)],
                       foreground=[("active", "white")])

        # 5. Genel Yazı Stili
        self.style.configure("Normal.TLabel", 
                             background=self.main_bg, 
                             foreground=self.text_color, 
                             font=("Segoe UI", 12))


        # --- SOL MENÜ PANELİ ---
        # Not: tk.Frame yerine ttk.Frame kullanıyoruz ve style veriyoruz
        self.left_frame = ttk.Frame(self.root, style="Sidebar.TFrame", width=200)
        self.left_frame.pack(side="left", fill="y")
        
        # Başlık
        self.title_label = ttk.Label(self.left_frame, text="Cat Shelter", style="Title.TLabel")
        self.title_label.pack(pady=30)

        # Menü Butonları
        self.create_menu_button("Kedileri Listele", self.show_cats)
        self.create_menu_button("Yeni Kedi Ekle", self.add_cat)
        self.create_menu_button("Sahiplendirme", self.adopt_cat)
        self.create_menu_button("Çıkış", self.root.quit)

        # --- SAĞ ANA İÇERİK PANELİ ---
        self.main_frame = ttk.Frame(self.root, style="Main.TFrame")
        self.main_frame.pack(side="right", fill="both", expand=True)
        
        # Açılış mesajı
        self.welcome_label = ttk.Label(self.main_frame, 
                                       text="Hoşgeldiniz!\nSol menüden işlem seçiniz.", 
                                       style="Normal.TLabel")
        self.welcome_label.pack(expand=True)

    def create_menu_button(self, text, command):
        """Menü butonlarını oluşturmak için yardımcı fonksiyon"""
        # Padding ile butonu biraz şişiriyoruz ki daha modern dursun (ipady)
        btn = ttk.Button(self.left_frame, text=text, command=command, style="Menu.TButton", cursor="hand2")
        btn.pack(fill="x", pady=5, padx=10, ipady=5)

    # --- Fonksiyon Taslakları ---
    def show_cats(self):
        self.clear_main_frame()
        lbl = ttk.Label(self.main_frame, text="Kedi Listesi Sayfası (Yapılacak)", style="Normal.TLabel")
        lbl.pack(pady=20)

    def add_cat(self):
        self.clear_main_frame()
        lbl = ttk.Label(self.main_frame, text="Kedi Ekleme Formu (Yapılacak)", style="Normal.TLabel")
        lbl.pack(pady=20)

    def adopt_cat(self):
        self.clear_main_frame()
        lbl = ttk.Label(self.main_frame, text="Sahiplendirme İşlemleri (Yapılacak)", style="Normal.TLabel")
        lbl.pack(pady=20)

    def clear_main_frame(self):
        """Sağ paneldeki her şeyi temizler"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()