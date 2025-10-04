import tkinter as tk

from button import Button
from returns import Returns


if __name__ == "__main__":
    app = Button()
    app2 = Returns(app.root)

    app.show_screen(app.screen_config)
    app2.show_screen(app2.screen_list)

    app.root.mainloop()
