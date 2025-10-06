class Window:
    def __init__(self):
        self.screens = []
        self.screens_packs = {}
        self.config = {}

    def get_config(self, key):
        config = self.config[key]
        return config
    
    def screen_register(self, screen, **kwargs):
        self.screens.append(screen)
        self.screens_packs[screen] = kwargs
        
    def create_function_show_screen(self, screen_to_show):
        return self.show_screen(screen_to_show)

    def show_screen(self, screen_to_show):
        for screen in self.screens:
            screen.pack_forget()
        screen_to_show.pack(self.screens_packs.get(screen_to_show, {}))
