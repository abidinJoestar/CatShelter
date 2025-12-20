import tkinter as tk
from ui.main_window import CatShelterApp
from ui.login_window import LoginWindow

if __name__ == "__main__":
    root = tk.Tk()
    # app = CatShelterApp(root)
    app=LoginWindow(root)
    root.mainloop()