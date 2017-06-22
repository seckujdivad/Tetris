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
            screen_blocks[index] = block(colour=piece.image, active=block_active)
    return return_clip