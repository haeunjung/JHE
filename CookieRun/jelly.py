from pico2d import*

class Jelly:
    def __init__(self, _x = 0, _y = 0, _type = 0):
        self.x, self.y = _x, _y
        self.sizeX, self.sizeY = 26, 34
        self.cameraX = 0
        self.type = _type#타입은 0big / 1score / 2hp
        self.isCollisionBox = False

    def __del__(self):
        self.exit()

    def enter(self):
        if self.type == 0:
            self.ability = 0
            self.image = load_image('Image\\big_jelly.png')
        elif self.type == 1:
            self.ability = 1
            self.image = load_image('Image\\item_Jelly.png')
        elif self.type == 2:
            self.ability = 50.0
            self.image = load_image('Image\\hp_jelly.png')

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
        self.image.draw(self.x - self.cameraX, self.y)
        if self.isCollisionBox:
            self.draw_bb()


    def exit(self):
        del (self.image)



    def get_bb(self):
        return self.x - 15 - self.cameraX, self.y - 15, \
               self.x + 15 - self.cameraX, self.y + 15



    def draw_bb(self):
        draw_rectangle(*self.get_bb())