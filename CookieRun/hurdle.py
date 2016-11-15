from pico2d import*

class Hurdle:
    def __init__(self, _x = 0, _type = 0, _imagetype = 0):
        self.x, self.y = _x, 0
        self.cameraX = 0
        self.type = _type#타입은 0위 / 1아래
        self.imagetype = _imagetype #0 2개(0~1) / 1 4개(0~3)
        self.isCollisionBox = False

    def __del__(self):
        self.exit()

    def enter(self):
        if self.type == 0:
            if self.imagetype == 0:
                self.sizeX, self.sizeY = 80, 448
                self.image = load_image('Image\\Stage1_Fork.png')
            elif self.imagetype == 1:
                self.sizeX, self.sizeY = 120, 448
                self.image = load_image('Image\\Stage1_Fork2.png')



            #y좌표 조정
            self.y = 600 - (self.sizeY / 2)
        elif self.type == 1:
            if self.imagetype == 0:
                self.sizeX, self.sizeY = 34, 50
                self.image = load_image('Image\\Stage1_thorn.png')
            elif self.imagetype == 1:
                self.sizeX, self.sizeY = 42, 60
                self.image = load_image('Image\\Stage1_thorn2.png')
            elif self.imagetype == 2:
                self.sizeX, self.sizeY = 30, 50
                self.image = load_image('Image\\Stage1_thorn3.png')
            elif self.imagetype == 3:
                self.sizeX, self.sizeY = 42, 60
                self.image = load_image('Image\\Stage1_thorn4.png')
            # y좌표 조정
            self.y = 100 + (self.sizeY / 2)


    def update(self, _event, _scroll):
        self.cameraX = _scroll

        # 키체크
        for event in _event:
            if event.type == SDL_KEYDOWN and event.key == SDLK_a:
                if self.isCollisionBox == False:
                    self.isCollisionBox = True
                else:
                    self.isCollisionBox = False


    def draw(self):
        if self.type == 0:
            self.image.draw(self.x - self.cameraX, self.y)
        elif self.type == 1:
            self.image.draw(self.x - self.cameraX, self.y)


        if self.isCollisionBox:
            self.draw_bb()


    def exit(self):
        del (self.image)



    def get_bb(self):
        return self.x - (self.sizeX / 2) - self.cameraX, self.y - (self.sizeY / 2),\
               self.x + (self.sizeX / 2) - self.cameraX, self.y + (self.sizeY / 2)



    def draw_bb(self):
        draw_rectangle(*self.get_bb())