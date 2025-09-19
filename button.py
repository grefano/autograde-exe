import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
import os
from pathlib import Path
import requests
import threading
from manage_config import config_load, config_save


class Client:
    def __init__(self):
        self.server_url = 'http://localhost:3000/'
        self.config = config_load()
        config_save({'first_use': False})
        print(self.config['first_use'])

        self.current_folder = None
        self.root = tk.Tk()
        self.root.title('autograde')

        w, h = 288, 180
        x, y = 1920-w-30, 1080-h-60
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.attributes('-topmost', '1')

        self.screens = []


        #       screen submit
        self.screen_submit = tk.Frame(self.root, padx=0, pady=0)
        btn_submit = tk.Button(self.screen_submit, text="teste", bg="#2196F3", fg="white", font=("Lexend", 24, "bold"), 
                               command=lambda: self.send_file(entry_folder.get(), 'teste.py'))
        btn_submit.pack(expand=True, fill='both', padx=0, pady=0)
        self.screens.append(self.screen_submit)


        #       screen config
        self.screen_config = tk.Frame(self.root)
        frame_folder = tk.Frame(self.screen_config, bg='blue')
        frame_folder.pack(pady=0, padx=0, fill='both')
        
        entry_folder = tk.Entry(frame_folder, font=("Arial", 10))
        entry_folder.insert(0, self.config['folder'])
        entry_folder.pack(side='left', fill='both', expand=True)

        entry_password = tk.Entry(self.screen_config, font=("Arial", 10))
        entry_password.insert(0, 'teste')
        entry_password.pack(side='left', fill='both', expand=True)
        
        
        def select_folder():
            folder = filedialog.askdirectory()
            if folder:
                entry_folder.delete(0, tk.END)
                entry_folder.insert(0, folder)
        
        def handle_config_accept():
            self.send_classroom_join(entry_password.get())
            self.show_screen(self.screen_submit)


        folder_btn = tk.Button(frame_folder, text="Selecionar", command=select_folder)
        folder_btn.pack(side='right', padx=(0, 0))
        btn_set = tk.Button(self.screen_config, text="Accept", command=handle_config_accept) #show_screen(self.screen_submit)
        btn_set.pack()
        self.screens.append(self.screen_config)


        
    def create_function_show_screen(self, screen_to_show):
        return self.show_screen(screen_to_show)

    def show_screen(self, screen_to_show):
        for screen in self.screens:
            screen.pack_forget()
        screen_to_show.pack(expand=True)

    def show(self):
        self.show_screen(self.screen_config)
        self.root.mainloop()
    

    def send_classroom_join(self, password):
        url = self.server_url+'api/class/join/'+password
        print(url)
        response = requests.post(url)
        config_save({'classroom_token': response.json()['token']})

    def send_file(self, dir: str, filename: str):
        filepath = dir + '/' + filename
        lang = filename.split('.')[-1]
        print(f"send filepath {filepath}")
        files = {'file': open(filepath, 'rb')}
        url = self.server_url+"api/code/"+lang
        print(f"url {url}")
        response = requests.post(url, files=files, headers={'Authorization': 'Bearer ' + self.config['classroom_token']})

if __name__ == "__main__":
    app = Client()
    app.show()
