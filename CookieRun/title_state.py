from pico2d import*

import game_framework
import stage_state

titleimage_kakao = None
titleimage_CI = None
titleimage = None
title_logo_time = 3.0
keyevents = None

def enter():
    global titleimage_kakao, titleimage_CI, titleimage

    titleimage_kakao = load_image('Image\\title_kakao.png')
    titleimage_CI = load_image('Image\\title_CI.png')
    titleimage = load_image('Image\\title.png')

    global title_logo_time
    title_logo_time = 3.0

def exit():
    global titleimage_kakao, titleimage_CI, titleimage
    del (titleimage_kakao)
    del (titleimage_CI)
    del (titleimage)


def update():
    global title_logo_time, keyevents

    title_logo_time -= 0.01

    if (title_logo_time < 0.0):
        title_logo_time = 0.0

        for event in keyevents:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
                game_framework.change_state(stage_state)
                return
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(stage_state)
                return

def draw():
    global titleimage, titleimage_kakao, titleimage_CI,title_logo_time
    clear_canvas()
    if (title_logo_time > 2.0):
        titleimage_kakao.draw(400, 300)
    elif (title_logo_time <= 2.0 and title_logo_time > 1.0):
        titleimage_CI.draw(400, 300)
    elif (title_logo_time <= 1.0 and title_logo_time >= 0.0):
        titleimage.draw(400, 300)
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