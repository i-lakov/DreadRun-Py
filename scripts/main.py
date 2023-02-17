import pygame
import sys
import time
from settings import *
from player import Player
from level import Level
from score import Score

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    level = Level(screen)

    # sprites/images
    background_image = pygame.transform.scale(pygame.image.load('assets/bg/BG.png').convert(), (screen_width, screen_height))
    background_image_transp = pygame.transform.scale(pygame.image.load('assets/bg/bg_transp.png').convert_alpha(), (screen_width, screen_height))
    bullet = pygame.transform.scale(pygame.image.load('assets/hud/bullet.png').convert_alpha(), (30, 30))
    heart = pygame.transform.scale(pygame.image.load('assets/hud/heart.png').convert_alpha(), (30, 30))

    # game states
    game_running = False
    game_startscreen = True
    game_paused = False

    file = open("highscore.txt", "r")
    highscore = int(file.read())
    file.close()

    # game loop
    while True:
        mouse = pygame.mouse.get_pos()

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and game_running:
                    game_running = False
                    game_startscreen = False
                    game_paused = True
            if event.type == pygame.MOUSEBUTTONUP:
                if not Player.is_alive: # death screen quitting
                    pygame.quit()
                    sys.exit()
                if screen_width/3 <= mouse[0] <= 2*screen_width/3:
                    if screen_height/2.5 <= mouse[1] <= screen_height/2.5 + screen_height/10:
                        game_startscreen = False
                        game_paused = False
                        game_running = True
                    elif screen_height/1.8 <= mouse[1] <= screen_height/1.8 + screen_height/10:
                        pygame.quit()
                        sys.exit()

        # state handling
        if game_running:
            if Player.is_alive:
                score_text_font = title_font = pygame.font.SysFont("arialblack", 46)
                score_text = score_text_font.render(str(int(Score.calculated_score)), True, "black")
                screen.blit(background_image, (0, 0))
                screen.blit(score_text, (20, 10))
                level.draw()

                # HUD
                match Player.health:
                    case 3:
                        screen.blit(heart, (20, 80))
                        screen.blit(heart, (60, 80))
                        screen.blit(heart, (100, 80))
                    case 2:
                        screen.blit(heart, (20, 80))
                        screen.blit(heart, (60, 80))
                    case 1:
                        screen.blit(heart, (20, 80))

                match Player.bullets:
                    case 3:
                        screen.blit(bullet, (20, 120))
                        screen.blit(bullet, (60, 120))
                        screen.blit(bullet, (100, 120))
                    case 2:
                        screen.blit(bullet, (20, 120))
                        screen.blit(bullet, (60, 120))
                    case 1:
                        screen.blit(bullet, (20, 120))               
            else:   # death splash screen
                time.sleep(death_screen_delay)  # wait 1 second before dying
                screen.fill("red")  # red for being humiliated
                title_font = pygame.font.SysFont("arialblack", 74)
                title = title_font.render("DreadRun", True, "white")
                dead_font = pygame.font.SysFont("arial", 58)
                dead_text = dead_font.render("You've died, sucker.", True, "white")
                quit_text = dead_font.render("Press anywhere to finally quit.", True, "white")

                screen.blit(title, (screen_width/3, screen_height/5))
                screen.blit(dead_text, (screen_width/3.1, screen_height/3))
                screen.blit(quit_text, (screen_width/4.1, screen_height/1.5))

        elif game_startscreen:
            # setup fonts
            screen.fill("gray")
            title_font = pygame.font.SysFont("arialblack", 74)
            title = title_font.render("DreadRun", True, "white")
            button_font = pygame.font.SysFont("arial", 58)
            highscore_text_font = title_font = pygame.font.SysFont("arial", 32)
            highscore_text = highscore_text_font.render("Highscore: " + str(highscore), True, "white")

            # render buttons with hover effect
            if screen_width/3 <= mouse[0] <= 2*screen_width/3 and screen_height/2.5 <= mouse[1] <= screen_height/2.5 + screen_height/10:
                pygame.draw.rect(screen, "cyan", [screen_width/3, screen_height/2.5, screen_width/3, screen_height/10], border_radius=15)
                pygame.draw.rect(screen, "darkcyan", [screen_width/3, screen_height/1.8, screen_width/3, screen_height/10], border_radius=15)
                buttonA = button_font.render("Start", True, "black")
                buttonB = button_font.render("Quit", True, "white")
            elif screen_width/3 <= mouse[0] <= 2*screen_width/3 and screen_height/1.8 <= mouse[1] <= screen_height/1.8 + screen_height/10:
                pygame.draw.rect(screen, "darkcyan", [screen_width/3, screen_height/2.5, screen_width/3, screen_height/10], border_radius=15)
                pygame.draw.rect(screen, "cyan", [screen_width/3, screen_height/1.8, screen_width/3, screen_height/10], border_radius=15)
                buttonA = button_font.render("Start", True, "white")
                buttonB = button_font.render("Quit", True, "black")
            else:
                pygame.draw.rect(screen, "darkcyan", [screen_width/3, screen_height/2.5, screen_width/3, screen_height/10], border_radius=15)
                pygame.draw.rect(screen, "darkcyan", [screen_width/3, screen_height/1.8, screen_width/3, screen_height/10], border_radius=15)
                buttonA = button_font.render("Start", True, "white")
                buttonB = button_font.render("Quit", True, "white")

            # render texts
            screen.blit(title, (screen_width/3, screen_height/5))
            screen.blit(buttonA, (screen_width/2.2, screen_height/2.5))
            screen.blit(buttonB, (screen_width/2.18, screen_height/1.8))
            screen.blit(highscore_text, (screen_width/2.3, screen_height/1.1))

        elif game_paused:
            # setup fonts
            screen.fill("black")
            screen.blit(background_image_transp, (0, 0))
            title_font = pygame.font.SysFont("arialblack", 74)
            title = title_font.render("  Paused ", True, "white")
            button_font = pygame.font.SysFont("arial", 58)
            score_text_font = title_font = pygame.font.SysFont("arialblack", 46)
            score_text = score_text_font.render(str(int(Score.calculated_score)), True, "black")

            # render buttons with hover effect
            if screen_width/3 <= mouse[0] <= 2*screen_width/3 and screen_height/2.5 <= mouse[1] <= screen_height/2.5 + screen_height/10:
                pygame.draw.rect(screen, "cyan", [screen_width/3, screen_height/2.5, screen_width/3, screen_height/10], border_radius=15)
                pygame.draw.rect(screen, "darkcyan", [screen_width/3, screen_height/1.8, screen_width/3, screen_height/10], border_radius=15)
                buttonA = button_font.render("Continue", True, "black")
                buttonB = button_font.render("Quit", True, "white")
            elif screen_width/3 <= mouse[0] <= 2*screen_width/3 and screen_height/1.8 <= mouse[1] <= screen_height/1.8 + screen_height/10:
                pygame.draw.rect(screen, "darkcyan", [screen_width/3, screen_height/2.5, screen_width/3, screen_height/10], border_radius=15)
                pygame.draw.rect(screen, "cyan", [screen_width/3, screen_height/1.8, screen_width/3, screen_height/10], border_radius=15)
                buttonA = button_font.render("Continue", True, "white")
                buttonB = button_font.render("Quit", True, "black")
            else:
                pygame.draw.rect(screen, "darkcyan", [screen_width/3, screen_height/2.5, screen_width/3, screen_height/10], border_radius=15)
                pygame.draw.rect(screen, "darkcyan", [screen_width/3, screen_height/1.8, screen_width/3, screen_height/10], border_radius=15)
                buttonA = button_font.render("Continue", True, "white")
                buttonB = button_font.render("Quit", True, "white")

            # render texts
            screen.blit(title, (screen_width/3, screen_height/5))
            screen.blit(buttonA, (screen_width/2.35, screen_height/2.5))
            screen.blit(buttonB, (screen_width/2.18, screen_height/1.8))
            screen.blit(score_text, (20, 20))

        pygame.display.flip()
        clock.tick(60)