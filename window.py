class Window:
    def __init_(self):
        self.screens = []
        self.screens_packs = {}
    def screen_register(self, screen, **kwargs):
        self.screens.append(screen)
        self.screens_packs[screen] = kwargs
        
    def create_function_show_screen(self, screen_to_show):
        return self.show_screen(screen_to_show)

    def show_screen(self, screen_to_show):
        for screen in self.screens:
            screen.pack_forget()
        screen_to_show.pack(self.screens_packs.get(screen_to_show, {}))
