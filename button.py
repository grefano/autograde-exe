import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
import os
from pathlib import Path
import requests
from manage_config import config_load, config_save
from dotenv import load_dotenv

from util import add_button_effect_hover, get_button_font, params_button_icon, params_button_text
from window import *
from returns import Returns

load_dotenv()

server_url = os.getenv("SERVER_URL") or ""




    
class Button(Window):
    def __init__(self):
        
        self.config = config_load()
        config_save({'first_use': False})
        print(self.config['first_use'])

        self.current_folder = None
        self.root = tk.Tk()
        self.root.title('autograde')

        w, h = 288, 180
        x, y = 1920-w-30, 1080-h-80
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.attributes('-topmost', '1')

        self.screens = []
        self.screens_packs = {}


        #       screen submit
        self.screen_submit = tk.Frame(self.root, padx=0, pady=0)
        icon_close = tk.PhotoImage(file="icons/icon_close.png")
        # icon_close = icon_close.subsample(icon_close.width() // 30, icon_close.height() // 30)
        btn_exit = tk.Button(self.screen_submit, image=icon_close, command=lambda: self.exit_classroom(), anchor='w', **params_button_icon)
        setattr(btn_exit, 'image', icon_close)
        add_button_effect_hover(btn_exit, 'icon')
        btn_exit.pack(anchor='nw')

        btn_submit = tk.Button(self.screen_submit, text="Submit", bg="#2196F3",
                               command=lambda: self.send_file(entry_folder.get(), 'teste.py'), font=get_button_font(20), fg='white', **params_button_text)
        add_button_effect_hover(btn_submit, 'text')
        btn_submit.pack(expand=True, fill='both', padx=0, pady=0)

        self.screen_register(self.screen_submit, expand=True, fill='both')
        # self.screens.append(self.screen_submit)



        #       screen config
        self.screen_config = tk.Frame(self.root)

        frame_name = tk.Frame(self.screen_config)
        frame_name.pack(padx=0, pady=0, fill='both')

        entry_name = tk.Entry(frame_name, font=get_button_font(10))
        entry_name.insert(0, self.config['name'])
        entry_name.pack(side='left', fill='both', expand=False, padx=0, pady=0)
        
        frame_folder = tk.Frame(self.screen_config, bg='blue')
        frame_folder.pack(pady=0, padx=0, fill='both')
        
        entry_folder = tk.Entry(frame_folder, font=get_button_font(10))
        entry_folder.insert(0, self.config['folder_files'])
        entry_folder.pack(side='left', fill='both', expand=True)

        entry_password = tk.Entry(self.screen_config, font=get_button_font(10))
        entry_password.insert(0, 'VdEgQ')
        entry_password.pack(side='left', fill='both', expand=True)
        
        def select_folder():
            folder = filedialog.askdirectory()
            if folder:
                entry_folder.delete(0, tk.END)
                entry_folder.insert(0, folder)
        
        def handle_config_accept():
            print("handle config accept")
            config_save({'folder_files': entry_folder.get(), 'folder_returns': entry_folder.get()})
            entrou = self.send_classroom_join(entry_password.get(), entry_name.get())
            if entrou:
                self.show_screen(self.screen_submit)


        folder_btn = tk.Button(frame_folder, text="Selecionar", command=select_folder, **params_button_text)
        folder_btn.pack(side='right', padx=(0, 0))
        btn_set = tk.Button(self.screen_config, text="Accept", command=handle_config_accept, **params_button_text) #show_screen(self.screen_submit)
        btn_set.pack()
        self.screen_register(self.screen_config, expand=False)
        # self.screens.append({screen=self.screen_config, args_pack=(fill='both')})



    def send_classroom_join(self, password, name):
        url = server_url+'api/class/join/'+password+'/'+name
        print(url)
        response = requests.post(url)
        print(response)
        data = response.json()
        print(data)


        
        if response.status_code == 200:
            token = data['token']
            print(f"join token: {token}")
            print("entrou")
            config_save({'classroom_token': token, 'name': name})
            self.config = config_load()
            return True
        return False
        # !!! e se a sala estiver fechada?

    def send_file(self, dir: str, filename: str):
        filepath = dir + '/' + filename
        lang = filename.split('.')[-1]
        print(f"send filepath {filepath}")
        files = {'file': open(filepath, 'rb')}
        url = server_url+"api/code/"+lang
        print(f"url {url}")
        try:

            response = requests.post(url, files=files, headers={'Authorization': 'Bearer ' + self.config['classroom_token']})
            print(response)

            if response.status_code == 404:
                self.show_screen(self.screen_config)

        except Exception as err:
            print(f"post code ERROR: {err}")

    def exit_classroom(self):
        try:
            response = requests.post(server_url+"api/class/exit", headers={'Authorization': 'Bearer ' + self.config['classroom_token']})
            print(response.json())
        except Exception as err:
            print(f"exit class ERROR: {err}")
        self.show_screen(self.screen_config)

