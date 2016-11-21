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

stageBack_image = None
stageLand_image = None

scrollX = 0

isResultUI = None
isGameEnd = None
keyevents = None

player = None
player_ui = None
player_result_ui = None

HURDLE, JELLY = 0, 1
hurdle_jelly_List = None

def enter():
    global stageBack_image, stageLand_image
    stageBack_image = load_image('Image\\First_Background.png')
    stageLand_image = load_image('Image\\First_ground.png')


    global isResultUI, isGameEnd
    isGameEnd = False
    isResultUI = False

    #맵데이터 가져오기
    load_map_data()

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


def update():
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
    if player.update(keyevents):
        #게임의 종료
        if isResultUI == False:
            #마지막 배너 추가
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
                    elif player.isBig == False:
                        player.isHurdleCollision, player.hurdleCollisionCount = True, 20
                        player.lifecount -= 10.0
            elif i == 1:
                if (collision.collisionAB(player, j)):
                    if j.type == 0:
                        player.isBig = True
                        player.bigCount = 150
                        player.sizeX, player.sizeY = 240, 300
                    elif j.type == 1:
                        player.jellyCount += j.ability
                    elif j.type == 2:
                        player.lifecount += j.ability
                        player.eatLifecount = 50
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



def load_map_data():
    global hurdle_jelly_List

    # json 예제
    # hurdle_file = open('MapData\\FirstHurdleData.txt', 'r')
    # hurdle_data = json.load(hurdle_file)
    # hurdle_file.close()

    # jelly_file = open('MapData\\FirstJellyData.txt', 'r')
    # jelly_data = json.load(jelly_file)
    # jelly_file.close()

    # 허들리스트
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

    # 젤리추가
    tempjelly = jelly.Jelly(1000, 130, 1)  # 마지막은 타입
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



    tempjelly = jelly.Jelly(2000, 130, 2)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(4050, 150, 2)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(5100, 130, 0)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)