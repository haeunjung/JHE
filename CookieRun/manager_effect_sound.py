from pico2d import *

SoundList = {}

def load_effect_sound():
    global SoundList

    SoundList['BIG_HIT'] = load_wav('Sound/big_hit.wav')
    SoundList['BIG_HIT'].set_volume(64)
    SoundList['COLLISION'] = load_wav('Sound/collide.wav')
    SoundList['COLLISION'].set_volume(64)
    #사운드 추가로 더하기


def CallEffectSound(sound_name):
    global SoundList

    SoundList[sound_name].play()
