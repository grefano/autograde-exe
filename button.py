import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
import os
from pathlib import Path
import requests
import threading
from manage_config import config_load, config_save
from dotenv import load_dotenv
import colorsys
from typing import Any

load_dotenv()

def get_button_font(size, style = None):
    if style == None:
        return ("Lexend", size)
    else:
        return ("Lexend", size, style)

server_url = os.getenv("SERVER_URL") or ""

def clamp(val, val_min, val_max):
    return max(min(val, val_max), val_min)

def color_hex_to_hsv(hex: str):
    print(f"hex {hex}")
    hex = hex.lstrip('#')
    print(f"hex strip {hex}")
    r, g, b = tuple(int(hex[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return (h, s, v)

def color_rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))

def color_hex_add_hsv(hex: str, h, s, v):
    ho, so, vo = color_hex_to_hsv(hex)
    ho += h
    so += s
    vo += v
    ho = clamp(ho, 0, 1)
    so = clamp(so, 0, 1)
    vo = clamp(vo, 0, 1)
    r, g, b = colorsys.hsv_to_rgb(ho, so, vo)
    return color_rgb_to_hex(r, g, b)



def add_button_effect_hover(button: tk.Button, btn_type):
    valid_types = {'text', 'icon'}
    if (btn_type not in valid_types):
        raise ValueError(f"btn_type {btn_type} é inválido")
    
    if btn_type == 'text':
        color = button.cget('bg')
        color_hover = color_hex_add_hsv(color, 0, -0.2, -0.2)
        button.bind("<Enter>", lambda e: button.config(bg=color_hover))
        button.bind("<Leave>", lambda e: button.config(bg=color))
    elif btn_type == 'icon':
        # color = button.cget('bg')
        # color_hover = color_hex_add_hsv(color, 0, -0.2, -0.2)
        # button.bind("<Enter>", lambda e: button.config(bg=color_hover, activebackground=color_hover))
        # button.bind("<Leave>", lambda e: button.config(bg=color, activebackground=color))
        pass


params_button_icon: dict[str, Any] = {
    'borderwidth': 0,
    'highlightthickness': 0,
    'relief':'flat',
    'cursor':'hand2',
}

params_button_text: dict[str, Any] = {
    'relief':'flat',
    'cursor':'hand2',
}

class Client:
    def __init__(self):
        
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
        entry_folder.insert(0, self.config['folder'])
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
            entrou = self.send_classroom_join(entry_password.get(), entry_name.get())
            if entrou:
                self.show_screen(self.screen_submit)


        folder_btn = tk.Button(frame_folder, text="Selecionar", command=select_folder, **params_button_text)
        folder_btn.pack(side='right', padx=(0, 0))
        btn_set = tk.Button(self.screen_config, text="Accept", command=handle_config_accept, **params_button_text) #show_screen(self.screen_submit)
        btn_set.pack()
        self.screen_register(self.screen_config, expand=False)
        # self.screens.append({screen=self.screen_config, args_pack=(fill='both')})

    def screen_register(self, screen, **kwargs):
        self.screens.append(screen)
        self.screens_packs[screen] = kwargs
        
    def create_function_show_screen(self, screen_to_show):
        return self.show_screen(screen_to_show)

    def show_screen(self, screen_to_show):
        for screen in self.screens:
            screen.pack_forget()
        screen_to_show.pack(self.screens_packs.get(screen_to_show, {}))

    def show(self):
        self.show_screen(self.screen_config)
        self.root.mainloop()
    

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

if __name__ == "__main__":
    app = Client()
    app.show()
