global fonts, start_menu, canvas, root, images, screen_blocks, active_piece
import tkinter as tk
import os, time, random, math, threading

root = tk.Tk()
root.title('Tetris')

class fonts: #unified fonts/formatting. please use
    face = ''
    title = (face, 50)
    large = (face, 25)
    #formatting
    relief = tk.FLAT
    overrelief = tk.GROOVE

#load all the images into memory at the same time instead of loading once each time they are needed
images = {}
for f in os.listdir('blocks'):
    images[f] = tk.PhotoImage(file='blocks/' + f)

#####

class block: #the blocks that everything is made from - "the building blocks of life"
    def __init__(self, colour='random', active=False):
        if colour == 'random':
            img = images[random.choice(os.listdir('blocks'))]
        else:
            img = colour
        self.obj = canvas.create_image(-10, -10, image=img) #coords are deliberately offscreen so that they aren't blinking as much in the top corner
        self.active = active
    obj = None
    last_render_coords = None
    active = None

class piece: #the shape you move down the screen
    def __init__(self):
        self.id = random.choice(os.listdir('models'))
        self.image = images[random.choice(os.listdir('blocks'))]
        self.orientation = 'up'
        for model in os.listdir('models/' + self.id):
            file = open('models/' + self.id + '/' + model, 'r')
            m = file.read()
            final_model = ''
            for char in m:
                if char == '0' or char == '1':
                    final_model += char
            self.models[model[:len(model) - 4]] = final_model
            file.close()
        self.linelen = math.sqrt(len(self.models[self.orientation]))
    def check_sides_ok(self):
        rows_occupied = []
        for b in self.models[self.orientation]:
            if b == '1':
                row = ''
                if not row in rows_occupied:
                    rows_occupied.append(row)
        if len(rows_occupied) == 1:
            return True
        return False
    rotations = ['up', 'right', 'down', 'left']
    coords = [5, 29]
    models = {}
    image = None #use the same image resource for all the blocks

#####

screen_blocks = []
for x in range(10 * 30): #add blank spaces to screen so that they can be replaced by blocks
    screen_blocks.append(None)
def play():
    global canvas
    start_menu.frame.pack_forget()
    canvas = tk.Canvas(root, bg='snow1', height=20 * 30, width=20 * 10)
    canvas.pack()
    for x in range(11):
        screen_blocks[x] = block()
    threading.Thread(target=render_loop).start()
    root.bind('<a>', apply_piece.move.left)
    root.bind('<d>', apply_piece.move.right)
    root.bind('<q>', apply_piece.rotate.left)
    root.bind('<e>', apply_piece.rotate.right)

def render_loop(): #rerender and move down on a timer
    global active_piece
    active_piece = piece()
    while True:
        render()
        time.sleep(0.3)
        active_piece.coords[1] -= 1

def render_block(index): #render from a specific index
    global screen_blocks
    b = screen_blocks[index]
    if not b == None:
        xcoord = (index % 10) * 20 + 11
        ycoord = (20 * 30) - ((int(index / 10) * 20) + 10)
        if not b.last_render_coords == [xcoord, ycoord]: #optimised rerender render skipping
            canvas.coords(b.obj, xcoord, ycoord)
            b.last_render_coords = [xcoord, ycoord]

class render: #uses objects because ... ... ... meh
    def __init__(self):
        self.active = False
    def render(self):
        if not self.active:
            self.active = True
            for x in range(len(screen_blocks)):
                b = screen_blocks[x]
                if not b == None:
                    if b.active:
                        canvas.delete(b.obj)
                        screen_blocks[x] = None
            send_piece_to_blocks(active_piece)
            for index in range(len(screen_blocks)):
                render_block(index)
            self.active = False
render = render().render #im giving up on life right now... who cares? if it works, it works *breaks*

def send_piece_to_blocks(piece):
    model = piece.models[piece.orientation]
    start_index = piece.coords[0] + (piece.coords[1] * 10)
    for i in range(len(model)):
        char = model[i]
        if char == '1':
            index = int((start_index + (i % piece.linelen) - int(i / piece.linelen) * 10) % len(screen_blocks))
            screen_blocks[index] = block(colour=piece.image, active=True)

class apply_piece:
    class move:
        def left(event):
            active_piece.coords[0] -= 1
            render()
        def right(event):
            active_piece.coords[0] += 1
            render()
    class rotate:
        def left(event):
            index = active_piece.rotations.index(active_piece.orientation) - 1
            if index < 0:
                index = len(active_piece.rotations) - 1
            active_piece.orientation = active_piece.rotations[index]
            render()
        def right(event):
            index = active_piece.rotations.index(active_piece.orientation) + 1
            if index > len(active_piece.rotations) - 1:
                index = 0
            active_piece.orientation = active_piece.rotations[index]
            render()

class start_menu:
    menu_width = 15
    frame = tk.Frame(root)
    title = tk.Label(frame, text='Tetris', font=fonts.title)
    play_game = tk.Button(frame, text='Play', font=fonts.large, width=menu_width, command=play, relief=fonts.relief, overrelief=fonts.overrelief)
    leaderboard = tk.Button(frame, text='Leaderboard', font=fonts.large, width=menu_width, relief=fonts.relief, overrelief=fonts.overrelief)
    #
    title.pack(fill=tk.X)
    play_game.pack(fill=tk.X)
    leaderboard.pack(fill=tk.X)
    frame.pack()

root.mainloop()
