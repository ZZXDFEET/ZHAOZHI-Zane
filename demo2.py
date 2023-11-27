#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pygame


pygame.init()
pygame.mixer.init()

placing_sound = pygame.mixer.Sound("placing.mp3")
alarm_sound = pygame.mixer.Sound("alarm.mp3")


# Constants
WIDTH, HEIGHT = 600, 600
LINE_COLOR = (0, 0, 0)
BG_COLOR = (171, 171, 101)
CIRCLE_COLOR = (0, 0, 0)  # Black player
CROSS_COLOR = (255, 255, 230)  # White player
FONT = pygame.font.SysFont('Arial', 24)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('gomoku-COMP1002-777770-Julia')

input_x = ''
input_y = ''
waiting_for_input = False




def pick_difficulty():
    global board_size, CELL_SIZE, board
    difficulties = [(9, '9x9'), (11, '11x11'), (15, '15x15')]
    difficulty_texts = []
    difficulty_rects = []
    y_offset = 0

    # Create text surfaces and rectangles for difficulty levels
    for difficulty in difficulties:
        size_text = difficulty[1]
        text_surface = FONT.render(size_text, True, LINE_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
        difficulty_texts.append(text_surface)
        difficulty_rects.append(text_rect)
        y_offset += 50

    picking = True
    while picking:
        screen.fill(BG_COLOR)

        for i in range(len(difficulty_texts)):
            screen.blit(difficulty_texts[i], difficulty_rects[i].topleft)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i in range(len(difficulty_rects)):
                    if difficulty_rects[i].collidepoint(mouse_pos):
                        board_size = difficulties[i][0]
                        CELL_SIZE = WIDTH // board_size
                        board = [[0 for _ in range(board_size)] for _ in range(board_size)]
                        picking = False
                        break

def display_winner(winner):
    global game_over, step_count
    screen.fill(BG_COLOR)
    if winner == "draw":
        winner_text = FONT.render('Draw!', True, LINE_COLOR)
    else:
        winner_text = FONT.render(f'Player {winner} wins in {step_count} steps!', True, LINE_COLOR)
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))

    restart_text = FONT.render('Press R to restart', True, LINE_COLOR)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + winner_text.get_height()))

    pygame.display.update()

def draw_board():
    screen.fill(BG_COLOR)
    for x in range(0, WIDTH, CELL_SIZE):  # grid lines
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, LINE_COLOR, rect, 1)

    # Draw pieces
    for x in range(board_size):
        for y in range(board_size):
            center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
            if board[x][y] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, center, CELL_SIZE // 2 - 5)
            elif board[x][y] == 2:
                pygame.draw.circle(screen, CROSS_COLOR, center, CELL_SIZE // 2 - 5)

    input_text = FONT.render(f'X: {input_x} Y: {input_y}', True, LINE_COLOR)
    screen.blit(input_text, (WIDTH - 200, HEIGHT - 30))
    
def valid_move(x, y):
    return 0 <= x < board_size and 0 <= y < board_size and board[x][y] == 0

def move(player, x, y):
    if not valid_move(x, y):
        show_message(screen, "Invalid move!")
        alarm_sound.play()
        return False
    board[x][y] = player
    placing_sound.play()

    
    if capture_pieces(player, x, y):
        print("Captured opponent's pieces!") 

    return True


def check_result(player, x, y):
    # Check if the game has a win (horizontally, vertically, or diagonally) or draw

    # Horizontal check
    for x_start in range(board_size - 4):
        for y in range(board_size):
            if all(board[x_start + i][y] == player for i in range(5)):
                return player  # Return the winner

    # Vertical check
    for x in range(board_size):
        for y_start in range(board_size - 4):
            if all(board[x][y_start + i] == player for i in range(5)):
                return player

    # Left-to-right diagonal check
    for x_start in range(board_size - 4):
        for y_start in range(board_size - 4):
            if all(board[x_start + i][y_start + i] == player for i in range(5)):
                return player

    # Right-to-left diagonal check
    for x_start in range(4, board_size):
        for y_start in range(board_size - 4):
            if all(board[x_start - i][y_start + i] == player for i in range(5)):
                return player

    # Draw check
    if all(cell != 0 for row in board for cell in row):
        return "draw"

    return 0  # Game continues


def capture_pieces(player, x, y):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    opponent = 3 - player
    captured = False

    for dx, dy in directions:
        for dist in [1, -1]:  
            x1, y1 = x + dx * dist, y + dy * dist
            x2, y2 = x + dx * dist * 2, y + dy * dist * 2

            if (0 <= x1 < board_size and 0 <= y1 < board_size and
                0 <= x2 < board_size and 0 <= y2 < board_size and
                board[x1][y1] == opponent and board[x2][y2] == player):
                board[x1][y1] = 0 
                captured = True
                alarm_sound.play() 

    return captured


def show_message(screen, message):
    font = pygame.font.SysFont('Arial', 24)
    text_surface = font.render(message, True, (255, 255, 255)) 
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    
    background_rect = pygame.Rect(0, 0, 300, 100)
    background_rect.center = (WIDTH // 2, HEIGHT // 2)
    
    screen.fill((0, 0, 0, 128), background_rect)
    screen.blit(text_surface, text_rect)
    pygame.display.update(background_rect) 
    pygame.time.delay(2000)  




def game_loop():
    global current_player, game_over, step_count, board, CELL_SIZE, board_size, input_x, input_y, waiting_for_input
    pick_difficulty()  # Let the user pick the difficulty at the start
    running = True
    step_count = 0
    current_player = 1  # Reset the current player
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

                if move(current_player, grid_x, grid_y):
                    step_count += 1
                    result = check_result(current_player, grid_x, grid_y)
                    if result:
                        game_over = True
                        display_winner(current_player if result != "draw" else "draw")
                    current_player = 3 - current_player  # Switch player
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    game_over = False
                    step_count = 0
                    pick_difficulty()  # Let the user pick the difficulty after a restart
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_x and input_y:
                    try:
                        x = int(input_x) - 1
                        y = int(input_y) - 1
                        if move(current_player, x, y):
                            step_count += 1
                            result = check_result(current_player, x, y)
                            if result:
                                game_over = True
                                display_winner(current_player if result != "draw" else "draw")
                            current_player = 3 - current_player  # Switch player
                            input_x = ''
                            input_y = ''
                            waiting_for_input = False
                    except ValueError:
                        pass
                elif event.key == pygame.K_SPACE:
                    
                    if input_y:
                        input_y = ''
                        waiting_for_input = False
                    else:
                        
                        waiting_for_input = True
                elif event.key == pygame.K_BACKSPACE:
                    if waiting_for_input:
                        input_y = input_y[:-1]
                    else:
                        input_x = input_x[:-1]
                elif event.key == pygame.K_ESCAPE:
                    
                    input_x = ''
                    input_y = ''
                    waiting_for_input = False
                elif event.unicode.isdigit():
                    
                    if waiting_for_input:
                        input_y += event.unicode
                    else:
                        input_x += event.unicode   
                


        if not game_over:
            draw_board()
            pygame.display.flip()

    pygame.quit()

game_loop()


# In[ ]:





# In[ ]:




