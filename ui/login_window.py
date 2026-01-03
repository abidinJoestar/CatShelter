import tkinter as tk
from tkinter import ttk, messagebox
import sys

sys.path.append("..") 
from database import DataBase

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        
        self.root.title("Kedi Barınağı Sistemi")
        self.root.geometry("600x700")
            
        self.bg_color = "#cbeef7" 
        self.root.configure(bg=self.bg_color)

        # --- TELEFON DOĞRULAMA KOMUTU (YENİ) ---
        # Kullanıcı her tuşa bastığında bu fonksiyon çalışacak
        self.vcmd = (self.root.register(self.validate_phone), '%P')

        # --- STİL AYARLARI ---
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TLabel", background=self.bg_color, foreground="#2c3e50", font=("Segoe UI", 11))
        self.style.configure("Baslik.TLabel", font=("Segoe UI", 20, "bold"), foreground="#2c3e50")
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=10, background="#4da5fd", foreground="white")
        self.style.map("TButton", background=[("active","#1abc9c")]) 
        self.style.configure("TRadiobutton", background=self.bg_color, font=("Segoe UI", 10))

        # --- ORTA ÇERÇEVE ---
        self.center_frame = tk.Frame(self.root, bg=self.bg_color, width=320, height=580)
        self.center_frame.pack_propagate(False)
        self.center_frame.pack(expand=True)

        # Başlık
        self.login_label = ttk.Label(self.center_frame, text="Sisteme Giriş", style="Baslik.TLabel")
        self.login_label.pack(pady=(40, 30))

        # Kullanıcı Adı
        self.user_label = ttk.Label(self.center_frame, text="Kullanıcı Adı:")
        self.user_label.pack(fill="x", pady=(5, 0))
        self.user_entry = ttk.Entry(self.center_frame, font=("Segoe UI", 11))
        self.user_entry.pack(fill="x", pady=5, ipady=3)

        # Şifre
        self.pass_label = ttk.Label(self.center_frame, text="Şifre:")
        self.pass_label.pack(fill="x", pady=(15, 0))
        self.pass_entry = ttk.Entry(self.center_frame, font=("Segoe UI", 11), show="*")
        self.pass_entry.pack(fill="x", pady=5, ipady=3)

        # --- ENTER TUŞU ZİNCİRİ ---
        self.user_entry.bind('<Return>', lambda event: self.pass_entry.focus_set())
        self.pass_entry.bind('<Return>', lambda event: self.login_kontrol())

        # ROL SEÇİMİ
        self.role_var = tk.StringVar(value="personel")
        self.role_var.trace("w", self.arayuzu_guncelle)

        self.radio_frame = tk.Frame(self.center_frame, bg=self.bg_color)
        self.radio_frame.pack(pady=20)

        self.rb_personel = ttk.Radiobutton(self.radio_frame, text="Personel / Vet", variable=self.role_var, value="personel")
        self.rb_personel.pack(side="left", padx=10)

        self.rb_customer = ttk.Radiobutton(self.radio_frame, text="Sahiplenen", variable=self.role_var, value="customer")
        self.rb_customer.pack(side="left", padx=10)

        # --- ÇIKIŞ BUTONU ---
        self.exit_btn = tk.Button(self.center_frame, text="Uygulamayı Kapat", bg=self.bg_color, fg="#c0392b",
                                  font=("Segoe UI", 10), borderwidth=0, cursor="hand2",
                                  activebackground=self.bg_color, activeforeground="red",
                                  command=self.uygulamayi_kapat)
        self.exit_btn.pack(side="bottom", pady=20)

        # GİRİŞ BUTONU
        self.login_btn = ttk.Button(self.center_frame, text="GİRİŞ YAP", cursor="hand2", command=self.login_kontrol)
        self.login_btn.pack(fill="x", pady=20)
        
        # KAYIT OL BUTONU
        self.register_btn = tk.Button(self.center_frame, text="Hesabınız yok mu? Kayıt Ol", 
                                      bg=self.bg_color, fg="#004f63", activebackground=self.bg_color,
                                      font=("Segoe UI", 10, "underline"), borderwidth=0, cursor="hand2",
                                      command=self.open_register_popup)

        # Başlangıç
        self.arayuzu_guncelle()

    # --- YENİ EKLENEN TELEFON DOĞRULAMA FONKSİYONU ---
    def validate_phone(self, new_value):
        """Telefon kutusuna girilen değeri kontrol eder"""
        # Eğer kutu boşaltılıyorsa izin ver (Silme işlemi için)
        if new_value == "":
            return True
        
        # 1. Sadece rakam girilsin
        if not new_value.isdigit():
            return False
            
        # 2. Maksimum 10 karakter olsun
        if len(new_value) > 10:
            return False
            
        # 3. İlk karakter mutlaka 5 olsun
        if len(new_value) > 0 and new_value[0] != '5':
            return False
            
        return True

    def uygulamayi_kapat(self):
        self.root.destroy()

    def arayuzu_guncelle(self, *args):
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)
        self.user_entry.focus_set()
        
        secilen = self.role_var.get()
        if secilen == "personel":
            self.login_btn.config(text="PERSONEL GİRİŞİ")
            self.register_btn.pack_forget()
        else:
            self.login_btn.config(text="MÜŞTERİ GİRİŞİ")
            self.register_btn.pack(pady=5)

    def login_kontrol(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun.")
            return

        try:
            db = DataBase()
            user = db.check_login(username, password, role)
            if user:
                self.on_login_success(user)
            else:
                messagebox.showerror("Hata", "Giriş bilgileri hatalı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Veritabanı hatası: {e}")

    # --- KAYIT PENCERESİ ---
    def open_register_popup(self):
        self.reg_window = tk.Toplevel(self.root)
        self.reg_window.title("Aramıza Katıl")
        self.reg_window.geometry("350x450")
        self.reg_window.configure(bg=self.bg_color)
        
        x = self.root.winfo_x() + 125
        y = self.root.winfo_y() + 100
        self.reg_window.geometry(f"+{x}+{y}")

        tk.Label(self.reg_window, text="Yeni Üyelik 🐾", bg=self.bg_color, fg="#2c3e50", font=("Segoe UI", 16, "bold")).pack(pady=20)

        form_frame = tk.Frame(self.reg_window, bg=self.bg_color)
        form_frame.pack(pady=10)

        self.create_reg_entry(form_frame, "Ad Soyad:", "reg_name")
        # Telefon için özel label ekliyoruz (Formatı belirtmek için)
        self.create_reg_entry(form_frame, "Telefon (5xxxxxxxxx):", "reg_phone")
        self.create_reg_entry(form_frame, "Kullanıcı Adı:", "reg_user")
        
        tk.Label(form_frame, text="Şifre:", bg=self.bg_color, font=("Segoe UI", 10)).pack(anchor="w")
        self.reg_pass = ttk.Entry(form_frame, width=30, show="*")
        self.reg_pass.pack(pady=5)

        ttk.Button(self.reg_window, text="KAYDOL", command=self.perform_register).pack(pady=20)

        self.reg_name.bind('<Return>', lambda e: self.reg_phone.focus_set())
        self.reg_phone.bind('<Return>', lambda e: self.reg_user.focus_set())
        self.reg_user.bind('<Return>', lambda e: self.reg_pass.focus_set())
        self.reg_pass.bind('<Return>', lambda e: self.perform_register())
        self.reg_name.focus_set()

    def create_reg_entry(self, parent, label, var_name):
        tk.Label(parent, text=label, bg=self.bg_color, font=("Segoe UI", 10)).pack(anchor="w")
        
        # Eğer oluşturulan kutucuk Telefon ise kısıtlamayı uygula
        if var_name == "reg_phone":
            entry = ttk.Entry(parent, width=30, validate="key", validatecommand=self.vcmd)
        else:
            entry = ttk.Entry(parent, width=30)
            
        entry.pack(pady=5)
        setattr(self, var_name, entry)

    def perform_register(self):
        fullname = self.reg_name.get()
        phone = self.reg_phone.get()
        username = self.reg_user.get()
        password = self.reg_pass.get()

        if not fullname or not username or not password:
            messagebox.showwarning("Eksik", "Lütfen tüm alanları doldurun.")
            return

        # Telefon kontrolü (Tam 10 hane olmalı)
        if len(phone) != 10:
            messagebox.showwarning("Hata", "Telefon numarası 10 haneli olmalıdır (Örn: 5321234567)")
            return

        db = DataBase()
        success, msg = db.add_user(username, password, "customer", fullname, phone)

        if success:
            messagebox.showinfo("Başarılı", "Kaydınız oluşturuldu! Giriş yapabilirsiniz.")
            self.reg_window.destroy()
            self.user_entry.delete(0, tk.END)
            self.user_entry.insert(0, username)
            self.pass_entry.focus_set()
        else:
            messagebox.showerror("Hata", msg)