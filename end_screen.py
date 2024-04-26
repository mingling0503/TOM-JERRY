from global_variable import*
def Is_game_over():
    global time,score ,record, FPS 
    if time < 0 : 
        pygame.time.wait(600)
        time, score, FPS = 60,0,60 
def game_win_text():
     win_text = win_font.render('YOU WIN',True,(White))
     screen.blit(win_text,((WIDTH/2)-200,(HEIGHT/2)-50))
def game_over_text():
    over_text =over_font.render("GAME OVER",True,(White))
    screen.blit(over_text,((WIDTH/2)-200,(HEIGHT/2)-50))


