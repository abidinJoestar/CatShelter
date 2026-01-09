import tkinter as tk
from tkinter import ttk
import sys
from tkinter import messagebox
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
        self.current_view_func = None
         
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

        self.cat_page = CatPage(self)
        self.user_page = UserPage(self)
        self.adoption_page = AdoptionPage(self)

        self.setup_ui()

    def setup_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.t = TEXTS[self.lang]
        self.root.title(f"Cat Shelter - {self.current_user[4]}") 
        self.root.geometry("1000x600")

        # left menu
        self.left_frame = ttk.Frame(self.root, style="Sidebar.TFrame", width=240) 
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.pack_propagate(False)
        ttk.Label(self.left_frame, text="Cat Shelter", style="Title.TLabel").pack(pady=(30, 5))

        user_role = self.current_user[3]
        role_baslik = self.t["admin_panel"] if user_role == 'personel' else self.t["user_panel"]
        ttk.Label(self.left_frame, text=role_baslik, background=self.sidebar_bg, foreground="#004f63", font=("Segoe UI", 10, "italic")).pack(pady=(0, 20))

        if user_role == 'personel':
            self.create_menu_button(self.t["menu_cat_manage"], lambda: self.navigate_to(self.cat_page.show_cats))
            self.create_menu_button(self.t["menu_cat_add"], lambda: self.navigate_to(self.cat_page.add_cat))
            self.create_menu_button(self.t["menu_apps"], lambda: self.navigate_to(self.adoption_page.show_applications))
            self.create_menu_button(self.t["menu_personnel"], lambda: self.navigate_to(self.user_page.show_personnel))
            self.create_menu_button(self.t["menu_customer"], lambda: self.navigate_to(self.user_page.show_customers))
            self.create_menu_button(self.t["menu_reports"], lambda: self.navigate_to(self.show_reports)) 
        else:
            self.create_menu_button(self.t["menu_cat_view"], lambda: self.navigate_to(self.cat_page.show_cats))
            self.create_menu_button(self.t["menu_my_cats"], lambda: self.navigate_to(self.adoption_page.show_my_cats))
            self.create_menu_button(self.t["menu_about"], lambda: self.navigate_to(self.show_about))

        self.create_menu_button(self.t["menu_logout"], self.cikis_yap)

        # main frame
        self.main_frame = ttk.Frame(self.root, style="Main.TFrame")
        self.main_frame.pack(side="right", fill="both", expand=True)

        # language btn
        btn_text = "🇹🇷 TR" if self.lang == "TR" else "🇬🇧 EN"
        lang_btn = tk.Button(self.root, text=btn_text, font=("Segoe UI", 10, "bold"), 
                             bg="white", fg="#004f63", bd=0, cursor="hand2",
                             activebackground="#e1e1e1",
                             command=self.toggle_language) # toggle_language güncellendi
        lang_btn.place(relx=0.95, y=20, anchor="ne")
        
        if not self.current_view_func:
            welcome_msg = self.t["welcome"].format(self.current_user[4])
            ttk.Label(self.main_frame, text=welcome_msg, style="Normal.TLabel").pack(expand=True)


    # about
    def show_about(self):
        self.clear_main_frame()
        
        tk.Label(self.main_frame, text=self.t["about_title"], 
                 bg=self.main_bg, fg="#004f63", 
                 font=("Segoe UI", 24, "bold")).pack(pady=(40, 20))

        desc_frame = tk.Frame(self.main_frame, bg="white", bd=1, relief="solid")
        desc_frame.pack(fill="x", padx=50, pady=10)
        
        tk.Label(desc_frame, text=self.t["about_desc"], 
                 bg="white", fg="#333", 
                 font=("Segoe UI", 12), wraplength=700, justify="center").pack(pady=20, padx=20)

        dev_frame = tk.Frame(self.main_frame, bg=self.main_bg)
        dev_frame.pack(pady=30)

        tk.Label(dev_frame, text=self.t["about_dev"] + "s", # Developers (Çoğul ekleyebilirsin veya tekil kalsın)
                 bg=self.main_bg, fg="#004f63", 
                 font=("Segoe UI", 14, "bold")).pack()
        
        tk.Label(dev_frame, text="Ufuk Karaçalı\nBurak Ege Kaya", 
                 bg=self.main_bg, fg="black", 
                 font=("Segoe UI", 16, "bold"), justify="center").pack(pady=5)
        
        tk.Label(dev_frame, text=self.t["about_uni"], 
                 bg=self.main_bg, fg="#555", 
                 font=("Segoe UI", 10, "italic")).pack()

        footer_frame = tk.Frame(self.main_frame, bg=self.main_bg)
        footer_frame.pack(side="bottom", pady=20)
        
        tk.Label(footer_frame, text=self.t["about_version"], 
                 bg=self.main_bg, fg="#888", font=("Segoe UI", 9)).pack()
        
    def toggle_language(self):
        self.lang = "EN" if self.lang == "TR" else "TR"
        self.setup_ui() # Arayüzü yeniden çiz
        if self.current_view_func:
            self.current_view_func()

    # side functions
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

    def navigate_to(self, func):
            self.current_view_func = func # save it
            func() # run it

    def cikis_yap(self):
        if self.on_logout: self.on_logout()
        self.on_logout(self.lang)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_reports(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text=self.t["header_reports"], bg=self.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)

        table_frame = tk.Frame(self.main_frame, bg=self.main_bg)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("date", "action")
        
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal")

        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15,
                            yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        y_scroll.config(command=tree.yview)
        x_scroll.config(command=tree.xview)
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")

        tree.heading("date", text=self.t["col_date"])
        tree.heading("action", text=self.t["col_action"])
        
        tree.column("date", width=150, anchor="center") 
        tree.column("action", width=600, anchor="w")    
        
        tree.pack(fill="both", expand=True)

        # get logs
        try:
            db = DataBase()
            logs = db.get_all_logs()
            
            for log in logs:
                date_time = log[0]
                raw_action = log[1]
                
                final_text = raw_action
                
                if "|||" in raw_action:
                    parts = raw_action.split("|||")
                    key = parts[0]    
                    params = parts[1:] 
                    
                    if key in self.t:
                        try:
                            final_text = self.t[key].format(*params)
                        except IndexError:
                            final_text = raw_action 
                
                tree.insert("", tk.END, values=(date_time, final_text))

        except Exception as e:
            print(e) 
            tk.Label(self.main_frame, text=f"Log error: {e}", fg="red").pack()

        # clear
        btn_clear = tk.Button(self.main_frame, text="🗑️ " + ("TEMİZLE" if self.lang=="TR" else "CLEAR LOGS"), 
                              bg="#c0392b", fg="white", font=("Segoe UI", 10, "bold"),
                              command=self.clear_logs_action)
        btn_clear.pack(pady=10)

    def clear_logs_action(self):
        confirm_msg = "Tüm geçmiş silinecek, emin misiniz?" if self.lang == "TR" else "Delete all history?"
        if messagebox.askyesno("Onay / Confirm", confirm_msg):
            try:
                db = DataBase()
                db.clear_all_logs() # Database'e bu metodu ekleyeceğiz
                self.show_reports() # Tabloyu yenile (boş halini göster)
                messagebox.showinfo("Başarılı", "Loglar temizlendi.")
            except Exception as e:
                messagebox.showerror("Hata", str(e))

    def clear_logs_action(self):
        confirm_msg = "Tüm geçmiş silinecek?" if self.lang == "TR" else "Delete all history?"
        if tk.messagebox.askyesno("Confirm", confirm_msg):
            DataBase().clear_all_logs()
            self.show_reports() # Listeyi yenile
    def show_about(self):
        self.clear_main_frame()
        
        tk.Label(self.main_frame, text=self.t["about_title"], 
                 bg=self.main_bg, fg="#004f63", 
                 font=("Segoe UI", 24, "bold")).pack(pady=(40, 20))

        desc_frame = tk.Frame(self.main_frame, bg="white", bd=1, relief="solid")
        desc_frame.pack(fill="x", padx=50, pady=10)
        
        tk.Label(desc_frame, text=self.t["about_desc"], 
                 bg="white", fg="#333", 
                 font=("Segoe UI", 12), wraplength=700, justify="center").pack(pady=20, padx=20)

        dev_frame = tk.Frame(self.main_frame, bg=self.main_bg)
        dev_frame.pack(pady=30)

        tk.Label(dev_frame, text=self.t["about_dev"], 
                 bg=self.main_bg, fg="#004f63", 
                 font=("Segoe UI", 14, "bold")).pack()
        
        tk.Label(dev_frame, text="Ufuk Karaçalı & Burak Ege Kaya", 
                 bg=self.main_bg, fg="black", 
                 font=("Segoe UI", 16)).pack(pady=5)
        
        tk.Label(dev_frame, text=self.t["about_uni"], 
                 bg=self.main_bg, fg="#555", 
                 font=("Segoe UI", 10, "italic")).pack()

        footer_frame = tk.Frame(self.main_frame, bg=self.main_bg)
        footer_frame.pack(side="bottom", pady=20)
        
        tk.Label(footer_frame, text=self.t["about_version"], 
                 bg=self.main_bg, fg="#888", font=("Segoe UI", 9)).pack()