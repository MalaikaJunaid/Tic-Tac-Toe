"""---
##Tic Tac Toe - using *Alpha-Beta Prunning*
###AI Computer vs Human
"""

import random
import math

def print_board(board):
    print("   A   B   C   D")
    for i in range(4):
        print(str(i + 1) + "  " + " | ".join(board[i]))

def check_winner(board, player):
    # Check rows, columns, and diagonals for a win
    for i in range(4):
        # Check rows and columns
        if all(board[i][j] == player for j in range(4)) or all(board[j][i] == player for j in range(4)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(4)) or all(board[i][3 - i] == player for i in range(4)):
        return True
    return False

def available_moves(board):
    return [(i, j) for i in range(4) for j in range(4) if board[i][j] == ' ']

def player_turn(board, player):
    while True:
        move = input("Enter your move (e.g. A1, B2): ").upper()
        if len(move) != 2 or move[0] not in 'ABCD' or move[1] not in '1234':
            print("Invalid input. Please enter a valid move.")
            continue
        row = int(move[1]) - 1
        col = ord(move[0]) - ord('A')
        if board[row][col] == ' ':
            board[row][col] = player
            break
        else:
            print("That position is already taken. Try again.")

def evaluate(board, player):
    # This function returns a score indicating how good the current board state is for the given player.

    # Define a mapping for the players
    player_map = {'●': -1, '■': 1, ' ': 0}

    # Score the board
    score = 0

    # Evaluate rows, columns, and diagonals
    for i in range(4):
        # Rows and columns
        row_values = [player_map[board[i][j]] for j in range(4)]
        col_values = [player_map[board[j][i]] for j in range(4)]
        score += row_values.count(player_map[player]) + col_values.count(player_map[player])

    # Diagonals
    diag1 = [player_map[board[i][i]] for i in range(4)]
    diag2 = [player_map[board[i][3 - i]] for i in range(4)]
    score += diag1.count(player_map[player]) + diag2.count(player_map[player])

    return score

def alpha_beta(board, depth, alpha, beta, maximizing_player, player):
    if depth == 0 or check_winner(board, '●') or check_winner(board, '■'):
        # Evaluate the board state and return the score
        return evaluate(board, player)

    if maximizing_player:
        max_eval = float('-inf')
        for move in available_moves(board):
            board[move[0]][move[1]] = '●'
            eval = alpha_beta(board, depth - 1, alpha, beta, False, player)
            board[move[0]][move[1]] = ' '  # Undo the move
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:
        min_eval = float('inf')
        for move in available_moves(board):
            board[move[0]][move[1]] = '■'
            eval = alpha_beta(board, depth - 1, alpha, beta, True, player)
            board[move[0]][move[1]] = ' '  # Undo the move
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval

def computer_turn(board, player):
    print("Computer's turn:")
    best_val = -float('inf')
    best_move = None
    block_move = None  # Record to block the opponent's winning move

    for move in available_moves(board):
        board[move[0]][move[1]] = player
        # Check if this move leads to the computer's win
        if check_winner(board, player):
            board[move[0]][move[1]] = ' '  # Undo the move
            board[move[0]][move[1]] = player
            return

        # Check if this move can block the opponent's winning move
        opponent = '●' if player == '■' else '■'
        board[move[0]][move[1]] = opponent
        if check_winner(board, opponent):
            block_move = move
        board[move[0]][move[1]] = ' '  # Undo the move

        board[move[0]][move[1]] = player
        val = alpha_beta(board, 3, -float('inf'), float('inf'), False, player)
        board[move[0]][move[1]] = ' '

        if val > best_val:
            best_val = val
            best_move = move

    # If there's a move that blocks the opponent, take that move, else proceed with alpha-beta evaluation
    if block_move:
        board[block_move[0]][block_move[1]] = player
    elif best_move:
        board[best_move[0]][best_move[1]] = player


# Initialize the board
board = [[' ' for _ in range(4)] for _ in range(4)]

# Welcome message
print("Welcome to 4x4 Tic Tac Toe!\n")

# Ask for player's choice of symbol
player_symbol_c = int(input("Choose your symbol (1 for ■ or 2 for ●): "))
while player_symbol_c not in [1, 2]:
    player_symbol_c = int(input("Invalid input. Please choose either 1 or 2: "))
if player_symbol_c == 1:
    player_symbol = '■'
else:
    player_symbol = '●'

# Determine who goes first
player_turns = input("Do you want to go first? (yes or no): ").lower().startswith('y')

# Game loop
turns = 0
while turns < 16:
    print_board(board)
    if player_turns:
        player_turn(board, player_symbol)
        if check_winner(board, player_symbol):
            print_board(board)
            print("Congratulations! You win!")
            break
    else:
        computer_turn(board, '■' if player_symbol == '●' else '●')
        if check_winner(board, '■' if player_symbol == '●' else '●'):
            print_board(board)
            print("Computer wins! Better luck next time.")
            break
    turns += 1
    if turns == 16:
        print_board(board)
        print("It's a draw!")
    player_turns = not player_turns
