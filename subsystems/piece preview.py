class preview:
    def __init__(self):
        self.canvas = tk.Canvas(game_frame.right, height=self.height, width=self.width, bg='snow1')
        #
        self.canvas.pack(side=tk.TOP)
        #
        self.objects = []
    def refresh(self, data):
        for object in self.objects:
            self.canvas.delete(object)
        self.objects = []
        #
        file = open(sys.path[0] + '/models/' + data['id'] + '/up.txt', 'r')
        raw_fc = file.read()
        file.close()
        fc = ''
        for char in raw_fc:
            if char in ['0', '1']:
                fc += char
        #
        sidelen = int(math.sqrt(len(fc)))
        for index in range(len(fc)):
            if fc[index] == '1':
                x = (index % sidelen) - sidelen / 2
                y = int(index / sidelen) - sidelen / 2
                x_absolute = (self.width / 2 - (x * 20)) - 10
                y_absolute = (self.height / 2 - (y * 20)) - 10
                self.objects.append(self.canvas.create_image(x_absolute, y_absolute, image=data['image']))
    width = 20 * 5
    height = 20 * 5
previewer = preview()