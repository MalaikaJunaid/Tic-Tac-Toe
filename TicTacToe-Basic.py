"""
Tic Tac Toe - *without applying specific Strategies*
"""
import random

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

def computer_turn(board, player):
    print("Computer's turn:")
    available = available_moves(board)
    if available:
        # Try to win
        for move in available:
            board[move[0]][move[1]] = player
            if check_winner(board, player):
                return
            board[move[0]][move[1]] = ' '

        # Try to block player's win
        opponent = '●' if player == '■' else '■'
        for move in available:
            board[move[0]][move[1]] = opponent
            if check_winner(board, opponent):
                board[move[0]][move[1]] = player
                return
            board[move[0]][move[1]] = ' '

        # Choose a random move if no immediate win/block
        move = random.choice(available)
        board[move[0]][move[1]] = player

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
