import tkinter as tk
from tkinter import ttk

from license_verifier import License_Verifier

class Application(ttk.Frame):

    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("Example for license verifier")
        
        self.text_box = tk.Text()
        self.text_box.pack()
        self.pack()
        
    def run(self):
        license = License_Verifier(self.text_box)
        
        license.check_license()


main_window = tk.Tk()
app = Application(main_window)

app.run()

app.mainloop()
