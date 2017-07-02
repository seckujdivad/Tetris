class settings:
    def __init__(self): #set out objects inside the frame
        self.data = sqlite3.connect(paths.persistent + 'persistent.db')
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
        self.item.interact.music_on = tk.Checkbutton(self.right, variable=self.values['music'])
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
        #get all
        for var in self.values:
            self.values[var].set(self.get_data(var))
        #
        root.bind('<Control-F2>', self.on_update)
        root.bind('<Control-F3>', self.reset)
    def show_settings(self):
        start_menu.frame.pack_forget()
        self.frame.pack()
    def hide_settings(self):
        self.on_update()
        self.frame.pack_forget()
        start_menu.frame.pack()
    class item:
        class label:
            pass
        class interact:
            pass
    def reset(self):
        self.data.close()
        reset_persistent()
        self.data = sqlite3.connect(paths.persistent + 'persistent.db')
    def on_update(self, event=None):
        if not self.values == self.prev_values:
            for key in self.values:
                self.write_data(key, self.values[key].get())
            self.prev_values = self.values.copy()
    def get_data(self, name):
        cursor = self.data.execute('SELECT name, data FROM settings')
        all = cursor.fetchall()
        for id, val in all:
            if id == name:
                return val
    def write_data(self, key, value):
        self.data.execute('DELETE FROM settings WHERE name = "' + key + '"')
        self.data.execute('INSERT INTO settings (name, data) VALUES ("' + key + '","' + value + '")')
        self.data.commit()
    values = {'music':tk.StringVar()}
    prev_values = {}
settings = settings()
