class apply_piece:
    running = False
    class move:
        def left(event):
            global apply_piece
            if not apply_piece.running and not render.rendering:
                apply_piece.running = True
                active_piece.coords[0] -= 1
                render.render(movement='x-1')
                apply_piece.running = False
        def right(event):
            if not apply_piece.running and not render.rendering:
                apply_piece.running = True
                active_piece.coords[0] += 1
                render.render(movement='x+1')
                apply_piece.running = False
    class rotate:
        def left(event):
            if not apply_piece.running and not render.rendering:
                apply_piece.running = True
                index = active_piece.rotations.index(active_piece.orientation) - 1
                if index < 0:
                    index = len(active_piece.rotations) - 1
                active_piece.orientation = active_piece.rotations[index]
                render.render()
                if not active_piece.check_sides_ok() == [False, False]:
                    index = active_piece.rotations.index(active_piece.orientation) + 1
                    if index > len(active_piece.rotations) - 1:
                        index = 0
                    active_piece.orientation = active_piece.rotations[index]
                    render.render()
                apply_piece.running = False
        def right(event):
            if not apply_piece.running and not render.rendering:
                apply_piece.running = True
                index = active_piece.rotations.index(active_piece.orientation) + 1
                if index > len(active_piece.rotations) - 1:
                    index = 0
                active_piece.orientation = active_piece.rotations[index]
                render.render()
                if not active_piece.check_sides_ok() == [False, False]:
                    index = active_piece.rotations.index(active_piece.orientation) - 1
                    if index < 0:
                        index = len(active_piece.rotations) - 1
                    active_piece.orientation = active_piece.rotations[index]
                    render.render()
                apply_piece.running = False
    def drop(event):
        global drop
        if event.keysym == 's':
            drop = True
    def undrop(event):
        global drop
        if event.keysym == 's':
            drop = False
apply_piece.bindings = {'<a>':apply_piece.move.left, '<d>':apply_piece.move.right, '<q>':apply_piece.rotate.left, '<e>':apply_piece.rotate.right,
                        '<KeyPress>':apply_piece.drop, '<KeyRelease>':apply_piece.undrop}
