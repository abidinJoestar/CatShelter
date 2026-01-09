import tkinter as tk
from ui.login_window import LoginWindow
from ui.main_window import CatShelterApp
# for the login for personel-> username:admin, password=1234 and
# for adopter username=musteri1, password=1234 
class MainApp:
    def __init__(self, root):
        self.root = root
        self.show_login(lang="TR")

    def show_login(self, lang="TR"):
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginWindow(self.root, on_login_success=self.show_main, lang=lang)

    def show_main(self, user, lang):
        for widget in self.root.winfo_children():
            widget.destroy()
  
        CatShelterApp(self.root, current_user=user, lang=lang, on_logout=self.show_login)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()