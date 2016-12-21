from pico2d import*
import json

import game_framework
import title_state

import cookie
import jelly
import hurdle

import ui
import result_ui

import collision
import manager_effect_sound

stageBack_image = None
stageLand_image = None

MAP_SIZE = 12000
scrollX = 0

isFirst = True
isResultUI = None
isGameEnd = None
keyevents = None

player = None
player_ui = None
player_result_ui = None

HURDLE, JELLY = 0, 1
hurdle_jelly_List = None

gBGM1 = None
gBGM2 = None

def enter():
    global stageBack_image, stageLand_image
    stageBack_image = load_image('Image\\First_Background.png')
    stageLand_image = load_image('Image\\First_ground.png')


    global isResultUI, isGameEnd
    isGameEnd = False
    isResultUI = False

    global gBGM1, gBGM2
    gBGM1 = load_music('Sound/Stage1.mp3')
    gBGM1.set_volume(32)
    gBGM2 = load_music('Sound/Stage2.mp3')
    gBGM2.set_volume(32)


    #맵데이터 가져오기
    global isFirst
    isFirst = True
    load_map_data()
    isFirst = False

    global player, player_ui, player_result_ui
    player = cookie.Cookie()
    player.enter()
    player_ui = ui.UI()
    player_ui.enter()
    player_result_ui = result_ui.Result_UI()
    player_result_ui.enter()


def exit():
    global stageBack_image, stageLand_image
    del (stageBack_image)
    del (stageLand_image)

    global gBGM1, gBGM2
    del (gBGM1)
    del (gBGM2)

    #플레이어 삭제
    global player, player_ui, player_result_ui
    del (player_ui)
    del (player)
    del (player_result_ui)

    # 허들젤리리스트 삭제
    global hurdle_jelly_List
    for i in hurdle_jelly_List:
        for j in hurdle_jelly_List[i]:
            hurdle_jelly_List[i].remove(j)


def update(_frametime):
    global scrollX, isGameEnd, isResultUI, keyevents

    #게임의 종료
    if isGameEnd == True:
        game_framework.change_state(title_state)
        return

    if isResultUI:
        if player_result_ui.update(keyevents):
            isGameEnd = True
            return

    # 플레이어
    global player
    if player.update(_frametime, keyevents):
        #게임의 종료
        if isResultUI == False:
            #마지막 배너 추가
            manager_effect_sound.CallEffectSound('END')
            isResultUI = True
        return

    # 허들젤리리스트 update
    global hurdle_jelly_List
    for i in hurdle_jelly_List:
        for j in hurdle_jelly_List[i]:
            j.update(keyevents, player.getPlayerX())

    #충돌
    for i in hurdle_jelly_List:
        for j in hurdle_jelly_List[i]:
            if i == 0:
                if (collision.collisionAB(player, j)):
                    if player.isBig:
                        hurdle_jelly_List[i].remove(j)
                        manager_effect_sound.CallEffectSound('BIG_HIT')
                    elif player.isBig == False:
                        player.isHurdleCollision, player.hurdleCollisionCount = True, 20
                        player.lifecount -= 10.0
                        manager_effect_sound.CallEffectSound('COLLISION')
            elif i == 1:
                if (collision.collisionAB(player, j)):
                    if j.type == 0:
                        player.isBig = True
                        player.bigCount = 150
                        player.sizeX, player.sizeY = 240, 300
                        manager_effect_sound.CallEffectSound('BIG')
                    elif j.type == 1:
                        player.jellyCount += j.ability
                        manager_effect_sound.CallEffectSound('JELLY')
                    elif j.type == 2:
                        player.lifecount += j.ability
                        player.eatLifecount = 50
                        manager_effect_sound.CallEffectSound('LARGE_JELLY')
                        if player.lifecount > 300.0:
                            player.lifecount = 300.0
                    # 삭제
                    hurdle_jelly_List[i].remove(j)


    # 게임의 스크롤링 받아오기
    scrollX = player.getPlayerX() % 3200


def draw():
    global stageBack_image, stageLand_image
    global scrollX
    clear_canvas()

    for i in range(0, 2):
        stageBack_image.draw(400 + (800 * i) - (scrollX / 4), 300)

    for i in range(0, 5):
        stageLand_image.draw(400 + (800 * i) - scrollX, 300)

    # 플레이어
    global player
    player.draw()

    # 허들젤리리스트 draw
    global hurdle_jelly_List
    for i in hurdle_jelly_List:
        for j in hurdle_jelly_List[i]:
            j.draw()

    #ui draw
    global player_ui
    player_ui.draw()

    #result ui
    global isResultUI, player_result_ui
    if isResultUI:
        player_result_ui.draw()

    update_canvas()

def handle_events():
    global keyevents
    keyevents = get_events()

    for event in keyevents:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()


def clear_map_data():
    global hurdle_jelly_List

    # 허들젤리리스트 삭제
    for i in hurdle_jelly_List:
        for j in hurdle_jelly_List[i]:
            hurdle_jelly_List[i].remove(j)


def load_reverse_map_data():
    # 초기화
    clear_map_data()

    global gBGM2
    gBGM2.repeat_play()

    global hurdle_jelly_List
    temphurdle = hurdle.Hurdle(MAP_SIZE - 1000, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List = {HURDLE: [temphurdle], JELLY: []}

    temphurdle = hurdle.Hurdle(MAP_SIZE - 2000, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 2200, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 2400, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(MAP_SIZE - 3300, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 3600, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 3900, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(MAP_SIZE - 5200, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 5300, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 5400, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 5500, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 5600, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 7400, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 7500, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 8250, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 8350, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 9300, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 9400, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 9500, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 9600, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 10300, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 10400, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(MAP_SIZE - 1300, 1, 2)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(MAP_SIZE - 1700, 1, 2)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(MAP_SIZE - 2600, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 2800, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 3000, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(MAP_SIZE - 4600, 1, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 4800, 1, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 5000, 1, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(MAP_SIZE - 5800, 1, 2)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 6200, 1, 2)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(MAP_SIZE - 6780, 1, 2)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 7030, 1, 2)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 7780, 1, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 8030, 1, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(MAP_SIZE - 8550, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 8750, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 8950, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 9800, 1, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 9900, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 10000, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(MAP_SIZE - 10100, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    # 젤리추가
    tempjelly = jelly.Jelly(MAP_SIZE - 1000, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1050, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1100, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1150, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1200, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1250, 170, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1300, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1350, 170, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1400, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1450, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1500, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1550, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1600, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1650, 170, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1700, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1750, 170, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1800, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1850, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1900, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 1950, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2000, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2050, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2050, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2100, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2150, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2200, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2250, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2300, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2350, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2400, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2450, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2500, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2550, 130, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2650, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2700, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2750, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2850, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2900, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 2950, 130, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 3400, 180, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 3450, 180, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 3500, 180, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 3700, 180, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 3750, 180, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 3800, 180, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4100, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4150, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4200, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4250, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4300, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4350, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4400, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4450, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4500, 150, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4650, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4700, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4750, 150, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4850, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4900, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4950, 150, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 5200, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 5250, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 5300, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 5350, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 5400, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 5450, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 5500, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 5550, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 5600, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 5650, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 5700, 130, 1)  # 마지막은 타입
    tempjelly.enter()

    tempjelly = jelly.Jelly(MAP_SIZE - 5850, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 5900, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 5950, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6000, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6050, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6100, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6150, 130, 1)  # 마지막은 타입
    tempjelly.enter()

    tempjelly = jelly.Jelly(MAP_SIZE - 6350, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6400, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6450, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6500, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6550, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6600, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6650, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6700, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6750, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6800, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6850, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6900, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 6950, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7000, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7050, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7100, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7150, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7200, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7250, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7300, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7350, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7400, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7450, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7500, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7550, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7600, 130, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7650, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7700, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7750, 220, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7850, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7900, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7950, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8000, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8050, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8100, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8150, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8200, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8250, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8300, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8350, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8400, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8450, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8500, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8550, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8600, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8650, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8700, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8750, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8800, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8850, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8900, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 8950, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9000, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9050, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9100, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9150, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9200, 130, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9300, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9350, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9400, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9450, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9500, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9550, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9600, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9650, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9700, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9750, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 10200, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 10250, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 10300, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 10350, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 10400, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 10450, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 10500, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 10550, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 10600, 130, 1)  # 마지막은 타입
    tempjelly.enter()


    tempjelly = jelly.Jelly(MAP_SIZE - 2000, 130, 2)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 4050, 150, 2)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 5100, 130, 0)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 7800, 220, 2)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9250, 130, 2)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 9700, 130, 0)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 10150, 130, 0)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(MAP_SIZE - 10800, 130, 2)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)


def load_map_data():
    #초기화
    global isFirst
    if isFirst == False:
        clear_map_data()

    global gBGM1
    gBGM1.repeat_play()

    # 허들리스트
    global hurdle_jelly_List
    temphurdle = hurdle.Hurdle(1000, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List = {HURDLE: [temphurdle], JELLY: []}

    temphurdle = hurdle.Hurdle(2000, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(2200, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(2400, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(3300, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(3600, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(3900, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(5200, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(5300, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(5400, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(5500, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(5600, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(7400, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(7500, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(8250, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(8350, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(9300, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(9400, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(9500, 0, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(9600, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(10300, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(10400, 0, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(1300, 1, 2)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(1700, 1, 2)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(2600, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(2800, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(3000, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(4600, 1, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(4800, 1, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(5000, 1, 0)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(5800, 1, 2)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(6200, 1, 2)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(6780, 1, 2)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(7030, 1, 2)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(7780, 1, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(8030, 1, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    temphurdle = hurdle.Hurdle(8550, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(8750, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(8950, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(9800, 1, 1)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(9900, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(10000, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)
    temphurdle = hurdle.Hurdle(10100, 1, 3)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    # 젤리추가
    tempjelly = jelly.Jelly(1000, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1050, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1100, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1150, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1200, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1250, 170, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1300, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1350, 170, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1400, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1450, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1500, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1550, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1600, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1650, 170, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1700, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1750, 170, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1800, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1850, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1900, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1950, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2000, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2050, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2050, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2100, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2150, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2200, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2250, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2300, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2350, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2400, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2450, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2500, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2550, 130, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2650, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2700, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2750, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2850, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2900, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2950, 130, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(3400, 180, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(3450, 180, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(3500, 180, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(3700, 180, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(3750, 180, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(3800, 180, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4100, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4150, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4200, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4250, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4300, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4350, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4400, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4450, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4500, 150, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4650, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4700, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4750, 150, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4850, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4900, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4950, 150, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5200, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5250, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5300, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5350, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5400, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5450, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5500, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5550, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5600, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5650, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5700, 130, 1)  # 마지막은 타입
    tempjelly.enter()

    tempjelly = jelly.Jelly(5850, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5900, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5950, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6000, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6050, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6100, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6150, 130, 1)  # 마지막은 타입
    tempjelly.enter()

    tempjelly = jelly.Jelly(6350, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6400, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6450, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6500, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6550, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6600, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6650, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6700, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6750, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6800, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6850, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6900, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(6950, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7000, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7050, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7100, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7150, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7200, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7250, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7300, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7350, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7400, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7450, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7500, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7550, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7600, 130, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7650, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7700, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7750, 220, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7850, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7900, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7950, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8000, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8050, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8100, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8150, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8200, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8250, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8300, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8350, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8400, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8450, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8500, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8550, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8600, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8650, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8700, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8750, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8800, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8850, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8900, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(8950, 220, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9000, 190, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9050, 150, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9100, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9150, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9200, 130, 1)  # 마지막은 타입
    tempjelly.enter()

    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9300, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9350, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9400, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9450, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9500, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9550, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9600, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9650, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9700, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9750, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(10200, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(10250, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(10300, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(10350, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(10400, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(10450, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(10500, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(10550, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(10600, 130, 1)  # 마지막은 타입
    tempjelly.enter()


    tempjelly = jelly.Jelly(2000, 130, 2)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4050, 150, 2)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5100, 130, 0)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(7800, 220, 2)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9250, 130, 2)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(9700, 130, 0)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(10150, 130, 0)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(10800, 130, 0)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)