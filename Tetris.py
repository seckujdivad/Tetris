global fonts, start_menu, canvas, root, images, screen_blocks, active_piece, game_frame, next_piece, drop, paths
import tkinter as tk
import os, time, random, math, threading, sys, winsound, shutil, sqlite3
#shutil is to copy files without using os.system. Executing commands is disabled at school

drop = False

root = tk.Tk()
root.title('Tetris')

class paths:
    assets = sys.path[0] + '/assets/'
    blocks = assets + 'blocks/'
    models = assets + 'models/'
    subsystems = sys.path[0] + '/subsystems/'
    persistent_template = assets + '/persistent template/'
    persistent = sys.path[0] + '/persistent/'
    debug = sys.path[0] + '/debug/'
if not os.path.isdir(paths.debug): #add file for logs or list dumps - should be in gitignore
    os.mkdir(paths.debug)

class fonts: #unified fonts/formatting. please use
    face = ''
    title = (face, 50)
    large = (face, 25)
    normal = (face, 14)
    small = (face, 11)
    #formatting
    relief = tk.FLAT
    overrelief = tk.GROOVE

class game_frame:
    frame = tk.Frame(root)
    left = tk.Frame(frame)
    right = tk.Frame(frame)
    go_back = tk.Button(right, text='Exit', font=fonts.normal, relief=fonts.relief)
    #
    go_back.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

#load all the images into memory at the same time instead of loading once each time they are needed
print('Loading images...')
images = {}
sys.stdout.write('[...]')
for f in os.listdir(paths.blocks):
    sys.stdout.flush()
    sys.stdout.write('{:30}'.format('\r' + f))
    images[f] = tk.PhotoImage(file=paths.blocks + f)
sys.stdout.write('{:30}'.format('\rDone') + '\n')
del f

#####

class block: #the blocks that everything is made from - "the building blocks of life"
    def __init__(self, colour='random', active=False):
        if colour == 'random':
            img = images[random.choice(os.listdir(paths.blocks))]
        else:
            img = colour
        self.obj = canvas.create_image(-10, -10, image=img) #coords are deliberately offscreen so that they aren't blinking as much in the top corner
        self.active = active
    obj = None
    last_render_coords = None
    active = None

class piece: #the shape you move down the screen
    def __init__(self, data):
        self.coords = self.topcoords.copy()
        self.id = data['id']
        self.image = data['image']
        self.last_blocks = []
        for model in os.listdir(paths.models + self.id):
            file = open(paths.models + self.id + '/' + model, 'r')
            m = file.read()
            final_model = ''
            for char in m:
                if char == '0' or char == '1':
                    final_model += char
            self.models[model[:len(model) - 4]] = final_model
            file.close()
        self.linelen = math.sqrt(len(self.models[self.orientation]))
    def check_sides_ok(self):
        sides = [False, False]
        for index in range(len(self.models[self.orientation])):
            if self.models[self.orientation][index] == '1':
                x = self.coords[0] + int(index % self.linelen)
                y = self.coords[1] + int(index / self.linelen)
                if x < 0:
                    sides[0] = True
                elif x > 9:
                    sides[1] = True
        return sides
    rotations = ['up', 'right', 'down', 'left']
    topcoords = [4, 1]
    models = {}
    image = None #use the same image resource for all the blocks
    orientation = 'up'

#####
def play():
    global canvas, active_piece, next_piece, screen_blocks
    screen_blocks = []
    single_row = []
    for i in range(10):
        single_row.append(None)
    for y in range(30):
        screen_blocks.append(single_row.copy())
    start_menu.frame.pack_forget()
    canvas = tk.Canvas(game_frame.left, bg='snow1', height=20 * 29 - 2, width=20 * 10) #screen height is 30 but the very bottom row shouldn't be displayed
    canvas.pack()
    game_frame.frame.pack()
    for i in range(10):
        screen_blocks[29][i] = block()
    active_piece = piece(data=make_new_piece_data())
    next_piece = make_new_piece_data()
    previewer.refresh(next_piece)
    threading.Thread(target=render.render_loop, daemon=True).start()
    music_player()

def display_screen_as_text(event=None): #debug tool to print screen_blocks
    print('Writing screen_blocks...')
    try:
        text = 'screen_blocks dump:\n\t'
        for i in range(10):
            text += str(i) + '\t\t'
        for i in range(len(screen_blocks)):
            text += '\n' + str(i) + '\t'
            for item in screen_blocks[i]:
                if type(item) == block:
                    text += 'block'
                elif type(item) == None:
                    text += '[]'
                else:
                    text += str(item)
                text += '\t'
    except:
        try:
            text = 'Error!\n' + str(screen_blocks)
        except NameError:
            text = 'Error!'
        print('Error!')
    file = open(paths.debug + 'screen_blocks dump.txt', 'w')
    file.write(text)
    file.close()
    print('Wrote screen_blocks')

def on_piece_stop():
    global active_piece, next_piece
    scoring_handler.on_piece_stop()
    active_piece = piece(data=next_piece)
    next_piece = make_new_piece_data()
    previewer.refresh(next_piece)

def stop_playing():
    winsound.PlaySound(None, winsound.SND_ASYNC)
    game_frame.frame.pack_forget()
    canvas.destroy()
    start_menu.frame.pack()
game_frame.go_back.config(command=stop_playing)

def make_new_piece_data():
    piece_data = {}
    piece_data['id'] = random.choice(os.listdir(paths.models))
    piece_data['image'] = images[random.choice(os.listdir(paths.blocks))]
    return piece_data

def reset_persistent():
    if os.path.isdir(paths.persistent): #copy through a database
        shutil.rmtree(paths.persistent)
    time.sleep(0.2)
    os.mkdir(paths.persistent)
    for file in os.listdir(paths.persistent_template):
        shutil.copy(paths.persistent_template + file, paths.persistent + file)

class render: #uses objects because ... ... ... meh
    def __init__(self):
        self.active = False
    def render(self, movement=None):
        global active_piece, next_piece
        if not self.rendering:
            self.rendering = True
            send_piece_to_blocks(active_piece, move=movement)
            for y in range(len(screen_blocks)):
                for x in range(10):
                    render_block_from_coords(x, y)
            self.rendering = False
    def tick(self):
        active_piece.coords[1] += 1
        self.render()
    def render_loop(self): #rerender and move down on a timer
        global active_piece
        while True:
            while apply_piece.running:
                time.sleep(0.01)
            self.tick()
            time.sleep(0.2)   
    rendering = False
render = render()

if not os.path.isdir(paths.persistent):
    reset_persistent()

print('Loading subsystems...')
sys.stdout.write('[...]')
for sub in os.listdir(paths.subsystems): #run all code in subsystems folder, makes it moddable if modded tetris is the sort of thing you're into
    sys.stdout.flush()
    sys.stdout.write('{:30}'.format('\r' + sub))
    file = open(paths.subsystems + sub, 'r')
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
    settings = tk.Button(frame, text='Settings', font=fonts.large, width=menu_width, relief=fonts.relief, overrelief=fonts.overrelief, command=settings.show_settings)
    #
    title.pack(fill=tk.X)
    play_game.pack(fill=tk.X)
    leaderboard.pack(fill=tk.X)
    settings.pack(fill=tk.X)
    frame.pack()

root.mainloop()
