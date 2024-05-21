"""---
##Tic Tac Toe - using **Monte Carlo Tree Search**
###*AI Computer vs Human*
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

class Node:
    def _init_(self, board, move=None, parent=None):
        self.board = board  # Store the current board state
        self.move = move  # Store the move that led to this state
        self.wins = 0  # Number of wins from this node
        self.visits = 0  # Number of visits to this node
        self.children = []  # List of child nodes
        self.parent = parent

def mcts_selection(node):
    C = 1.4  # Constant for exploration factor
    best_child = None
    best_score = -float('inf')

    for child in node.children:
        if child.visits == 0:
            score = float('inf')  # Assign a very high score for unvisited nodes
        else:
            exploitation_term = child.wins / child.visits
            if node.visits == 0 or child.visits == 0:
                exploration_term = C  # Set a default exploration value
            else:
                exploration_term = C * (math.sqrt(math.log(node.visits) / child.visits))
            score = exploitation_term + exploration_term

        if score > best_score:
            best_child = child
            best_score = score

    return best_child


def mcts_expansion(node):
    available_moves = [(i, j) for i in range(4) for j in range(4) if node.board[i][j] == ' ']
    if available_moves:
        move = random.choice(available_moves)
        new_board = [row[:] for row in node.board]  # Copy the board
        new_board[move[0]][move[1]] = '●'  # Assume AI always plays '●'
        new_node = Node(new_board, move, node)  # Include the parent node
        node.children.append(new_node)
        return new_node
    return None


def mcts_simulation(node):
    # Simulate random games (rollout) to determine potential outcomes
    simulated_board = [row[:] for row in node.board]  # Copy the board
    current_player = '■'  # Assuming human player always plays '■'
    winner = None

    while True:
        available_moves = [(i, j) for i in range(4) for j in range(4) if simulated_board[i][j] == ' ']
        if not available_moves or check_winner(simulated_board, '●') or check_winner(simulated_board, '■'):
            winner = check_winner(simulated_board, '●') or check_winner(simulated_board, '■')
            break
        move = random.choice(available_moves)
        simulated_board[move[0]][move[1]] = current_player
        current_player = '■' if current_player == '●' else '●'  # Switch players

    return 1 if winner == '●' else 0  # Assuming the goal is to maximize AI's wins


def mcts_backpropagation(node, result):
    # Update node statistics (wins and visits) based on the simulation result
    while node is not None:
        node.visits += 1
        node.wins += result
        node = node.parent


def computer_turn(board, player):
    root = Node(board)
    max_simulations = 1000

    for _ in range(max_simulations):
        node = root
        while node.children:
            node = mcts_selection(node)

        new_node = mcts_expansion(node)
        if new_node:
            result = mcts_simulation(new_node)
            mcts_backpropagation(new_node, result)

    # Check if AI can win or block the user from winning
    for i in range(4):
        for j in range(4):
            if board[i][j] == ' ':
                board[i][j] = '●'  # Assume AI's move

                # Check if AI can complete a line of 4
                if check_winner(board, '●'):
                    board[i][j] = player
                    return

                # Check if AI can block the player from completing a line of 4
                board[i][j] = '■' if player == '●' else '●'
                if check_winner(board, '■' if player == '●' else '●'):
                    board[i][j] = player
                    return

                board[i][j] = ' '  # Reset the position if no advantage
    # If no immediate win or block is possible, perform MCTS move selection
    best_child = max(root.children, key=lambda x: x.wins / x.visits)
    if best_child:
        row, col = best_child.move
        board[row][col] = player


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
