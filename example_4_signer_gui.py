__version__ = "$Version: 1.0.0"

import tkinter as tk
from tkinter import ttk

from signer import Signer

class Application(ttk.Frame):

    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("Example for license maker")
        
        self.place(relwidth=1, relheight=1)
        
        self.frame_key = tk.Frame(main_window)
        self.label_key = tk.Label(self.frame_key, text="Key: ")
        self.label_key.pack(side=tk.LEFT)
        self.text_key = tk.Entry(self.frame_key, show='*')
        self.text_key.pack(side=tk.RIGHT)
        self.frame_key.pack()
        
        self.button_signer = tk.Button(self, text ="Sign", command=self.run)
        self.button_signer.pack()
        
        self.frame_log = tk.Frame(main_window)
        self.list_log = tk.Listbox(self.frame_log, width=60)
        self.list_log.pack()
        self.frame_log.pack(side=tk.BOTTOM)
        
        self.pack()
        
    def run(self):
        key = self.text_key.get().encode()
        license_maker = Signer(key, self.list_log)


main_window = tk.Tk()
app = Application(main_window)

app.mainloop()
