from pico2d import*

import stage_state
#버튼 추가
class UI:
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

        self.jelly_image = load_image('Image\\item_Jelly.png')
        self.hp_image = load_image('Image\\hp.png')
        self.big_image = load_image('Image\\big_icon.png')
        self.hpup_image = load_image('Image\\hp_icon.png')

        #마지막 결과창
        self.result_image = load_image('Image\\result.png')

        self.playerscore = 0


    def __del__(self):
        self.exit()


    def enter(self):
        pass


    def update(self, _events):
        pass


    def draw(self):
        if (stage_state.player.lifecount > 0):
            #플레이어의 체력상태
            temprate = (int)(200 * (stage_state.player.lifecount / 300.0))
            self.hp_image.clip_draw(0, 0,
                                    temprate * 2, 64,
                                    temprate + 50, 550)

            # 점수가져오기
            self.playerscore = (int)(stage_state.player.jellyCount)

            #젤리카운트 draw
            self.jelly_image.draw(600, 550)
            self.score_draw((int)(self.playerscore / 100), 650, 550)
            self.score_draw((int)(self.playerscore % 100 / 10), 700, 550)
            self.score_draw((int)(self.playerscore % 10), 750, 550)

            if stage_state.player.bigCount > 100:
                self.big_image.draw(400, 300)

            if stage_state.player.eatLifecount > 0:
                self.hpup_image.draw(400, 300)


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

        del (self.jelly_image)
        del (self.big_image)
        del (self.hp_image)
        del (self.hpup_image)


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