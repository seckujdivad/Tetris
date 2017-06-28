class settings:
    def __init__(self): #set out objects inside the frame
        self.frame = tk.Frame(root)
        self.title = tk.Label(self.frame, text='Settings', font=fonts.title)
        self.backbutton = tk.Button(self.frame, text='Return to Menu', font=fonts.normal, command=self.hide_settings, relief=fonts.relief, overrelief=fonts.overrelief)
        #
        self.title.pack(fill=tk.X)
        self.backbutton.pack(side=tk.BOTTOM, fill=tk.X)
    def show_settings(self):
        start_menu.frame.pack_forget()
        self.frame.pack()
    def hide_settings(self):
        self.frame.pack_forget()
        start_menu.frame.pack()
settings = settings()
