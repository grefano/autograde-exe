import requests
from dotenv import load_dotenv
import tkinter as tk
import os

from window import *
from manage_config import config_load
from util import params_button_text, params_button_icon

server_url = os.getenv("SERVER_URL") or ""


class Returns(Window):
    def __init__(self, root) -> None:
        self.config = config_load()
        self.returns = []

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

        update = tk.Button(self.screen_list, text="recarregar", command=self.get_returns, **params_button_text)
        update.pack()

        self.screen_register(self.screen_list)

    def add_returns_to_screen(self):
        for r in self.returns:
            print('botou')
            frame = tk.LabelFrame(self.screen_list, text='label')
            frame.pack(expand=True)
            btn_return = tk.Button(frame, text=f"return")
            btn_return.pack(fill='x')

    def get_returns(self):
        self.config = config_load()
        response = requests.get(server_url+'api/code/return', headers={'Authorization': 'Bearer ' + self.config['classroom_token']})
        print(response)
        data = response.json()
        print(data)
        self.returns = data
        self.add_returns_to_screen()

        
