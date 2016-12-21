from pico2d import*

import manager_effect_sound

running = None
stack = None

def change_state(state):
    global stack
    pop_state()
    stack.append(state)
    state.enter()



def push_state(state):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(state)
    state.enter()



def pop_state():
    global stack
    if (len(stack) > 0):
        # execute the current state's exit function
        stack[-1].exit()
        # remove the current state
        stack.pop()

    # execute resume function of the previous state
    if (len(stack) > 0):
        stack[-1].resume()


def quit():
    global running
    running = False


def run(start_state):
    global running, stack
    running = True

    open_canvas()

    current_time = get_time()
    manager_effect_sound.load_effect_sound()

    stack = [start_state]
    start_state.enter()

    while (running):
        stack[-1].handle_events()

        frame_time = get_time() - current_time
        stack[-1].update(frame_time)
        current_time += frame_time

        stack[-1].draw()

        delay(0.02)

    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].exit()
        stack.pop()

    close_canvas()