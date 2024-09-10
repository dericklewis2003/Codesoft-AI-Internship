import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 500
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = 100
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (240, 240, 240)
LINE_COLOR = (50, 50, 50)
CIRCLE_COLOR = (220, 20, 60)  # Crimson red for O
CROSS_COLOR = (66, 66, 66)  # Dark gray for X
BUTTON_COLOR = (52, 152, 219)
BUTTON_HOVER_COLOR = (41, 128, 185)
TEXT_COLOR = (50, 50, 50)
SCORE_BG_COLOR = (220, 220, 220)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

# Board
board = [' ' for _ in range(9)]

# Players
HUMAN = 'X'
AI = 'O'

# Fonts
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)
title_font = pygame.font.Font(None, 48)

# Scores
human_score = 0
ai_score = 0
games_played = 0

# Difficulty
difficulty = "medium"

def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (50, 150), (350, 150), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (50, 250), (350, 250), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (150, 50), (150, 350), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (250, 50), (250, 350), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row * 3 + col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2 + 50), int(row * SQUARE_SIZE + SQUARE_SIZE // 2 + 50)), CIRCLE_RADIUS, CIRCLE_WIDTH)
                # Add an inner circle to make 'O' more distinct
                pygame.draw.circle(screen, BG_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2 + 50), int(row * SQUARE_SIZE + SQUARE_SIZE // 2 + 50)), CIRCLE_RADIUS - CIRCLE_WIDTH)
            elif board[row * 3 + col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE + 50, row * SQUARE_SIZE + SQUARE_SIZE - SPACE + 50), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE + 50, row * SQUARE_SIZE + SPACE + 50), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE + 50, row * SQUARE_SIZE + SPACE + 50), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE + 50, row * SQUARE_SIZE + SQUARE_SIZE - SPACE + 50), CROSS_WIDTH)

def is_winner(board, player):
    # Check rows, columns and diagonals
    for i in range(3):
        if board[i*3] == board[i*3+1] == board[i*3+2] == player: return True
        if board[i] == board[i+3] == board[i+6] == player: return True
    if board[0] == board[4] == board[8] == player: return True
    if board[2] == board[4] == board[6] == player: return True
    return False

def is_board_full(board):
    return ' ' not in board

def get_empty_cells(board):
    return [i for i, cell in enumerate(board) if cell == ' ']

def minimax(board, depth, is_maximizing):
    if is_winner(board, AI):
        return 1
    if is_winner(board, HUMAN):
        return -1
    if is_board_full(board):
        return 0
    
    if is_maximizing:
        best_score = -math.inf
        for move in get_empty_cells(board):
            board[move] = AI
            score = minimax(board, depth + 1, False)
            board[move] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in get_empty_cells(board):
            board[move] = HUMAN
            score = minimax(board, depth + 1, True)
            board[move] = ' '
            best_score = min(score, best_score)
        return best_score

def get_best_move(board, difficulty):
    if difficulty == "easy":
        return random.choice(get_empty_cells(board))
    elif difficulty == "medium":
        if random.random() < 0.5:
            return random.choice(get_empty_cells(board))
        else:
            return get_best_move(board, "hard")
    else:  # hard
        best_score = -math.inf
        best_move = None
        for move in get_empty_cells(board):
            board[move] = AI
            score = minimax(board, 0, False)
            board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))

    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)

def start_game():
    global board, games_played
    board = [' ' for _ in range(9)]
    games_played += 1
    game_loop()

def set_difficulty(diff):
    global difficulty, human_score, ai_score, games_played
    difficulty = diff
    human_score = 0
    ai_score = 0
    games_played = 0
    start_game()

def quit_game():
    pygame.quit()
    sys.exit()

def home_screen():
    global human_score, ai_score, games_played
    human_score = 0
    ai_score = 0
    games_played = 0
    while True:
        screen.fill(BG_COLOR)
        title = title_font.render("Tic Tac Toe", True, TEXT_COLOR)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        draw_button("Easy", 100, 150, 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: set_difficulty("easy"))
        draw_button("Medium", 100, 220, 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: set_difficulty("medium"))
        draw_button("Hard", 100, 290, 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: set_difficulty("hard"))
        draw_button("Quit", 100, 360, 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR, quit_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def game_loop():
    global human_score, ai_score, games_played
    game_over = False
    
    while True:
        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures()

        # Draw scores and labels
        pygame.draw.rect(screen, SCORE_BG_COLOR, (0, 370, WIDTH, 80))
        human_text = small_font.render("Human:", True, TEXT_COLOR)
        ai_text = small_font.render("AI:", True, TEXT_COLOR)
        human_score_text = font.render(str(human_score), True, TEXT_COLOR)
        ai_score_text = font.render(str(ai_score), True, TEXT_COLOR)
        games_text = small_font.render(f"Game {games_played}", True, TEXT_COLOR)
        
        screen.blit(human_text, (20, 380))
        screen.blit(human_score_text, (90, 380))
        screen.blit(ai_text, (WIDTH - 100, 380))
        screen.blit(ai_score_text, (WIDTH - 30, 380))
        screen.blit(games_text, (WIDTH//2 - games_text.get_width()//2, 380))

        draw_button("Quit", WIDTH - 100, HEIGHT - 50, 80, 40, BUTTON_COLOR, BUTTON_HOVER_COLOR, home_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] - 50
                mouseY = event.pos[1] - 50
                
                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)
                
                if 0 <= clicked_row < 3 and 0 <= clicked_col < 3 and board[clicked_row * 3 + clicked_col] == ' ':
                    board[clicked_row * 3 + clicked_col] = HUMAN
                    
                    if is_winner(board, HUMAN):
                        print("You win!")
                        human_score += 1
                        game_over = True
                    elif is_board_full(board):
                        print("It's a tie!")
                        game_over = True
                    else:
                        # AI's turn
                        ai_move = get_best_move(board, difficulty)
                        board[ai_move] = AI
                        
                        if is_winner(board, AI):
                            print("AI wins!")
                            ai_score += 1
                            game_over = True
                        elif is_board_full(board):
                            print("It's a tie!")
                            game_over = True

        if game_over:
            if human_score == 3 or ai_score == 3:
                winner_text = "Human wins the series!" if human_score > ai_score else "AI wins the series!"
                winner_surface = font.render(winner_text, True, TEXT_COLOR)
                screen.blit(winner_surface, (WIDTH//2 - winner_surface.get_width()//2, 420))
                draw_button("New Series", 20, HEIGHT - 50, 180, 40, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: set_difficulty(difficulty))
            else:
                draw_button("Next Game", 20, HEIGHT - 50, 180, 40, BUTTON_COLOR, BUTTON_HOVER_COLOR, start_game)
        
        pygame.display.update()

if __name__ == "__main__":
    home_screen()