#yeah nah... isaac can do this
#code is just to set out variable names that I need
#by all means change what you want
#be prepared to run it a few times and change a couple variable names in the main code though

class leaderboard:
    def __init__(self): #set out objects inside the frame
        self.frame = tk.Frame(root)
        self.title = tk.Label(self.frame, text='Leaderboard', font=fonts.title)
        self.backbutton = tk.Button(self.frame, text='Return to Menu', font=fonts.normal, command=self.hide_leaderboard, relief=fonts.relief, overrelief=fonts.overrelief)
        #
        self.title.pack(fill=tk.X)
        self.backbutton.pack(side=tk.BOTTOM, fill=tk.X)
    def show_leaderboard(self):
        start_menu.frame.pack_forget()
        self.frame.pack()
    def hide_leaderboard(self):
        self.frame.pack_forget()
        start_menu.frame.pack()
leaderboard = leaderboard()
