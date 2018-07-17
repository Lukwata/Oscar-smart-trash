# -*- coding: utf-8 -*-
from aos.system.libs.audio_player import AudioPlayer


def get_speaker_hwindex():
    card_file = '/proc/asound/cards'
    speak_name1 = 'usb pnp sound device'
    speak_name2 = 'c-media usb headphone set'
    hwind = 0
    with open(card_file, 'r') as fp:
        while True:
            line = fp.readline()
            if line == '':
                break            
            if speak_name1 in line.lower():
                break
            if speak_name2 in line.lower():
                break
            line = fp.readline()
            if line == '':
                break
            hwind += 1
    return hwind


def get_speaker_name():
    card_file = '/proc/asound/cards'
    speak_name1 = 'usb pnp sound device'
    speak_name2 = 'c-media usb headphone set'
    hwind = 0
    speaker_name = ''
    with open(card_file, 'r') as fp:
        while True:
            line = fp.readline()
            if line == '':
                break            
            if speak_name1 in line.lower():
                speaker_name = 'Speaker'
                break
            if speak_name2 in line.lower():
                speaker_name = 'Headphone'
                break
            line = fp.readline()
            if line == '':
                break
            hwind += 1
    return speaker_name


def play_sound(path):
    audio_player = AudioPlayer()
    audio_player.play_sound_with_animation(path)
