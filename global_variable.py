import pygame
from class_file  import*
sound_on = True
FPS = 60 
clock = pygame.time.Clock()

pygame.font.init()
time = 60
score = 0
RES = WIDTH, HEIGHT = 902, 602
# create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# background
background = pygame.image.load('background.png')

# Sound


# Ready - You can't see the bullet on the screen


# Score :
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
# Game Winner Text :
win_font = pygame.font.Font('freesansbold.ttf', 60)
# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 60)
diesound_times = 0

screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
ImMenu = pygame.image.load('menubackground.jpg')
ImMenu = pygame.transform.scale(ImMenu, (screen_width, screen_height))