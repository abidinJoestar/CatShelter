import tkinter as tk
from tkinter import ttk
import sys

# DİĞER SAYFALARI İMPORT EDİYORUZ
from ui.cat_page import CatPage
from ui.user_page import UserPage
from ui.adoption_page import AdoptionPage

sys.path.append("..") 
from database import DataBase 

class CatShelterApp:
    def __init__(self, root, current_user, on_logout=None):
        self.root = root
        self.current_user = current_user 
        self.on_logout = on_logout 

        # TELEFON DOĞRULAMA (GLOBAL)
        self.vcmd = (self.root.register(self.validate_phone), '%P')

        # Temizlik
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(f"Cat Shelter - {self.current_user[4]}") 
        self.root.geometry("1000x600")
        
        # --- RENKLER ---
        self.sidebar_bg = "#7ce1ff"   
        self.main_bg = "#cbeef7"      
        self.btn_bg = "#4da5fd"       
        self.text_color = "#004f63"   

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Sidebar.TFrame", background=self.sidebar_bg)
        self.style.configure("Main.TFrame", background=self.main_bg)
        self.style.configure("Title.TLabel", background=self.sidebar_bg, foreground="white", font=("Segoe UI", 16, "bold"))
        self.style.configure("Menu.TButton", font=("Segoe UI", 10, "bold"), background=self.btn_bg, foreground="white", borderwidth=0)
        self.style.configure("Normal.TLabel", background=self.main_bg, foreground=self.text_color, font=("Segoe UI", 12))
        
        self.style.configure("Treeview", background="white", fieldbackground="white", foreground="black", font=("Segoe UI", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e1e1e1")

        # --- SAYFA YÖNETİCİLERİNİ BAŞLAT ---
        # Kendimizi (self) parametre olarak gönderiyoruz ki diğer sayfalar bize erişebilsin
        self.cat_page = CatPage(self)
        self.user_page = UserPage(self)
        self.adoption_page = AdoptionPage(self)

        # --- SOL MENÜ ---
        self.left_frame = ttk.Frame(self.root, style="Sidebar.TFrame", width=200)
        self.left_frame.pack(side="left", fill="y")
        
        ttk.Label(self.left_frame, text="Cat Shelter", style="Title.TLabel").pack(pady=(30, 5))

        user_role = self.current_user[3]
        role_baslik = "Yönetici Paneli" if user_role == 'personel' else "Sahiplenme Paneli"
        ttk.Label(self.left_frame, text=role_baslik, background=self.sidebar_bg, foreground="#004f63", font=("Segoe UI", 10, "italic")).pack(pady=(0, 20))

        if user_role == 'personel':
            self.create_menu_button("Kedileri Yönet", self.cat_page.show_cats)
            self.create_menu_button("Yeni Kedi Ekle", self.cat_page.add_cat)
            self.create_menu_button("Başvurular", self.adoption_page.show_applications)
            self.create_menu_button("Personel Listesi", self.user_page.show_personnel)
            self.create_menu_button("Müşteri Listesi", self.user_page.show_customers)
            self.create_menu_button("Raporlar", self.show_reports) 
        else:
            self.create_menu_button("Kedileri Gör", self.cat_page.show_cats)
            self.create_menu_button("Sahiplendiklerim", self.adoption_page.show_my_cats)
            self.create_menu_button("Hakkımızda", self.show_about)

        self.create_menu_button("Çıkış Yap", self.cikis_yap)

        # --- SAĞ PANEL ---
        self.main_frame = ttk.Frame(self.root, style="Main.TFrame")
        self.main_frame.pack(side="right", fill="both", expand=True)
        
        ttk.Label(self.main_frame, text=f"Merhaba, {self.current_user[4]}!", style="Normal.TLabel").pack(expand=True)

    # --- ORTAK YARDIMCI FONKSİYONLAR ---
    def validate_phone(self, new_value):
        if new_value == "": return True
        if not new_value.isdigit(): return False
        if len(new_value) > 10: return False
        if len(new_value) > 0 and new_value[0] != '5': return False
        return True

    def create_form_entry(self, parent, label_text, var_name, row=0):
        # Bu fonksiyonu diğer sayfalar self.app.create_form_entry diye çağıracak
        tk.Label(parent, text=label_text, bg=self.main_bg, font=("Segoe UI", 12)).grid(row=row, column=0, sticky="e", pady=10, padx=10)
        
        if "phone" in var_name:
            entry = ttk.Entry(parent, width=30, font=("Segoe UI", 10), validate="key", validatecommand=self.vcmd)
        else:
            entry = ttk.Entry(parent, width=30, font=("Segoe UI", 10))
            
        entry.grid(row=row, column=1, pady=10, sticky="w")
        # Değişkeni 'Main Window' üzerine kaydediyoruz ki her yerden erişilsin
        setattr(self, var_name, entry)

    def create_menu_button(self, text, command):
        btn = ttk.Button(self.left_frame, text=text, command=command, style="Menu.TButton", cursor="hand2")
        btn.pack(fill="x", pady=5, padx=10, ipady=5)

    def cikis_yap(self):
        if self.on_logout: self.on_logout()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_reports(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Raporlar (Yapım Aşamasında)", style="Normal.TLabel").pack(pady=50)

    def show_about(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Kedi Barınağı Sistemi v1.0", style="Normal.TLabel").pack(pady=50)