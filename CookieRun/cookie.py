from pico2d import*
import manager_effect_sound
import stage_state

DIR_RIGHT, DIR_LEFT = 0, 1
MAP_SIZE = 11000

class Cookie:
    def __init__(self):
        self.x, self.y = 135, 142   #시작점이 135 / 카메라는 0
        self.sizeX, self.sizeY = 50, 80
        self.cameraX = 0
        self.frame, self.deadframe = 0, 0
        self.isJump, self.jumpCount = False, 0
        self.isSliding = False
        self.isBig, self.bigCount = False, 0
        self.lifecount, self.isDead, self.eatLifecount, self.jellyCount = 300.0, False, 0, 0
        self.isCollisionBox = False
        self.isHurdleCollision, self.hurdleCollisionCount = False, 0

        #방향추가
        self.dir = DIR_RIGHT

        #일반이미지
        self.run_image = load_image('Image\\stage1_cookie\\cookie_run.png')
        self.jump_image_up = load_image('Image\\stage1_cookie\\cookie_run_jump2.png')
        self.jump_image_down = load_image('Image\\stage1_cookie\\cookie_run_jump.png')
        self.sliding_image = load_image('Image\\stage1_cookie\\cookie_run_slide.png')
        self.collision_image = load_image('Image\\stage1_cookie\\cookie_run_collid2.png')
        self.dead_image = load_image('Image\\stage1_cookie\\cookie_run_dead.png')
        #빅이 되었을경우의 이미지들
        self.run_bigimage = load_image('Image\\stage1_cookie\\cookie_run_big.png')
        self.jump_bigimage_up = load_image('Image\\stage1_cookie\\cookie_run_jump2_big.png')
        self.jump_bigimage_down = load_image('Image\\stage1_cookie\\cookie_run_jump_big.png')
        self.sliding_bigimage = load_image('Image\\stage1_cookie\\cookie_run_slide_big.png')


        # 반대 일반이미지
        self.rev_run_image = load_image('Image\\stage2_cookie\\cookie_run.png')
        self.rev_jump_image_up = load_image('Image\\stage2_cookie\\cookie_run_jump2.png')
        self.rev_jump_image_down = load_image('Image\\stage2_cookie\\cookie_run_jump.png')
        self.rev_sliding_image = load_image('Image\\stage2_cookie\\cookie_run_slide.png')
        self.rev_collision_image = load_image('Image\\stage2_cookie\\cookie_run_collid2.png')
        self.rev_dead_image = load_image('Image\\stage2_cookie\\cookie_run_dead.png')
        # 반대 빅이 되었을경우의 이미지들
        self.rev_run_bigimage = load_image('Image\\stage2_cookie\\cookie_run_big.png')
        self.rev_jump_bigimage_up = load_image('Image\\stage2_cookie\\cookie_run_jump2_big.png')
        self.rev_jump_bigimage_down = load_image('Image\\stage2_cookie\\cookie_run_jump_big.png')
        self.rev_sliding_bigimage = load_image('Image\\stage2_cookie\\cookie_run_slide_big.png')

    def __del__(self):
        self.exit()

    def enter(self):
        self.isFinishDead = False

    def update(self, _frametime, _events):
        #죽는지 확인
        if self.isDead == False:
            self.lifecount -= 0.3
        elif (self.isDead) and (self.isFinishDead == False):
            # 죽음
            self.frame += 1
            self.deadframe = (int)(self.frame / 8 % 4)
            if self.frame > 28:
                self.isFinishDead = True
                return True
            return False
        elif self.isFinishDead == True:
            return True
        if self.lifecount < 0:
            self.isDead = True
            self.lifecount = 0
            self.frame = 0

        #방향전환
        if (self.dir == DIR_RIGHT) and ((self.x - self.cameraX) > (800 - 135)):
            self.x = self.cameraX + (800 - 135)
            self.dir = DIR_LEFT
            self.frame = 0
            stage_state.load_reverse_map_data()
        elif (self.dir == DIR_LEFT) and ((self.x - self.cameraX) < 135):
            self.x = self.cameraX + 135
            self.dir = DIR_RIGHT
            self.frame = 0
            stage_state.load_map_data()


        #키체크
        for event in _events:
            if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
                if self.isJump == False:
                    manager_effect_sound.CallEffectSound('JUMP')
                    self.isJump = True
                    self.frame = 0
            #슬라이딩 관련 키체크
            elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN and (not self.isJump):
                self.isSliding = True
                manager_effect_sound.CallEffectSound('LAND')
            elif event.type == SDL_KEYUP and event.key == SDLK_DOWN and (self.isSliding):
                self.isSliding = False
                self.frame = 0
            #충돌체크박스보여주기
            elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
                if self.isCollisionBox == False:
                    self.isCollisionBox = True
                else:
                    self.isCollisionBox = False

        #프레임움직임
        self.frame = (self.frame + 1) % 5

        #움직임
        if self.isHurdleCollision:
            if self.hurdleCollisionCount == 20:
                if self.dir == DIR_RIGHT:
                    self.x -= 30
                    self.cameraX -= 30
                elif self.dir == DIR_LEFT:
                    self.x += 30
                    self.cameraX += 30

            self.hurdleCollisionCount -= 1
            if self.hurdleCollisionCount < 0:
                self.hurdleCollisionCount = 0
                self.isHurdleCollision = False
        elif (self.lifecount > 0):

            #이부분을 바꿔야함 + 스크롤링
            if self.dir == DIR_RIGHT:
                self.x += 6 * 50 * _frametime
                if self.x > MAP_SIZE:
                    pass
                else:
                    self.cameraX += 6 * 50 * _frametime
            elif self.dir == DIR_LEFT:
                self.x -= 6 * 50 * _frametime
                if self.x < 0:
                    pass
                else:
                    self.cameraX -= 6 * 50 * _frametime


            if self.isJump:
                self.jumpCount += 1
                if self.jumpCount == 24:
                    self.jumpCount = 0
                    self.isJump = False
                elif self.jumpCount < 12:
                    self.y += (12 - self.jumpCount) * 2
                else:
                    self.y -= (self.jumpCount - 12) * 2

            if self.eatLifecount != 0:
                self.eatLifecount -= 1

        if self.isBig:
            self.bigCount -= 1
            if self.bigCount < 0:
                self.bigCount = 0
                self.isBig = False
                self.sizeX, self.sizeY = 50, 80


    def draw(self):
        if self.dir == DIR_RIGHT:
            if self.isDead:
                self.dead_image.clip_draw(self.deadframe * 100, 0, 100, 100, self.x - self.cameraX, self.y + 10)
            elif self.isHurdleCollision:
                self.collision_image.clip_draw(self.frame * 53, 0, 53, 81, self.x - self.cameraX, self.y)
            elif (self.isJump == False) and (self.isSliding == False):
                if self.isBig:
                    self.run_bigimage.clip_draw(self.frame * 300, 0, 300, 348, self.x - self.cameraX, self.y + 130)
                elif self.isBig == False:
                    self.run_image.clip_draw(self.frame * 75, 0, 75, 87, self.x - self.cameraX, self.y)
            elif (self.isJump) and (self.jumpCount < 12):
                if self.isBig:
                    self.jump_bigimage_up.draw(self.x - self.cameraX, self.y + 130)
                elif self.isBig == False:
                    self.jump_image_up.draw(self.x - self.cameraX, self.y)
            elif self.isJump:
                if self.isBig:
                    self.jump_bigimage_down.draw(self.x - self.cameraX, self.y + 130)
                elif self.isBig == False:
                    self.jump_image_down.draw(self.x - self.cameraX, self.y)
            elif self.isSliding:
                if self.isBig:
                    self.sliding_bigimage.draw(self.x - self.cameraX, self.y + 50)  # 슬라이딩 값 보정
                elif self.isBig == False:
                    self.sliding_image.draw(self.x - self.cameraX, self.y - 20)#슬라이딩 값 보정

        elif self.dir == DIR_LEFT:
            if self.isDead:
                self.rev_dead_image.clip_draw(self.deadframe * 100, 0, 100, 100, self.x - self.cameraX, self.y + 10)
            elif self.isHurdleCollision:
                self.rev_collision_image.clip_draw(self.frame * 53, 0, 53, 81, self.x - self.cameraX, self.y)
            elif (self.isJump == False) and (self.isSliding == False):
                if self.isBig:
                    self.rev_run_bigimage.clip_draw(self.frame * 300, 0, 300, 348, self.x - self.cameraX, self.y + 130)
                elif self.isBig == False:
                    self.rev_run_image.clip_draw(self.frame * 75, 0, 75, 87, self.x - self.cameraX, self.y)
            elif (self.isJump) and (self.jumpCount < 12):
                if self.isBig:
                    self.rev_jump_bigimage_up.draw(self.x - self.cameraX, self.y + 130)
                elif self.isBig == False:
                    self.rev_jump_image_up.draw(self.x - self.cameraX, self.y)
            elif self.isJump:
                if self.isBig:
                    self.rev_jump_bigimage_down.draw(self.x - self.cameraX, self.y + 130)
                elif self.isBig == False:
                    self.rev_jump_image_down.draw(self.x - self.cameraX, self.y)
            elif self.isSliding:
                if self.isBig:
                    self.rev_sliding_bigimage.draw(self.x - self.cameraX, self.y + 50)  # 슬라이딩 값 보정
                elif self.isBig == False:
                    self.rev_sliding_image.draw(self.x - self.cameraX, self.y - 20)#슬라이딩 값 보정


        if self.isCollisionBox:
            self.draw_bb()


    def exit(self):
        del (self.run_image)
        del (self.jump_image_up)
        del (self.jump_image_down)
        del (self.sliding_image)
        del (self.collision_image)
        del (self.dead_image)

        del (self.run_bigimage)
        del (self.jump_bigimage_up)
        del (self.jump_bigimage_down)
        del (self.sliding_bigimage)


    def getPlayerX(self):
        return self.x


    def get_bb(self):
        if (self.isSliding) and (self.isBig == False):
            return self.x - 45 - self.cameraX, self.y - 45, \
                   self.x + 45 - self.cameraX, self.y
        elif (self.isSliding == False) and (self.isBig == False):
            return self.x - self.sizeX / 2 - self.cameraX - 5, self.y - self.sizeY / 2, \
                self.x + self.sizeX / 2 - self.cameraX, self.y + self.sizeY / 2
        #커졌을경우
        elif (self.isSliding) and (self.isBig):
            return self.x - 180 - self.cameraX, self.y - 45, \
                   self.x + 180 - self.cameraX, self.y + 100
        elif (self.isSliding == False) and (self.isBig):
            return self.x - self.sizeX / 2 - self.cameraX - 5, self.y - self.sizeY / 2 + 110, \
                self.x + self.sizeX / 2 - self.cameraX, self.y + self.sizeY / 2 + 110



    def draw_bb(self):
        draw_rectangle(*self.get_bb())