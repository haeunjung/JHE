from pico2d import*

import stage_state

import button
#버튼 추가
class Result_UI:
    def __init__(self):
        self.number0_image = load_image('Image\\Number\\0.png')
        self.number1_image = load_image('Image\\Number\\1.png')
        self.number2_image = load_image('Image\\Number\\2.png')
        self.number3_image = load_image('Image\\Number\\3.png')
        self.number4_image = load_image('Image\\Number\\4.png')
        self.number5_image = load_image('Image\\Number\\5.png')
        self.number6_image = load_image('Image\\Number\\6.png')
        self.number7_image = load_image('Image\\Number\\7.png')
        self.number8_image = load_image('Image\\Number\\8.png')
        self.number9_image = load_image('Image\\Number\\9.png')

        #마지막 결과창
        self.result_image = load_image('Image\\result.png')


        #버튼 1개 추가
        self.button_ui = button.Button()
        self.button_ui.enter()


        #플레이어의 점수 받아오기
        self.playerscore = 0


    def __del__(self):
        self.exit()


    def enter(self):
        pass


    def update(self, _events):
        # 점수가져오기
        self.playerscore = (int)(stage_state.player.jellyCount)

        #버튼 눌리면 True 반환
        if self.button_ui.update(_events):
            return True
        else:
            return False

    def draw(self):
        self.result_image.draw(400, 300)

        self.score_draw((int)(self.playerscore / 100), 350, 345)
        self.score_draw((int)(self.playerscore % 100 / 10), 400, 345)
        self.score_draw((int)(self.playerscore % 10), 450, 345)

        self.button_ui.draw()


    def exit(self):
        del (self.number0_image)
        del (self.number1_image)
        del (self.number2_image)
        del (self.number3_image)
        del (self.number4_image)
        del (self.number5_image)
        del (self.number6_image)
        del (self.number7_image)
        del (self.number8_image)
        del (self.number9_image)

        del (self.result_image)

        del (self.button_ui)


    def score_draw(self, number, x, y):
        if number == 0:
            self.number0_image.draw(x, y)
        elif number == 1:
            self.number1_image.draw(x, y)
        elif number == 2:
            self.number2_image.draw(x, y)
        elif number == 3:
            self.number3_image.draw(x, y)
        elif number == 4:
            self.number4_image.draw(x, y)
        elif number == 5:
            self.number5_image.draw(x, y)
        elif number == 6:
            self.number6_image.draw(x, y)
        elif number == 7:
            self.number7_image.draw(x, y)
        elif number == 8:
            self.number8_image.draw(x, y)
        elif number == 9:
            self.number9_image.draw(x, y)