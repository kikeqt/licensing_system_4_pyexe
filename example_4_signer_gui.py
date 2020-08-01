__version__ = "$Version: 1.0.0"

from datetime import datetime
import tkinter as tk
from tkinter import ttk

from signer import Signer

class Application(ttk.Frame):

    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("Example for license maker")
        
        self.place(relwidth=1, relheight=1)
        
        self.frame_key = tk.Frame(main_window)
        self.label_key = tk.Label(self.frame_key, text="         Key: ")
        self.label_key.pack(side=tk.LEFT)
        self.text_key = tk.Entry(self.frame_key, show='*')
        self.text_key.pack(side=tk.RIGHT)
        self.frame_key.pack()
        
        self.frame_confirm_key = tk.Frame(main_window)
        self.label_confirm_key = tk.Label(self.frame_confirm_key, text="Confirm: ")
        self.label_confirm_key.pack(side=tk.LEFT)
        self.text_confirm_key = tk.Entry(self.frame_confirm_key, show='*')
        self.text_confirm_key.pack(side=tk.RIGHT)
        self.frame_confirm_key.pack()
        
        self.button_signer = tk.Button(self, text ="Sign", command=self.run)
        self.button_signer.pack()
        
        self.frame_log = tk.Frame(main_window)
        self.list_log = tk.Listbox(self.frame_log, width=60)
        self.list_log.pack()
        self.frame_log.pack(side=tk.BOTTOM)
        
        self.pack()
        
    def run(self):
        key = self.text_key.get()
        confirmed_key = self.text_confirm_key.get()
        
        if key == confirmed_key:
            license_maker = Signer(key, self.list_log)
            
        else:
            time_stamp = datetime.now().strftime("%y/%m/%d %H:%M:%S.%f")[:-4]
            self.list_log.insert(tk.END, f"{time_stamp}  Fatal error: the keys do not match")


main_window = tk.Tk()
app = Application(main_window)

app.mainloop()
