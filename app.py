import tkinter as tk

from button import Button
from returns import Returns


if __name__ == "__main__":
    app = Button()

    app.show_screen(app.screen_config)

    app.root.mainloop()
