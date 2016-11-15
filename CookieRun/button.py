from pico2d import *

class Button:
    def __init__(self):
        self.isCollisionBox = False

        self.isCollision = False

        self.buttonon_image = load_image('Image\\result_ok.png')
        self.buttonoff_image = load_image('Image\\result_ok_click.png')

        self.x, self.y = 400, 175
        self.mouseX, self.mouseY = 0, 0


    def __del__(self):
        self.exit()


    def enter(self):
        pass


    def update(self, _events):
        #충돌처리
        if (((self.x - 46) < self.mouseX) and ((self.x + 46) > self.mouseX)) \
                and (((self.y - 16) < (600 - self.mouseY)) and ((self.y + 16) > (600 - self.mouseY))):
            self.isCollision = True
        else:
            self.isCollision = False
        #a키 입력받을 경우 충돌박스 넣기
        for event in _events:
            if event.type == SDL_KEYDOWN and event.key == SDLK_a:
                if self.isCollisionBox == False:
                    self.isCollisionBox = True
                else:
                    self.isCollisionBox = False

            if event.type == SDL_MOUSEMOTION:
                self.mouseX, self.mouseY = event.x, event.y

            if (event.type, self.isCollision) == (SDL_MOUSEBUTTONUP, True):
                return True

        return False


    def draw(self):
        if self.isCollision == True:
            self.buttonoff_image.draw(self.x, self.y)
        elif self.isCollision == False:
            self.buttonon_image.draw(self.x, self.y)

        if self.isCollisionBox:
            self.draw_bb()


    def exit(self):
        del (self.buttonon_image)
        del (self.buttonoff_image)


    def get_bb(self):
        return self.x - 46, self.y - 16, self.x + 46, self.y + 16


    def draw_bb(self):
        draw_rectangle(*self.get_bb())