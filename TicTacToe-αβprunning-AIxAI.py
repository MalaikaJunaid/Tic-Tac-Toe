"""
###AI Computer 1 vs AI Computer 2
"""

import random
import math

def print_board(board):
    print("   A   B   C   D")
    for i in range(4):
        print(str(i + 1) + "  " + " | ".join(board[i]))

def check_winner(board, player):
    for i in range(4):
        if all(board[i][j] == player for j in range(4)) or all(board[j][i] == player for j in range(4)):
            return True
    if all(board[i][i] == player for i in range(4)) or all(board[i][3 - i] == player for i in range(4)):
        return True
    return False

def available_moves(board):
    return [(i, j) for i in range(4) for j in range(4) if board[i][j] == ' ']

def evaluate_defensive(board, player):
    player_map = {'●': -1, '■': 1, ' ': 0}
    score = 0
    for i in range(4):
        row_values = [player_map[board[i][j]] for j in range(4)]
        col_values = [player_map[board[j][i]] for j in range(4)]
        score += row_values.count(player_map[player]) + col_values.count(player_map[player])
    diag1 = [player_map[board[i][i]] for i in range(4)]
    diag2 = [player_map[board[i][3 - i]] for i in range(4)]
    score += diag1.count(player_map[player]) + diag2.count(player_map[player])
    return score

def evaluate_offensive(board, player):
    player_map = {'●': -1, '■': 1, ' ': 0}
    score = 0
    for i in range(4):
        row_values = [player_map[board[i][j]] for j in range(4)]
        col_values = [player_map[board[j][i]] for j in range(4)]
        score += row_values.count(player_map[player]) + col_values.count(player_map[player])
    diag1 = [player_map[board[i][i]] for i in range(4)]
    diag2 = [player_map[board[i][3 - i]] for i in range(4)]
    score += diag1.count(player_map[player]) + diag2.count(player_map[player])
    return score

def alpha_beta_defensive(board, depth, alpha, beta, maximizing_player, player):
    if depth == 0 or check_winner(board, '●') or check_winner(board, '■'):
        return evaluate_defensive(board, player)

    if maximizing_player:
        max_eval = float('-inf')
        for move in available_moves(board):
            board[move[0]][move[1]] = '●'
            eval = alpha_beta_defensive(board, depth - 1, alpha, beta, False, player)
            board[move[0]][move[1]] = ' '
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in available_moves(board):
            board[move[0]][move[1]] = '■'
            eval = alpha_beta_defensive(board, depth - 1, alpha, beta, True, player)
            board[move[0]][move[1]] = ' '
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def alpha_beta_offensive(board, depth, alpha, beta, maximizing_player, player):
    if depth == 0 or check_winner(board, '●') or check_winner(board, '■'):
        return evaluate_offensive(board, player)

    if maximizing_player:
        max_eval = float('-inf')
        for move in available_moves(board):
            board[move[0]][move[1]] = '■'
            eval = alpha_beta_offensive(board, depth - 1, alpha, beta, False, player)
            board[move[0]][move[1]] = ' '
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in available_moves(board):
            board[move[0]][move[1]] = '●'
            eval = alpha_beta_offensive(board, depth - 1, alpha, beta, True, player)
            board[move[0]][move[1]] = ' '
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def defensive_computer_turn(board, player):
    best_val = -float('inf')
    best_move = None
    block_move = None
    for move in available_moves(board):
        board[move[0]][move[1]] = player
        if check_winner(board, player):
            board[move[0]][move[1]] = ' '
            return
        opponent = '●' if player == '■' else '■'
        board[move[0]][move[1]] = opponent
        if check_winner(board, opponent):
            block_move = move
        board[move[0]][move[1]] = ' '
        board[move[0]][move[1]] = player
        val = alpha_beta_defensive(board, 3, -float('inf'), float('inf'), False, player)
        board[move[0]][move[1]] = ' '
        if val > best_val:
            best_val = val
            best_move = move
    if block_move:
        board[block_move[0]][block_move[1]] = player
    elif best_move:
        board[best_move[0]][best_move[1]] = player

def offensive_computer_turn(board, player):
    best_val = -float('inf')
    best_move = None
    for move in available_moves(board):
        board[move[0]][move[1]] = player
        val = alpha_beta_offensive(board, 4, -float('inf'), float('inf'), False, player)
        board[move[0]][move[1]] = ' '
        if val > best_val:
            best_val = val
            best_move = move
    if best_move:
        board[best_move[0]][best_move[1]] = player

# Initialize the board
board = [[' ' for _ in range(4)] for _ in range(4)]

# Welcome message
print("Welcome to 4x4 Tic Tac Toe!\n")

# Ask the user to choose their symbol
offensive_symbol = input("Choose AI 1 symbol (1 for '●' or 2 for '■'): ")
while offensive_symbol not in ['1', '2']:
    offensive_symbol = input("Invalid input. Please choose either 1 or 2: ")
if offensive_symbol == '1':
    offensive_player = '●'
    defensive_player = '■'
else:
    offensive_player = '■'
    defensive_player = '●'

# Game loop between two AI players
turns = 0
while turns < 16:
    print_board(board)
    if turns % 2 == 0:
        print("\nAI1 (O) turn:\n")
        offensive_computer_turn(board, offensive_player)
        if check_winner(board, offensive_player):
            print_board(board)
            print("\nAI1 (O) wins!")
            break
    else:
        print("\nAI2 (D) turn:\n")
        defensive_computer_turn(board, defensive_player)
        if check_winner(board, defensive_player):
            print_board(board)
            print("AI2 (D) wins!")
            break
    turns += 1
if turns == 16:
    print_board(board)
    print("It's a draw!")
