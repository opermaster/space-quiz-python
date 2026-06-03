import pygame
import sys
from enum import Enum
from questions import *

score = 0

class State(Enum):# State of app
    Login   = 1
    Quiz    = 2
    Result  = 3
    Error   = 4   # If Failed to load questions

def print_question(screen, question, selected=None):
    screen.fill((18, 18, 18))

    W, H = screen.get_size()
    CARD_BOTTON_PADDING = 30
    CARD_H = 120
    CARD_MARGIN = 20
    CARD_Y = H - CARD_H - CARD_MARGIN - CARD_BOTTON_PADDING
    CARD_W = (W - CARD_MARGIN * 5) // 4

    font_question = pygame.font.SysFont(None, 48)
    font_answer   = pygame.font.SysFont(None, 32)

    question_area_w = W // 2 - 40 if question.image_path else W - 80

    words = question.text.split()
    lines, line = [], ""
    for word in words:
        test = line + (" " if line else "") + word
        if font_question.size(test)[0] <= question_area_w:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)

    y = 60
    for l in lines:
        surf = font_question.render(l, True, (255, 255, 255))
        screen.blit(surf, (60, y))
        y += surf.get_height() + 8

    if question.image_path:
        try:
            img = pygame.image.load("images/"+question.image_path).convert()
            img_area_w = W // 2 - 60
            img_area_h = CARD_Y - 40
            scale = min(img_area_w / img.get_width(), img_area_h / img.get_height())
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            img_x = W // 2 + 30
            img_y = 40
            screen.blit(img, (img_x, img_y))
        except:
            pass

    card_rects = []
    for i, answer in enumerate(question.answers):
        x = CARD_MARGIN + i * (CARD_W + CARD_MARGIN)

        if selected == i:
            color = (80, 200, 80) if answer.isCorrect else (200, 80, 80)
        else:
            color = (40, 40, 60)

        rect = pygame.Rect(x, CARD_Y, CARD_W, CARD_H)
        pygame.draw.rect(screen, color, rect, border_radius=12)
        pygame.draw.rect(screen, (120, 120, 180), rect, 2, border_radius=12)
        card_rects.append(rect)

        ans_words = answer.text.split()
        ans_lines, ans_line = [], ""
        for w in ans_words:
            test = ans_line + (" " if ans_line else "") + w
            if font_answer.size(test)[0] <= CARD_W - 20:
                ans_line = test
            else:
                if ans_line:
                    ans_lines.append(ans_line)
                ans_line = w
        if ans_line:
            ans_lines.append(ans_line)

        total_h = len(ans_lines) * (font_answer.get_height() + 4)
        ty = CARD_Y + (CARD_H - total_h) // 2
        for al in ans_lines:
            asurf = font_answer.render(al, True, (255, 255, 255))
            screen.blit(asurf, (x + (CARD_W - asurf.get_width()) // 2, ty))
            ty += font_answer.get_height() + 4

    return card_rects
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


questions = []

qn = 0               # Question index
file_error_msg = ""
error_msg = ""

try:
    questions = load_questions('questions.txt')
    for q in questions:
        q._print()
except FileNotFoundError:
    state = State.Error
    file_error_msg = font_large.render("Error: questions.txt not found", True, (255, 0, 0))
except ValueError as e:
    state = State.Error
    error_msg = font_large.render(f"Error: {e}", True, (255, 0, 0))
selected = None
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

        elif state == State.Quiz:
            if event.type == pygame.MOUSEBUTTONDOWN and selected is None:
                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(event.pos):
                        selected = i
                        is_correct = questions[qn].answers[i].isCorrect
                        if is_correct:
                            score = score + 1
                        print(f"Answer {i}: {'✓ Correct' if is_correct else '✗ Wrong'}")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and selected is not None:
                qn += 1
                selected = None
                if qn >= len(questions):
                    state = State.Result
    
        
    match state:
        case State.Login:
            screen.fill((18,18,18))     

            if error_msg =="" and file_error_msg =="":
                succes_text = font_medium.render("Question succesfuly loaded!", True, (0, 255, 0))
                screen.blit(succes_text, (screen_width // 2 - succes_text.get_width() // 2, 500))

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
            card_rects = print_question(screen, questions[qn], selected)
            if selected is not None:
                hint = pygame.font.SysFont(None, 32).render("Press SPACE for next question", True, (160, 160, 160))
                screen.blit(hint, (screen.get_width() // 2 - hint.get_width() // 2, screen.get_height() - 30))

        case State.Result:
            screen.fill((18,18,18)) 
            _range = len(questions) // 3

            if score >= _range * 2:
                result_surf_color = (80, 200, 80)    # Green
            elif score >= _range:
                result_surf_color = (255, 165, 0)    # Orange
            else:
                result_surf_color = (200, 80, 80)    # Red

            result_surf = font_large.render(f"{login}, you got {score}/{len(questions)}", True, result_surf_color)
            screen.blit(result_surf, (box_rect.x + 16, box_rect.y + 14))

        case State.Error:
            screen.fill((18,18,18))     
            if error_msg !="":
                screen.blit(error_msg, (screen_width // 2 - error_msg.get_width() // 2, screen_height //2))
            if file_error_msg !="":
                screen.blit(file_error_msg, (screen_width // 2 - file_error_msg.get_width() // 2, screen_height //2))
            
            
    pygame.display.flip()

pygame.quit()
sys.exit()