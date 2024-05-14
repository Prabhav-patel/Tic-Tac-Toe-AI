import math
import sys

import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Initialize the board
board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Function to draw the grid lines
def draw_lines():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (row * SQUARE_SIZE, 0), (row * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Function to draw the figures (X and O)
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

# Function to check for a win
def check_win(player):
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            return True
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        return True
    if all(board[i][BOARD_ROWS-i-1] == player for i in range(BOARD_ROWS)):
        return True
    return False

# Function to check for a draw
def check_draw():
    return all(board[row][col] != ' ' for row in range(BOARD_ROWS) for col in range(BOARD_COLS))

# Function to evaluate the board
def evaluate():
    if check_win('X'):
        return 1
    elif check_win('O'):
        return -1
    else:
        return 0

# Minimax function with alpha-beta pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    score = evaluate()
    if score == 1:
        return score - depth
    if score == -1:
        return score + depth
    if check_draw():
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[row][col] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[row][col] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Function to find the best move for the AI
def find_best_move():
    best_move = None
    best_value = -math.inf
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                board[row][col] = 'X'
                move_value = minimax(board, 0, False, -math.inf, math.inf)
                board[row][col] = ' '
                if move_value > best_value:
                    best_value = move_value
                    best_move = (row, col)
    return best_move

# Function to mark the square
def mark_square(row, col, player):
    board[row][col] = player

# Function to check if the square is empty
def is_square_empty(row, col):
    return board[row][col] == ' '

# Main game loop
def main():
    draw_lines()
    player = 'O'  # Human player
    ai = 'X'  # AI player
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if is_square_empty(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    if check_win(player):
                        game_over = True
                    elif check_draw():
                        game_over = True
                    else:
                        player, ai = ai, player

                    draw_figures()

        if player == 'X' and not game_over:
            move = find_best_move()
            if move:
                mark_square(move[0], move[1], player)
                if check_win(player):
                    game_over = True
                elif check_draw():
                    game_over = True
                else:
                    player, ai = ai, player

                draw_figures()

        pygame.display.update()

if __name__ == '__main__':
    main()
