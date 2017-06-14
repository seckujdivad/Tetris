global fonts, start_menu, canvas, root
import tkinter as tk

root = tk.Tk()
root.title('Tetris')

class fonts:
    face = ''
    title = (face, 50)
    large = (face, 25)

def play():
    global canvas
    start_menu.frame.pack_forget()
    canvas = tk.Canvas(root, bg='snow1')
    canvas.pack()

class start_menu:
    menu_width = 15
    frame = tk.Frame(root)
    title = tk.Label(frame, text='Tetris', font=fonts.title)
    play_game = tk.Button(frame, text='Play', font=fonts.large, width=menu_width, command=play)
    leaderboard = tk.Button(frame, text='Leaderboard', font=fonts.large, width=menu_width)
    #
    title.pack(fill=tk.X)
    play_game.pack(fill=tk.X)
    leaderboard.pack(fill=tk.X)
    frame.pack()

root.mainloop()
