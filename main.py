import tkinter as tk
from ui.main_window import CatShelterApp
from ui.login_window import loginWindow

if __name__ == "__main__":
    root = tk.Tk()
    # app = CatShelterApp(root)
    app=loginWindow(root)
    root.mainloop()