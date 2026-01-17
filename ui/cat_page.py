import tkinter as tk
from tkinter import ttk, messagebox
import sys
sys.path.append("..") 
from database import DataBase 
from languages import DB_MAPPING, get_display_text # Dil eşleştirme araçları

class CatPage:
    def __init__(self, app):
        self.app = app

    def show_cats(self):
        self.app.clear_main_frame()
        baslik = self.app.t["menu_cat_manage"] if self.app.current_user[3] == 'personel' else self.app.t["menu_cat_view"]
        
        tk.Label(self.app.main_frame, text=baslik, bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)

        table_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("id", "name", "breed", "age", "gender", "status")
        
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal")

        self.app.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15, 
                                     yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        y_scroll.config(command=self.app.tree.yview)
        x_scroll.config(command=self.app.tree.xview)

        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        
        self.app.tree.pack(fill="both", expand=True)
        # ---------------------------
        
        for col in columns: self.app.tree.heading(col, text=col.capitalize())
        self.app.tree.column("id", width=30, anchor="center")
        self.app.tree.column("age", width=50, anchor="center")
        self.app.tree.column("gender", width=70)
        
        try:
            db = DataBase()
            cats = db.get_all_cats()
            for cat in cats:
                cat_list = list(cat)
                
                cat_list[2] = get_display_text(cat_list[2], self.app.lang)
                cat_list[4] = get_display_text(cat_list[4], self.app.lang)
                cat_list[5] = get_display_text(cat_list[5], self.app.lang)

                self.app.tree.insert("", tk.END, values=cat_list)
        except Exception as e:
            tk.Label(self.app.main_frame, text=f"Hata: {e}").pack()

        btn_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        btn_frame.pack(pady=10)

        if self.app.current_user[3] == 'personel':
            ttk.Button(btn_frame, text=self.app.t["btn_delete"], style="Menu.TButton", command=self.delete_selected_cat).pack(side="left", padx=5)
            ttk.Button(btn_frame, text=self.app.t["btn_update"], style="Menu.TButton", command=self.open_update_form).pack(side="left", padx=5)
            ttk.Button(btn_frame, text=self.app.t["btn_health"], style="Menu.TButton", command=self.show_health_popup).pack(side="left", padx=5)
        else:
            ttk.Button(btn_frame, text=self.app.t["btn_apply"], style="Menu.TButton", command=self.app.adoption_page.apply_for_cat).pack(side="left", padx=5)
            ttk.Button(btn_frame, text=self.app.t["btn_health"], style="Menu.TButton", command=self.show_health_popup).pack(side="left", padx=5)

    def show_health_popup(self):
        selected = self.app.tree.selection()
        if not selected: return 

        values = self.app.tree.item(selected)['values']
        cat_id = values[0]
        cat_name = values[1]

        db = DataBase()
        health_note = db.get_cat_health(cat_id)

        if not health_note or health_note.strip() == "":
            display_text = self.app.t["msg_no_health"]
        else:
            display_text = health_note

        messagebox.showinfo(f"{self.app.t['title_health']} - {cat_name}", display_text)

    def add_cat(self):
        self.app.clear_main_frame()
        tk.Label(self.app.main_frame, text=self.app.t["title_new_cat"], bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)
        form_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        form_frame.pack(pady=10)

        self.app.create_form_entry(form_frame, self.app.t["lbl_cat_name"], "name_entry", row=0)
        
        tk.Label(form_frame, text=self.app.t["lbl_cat_breed"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="e", pady=10, padx=10)
        self.breed_combo = ttk.Combobox(form_frame, values=self.app.t["combo_breeds"], width=28, state="readonly")
        self.breed_combo.grid(row=1, column=1, pady=10, sticky="w")
        self.breed_combo.current(0) 

        tk.Label(form_frame, text=self.app.t["lbl_cat_age"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=2, column=0, sticky="e", pady=10, padx=10)
        self.age_combo = ttk.Combobox(form_frame, values=self.app.t["combo_ages"], width=28, state="readonly")
        self.age_combo.grid(row=2, column=1, pady=10, sticky="w")
        self.age_combo.current(0) 

        tk.Label(form_frame, text=self.app.t["lbl_cat_gender"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=3, column=0, sticky="e", pady=10, padx=10)
        self.gender_combo = ttk.Combobox(form_frame, values=self.app.t["combo_genders"], width=28, state="readonly")
        self.gender_combo.grid(row=3, column=1, pady=10, sticky="w")
        self.gender_combo.current(0)
        
        tk.Label(form_frame, text=self.app.t["lbl_cat_health"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=4, column=0, sticky="ne", pady=10, padx=10)
        text_frame = tk.Frame(form_frame)
        text_frame.grid(row=4, column=1, pady=10, sticky="w")
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        self.health_text = tk.Text(text_frame, height=4, width=38, font=("Segoe UI", 10),
                                   yscrollcommand=scrollbar.set)
        self.health_text.pack(side="left", fill="both")
        scrollbar.config(command=self.health_text.yview)
        
        
        ttk.Button(self.app.main_frame, text=self.app.t["btn_save"], style="Menu.TButton", command=self.save_new_cat).pack(pady=30, ipadx=20, ipady=5)
    
    def save_new_cat(self):
        name = self.app.name_entry.get()
        if not name: return
        
        raw_breed = self.breed_combo.get()
        raw_gender = self.gender_combo.get()
        
        db_breed = DB_MAPPING.get(raw_breed, raw_breed)
        db_gender = DB_MAPPING.get(raw_gender, raw_gender)
        health_notes = self.health_text.get("1.0", "end-1c")

        try:
            db = DataBase()
            db.add_cat(name, db_breed, self.age_combo.get(), db_gender, "Barınakta", health_notes, "", lang=self.app.lang) 

            messagebox.showinfo("OK", self.app.t["msg_added"])
            self.show_cats() 
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def delete_selected_cat(self):
        selected = self.app.tree.selection()
        if selected:
            cat_id = self.app.tree.item(selected)['values'][0]
            
            try:
                db = DataBase()
                db.delete_cat(cat_id)
                
                db.add_log(f"log_delete_cat|||{cat_id}")
                
                self.show_cats()
            except Exception as e:
                messagebox.showerror("Hata", str(e))

    def open_update_form(self):
        selected = self.app.tree.selection()
        if not selected: return

        values = self.app.tree.item(selected)['values']
        
        self.selected_cat_id = values[0] 
        
        db_health_note = DataBase().get_cat_health(self.selected_cat_id)

        db_name = values[1]
        db_breed = values[2]
        db_age = values[3]
        db_gender = values[4]
        db_status = values[5]
        
        display_breed = get_display_text(db_breed, self.app.lang)
        display_gender = get_display_text(db_gender, self.app.lang)
        display_status = get_display_text(db_status, self.app.lang)

        self.app.clear_main_frame()
        tk.Label(self.app.main_frame, text=self.app.t["title_update_cat"], bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)
        
        form_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        form_frame.pack(pady=10)

        self.app.create_form_entry(form_frame, self.app.t["lbl_cat_name"], "upt_name", row=0)
        self.app.upt_name.insert(0, db_name)

        tk.Label(form_frame, text=self.app.t["lbl_cat_breed"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="e", pady=10, padx=10)
        self.upt_breed = ttk.Combobox(form_frame, values=self.app.t["combo_breeds"], width=28, state="readonly")
        self.upt_breed.grid(row=1, column=1, pady=10, sticky="w")
        self.upt_breed.set(display_breed) 

        tk.Label(form_frame, text=self.app.t["lbl_cat_age"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=2, column=0, sticky="e", pady=10, padx=10)
        self.upt_age = ttk.Combobox(form_frame, values=self.app.t["combo_ages"], width=28, state="readonly")
        self.upt_age.grid(row=2, column=1, pady=10, sticky="w")
        self.upt_age.set(db_age)

        tk.Label(form_frame, text=self.app.t["lbl_cat_gender"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=3, column=0, sticky="e", pady=10, padx=10)
        self.upt_gender = ttk.Combobox(form_frame, values=self.app.t["combo_genders"], width=28, state="readonly")
        self.upt_gender.grid(row=3, column=1, pady=10, sticky="w")
        self.upt_gender.set(display_gender) 

        tk.Label(form_frame, text=self.app.t["lbl_cat_status"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=4, column=0, sticky="e", pady=10, padx=10)
        self.upt_status = ttk.Combobox(form_frame, values=self.app.t["combo_status"], width=28, state="readonly")
        self.upt_status.grid(row=4, column=1, pady=10, sticky="w")
        self.upt_status.set(display_status) 

        tk.Label(form_frame, text=self.app.t["lbl_cat_health"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=5, column=0, sticky="ne", pady=10, padx=10)
        
        text_frame = tk.Frame(form_frame)
        text_frame.grid(row=5, column=1, pady=10, sticky="w")
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.upt_health_text = tk.Text(text_frame, height=4, width=38, font=("Segoe UI", 10),
                                       yscrollcommand=scrollbar.set)
        self.upt_health_text.pack(side="left", fill="both")
        scrollbar.config(command=self.upt_health_text.yview)
        
        if db_health_note:
            self.upt_health_text.insert("1.0", db_health_note)
    
        
        ttk.Button(self.app.main_frame, text=self.app.t["btn_save"], style="Menu.TButton", command=self.save_update).pack(pady=20)
        ttk.Button(self.app.main_frame, text=self.app.t["btn_cancel"], command=self.show_cats).pack()

       
    def save_update(self):
        raw_breed = self.upt_breed.get()
        raw_gender = self.upt_gender.get()
        raw_status = self.upt_status.get()
        
        db_breed = DB_MAPPING.get(raw_breed, raw_breed)
        db_gender = DB_MAPPING.get(raw_gender, raw_gender)
        db_status = DB_MAPPING.get(raw_status, raw_status)
        
        new_health_notes = self.upt_health_text.get("1.0", "end-1c")

        try:
            db = DataBase()
            
            db.update_cat(
                self.selected_cat_id, 
                self.app.upt_name.get(), 
                db_breed, 
                self.upt_age.get(), 
                db_gender, 
                db_status, 
                new_health_notes  
            )
            
            db.add_log(f"log_update|||{self.app.upt_name.get()}")

            messagebox.showinfo("OK", self.app.t["msg_updated"])
            self.show_cats() 
            
        except AttributeError:
             messagebox.showerror("Hata", "Güncellenecek kedi seçilmedi veya ID alınamadı.")
        except Exception as e:
            messagebox.showerror("Hata", str(e))