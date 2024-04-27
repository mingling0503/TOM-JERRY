import pygame
from class_file import *
from algorithms import *
from global_variable import *
from sound import *
from menu import *
from end_screen import *
from maze_generator import *

# Định nghĩa biến font
pygame.font.init()
font = pygame.font.Font(None, 36)

pygame.init()
pygame.mixer.init()
pygame.time.set_timer(pygame.USEREVENT, 1000)

Mode_Findpath = 2
Mode_Game = 1
paused = False
surface = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
DarkGray = (128, 128, 128)
White = (255, 255, 255)
Black = (0, 0, 0)

def pause_screen(screen):
    # Hiển thị màn hình tạm dừng
    pygame.draw.rect(surface, (128, 128, 128, 2), [0, 0, WIDTH, HEIGHT])
    pygame.draw.rect(surface, DarkGray, [200, 150, 600, 50], 0, 10)
    reset = pygame.draw.rect(surface, White, [200, 220, 280, 50], 0, 10)
    save = pygame.draw.rect(surface, White, [520, 220, 280, 50], 0, 10)
    surface.blit(font.render('Game Paused: Escape to Resume', True, Black), (220, 160))
    surface.blit(font.render('Restart', True, Black), (220, 230))
    surface.blit(font.render('Save', True, Black), (540, 230))
    screen.blit(surface, (0, 0))
    pygame.display.update()

def reset_game(grid_cells):
    # Thiết lập lại trạng thái trò chơi về trạng thái ban đầu
    for cell in grid_cells:
        cell.path = False
    return grid_cells

def continue_game():
    # Tiếp tục trò chơi
    global paused
    paused = False
def select_start_end_manually(grid_cells, cols, rows, TILE,sc):
    start_color = (0, 255, 0)  # Green
    end_color = (255, 0, 0)  # Red
    bright_color = (255, 255, 0)  # Yellow

    start_selected = False
    end_selected = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // TILE
                row = mouse_pos[1] // TILE
                index = col + row * cols
                cell = grid_cells[index]

                if not start_selected:
                    start_selected = True
                    start_cell = cell
                    pygame.draw.rect(sc, Black, (start_cell.x * TILE + 4, start_cell.y * TILE + 4, TILE - 8, TILE - 8))
                elif not end_selected:
                    if cell != start_cell:
                        end_selected = True
                        end_cell = cell
                        pygame.draw.rect(sc, Green, (end_cell.x * TILE + 4, end_cell.y * TILE + 4, TILE - 8, TILE - 8))
                        pygame.time.delay(400)
                        
                
        pygame.display.update()

        if start_selected and end_selected:
            return start_cell, end_cell


def main():
    TILE = 30
    global Mode_Findpath
    global Mode_Game
    global paused

    sc = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()
    Daisize, RongSize = 20, 20
    grid_cells = generate_maze(Daisize, RongSize, TILE)
    sc.fill(pygame.Color('aquamarine'))
    screen.fill(Black)
    background = pygame.image.load('background3.jpg')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    [cell.draw(sc, TILE) for cell in grid_cells]
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
    
    # Chọn điểm bắt đầu và điểm kết thúc thủ công
    start, end = select_start_end_manually(grid_cells, Daisize, RongSize, TILE,sc)

    player = Player(start.x, start.y)
    position = []
    path = None
    time = 60
    player.draw(sc, TILE)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

    while True:
        player_index = player.x + player.y * Daisize
        target_cell = grid_cells[player_index]

        if target_cell == end:
            Win_sound.play()
            game_win_text()
            pygame.display.update()
            pygame.time.delay(3000)
            xulymenu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.USEREVENT:
                time -= 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move('up', grid_cells, Daisize, RongSize)
                elif event.key == pygame.K_DOWN:
                    player.move('down', grid_cells, Daisize, RongSize)
                elif event.key == pygame.K_LEFT:
                    player.move('left', grid_cells, Daisize, RongSize)
                elif event.key == pygame.K_RIGHT:
                    player.move('right', grid_cells, Daisize, RongSize)
                elif event.key == pygame.K_w:
                    if Mode_Game == 1:
                        if path:
                            for cell in path:
                                player.x = cell.x
                                player.y = cell.y
                                screen.blit(background, (0, 0))
                                [cell.draw(sc, TILE) for cell in grid_cells]
                                player.draw(sc, TILE)
                                pygame.display.flip()
                                pygame.display.update()
                                clock.tick(60)
                                pygame.time.delay(50)
                    else:
                        Mode_Game = 2
                elif event.key == pygame.K_q:
                    if Mode_Findpath == 1:
                        Mode_Findpath = 2
                    elif Mode_Findpath == 2:
                        Mode_Findpath = 1
                    print(Mode_Findpath)
                elif event.key == pygame.K_SPACE:
                    if len(position) == 0:
                        if Mode_Findpath == 1:
                            path = DFS_findPath(grid_cells, target_cell, end, Daisize, RongSize)
                        elif Mode_Findpath == 2:
                            path = BFS_findPath(grid_cells, target_cell, end, Daisize, RongSize)
                        if path:
                            for cell in path:
                                cell.path = True
                            position.append(target_cell)
                    elif position[-1] == target_cell:
                        if path:
                            for cell in path:
                                cell.path = False
                    else:
                        if path:
                            for cell in path:
                                cell.path = False
                            position = []

                # Phím bổ sung để tạm dừng, thiết lập lại, tiếp tục
                elif event.key == pygame.K_p:  # Tạm dừng trò chơi
                    paused = not paused
                elif event.key == pygame.K_r:  # Thiết lập lại trò chơi
                    grid_cells = reset_game(grid_cells)
                    paused = False
                elif event.key == pygame.K_c:  # Tiếp tục trò chơi
                    continue_game()

        if paused:
            pause_screen(sc)
            continue  # Bỏ qua phần còn lại của vòng lặp nếu tạm dừng

        sc.fill(pygame.Color('aquamarine'))
        screen.fill(Black)
        screen.blit(background, (0, 0))
        [cell.draw(sc, TILE) for cell in grid_cells]
        player.draw(sc, TILE)
        pygame.draw.rect(sc, Black, (start.x * TILE + 4, start.y * TILE + 4, TILE - 8, TILE - 8))
        pygame.draw.rect(sc,Green, (end.x * TILE + 4, end.y * TILE + 4, TILE - 8, TILE - 8))
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)

screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h

if __name__ == "__main__":
    xulymenu()
    mazeloader = MazeGameLoader(screen_width, screen_height)
    main()
