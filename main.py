import tkinter as tk
from ui.login_window import LoginWindow
from ui.main_window import CatShelterApp

class MainApp:
    def __init__(self, root):
        self.root = root
        self.show_login()

    def show_login(self):
        """Giriş ekranını başlatır"""
        # --- EKRANI TEMİZLEME KODU ---
        for widget in self.root.winfo_children():
            widget.destroy()
        # -----------------------------
        
        LoginWindow(self.root, on_login_success=self.show_main)

    def show_main(self, user):
        """Ana ekranı başlatır"""
        # --- EKRANI TEMİZLEME KODU ---
        for widget in self.root.winfo_children():
            widget.destroy()
        # -----------------------------
            
        CatShelterApp(self.root, current_user=user, on_logout=self.show_login)

if __name__ == "__main__":
    root = tk.Tk()
    # Pencere iconu vs eklenebilir
    app = MainApp(root)
    root.mainloop()