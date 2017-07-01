def render_block_from_coords(x, y, forced_rerender=False): #render from a specific coord
    global screen_blocks
    b = screen_blocks[y][x]
    if not b == None:
        xcoord = x * 20 + 10
        ycoord = y * 20 + 10
        if (not b.last_render_coords == [xcoord, ycoord]) or forced_rerender: #optimised rerender render skipping
            canvas.coords(b.obj, xcoord, ycoord)
            b.last_render_coords = [xcoord, ycoord]

def send_piece_to_blocks(given_piece, block_active=True, move=None, escape_next=False):
    global active_piece
    dup_move = move
    dup_block_active = block_active
    for y in range(len(screen_blocks)):
        for x in range(10):
            b = screen_blocks[y][x]
            if not b == None:
                if b.active:
                    canvas.delete(b.obj)
                    screen_blocks[y][x] = None
    clips = given_piece.check_sides_ok()
    if clips == [False, False]:
        model = given_piece.models[given_piece.orientation]
        model_length = int(math.sqrt(len(model)))
        return_clip = False
        for i in range(len(model)):
            char = model[i]
            if char == '1':
                x = (given_piece.coords[0]) + int(i % model_length)
                y = (given_piece.coords[1]) + int(i / model_length)
                if screen_blocks[y][x] == None:
                    screen_blocks[y][x] = block(colour=given_piece.image, active=block_active)
                else:
                    return_clip = True
        if escape_next:
            on_piece_stop()
        elif return_clip:
            if move == None:
                given_piece.coords[1] -= 1
                esc = True
            else:
                esc = False
                if move == 'x+1':
                    given_piece.coords[0] -= 1
                elif move == 'x-1':
                    given_piece.coords[0] += 1
            send_piece_to_blocks(given_piece, block_active=False, move=dup_move, escape_next=esc)
    else:
        if clips[0]:
            given_piece.coords[0] += 1
        if clips[1]:
            given_piece.coords[0] -= 1
        send_piece_to_blocks(given_piece, block_active=dup_block_active, move=dup_move)

class scoring:
    def __init__(self):
        self.output = tk.Label(game_frame.right, text='- - - -', font=fonts.large)
        #
        self.output.pack()
    def check_complete_rows(self):
        row_nums = []
        for y in range(len(screen_blocks)):
            if not y == 29: #bottom invisible row
                if not None in screen_blocks[y]:
                    row_nums.append(y)
        row_nums.sort()
        return row_nums
    def on_piece_stop(self):
        row_ids = self.check_complete_rows()
        if len(row_ids) > 0:
            self.score += [0, 40, 100, 300, 1200][len(row_ids)]
            self.score += self.lines_soft_dropped
            self.lines_soft_dropped = 0
            self.score_update()
            blank_list = []
            for i in range(10):
                blank_list.append(None)
            to_delete = []
            for y in row_ids:
                for b in screen_blocks[y]:
                    canvas.delete(b.obj)
                screen_blocks.pop(y)
                screen_blocks.insert(0, blank_list.copy())
            for y in range(len(screen_blocks)):
                for x in range(len(screen_blocks[y])):
                    render_block_from_coords(x, y, forced_rerender=True)
    def score_update(self):
        self.output.config(text=str(self.score))
    score = 0
    lines_soft_dropped = 0
scoring_handler = scoring() #run scoring_handler functions, not scoring