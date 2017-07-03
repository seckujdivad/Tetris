class keybinds:
    def __init__(self):
        root.bind('<KeyPress>', self.on_press)
        root.bind('<KeyRelease>', self.on_release)
        self.find_from_file()
    def on_press(self, event):
        if not event.keysym in self.pressed:
            self.pressed.append(event.keysym)
    def on_release(self, event):
        while event.keysym in self.pressed:
            self.pressed.remove(event.keysym)
    def find_from_file(self):
        file = open(paths.persistent + 'keybinds.txt', 'r')
        fc = file.read().split('\n')
        file.close()
        for line in fc:
            if (not line == '') and (not line.startswith('#')):
                function, keysyms, delay = line.split(':')
                if function in self.funcs:
                    self.bind(eval(keysyms), self.funcs[function], float(delay))
    def bind(self, keys, function, clock_duration, error_messages=True):
        threading.Thread(target=self._bind, args=[keys, function, clock_duration, error_messages], name=str(keys) + ' binding', daemon=True).start()
    def _bind(self, keys, function, clock_duration, error_messages):
        while True:
            time.sleep(0.01) #performance enhancing. trust me. comment it out. i dare you
            cont = True
            while cont:
                cont = True
                for key in keys:
                    if not (key in self.pressed):
                        cont = False
                        continue
                if cont:
                    threading.Thread(target=self._run, args=[function, error_messages], name=str(key) + ' press response', daemon=True).start()
                    time.sleep(clock_duration)
    def _run(self, function, error_messages):
        if error_messages:
            function()
        else:
            try: #catch errors
                function()
            except:
                pass
    pressed = []
    funcs = {'screen image':display_screen_as_text,
    'move left':apply_piece.move.left, 'move right':apply_piece.move.right,
    'rotate left':apply_piece.rotate.left, 'rotate right':apply_piece.rotate.right,
    'drop':render.tick}
keys = keybinds()