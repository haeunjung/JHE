from pico2d import *

SoundList = {}

def load_effect_sound():
    global SoundList

    SoundList['BIG_HIT'] = load_wav('Sound/big_hit.wav')
    SoundList['BIG_HIT'].set_volume(32)
    SoundList['COLLISION'] = load_wav('Sound/collide.wav')
    SoundList['COLLISION'].set_volume(32)
    SoundList['END'] = load_wav('Sound/g_end.wav')
    SoundList['END'].set_volume(32)
    SoundList['JUMP'] = load_wav('Sound/g_giantjump.wav')
    SoundList['JUMP'].set_volume(32)
    SoundList['LAND'] = load_wav('Sound/g_giantland.wav')
    SoundList['LAND'].set_volume(32)
    SoundList['JELLY'] = load_wav('Sound/g_jelly.wav')
    SoundList['JELLY'].set_volume(32)
    SoundList['BIG'] = load_wav('Sound/i_giant.wav')
    SoundList['BIG'].set_volume(32)
    SoundList['LARGE_JELLY'] = load_wav('Sound/i_large_energy.wav')
    SoundList['LARGE_JELLY'].set_volume(32)

def CallEffectSound(sound_name):
    global SoundList

    SoundList[sound_name].play()
