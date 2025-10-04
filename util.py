import colorsys
from tkinter import Button
from typing import Any

def get_button_font(size, style = None):
    if style == None:
        return ("Lexend", size)
    else:
        return ("Lexend", size, style)

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



def add_button_effect_hover(button: Button, btn_type):
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

