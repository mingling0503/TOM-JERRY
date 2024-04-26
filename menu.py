from class_file import*
from global_variable import*
from sound import*

def draw_menu(current_option):
    screen_width = pygame.display.Info().current_w
    screen_height = pygame.display.Info().current_h
    ImMenu = pygame.image.load('menubackground.jpg')
    ImMenu = pygame.transform.scale(ImMenu, (screen_width, screen_height))

    global screen
    screen.fill(Black)
    screen.blit(ImMenu, (0, 0))
    title_font = pygame.font.Font('8-BIT WONDER.ttf', 60)
    option_font = pygame.font.Font('8-BIT WONDER.ttf', 32)
    title_text = title_font.render("MAZE GAME", True, Purple)
    screen.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 150))
    options = ["Start Game", "Toggle Sound", "Exit"]
    for i, option in enumerate(options):
        if i == current_option:
            rendered_text = option_font.render(option, True, Green)
        else:
            rendered_text = option_font.render(option, True, Yellow)
        screen.blit(rendered_text, (WIDTH / 2 - rendered_text.get_width() / 2, 300 + 50 * i))


def handle_menu_input(current_option):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            return current_option, False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current_option = (current_option - 1) % 3
            elif event.key == pygame.K_DOWN:
                current_option = (current_option + 1) % 3
            elif event.key == pygame.K_RETURN:
                return current_option, True
    return current_option, False

#Menu
def xulymenu():
    menu_option = 0
    in_menu = True
    while in_menu:
        menu_option, selected = handle_menu_input(menu_option)
        draw_menu(menu_option)
        pygame.display.update()
        if selected:
            if menu_option == 0:
                in_menu = False
            elif menu_option == 1:
                toggle_sound()
            elif menu_option == 2:
                pygame.quit()
                sys.exit()


    if menu_option == 0:
                mixer.music.stop()
                transition.play()
                sleep(1)
                mixer.music.load('background.wav')
                mixer.music.play(-1)
