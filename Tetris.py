global fonts, start_menu, canvas, root, images, screen_blocks, active_piece
import tkinter as tk
import os, time, random, math, threading

root = tk.Tk()
root.title('Tetris')

class fonts:
    face = ''
    title = (face, 50)
    large = (face, 25)

images = {}
for f in os.listdir('blocks'):
    images[f] = tk.PhotoImage(file='blocks/' + f)

#####

class block:
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

class piece:
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
    rotations = ['up', 'right', 'down', 'left']
    coords = [5, 30]
    models = {}
    image = None #use the same image resource for all the blocks

#####

screen_blocks = []
for x in range(10 * 30):
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

def render_loop():
    global active_piece
    active_piece = piece()
    while True:
        render()
        time.sleep(1)
        active_piece.coords[1] -= 1

def render_block(index):
    global screen_blocks
    b = screen_blocks[index]
    if not b == None:
        xcoord = (index % 10) * 20 + 11
        ycoord = (20 * 30) - ((int(index / 10) * 20) + 10)
        if b.last_render_coords == [xcoord, ycoord]:
            pass
        else:
            canvas.coords(b.obj, xcoord, ycoord)
            b.last_render_coords = [xcoord, ycoord]

class render: #uses oop because...
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
    all_index = []
    for i in range(len(model)):
        char = model[i]
        if char == '1':
            index = int((start_index + (i % piece.linelen) - int(i / piece.linelen) * 10) % len(screen_blocks))
            all_index.append(index)
            screen_blocks[index] = block(colour=piece.image, active=True)
    print(*all_index)

class apply_piece:
    class move:
        def left(event):
            print('ml')
            active_piece.coords[0] -= 1
            render()
        def right(event):
            print('mr')
            active_piece.coords[0] += 1
            render()
    class rotate:
        def left(event):
            print('rl')
            index = active_piece.rotations.index(active_piece.orientation) - 1
            if index < 0:
                index = len(active_piece.rotations) - 1
            active_piece.orientation = active_piece.rotations[index]
            print(active_piece.orientation)
            render()
        def right(event):
            print('rr')
            index = active_piece.rotations.index(active_piece.orientation) + 1
            if index > len(active_piece.rotations) - 1:
                index = 0
            active_piece.orientation = active_piece.rotations[index]
            print(active_piece.orientation)
            render()

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
