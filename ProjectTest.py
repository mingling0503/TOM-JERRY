from class_file import*
from algorithms import *
from global_variable import*
from sound import*
from menu import*
from end_screen import*
from maze_generator import*
# Initialize pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.time.set_timer(pygame.USEREVENT, 1000)

Mode_Findpath = 2
Mode_Game = 1  
def main():
    TILE = 30
    global Mode_Findpath
    global cnt  # Sử dụng global để truy cập biến cnt trong hàm main
    global Mode_Game
    pygame.init()
    sc = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()
    Daisize, RongSize = 20, 20
    grid_cells = generate_maze(Daisize, RongSize, TILE)
    start = grid_cells[0]
    end = grid_cells[-1]
    player = Player(start.x, start.y)
    position = []
    path = None
    time = 60
    while True:
        player_index = player.x + player.y * Daisize
        target_cell = grid_cells[player_index]
        if target_cell == end:
            Win_sound.play()
            game_win_text()
            pygame.display.update()  # Make sure the message is displayed
            pygame.time.delay(3000)  # Delay for 3 seconds (adjust as needed)
            xulymenu()  # Return to menu after displaying the message
            """
            progress = 1
            finished = False
            while not finished:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        finished = True
                # Update progress
                progress += 1  # Update progress however you want
                # Draw everything
            screen.fill((0, 0, 0))  # Fill the screen with black
            draw_progress_bar(screen, progress)  # Draw the progress bar
            """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.USEREVENT  : 
                time -=1
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
                    if (Mode_Game == 1):
                        if(path):
                            for cell in path:
                                player.x = cell.x 
                                player.y = cell.y
                                
                                print(player.x,player.y)
                                screen.blit(background,(0,0))
                                [cell.draw(sc, TILE) for cell in grid_cells]
                                player.draw(sc, TILE)
                                pygame.display.flip()
                                pygame.display.update()
                                clock.tick(60)
                                pygame.time.delay(50)
                                
                    else:
                        Mode_Game = 2 
                elif event.key == pygame.K_q:
                    if (Mode_Findpath == 1):
                        Mode_Findpath = 2
                    elif (Mode_Findpath == 2):
                        Mode_Findpath = 1
                    print(Mode_Findpath)
                elif event.key == pygame.K_SPACE:  # Toggle path display with spacebar

                    if len(position) == 0:
                        if (Mode_Findpath == 1):
                            path = DFS_findPath(grid_cells, target_cell, end, Daisize, RongSize)
                        elif (Mode_Findpath == 2):
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
        #Backgrou
        sc.fill(pygame.Color('aquamarine'))
        
        # RGB = Red, Green ,Blue        
        screen.fill(Black)
        background = pygame.image.load('background3.jpg')
        background= pygame.transform.scale(background, (WIDTH, HEIGHT))
        #background image 
        screen.blit(background,(0,0))
        [cell.draw(sc, TILE) for cell in grid_cells]
        #Draw player
        player.draw(sc, TILE)
        #draw stats 
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)
if __name__ == "__main__":
    xulymenu()
    #maze_game_loader = MazeGameLoader()
    #maze_game_loader.run()
    main()

  