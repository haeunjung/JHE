from pico2d import*

import game_framework
import title_state

import cookie
import jelly
import hurdle
#ui만들기
import ui

import collision

stageBack_image = None
stageLand_image = None

scrollX = 0

isGameEnd = False
keyevents = None

player = None
player_ui = None

HURDLE, JELLY = 0, 1
hurdle_jelly_List = None

def enter():
    global stageBack_image, stageLand_image
    stageBack_image = load_image('Image\\First_Background.png')
    stageLand_image = load_image('Image\\First_ground.png')


    #허들젤리리스트
    global hurdle_jelly_List
    temphurdle = hurdle.Hurdle(1000)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List = {HURDLE: [temphurdle], JELLY: []}
    temphurdle = hurdle.Hurdle(1300, 1, 2)  # 타입 + 이미지스타일
    temphurdle.enter()
    hurdle_jelly_List[HURDLE].append(temphurdle)

    tempjelly = jelly.Jelly(1000, 130, 0)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(1500, 130, 1)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)
    tempjelly = jelly.Jelly(2000, 130, 2)  # 마지막은 타입
    tempjelly.enter()
    hurdle_jelly_List[JELLY].append(tempjelly)



    global player, player_ui
    player = cookie.Cookie()
    player.enter()
    player_ui = ui.UI()
    player_ui.enter()


def exit():
    global stageBack_image, stageLand_image
    del (stageBack_image)
    del (stageLand_image)

    #플레이어 삭제
    global player, player_ui
    del (player_ui)
    del (player)

    # 허들젤리리스트 삭제
    global hurdle_jelly_List
    for i in hurdle_jelly_List:
        for j in hurdle_jelly_List[i]:
            hurdle_jelly_List[i].remove(j)


def update():
    global scrollX, isGameEnd, keyevents

    #게임의 종료
    if isGameEnd == True:
        game_framework.change_state(title_state)

    # 플레이어
    global player
    if player.update(keyevents):
        game_framework.change_state(title_state)
        return

    # 허들젤리리스트 update
    global hurdle_jelly_List
    for i in hurdle_jelly_List:
        for j in hurdle_jelly_List[i]:
            j.update(keyevents, player.getPlayerX())

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