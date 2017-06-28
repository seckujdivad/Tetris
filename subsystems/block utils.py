def render_block_from_index(index): #render from a specific index
    global screen_blocks
    b = screen_blocks[index]
    if not b == None:
        xcoord = (index % 10) * 20 + 11
        ycoord = (20 * 30) - ((int(index / 10) * 20) + 10)
        if not b.last_render_coords == [xcoord, ycoord]: #optimised rerender render skipping
            canvas.coords(b.obj, xcoord, ycoord)
            b.last_render_coords = [xcoord, ycoord]

def send_piece_to_blocks(piece, block_active=True):
    model = piece.models[piece.orientation]
    start_index = piece.coords[0] + (piece.coords[1] * 10)
    return_clip = False
    for i in range(len(model)):
        char = model[i]
        if char == '1':
            index = int((start_index + (i % piece.linelen) - int(i / piece.linelen) * 10) % len(screen_blocks))
            if type(screen_blocks[index]) == block:
                return_clip = True
            else:
                screen_blocks[index] = block(colour=piece.image, active=block_active)
    if return_clip:
        for i in range(len(model)):
            char = model[i]
            if char == 1:
                index = int((start_index + (i % piece.linelen) - int(i / piece.linelen) * 10) % len(screen_blocks))
                screen_blocks[index] = None
    return return_clip

class scoring:
    def __init__(self):
        self.output = tk.Label(game_frame.right, text='- - - -', font=fonts.large)
        #
        self.output.pack()
    def check_complete_rows(self):
        rows_cleared = 0
        row_nums = []
        for index in range(10, len(screen_blocks) - 1, 10):
            top = index + 10
            scored = True
            for sub_index in range(index, top):
                if screen_blocks[sub_index] == None:
                    scored = False
            if scored:
                rows_cleared += 1
                row_nums.append(index)
        return rows_cleared, row_nums
    def on_piece_stop(self):
        rows_cleared, row_ids = self.check_complete_rows()
        if rows_cleared > 0:
            self.score += [0, 40, 100, 300, 1200][rows_cleared]
            self.score += self.lines_soft_dropped
            self.lines_soft_dropped = 0
            self.score_update()
            for index in row_ids:
                bottom = index
                top = index + 10
                for sub_index in range(top, bottom, -1):
                    if not screen_blocks[sub_index] == None:
                        canvas.delete(screen_blocks[sub_index].obj)
                    screen_blocks.pop(sub_index)
                    screen_blocks.append(None)
    def score_update(self):
        self.output.config(text=str(self.score))
    score = 0
    lines_soft_dropped = 0
scoring_handler = scoring()