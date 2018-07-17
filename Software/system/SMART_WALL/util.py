from aos.system.libs.audio_player import AudioPlayer


def get_speaker_hwindex():
    card_file = '/proc/asound/cards'
    speak_name = 'bcm2835 alsa'
    hwind = 0
    with open(card_file, 'r') as fp:
        while True:
            line = fp.readline()
            if line == '':
                break
            if speak_name in line.lower():
                break
            line = fp.readline()
            if line == '':
                break
            hwind += 1
    return hwind

def get_speaker_name():
    return "PCM"

def play_sound(path):
    audio_player = AudioPlayer()
    audio_player.play_sound(path)
