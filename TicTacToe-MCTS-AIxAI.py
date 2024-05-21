"""###AI Computer 1 vs AI Computer 2"""

import random
import math

class Node:
    def init(self, board, move=None, parent=None):
        self.board = board
        self.move = move
        self.wins = 0
        self.visits = 0
        self.children = []
        self.parent = parent

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

def mcts_selection(node):
    C = 1.4
    best_child = None
    best_score = -float('inf')

    for child in node.children:
        if child.visits == 0:
            score = float('inf')
        else:
            exploitation_term = child.wins / child.visits
            if node.visits == 0 or child.visits == 0:
                exploration_term = C
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
        new_board = [row[:] for row in node.board]
        new_board[move[0]][move[1]] = '●'
        new_node = Node(new_board, move, node)
        node.children.append(new_node)
        return new_node
    return None

def mcts_simulation(node):
    simulated_board = [row[:] for row in node.board]
    current_player = '■'
    winner = None

    while True:
        available_moves = [(i, j) for i in range(4) for j in range(4) if simulated_board[i][j] == ' ']
        if not available_moves or check_winner(simulated_board, '●') or check_winner(simulated_board, '■'):
            winner = check_winner(simulated_board, '●') or check_winner(simulated_board, '■')
            break
        move = random.choice(available_moves)
        simulated_board[move[0]][move[1]] = current_player
        current_player = '■' if current_player == '●' else '●'

    return 1 if winner == '●' else 0

def mcts_backpropagation(node, result):
    while node is not None:
        node.visits += 1
        node.wins += result
        node = node.parent

def defensive_computer_turn(board, player):
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

    best_child = max(root.children, key=lambda x: x.wins / x.visits)
    if best_child:
        row, col = best_child.move
        board[row][col] = player

def offensive_computer_turn(board, player):
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

    best_child = max(root.children, key=lambda x: x.wins / x.visits)
    if best_child:
        row, col = best_child.move
        board[row][col] = player

def ask_user():
    user_input = input("Enter 1 for AI1 (Defensive) to start or 2 for AI2 (Offensive) to start: ")
    if user_input in ['1', '2']:
        return user_input
    return ask_user()

# Initialize the board
board = [[' ' for _ in range(4)] for _ in range(4)]

first_turn = ask_user()
turns = 0
while turns < 16:
    print_board(board)
    if first_turn == '1':
        if turns % 2 == 0:
            print("\nAI1 (Defensive) turn:\n")
            defensive_computer_turn(board, '■')
            if check_winner(board, '■'):
                print_board(board)
                print("\nAI1 (Defensive) wins!")
                break
        else:
            print("\nAI2 (Offensive) turn:\n")
            offensive_computer_turn(board, '●')
            if check_winner(board, '●'):
                print_board(board)
                print("AI2 (Offensive) wins!")
                break
    else:
        if turns % 2 == 0:
            print("\nAI2 (Offensive) turn:\n")
            offensive_computer_turn(board, '●')
            if check_winner(board, '●'):
                print_board(board)
                print("AI2 (Offensive) wins!")
                break
        else:
            print("\nAI1 (Defensive) turn:\n")
            defensive_computer_turn(board, '■')
            if check_winner(board, '■'):
                print_board(board)
                print("\nAI1 (Defensive) wins!")
                break
    turns += 1
if turns == 16:
    print_board(board)
    print("It's a draw!")
