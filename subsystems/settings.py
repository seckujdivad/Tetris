class settings:
    def __init__(self): #set out objects inside the frame
        self.data = sqlite3.connect('persistent.db')
        self.frame = tk.Frame(root)
        self.title = tk.Label(self.frame, text='Settings', font=fonts.title)
        self.backbutton = tk.Button(self.frame, text='Return to Menu', font=fonts.normal, command=self.hide_settings, relief=fonts.relief, overrelief=fonts.overrelief)
        self.functions = tk.Frame(self.frame)
        self.left = tk.Frame(self.functions)
        self.right = tk.Frame(self.functions)
        #
        self.item.label.music_on = tk.Label(self.left, text='Play music', font=fonts.small)
        self.item.label.reset = tk.Label(self.left, text='Reset all', font=fonts.small)
        #
        self.item.interact.music_on = tk.Checkbutton(self.right, command=self.toggle_music)
        self.item.interact.reset = tk.Button(self.right, text='Reset', font=fonts.small, relief=fonts.relief, overrelief=fonts.overrelief, command=self.reset)
        #
        self.item.label.music_on.pack(anchor='nw')
        self.item.label.reset.pack(anchor='nw')
        #
        self.item.interact.music_on.pack(anchor='nw', fill=tk.X, expand=True)
        self.item.interact.reset.pack(anchor='nw', fill=tk.X, expand=True)
        #
        self.title.pack(fill=tk.X)
        self.left.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.right.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        self.functions.pack(fill=tk.BOTH)
        self.backbutton.pack(side=tk.BOTTOM, fill=tk.X)
    def show_settings(self):
        start_menu.frame.pack_forget()
        self.frame.pack()
    def hide_settings(self):
        self.frame.pack_forget()
        start_menu.frame.pack()
    class item:
        class label:
            pass
        class interact:
            pass
    def reset(self):
        shutil.copyfile(paths.assets + 'persistent_default.db', 'persistent.db')
    def toggle_music(self):
        print(self.item.interact.music_on.get())
settings = settings()
