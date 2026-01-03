import tkinter as tk
from tkinter import ttk, messagebox
import sys

sys.path.append("..") 
from database import DataBase
from languages import TEXTS

class LoginWindow:
    def __init__(self, root, on_login_success, lang="TR"):
        self.root = root
        self.on_login_success = on_login_success
        self.current_lang = lang # DEĞİŞİKLİK 2: Gelen dili kullandık (Eskiden direkt "TR" idi)
        
        self.root.geometry("600x750")
        self.bg_color = "#cbeef7" 
        self.root.configure(bg=self.bg_color)
        
        # Telefon doğrulama
        self.vcmd = (self.root.register(self.validate_phone), '%P')

        # --- STİL ---
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TLabel", background=self.bg_color, foreground="#2c3e50", font=("Segoe UI", 11))
        self.style.configure("Baslik.TLabel", font=("Segoe UI", 20, "bold"), foreground="#2c3e50")
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=10, background="#4da5fd", foreground="white")
        self.style.map("TButton", background=[("active","#1abc9c")]) 
        self.style.configure("TRadiobutton", background=self.bg_color, font=("Segoe UI", 10))

        # --- DİL BUTONU (YENİ & ŞIK) ---
        btn_text = "🇹🇷 TR" if self.current_lang == "TR" else "🇬🇧 EN"
        
        self.lang_btn = tk.Button(self.root, text=btn_text, font=("Segoe UI", 10, "bold"), 
                                  bg="white", fg="#004f63", bd=0, cursor="hand2",
                                  activebackground="#e1e1e1",
                                  command=self.toggle_language)
        
        self.lang_btn.place(relx=0.95, y=20, anchor="ne")

        # --- ORTA ÇERÇEVE ---
        self.center_frame = tk.Frame(self.root, bg=self.bg_color, width=320, height=600)
        self.center_frame.pack_propagate(False)
        self.center_frame.pack(expand=True)

        self.login_label = ttk.Label(self.center_frame, text="", style="Baslik.TLabel")
        self.login_label.pack(pady=(40, 30))

        self.user_label = ttk.Label(self.center_frame, text="")
        self.user_label.pack(fill="x", pady=(5, 0))
        self.user_entry = ttk.Entry(self.center_frame, font=("Segoe UI", 11))
        self.user_entry.pack(fill="x", pady=5, ipady=3)

        self.pass_label = ttk.Label(self.center_frame, text="")
        self.pass_label.pack(fill="x", pady=(15, 0))
        self.pass_entry = ttk.Entry(self.center_frame, font=("Segoe UI", 11), show="*")
        self.pass_entry.pack(fill="x", pady=5, ipady=3)

        self.user_entry.bind('<Return>', lambda event: self.pass_entry.focus_set())
        self.pass_entry.bind('<Return>', lambda event: self.login_kontrol())

        self.role_var = tk.StringVar(value="personel")
        self.role_var.trace("w", self.update_ui_text)

        self.radio_frame = tk.Frame(self.center_frame, bg=self.bg_color)
        self.radio_frame.pack(pady=20)

        self.rb_personel = ttk.Radiobutton(self.radio_frame, variable=self.role_var, value="personel")
        self.rb_personel.pack(side="left", padx=10)

        self.rb_customer = ttk.Radiobutton(self.radio_frame, variable=self.role_var, value="customer")
        self.rb_customer.pack(side="left", padx=10)

        self.exit_btn = tk.Button(self.center_frame, bg=self.bg_color, fg="#c0392b",
                                  font=("Segoe UI", 10), borderwidth=0, cursor="hand2",
                                  command=self.root.destroy)
        self.exit_btn.pack(side="bottom", pady=20)

        self.login_btn = ttk.Button(self.center_frame, cursor="hand2", command=self.login_kontrol)
        self.login_btn.pack(fill="x", pady=20)
        
        self.register_btn = tk.Button(self.center_frame, bg=self.bg_color, fg="#004f63",
                                      font=("Segoe UI", 10, "underline"), borderwidth=0, cursor="hand2",
                                      command=self.open_register_popup)

        self.update_ui_text()

    def validate_phone(self, new_value):
        if new_value == "": return True
        if not new_value.isdigit(): return False
        if len(new_value) > 10: return False
        if len(new_value) > 0 and new_value[0] != '5': return False
        return True

    def toggle_language(self):
        """Dili değiştirir ve butonu günceller"""
        if self.current_lang == "TR":
            self.current_lang = "EN"
            self.lang_btn.config(text="🇬🇧 EN") # İngiliz Bayrağı Emojisi
        else:
            self.current_lang = "TR"
            self.lang_btn.config(text="🇹🇷 TR") # Türk Bayrağı Emojisi
            
        self.update_ui_text()

    def update_ui_text(self, *args):
        t = TEXTS[self.current_lang]
        self.root.title(t["window_title"])
        self.login_label.config(text=t["login_title"])
        
        role = self.role_var.get()
        if role == "personel":
             self.user_label.config(text=t["user_label"])
             self.pass_label.config(text=t["pass_label"])
             self.login_btn.config(text=t["login_btn_personel"])
             self.register_btn.pack_forget()
        else:
             self.user_label.config(text=t["user_label"])
             self.pass_label.config(text=t["pass_label"])
             self.login_btn.config(text=t["login_btn_customer"])
             self.register_btn.pack(pady=5)
             self.register_btn.config(text=t["register_link"])

        self.rb_personel.config(text=t["personel_role"])
        self.rb_customer.config(text=t["customer_role"])
        self.exit_btn.config(text=t["exit_btn"])

    def login_kontrol(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        role = self.role_var.get()
        t = TEXTS[self.current_lang]

        if not username or not password:
            messagebox.showwarning("Uyarı", t["error_fill"])
            return

        db = DataBase()
        user = db.check_login(username, password, role)
        if user:
            self.on_login_success(user, self.current_lang)
        else:
            messagebox.showerror("Hata", t["error_login"])

    def open_register_popup(self):
        t = TEXTS[self.current_lang]
        self.reg_window = tk.Toplevel(self.root)
        self.reg_window.title(t["register_title"])
        self.reg_window.geometry("350x450")
        self.reg_window.configure(bg=self.bg_color)
        
        x = self.root.winfo_x() + 125
        y = self.root.winfo_y() + 100
        self.reg_window.geometry(f"+{x}+{y}")

        tk.Label(self.reg_window, text=t["register_title"], bg=self.bg_color, fg="#2c3e50", font=("Segoe UI", 16, "bold")).pack(pady=20)
        form_frame = tk.Frame(self.reg_window, bg=self.bg_color)
        form_frame.pack(pady=10)

        self.create_reg_entry(form_frame, t["name_label"], "reg_name")
        self.create_reg_entry(form_frame, t["phone_hint_label"], "reg_phone")
        self.create_reg_entry(form_frame, t["user_label"], "reg_user")
        
        tk.Label(form_frame, text=t["pass_label"], bg=self.bg_color, font=("Segoe UI", 10)).pack(anchor="w")
        self.reg_pass = ttk.Entry(form_frame, width=30, show="*")
        self.reg_pass.pack(pady=5)

        ttk.Button(self.reg_window, text=t["register_btn"], command=self.perform_register).pack(pady=20)
        self.reg_name.focus_set()

    def create_reg_entry(self, parent, label, var_name):
        tk.Label(parent, text=label, bg=self.bg_color, font=("Segoe UI", 10)).pack(anchor="w")
        if var_name == "reg_phone":
            entry = ttk.Entry(parent, width=30, validate="key", validatecommand=self.vcmd)
        else:
            entry = ttk.Entry(parent, width=30)
        entry.pack(pady=5)
        setattr(self, var_name, entry)

    def perform_register(self):
        t = TEXTS[self.current_lang]
        fullname = self.reg_name.get()
        phone = self.reg_phone.get()
        username = self.reg_user.get()
        password = self.reg_pass.get()

        if not fullname or not username or not password:
            messagebox.showwarning("Eksik", t["error_fill"])
            return
        
        if len(phone) != 10:
            messagebox.showwarning("Hata", t["error_phone"])
            return

        db = DataBase()
        success, msg = db.add_user(username, password, "customer", fullname, phone)

        if success:
            messagebox.showinfo("Başarılı", t["success_reg"])
            self.reg_window.destroy()
            self.user_entry.delete(0, tk.END)
            self.user_entry.insert(0, username)
        else:
            messagebox.showerror("Hata", msg)