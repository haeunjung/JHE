from pico2d import*

import game_framework
import title_state

start_image = None

keyevents = None
start_logo_time = 1.0


def enter():
    global start_image, start_logo_time
    start_image = load_image('Image\\kpu_credit.png')
    start_logo_time = 1.0

def exit():
    global start_image
    del(start_image)



def update():
    global start_logo_time

    if(start_logo_time < 0.0):
        start_logo_time = 1.0
        game_framework.change_state(title_state)

    start_logo_time -= 0.01

def draw():
    global start_image
    clear_canvas()
    start_image.draw(400, 300)
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