from pico2d import *

class Button:
    def __init__(self):
        self.isCollisionBox = False

        self.buttonon_image = load_image('Image\\result_ok.png')
        self.buttonoff_image = load_image('Image\\result_ok_click.png')


    def __del__(self):
        self.exit()


    def enter(self):
        pass


    def update(self, _events):
        #a키 입력받을 경우 충돌박스 넣기
        pass


    def draw(self):
        self.buttonon_image.draw(self.x - self.cameraX, self.y)
        self.buttonoff_image.draw(self.x - self.cameraX, self.y)

        if self.isCollisionBox:
            self.draw_bb()


    def exit(self):
        del (self.buttonon_image)
        del (self.buttonoff_image)



    def get_bb(self):
        return self.x - 15 - self.cameraX, self.y - 15, \
               self.x + 15 - self.cameraX, self.y + 15



    def draw_bb(self):
        draw_rectangle(*self.get_bb())