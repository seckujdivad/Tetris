global fonts, start_menu, canvas, root, images, screen_blocks, active_piece
import tkinter as tk
import os, time, random, math, threading, sys

root = tk.Tk()
root.title('Tetris')

class fonts: #unified fonts/formatting. please use
    face = ''
    title = (face, 50)
    large = (face, 25)
    normal = (face, 14)
    #formatting
    relief = tk.FLAT
    overrelief = tk.GROOVE

#load all the images into memory at the same time instead of loading once each time they are needed
print('Loading images...')
images = {}
sys.stdout.write('[...]')
for f in os.listdir(sys.path[0] + '/blocks'):
    sys.stdout.flush()
    sys.stdout.write('{:30}'.format('\r/blocks/' + f))
    images[f] = tk.PhotoImage(file=sys.path[0] + '/blocks/' + f)
sys.stdout.write('{:30}'.format('\rDone') + '\n')
del f

#####

class block: #the blocks that everything is made from - "the building blocks of life"
    def __init__(self, colour='random', active=False):
        if colour == 'random':
            img = images[random.choice(os.listdir(sys.path[0] + '/blocks'))]
        else:
            img = colour
        self.obj = canvas.create_image(-10, -10, image=img) #coords are deliberately offscreen so that they aren't blinking as much in the top corner
        self.active = active
    obj = None
    last_render_coords = None
    active = None

class piece: #the shape you move down the screen
    def __init__(self, coords=[3, 20]):
        self.coords = self.topcoords.copy()
        self.id = random.choice(os.listdir(sys.path[0] + '/models'))
        self.image = images[random.choice(os.listdir(sys.path[0] + '/blocks'))]
        self.orientation = 'up'
        for model in os.listdir(sys.path[0] + '/models/' + self.id):
            file = open(sys.path[0] + '/models/' + self.id + '/' + model, 'r')
            m = file.read()
            final_model = ''
            for char in m:
                if char == '0' or char == '1':
                    final_model += char
            self.models[model[:len(model) - 4]] = final_model
            file.close()
        self.linelen = math.sqrt(len(self.models[self.orientation]))
    def check_sides_ok(self):
        num_lines = []
        sum_index = 0
        for index in range(len(self.models[self.orientation])):
            char = self.models[self.orientation][index]
            if char == '1':
                if not int(index / self.linelen) in num_lines:
                    num_lines.append(int(index / self.linelen))
        rows_occupied = []
        for index in range(len(screen_blocks)):
            b = screen_blocks[index]
            if not b == None:
                if b.active:
                    row = int(index / 10)
                    if not row in rows_occupied:
                        rows_occupied.append(row)
        if len(rows_occupied) == len(num_lines):
            return True
        return False
    def get_high_low_x(self):
        indexes = []
        for index in range(len(screen_blocks)):
            b = screen_blocks[index]
            if not b == None:
                if b.active:
                    indexes.append(int(index % 10))
        indexes.sort()
        return indexes[0], indexes[len(indexes) - 1]
    rotations = ['up', 'right', 'down', 'left']
    coords = [3, 28]
    topcoords = [4, 29]
    models = {}
    image = None #use the same image resource for all the blocks

#####

screen_blocks = []
for x in range(10 * 30): #add blank spaces to screen so that they can be replaced by blocks
    screen_blocks.append(None)
del x
def play():
    global canvas, active_piece
    start_menu.frame.pack_forget()
    canvas = tk.Canvas(root, bg='snow1', height=20 * 29 - 2, width=20 * 10) #screen height is 30 but the very bottom row shouldn't be displayed
    canvas.pack()
    for x in range(10): #add a bottom row of blocks to make impacting the bottom easier to calculate
        screen_blocks[x] = block()
    active_piece = piece()
    threading.Thread(target=render_loop).start()
    root.bind('<a>', apply_piece.move.left)
    root.bind('<d>', apply_piece.move.right)
    root.bind('<q>', apply_piece.rotate.left)
    root.bind('<e>', apply_piece.rotate.right)

def render_loop(): #rerender and move down on a timer
    global active_piece
    while True:
        while apply_piece.running:
            time.sleep(0.01)
        active_piece.coords[1] -= 1
        render.render()
        time.sleep(0.2)

class render: #uses objects because ... ... ... meh
    def __init__(self):
        self.active = False
    def render(self):
        global active_piece
        if not self.rendering:
            self.rendering = True
            for x in range(len(screen_blocks)):
                b = screen_blocks[x]
                if not b == None:
                    if b.active:
                        canvas.delete(b.obj)
                        screen_blocks[x] = None
            if send_piece_to_blocks(active_piece):
                while apply_piece.running:
                    time.sleep(0.01)
                active_piece.coords[1] += 1
                for x in range(len(screen_blocks)):
                    b = screen_blocks[x]
                    if not b == None:
                        if b.active:
                            canvas.delete(b.obj)
                            screen_blocks[x] = None
                send_piece_to_blocks(active_piece, block_active=False)
                active_piece = piece()
                active_piece.coords = active_piece.topcoords.copy()
            for index in range(len(screen_blocks)):
                render_block_from_index(index)
            self.rendering = False
    rendering = False
render = render()

print('Loading subsystems...')
sys.stdout.write('[...]')
for sub in os.listdir(sys.path[0] + '/subsystems'): #run all code in subsystems folder, makes it moddable if modded tetris is the sort of thing you're into
    sys.stdout.flush()
    sys.stdout.write('{:30}'.format('\r/subsystems/' + sub))
    file = open(sys.path[0] + '/subsystems/' + sub, 'r')
    fc = file.read()
    file.close()
    exec(fc)
sys.stdout.write('{:30}'.format('\rDone') + '\n')
del fc, sub, file

class start_menu:
    menu_width = 15
    frame = tk.Frame(root)
    title = tk.Label(frame, text='Tetris', font=fonts.title)
    play_game = tk.Button(frame, text='Play', font=fonts.large, width=menu_width, command=play, relief=fonts.relief, overrelief=fonts.overrelief)
    leaderboard = tk.Button(frame, text='Leaderboard', font=fonts.large, width=menu_width, relief=fonts.relief, overrelief=fonts.overrelief, command=leaderboard.show_leaderboard)
    #
    title.pack(fill=tk.X)
    play_game.pack(fill=tk.X)
    leaderboard.pack(fill=tk.X)
    frame.pack()

root.mainloop()
