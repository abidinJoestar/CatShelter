# main.py TAM KODU

import tkinter as tk
from ui.login_window import LoginWindow
from ui.main_window import CatShelterApp

class MainApp:
    def __init__(self, root):
        self.root = root
        # İlk açılışta Türkçe başlasın
        self.show_login(lang="TR")

    def show_login(self, lang="TR"):
        """Giriş ekranını başlatır (Dil seçeneğini hatırlar)"""
        # Ekranı temizle
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # LoginWindow'a 'lang' bilgisini gönderiyoruz
        LoginWindow(self.root, on_login_success=self.show_main, lang=lang)

    def show_main(self, user, lang):
        """Ana ekranı başlatır"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Çıkış yaparken show_login fonksiyonunu çağıracak,
        # CatShelterApp çıkış yaparken 'lang' parametresini show_login'e gönderecek.
        CatShelterApp(self.root, current_user=user, lang=lang, on_logout=self.show_login)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()