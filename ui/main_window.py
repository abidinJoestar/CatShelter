import tkinter as tk
from tkinter import ttk
import sys

# Dil dosyasını ve sayfaları import ediyoruz
from languages import TEXTS
from ui.cat_page import CatPage
from ui.user_page import UserPage
from ui.adoption_page import AdoptionPage

sys.path.append("..") 
from database import DataBase 

class CatShelterApp:
    def __init__(self, root, current_user, lang="TR", on_logout=None):
        self.root = root
        self.current_user = current_user
        self.lang = lang
        self.on_logout = on_logout 
        self.vcmd = (self.root.register(self.validate_phone), '%P')

        # Renkler
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

        # Sayfaları bir kere başlatıyoruz
        self.cat_page = CatPage(self)
        self.user_page = UserPage(self)
        self.adoption_page = AdoptionPage(self)

        # Arayüzü kur
        self.setup_ui()

    def setup_ui(self):
        """Tüm arayüzü (yeniden) oluşturur"""
        # Ekranı temizle
        for widget in self.root.winfo_children():
            widget.destroy()

        self.t = TEXTS[self.lang] # Seçili dile göre sözlüğü güncelle
        self.root.title(f"Cat Shelter - {self.current_user[4]}") 
        self.root.geometry("1000x600")

        # --- SOL MENÜ ---
        self.left_frame = ttk.Frame(self.root, style="Sidebar.TFrame", width=200)
        self.left_frame.pack(side="left", fill="y")
        
        ttk.Label(self.left_frame, text="Cat Shelter", style="Title.TLabel").pack(pady=(30, 5))

        user_role = self.current_user[3]
        role_baslik = self.t["admin_panel"] if user_role == 'personel' else self.t["user_panel"]
        ttk.Label(self.left_frame, text=role_baslik, background=self.sidebar_bg, foreground="#004f63", font=("Segoe UI", 10, "italic")).pack(pady=(0, 20))

        if user_role == 'personel':
            self.create_menu_button(self.t["menu_cat_manage"], self.cat_page.show_cats)
            self.create_menu_button(self.t["menu_cat_add"], self.cat_page.add_cat)
            self.create_menu_button(self.t["menu_apps"], self.adoption_page.show_applications)
            self.create_menu_button(self.t["menu_personnel"], self.user_page.show_personnel)
            self.create_menu_button(self.t["menu_customer"], self.user_page.show_customers)
            self.create_menu_button(self.t["menu_reports"], self.show_reports) 
        else:
            self.create_menu_button(self.t["menu_cat_view"], self.cat_page.show_cats)
            self.create_menu_button(self.t["menu_my_cats"], self.adoption_page.show_my_cats)
            self.create_menu_button(self.t["menu_about"], self.show_about)

        self.create_menu_button(self.t["menu_logout"], self.cikis_yap)

        # --- SAĞ PANEL (Main Frame) ---
        self.main_frame = ttk.Frame(self.root, style="Main.TFrame")
        self.main_frame.pack(side="right", fill="both", expand=True)

        # --- DİL DEĞİŞTİRME BUTONU (SAĞ ÜST) ---
        btn_text = "🇹🇷 TR" if self.lang == "TR" else "🇬🇧 EN"
        lang_btn = tk.Button(self.root, text=btn_text, font=("Segoe UI", 10, "bold"), 
                             bg="white", fg="#004f63", bd=0, cursor="hand2",
                             activebackground="#e1e1e1",
                             command=self.toggle_language)
        # Main frame'in içinde sağ üst köşeye yerleştiriyoruz
        lang_btn.place(relx=0.95, y=20, anchor="ne")
        
        # Hoşgeldin mesajı
        welcome_msg = self.t["welcome"].format(self.current_user[4])
        ttk.Label(self.main_frame, text=welcome_msg, style="Normal.TLabel").pack(expand=True)

    def toggle_language(self):
        """Dili değiştirir ve tüm arayüzü yeniler"""
        self.lang = "EN" if self.lang == "TR" else "TR"
        self.setup_ui() # Arayüzü yeniden çiz

    # --- YARDIMCI FONKSİYONLAR ---
    def validate_phone(self, new_value):
        if new_value == "": return True
        if not new_value.isdigit(): return False
        if len(new_value) > 10: return False
        if len(new_value) > 0 and new_value[0] != '5': return False
        return True

    def create_form_entry(self, parent, label_text, var_name, row=0):
        tk.Label(parent, text=label_text, bg=self.main_bg, font=("Segoe UI", 12)).grid(row=row, column=0, sticky="e", pady=10, padx=10)
        
        if "phone" in var_name:
            entry = ttk.Entry(parent, width=30, font=("Segoe UI", 10), validate="key", validatecommand=self.vcmd)
        else:
            entry = ttk.Entry(parent, width=30, font=("Segoe UI", 10))
            
        entry.grid(row=row, column=1, pady=10, sticky="w")
        setattr(self, var_name, entry)

    def create_menu_button(self, text, command):
        btn = ttk.Button(self.left_frame, text=text, command=command, style="Menu.TButton", cursor="hand2")
        btn.pack(fill="x", pady=5, padx=10, ipady=5)

    def cikis_yap(self):
        if self.on_logout: self.on_logout()
        self.on_logout(self.lang)

    def clear_main_frame(self):
        # Sadece frame'in içindekileri sil, üstteki Dil butonuna dokunma
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_reports(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Raporlar / Reports", style="Normal.TLabel").pack(pady=50)

    def show_about(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Kedi Barınağı Sistemi v1.0", style="Normal.TLabel").pack(pady=50)