
from numbers import Number
from re import S
from time import sleep
from turtle import position
import pygame
import random
import winsound
import math
from pygame import font, mixer
import sys
import time
import threading
from queue import PriorityQueue
from random import choice
from pygame.locals import *
from class_file import*
Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Cyan = (0, 255, 255)
Magenta = (255, 0, 255)
Orange = (255, 165, 0)
Purple = (128, 0, 128)
Pink = (255, 192, 203)
Brown = (165, 42, 42)
Teal = (0, 128, 128)
Navy = (0, 0, 128)
Olive = (128, 128, 0)
Lime = (0, 255, 0)
Maroon = (128, 0, 0)
Silver = (192, 192, 192)
Gold = (255, 215, 0)
pygame.display.init()
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
ImMenu = pygame.image.load('menubackground.jpg')
ImMenu = pygame.transform.scale(ImMenu, (screen_width, screen_height))
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.passed = False
        self.path = False
        self.thickness = 2

    def draw(self, sc, TILE):
        x, y = self.x * TILE, self.y * TILE

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x + TILE, y), self.thickness)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), self.thickness)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y + TILE), (x, y + TILE), self.thickness)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y + TILE), (x, y), self.thickness)

        if self.path:
            pygame.draw.rect(sc, pygame.Color('red'), (x +13 , y + 13, TILE - 25, TILE - 25))

    def get_rects(self, TILE):
        rects = []
        x, y = self.x * TILE, self.y * TILE
        if self.walls['top']:
            rects.append(pygame.Rect((x, y), (TILE, self.thickness)))
        if self.walls['right']:
            rects.append(pygame.Rect((x + TILE, y), (self.thickness, TILE)))
        if self.walls['bottom']:
            rects.append(pygame.Rect((x, y + TILE), (TILE, self.thickness)))
        if self.walls['left']:
            rects.append(pygame.Rect((x, y), (self.thickness, TILE)))
        return rects

    def check_cell(self, x, y, cols, rows):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return self.grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells, cols, rows):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1, cols, rows)
        right = self.check_cell(self.x + 1, self.y, cols, rows)
        bottom = self.check_cell(self.x, self.y + 1, cols, rows)
        left = self.check_cell(self.x - 1, self.y, cols, rows)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False

    def check_neighbors_pass(self, grid_cells, cols, rows):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1, cols, rows)
        right = self.check_cell(self.x + 1, self.y, cols, rows)
        bottom = self.check_cell(self.x, self.y + 1, cols, rows)
        left = self.check_cell(self.x - 1, self.y, cols, rows)
        if top and not self.walls['top']:
            neighbors.append(top)
        if right and not self.walls['right']:
            neighbors.append(right)
        if bottom and not self.walls['bottom']:
            neighbors.append(bottom)
        if left and not self.walls['left']:
            neighbors.append(left)
        return neighbors
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, sc, TILE):
        pygame.draw.rect(sc, pygame.Color('blue'), (self.x * TILE + 4, self.y * TILE + 4, TILE - 8, TILE - 8))    
    def move(self, direction, grid_cells, cols, rows):
        if direction == 'up' and self.y > 0:
            if not grid_cells[self.x + (self.y - 1) * cols].walls['bottom']:
                self.y -= 1
        elif direction == 'down' and self.y < rows - 1:
            if not grid_cells[self.x + (self.y + 1) * cols].walls['top']:
                self.y += 1
        elif direction == 'left' and self.x > 0:
            if not grid_cells[self.x - 1 + self.y * cols].walls['right']:
                self.x -= 1
        elif direction == 'right' and self.x < cols - 1:
            if not grid_cells[self.x + 1 + self.y * cols].walls['left']:
                self.x += 1
class MazeGameLoader:
    def __init__(self, width=800, height=600):
        self.WIDTH = width
        self.HEIGHT = height
        self.progress = 0
        self.bar_width, self.bar_height = 600, 30
        self.bar_x, self.bar_y = (self.WIDTH - self.bar_width) // 2, (self.HEIGHT - self.bar_height) // 2 + 50
        self.loading_tips = [
            "Tip 1: Don't forget to explore every corner of the maze!",
            "Tip 2: Some paths might seem blocked, but they could be shortcuts!",
            "Tip 3: Keep an eye out for hidden passages behind walls!",
            "Tip 4: If you're stuck, try retracing your steps to find a new route!",
            "Tip 5: Don't rush through the maze - take your time to solve it!"
        ]
        self.tip_timer = 0
        self.tip_delay = 2000
        self.current_tips = []
        self.angle = 0
        self.wave_amplitude = 5
        self.wave_frequency = 0.1
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Maze Game Loading")
        self.font = pygame.font.Font(None, 36)

    def run(self):
        running = True
        backgroundLoading = pygame.image.load('backgroundload.jpg')
        backgroundLoading = pygame.transform.scale(backgroundLoading, (screen_width, screen_height))
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(Black)
            self.screen.blit(backgroundLoading,(-80,-20))
            self.draw_progress_bar()
            self.render_text()
            self.update_loading_tips()
            self.draw_wave_animation()
            pygame.display.flip()
            self.progress += 0.2
            if self.progress >= 100:
                running = False
            pygame.time.delay(10)

        

    def draw_progress_bar(self):
        # Draw outer border
        outer_border_rect = pygame.Rect(self.bar_x - 2, self.bar_y - 2, self.bar_width + 4, self.bar_height + 4)
        pygame.draw.rect(self.screen, (255, 255, 255), outer_border_rect, 2)
        
        progress_width = int(self.progress / 100 * self.bar_width)
        color_gradient = (min(255, int(255 * (100 - self.progress) / 100)),
                          min(255, int(255 * self.progress / 100)), 200)
        pygame.draw.rect(self.screen, color_gradient, (self.bar_x, self.bar_y, progress_width, self.bar_height))

    def render_text(self):
        percentage_text = self.font.render(f"{int(self.progress)}%", True, (Black))
        text_rect = percentage_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 50))
        self.screen.blit(percentage_text, text_rect)
        dynamic_text = self.font.render("Loading Maze Game...", True, (255, 255, 255))
        dynamic_text_rect = dynamic_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))
        self.screen.blit(dynamic_text, dynamic_text_rect)
        for i, tip in enumerate(self.current_tips):
            tip_text = self.font.render(tip, True, (255, 255, 255))
            tip_text_rect = tip_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 100 + i * 40))
            self.screen.blit(tip_text, tip_text_rect)

    def update_loading_tips(self):
        if pygame.time.get_ticks() - self.tip_timer > self.tip_delay:
            self.tip_timer = pygame.time.get_ticks()
            self.current_tips = self.loading_tips[:int(self.progress / 20) + 1]

    def draw_wave_animation(self):
        wave_offset = self.wave_amplitude * math.sin(self.angle)
        progress_width = int(self.progress / 100 * self.bar_width)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.bar_x + progress_width - 5, self.bar_y - 5 + wave_offset, 5, self.bar_height + 10))
        self.angle += self.wave_frequency
# Define the TextProgress class
class TextProgress:
    def __init__(self, font, message, color, bgcolor):
        self.font = font
        self.message = message
        self.color = color
        self.bgcolor = bgcolor
        self.offcolor = [c^40 for c in color]
        self.notcolor = [c^0xFF for c in color]
        self.text = font.render(message, 0, (255, 0, 0), self.notcolor)
        self.text.set_colorkey(1)
        self.outline = self.textHollow(font, message, color)
        self.bar = pygame.Surface(self.text.get_size())
        self.bar.fill(self.offcolor)
        width, height = self.text.get_size()
        stripe = Rect(0, height/2, width, height/4)
        self.bar.fill(color, stripe)
        self.ratio = width / 100.0

    def textHollow(self, font, message, fontcolor):
        base = font.render(message, 0, fontcolor, self.notcolor)
        size = base.get_width() + 2, base.get_height() + 2
        img = pygame.Surface(size, 16)
        img.fill(self.notcolor)
        base.set_colorkey(0)
        img.blit(base, (0, 0))
        img.blit(base, (2, 0))
        img.blit(base, (0, 2))
        img.blit(base, (2, 2))
        base.set_colorkey(0)
        base.set_palette_at(1, self.notcolor)
        img.blit(base, (1, 1))
        img.set_colorkey(self.notcolor)
        return img

    def render(self, percent=50):
        surf = pygame.Surface(self.text.get_size())
        if percent < 100:
            surf.fill(self.bgcolor)
            surf.blit(self.bar, (0, 0), (0, 0, percent * self.ratio, 100))
        else:
            surf.fill(self.color)
        surf.blit(self.text, (0, 0))
        surf.blit(self.outline, (-1, -1))
        surf.set_colorkey(self.notcolor)
        return surf

# Function to draw the progress bar
def draw_progress_bar(screen, progress):
    # Create a TextProgress instance
    renderer = TextProgress(pygame.font.Font(None, 60), "EDIT BY DUY MINH", (255, 255, 255), (40, 40, 40))
    # Render the progress bar
    progress_bar = renderer.render(progress)
    # Draw the progress bar on the screen
    screen.blit(progress_bar, (0, 0))
    cnt = 0  # Khai báo biến cnt ở đầu chương trình