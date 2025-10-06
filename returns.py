import requests
from dotenv import load_dotenv
import tkinter as tk
import os

from window import *
from manage_config import config_load
from util import add_button_effect_hover, params_button_text, params_button_icon

load_dotenv()
server_url = os.getenv("SERVER_URL")
if server_url == None:
    print(f"!!!!!")
    server_url = ""

class Returns(Window):
    def __init__(self, root) -> None:
        self.config = config_load()
        self.returns = []
        self.returns_frame = None

        self.root = tk.Toplevel(root)
        self.root.title("returns")

        w, h = 288, 512
        x, y = 1920-w-20, 40
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.attributes('-topmost', '1')

        self.screens = []
        self.screens_packs = {}
        # list
        self.screen_list = tk.Frame(self.root, padx=0, pady=0) 
        self.returns_frame = tk.Frame(self.screen_list) # essa linha é repetida
        icon_refresh = tk.PhotoImage(file="icons/icon_refresh.png")
        btn_update = tk.Button(self.screen_list, image=icon_refresh, command=self.get_returns, **params_button_text)
        setattr(btn_update, 'image', icon_refresh)
        # add_button_effect_hover(btn_update, 'text')
        btn_update.pack()

        self.screen_register(self.screen_list)

    def handle_download_return(self, code: str):
        filename = 'file.py'
        code = code.replace('\r\n', '\n')
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
        except Exception as e:
            print(f"erro ao salvar arquivo {e}")

    def add_returns_to_screen(self):
        if self.returns_frame == None:
            raise ValueError(f"self.returns_frame = None")
        
        self.returns_frame.destroy()
        self.returns_frame = tk.Frame(self.screen_list)

        icon_download = tk.PhotoImage(file="icons/icon_download.png")
        icon_close = tk.PhotoImage(file="icons/icon_close.png")


        for r in self.returns:
            print('botou')
            self.returns_frame = tk.LabelFrame(self.screen_list, text='label')
            self.returns_frame.pack()

            btn_download = tk.Button(self.returns_frame, image=icon_download, text="download", command=lambda: self.handle_download_return(r['code']), **params_button_icon)
            setattr(btn_download, 'image', icon_download)
            
            btn_download.pack(side='left')

            btn_ignore = tk.Button(self.returns_frame, image=icon_close, **params_button_icon)
            setattr(btn_ignore, 'image', icon_close)
            btn_ignore.pack()

        self.returns_frame.pack()


    def get_returns(self):
        self.config = config_load()
        if server_url == None:
            return
        print(f"server url {server_url}")
        response = requests.get(server_url+'api/code/return', headers={'Authorization': 'Bearer ' + self.config['classroom_token']})
        print(response)
        data = response.json()
        print(data)
        self.returns = data
        self.add_returns_to_screen()

        
