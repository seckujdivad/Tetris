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