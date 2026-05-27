import pygame
import sys
from enum import Enum

class State(Enum):# State of app
    Login   = 1
    Quiz    = 2
    Result  = 3
    
pygame.init()

screen_width = 1280
screen_height = 720

state = State.Login # Initial state of an App
login = ""          # Empty user login
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Space quiz")

font_large = pygame.font.SysFont(None, 64)
font_medium = pygame.font.SysFont(None, 40)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if state == State.Login:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if login.strip():
                        state = State.Quiz
                elif event.key == pygame.K_BACKSPACE:
                    login = login[:-1]
                else:
                    if len(login) < 20:
                        login += event.unicode

    match state:
        case State.Login:
            screen.fill((18,18,18))     
            title = font_large.render("Enter your name", True, (255, 255, 255))
            screen.blit(title, (screen_width // 2 - title.get_width() // 2, 200))

            box_rect = pygame.Rect(screen_width // 2 - 200, 320, 400, 60)
            pygame.draw.rect(screen, (60, 60, 60), box_rect, border_radius=8)
            pygame.draw.rect(screen, (180, 180, 255), box_rect, 2, border_radius=8)

            login_surf = font_medium.render(login, True, (255, 255, 255))
            screen.blit(login_surf, (box_rect.x + 16, box_rect.y + 14))

            hint = font_medium.render("Press Enter to continue", True, (120, 120, 120))
            screen.blit(hint, (screen_width // 2 - hint.get_width() // 2, 420))
        case State.Quiz:
            screen.fill((18,255,18))  

        case State.Result:
            screen.fill((18,18,255))    

            
            
    pygame.display.flip()

pygame.quit()
sys.exit()