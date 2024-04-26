from class_file import*
# Function to toggle sound
pygame.mixer.init()
mixer.music.load('background2.wav')
mixer.music.play(-1)

# bullet
shoot_Sound = mixer.Sound('shoot.wav')
shoot2_Sound = mixer.Sound('shoot1.wav')
# explosion2
explosion_Sound = mixer.Sound('explosion.wav')
explosion2_Sound = mixer.Sound('explosion2.wav')
explosion3_Sound = mixer.Sound('explosion3.wav')
# die
die_sound = mixer.Sound('die.wav')
# levelup
levelup_Sound = mixer.Sound('levelup.wav')
# WinSound
Win_sound = mixer.Sound('WIN.wav')
# error
error_Sound = mixer.Sound('error.wav')
# transistion
transition = mixer.Sound('transition.wav')

# Main game loop starts here...
# game loop
def toggle_sound():
    global sound_on
    sound_on = not sound_on
# Function to play sound :
def play_sound(sound_file):
    if sound_on:
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)