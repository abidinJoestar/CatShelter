import tkinter as tk
from tkinter import ttk, messagebox

class CatShelterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cat Shelter Yönetim Sistemi")
        self.root.geometry("1000x600")
        
        # --- Sol Menü Paneli ---
        self.left_frame = tk.Frame(self.root, bg="#2c3e50", width=200)
        self.left_frame.pack(side="left", fill="y")
        
        # Başlık
        self.title_label = tk.Label(self.left_frame, text="🐱 Cat Shelter", bg="#2c3e50", fg="white", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=30)

        # Menü Butonları
        self.create_menu_button("Kedileri Listele", self.show_cats)
        self.create_menu_button("Yeni Kedi Ekle", self.add_cat)
        self.create_menu_button("Sahiplendirme", self.adopt_cat)
        self.create_menu_button("Çıkış", self.root.quit)

        # --- Sağ Ana İçerik Paneli ---
        self.main_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.main_frame.pack(side="right", fill="both", expand=True)
        
        # Açılış mesajı
        self.welcome_label = tk.Label(self.main_frame, text="Hoşgeldiniz!\nSol menüden işlem seçiniz.", bg="#ecf0f1", font=("Arial", 14))
        self.welcome_label.pack(expand=True)

    def create_menu_button(self, text, command):
        """Menü butonlarını oluşturmak için yardımcı fonksiyon"""
        btn = tk.Button(self.left_frame, text=text, command=command, 
                        bg="#34495e", fg="white", bd=0, pady=10, 
                        activebackground="#1abc9c", activeforeground="white", font=("Arial", 10))
        btn.pack(fill="x", pady=2, padx=5)

    # --- Fonksiyon Taslakları (Şimdilik boş) ---
    def show_cats(self):
        self.clear_main_frame()
        lbl = tk.Label(self.main_frame, text="Kedi Listesi Sayfası (Yapılacak)", bg="#ecf0f1", font=("Arial", 12))
        lbl.pack(pady=20)

    def add_cat(self):
        self.clear_main_frame()
        lbl = tk.Label(self.main_frame, text="Kedi Ekleme Formu (Yapılacak)", bg="#ecf0f1", font=("Arial", 12))
        lbl.pack(pady=20)

    def adopt_cat(self):
        self.clear_main_frame()
        lbl = tk.Label(self.main_frame, text="Sahiplendirme İşlemleri (Yapılacak)", bg="#ecf0f1", font=("Arial", 12))
        lbl.pack(pady=20)

    def clear_main_frame(self):
        """Sağ paneldeki her şeyi temizler"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()