"""
---
##Game Problem:  **Tic-Tac-Toe**
###Description:
* Grid Size: The game is played on a 4x4 grid.
* Players: One human player and one computer player.
* Symbols: Players take turns marking symbols (●s or ■s) in empty cells.
* Target: The target remains to form a straight line with four of your symbols horizontally, vertically, or diagonally.

###Rules:
* Setup: The game is played on a 4x4 grid (16 cells) where two players take turns marking the cells. One player uses '●', and the other uses '■'.
* Gameplay: Players take turns placing their symbol in an empty cell until one player achieves four of their symbols in a row.
* Turns: Players alternate placing their symbol on the board. Once a cell is marked, it cannot be changed.
* Winning: The game can be won by getting four of your symbols in a row. This can be horizontally, vertically, or diagonally.
* Draw: If all cells are filled before either player achieves four in a row, the game is a draw.
* Goal: Don't lose - either Win or end up on draw.

###Objectives:
  - The primary objective is to form a sequence of four symbols in a row, either horizontally, vertically, or diagonally, before the opponent does.
  - Players aim to strategically place their symbols to either create winning sequences or block their opponent's attempts at achieving a winning sequence.

---


##Tic Tac Toe - *using* ***Monte Carlo Tree Search***

MCTS (Monte Carlo Tree Search) dynamically explores the game space by conducting a four-phase process. This method intelligently samples potential moves, focusing on those demonstrating higher success rates, and expands unvisited nodes for further analysis. By simulating random games and updating node statistics, MCTS ensures a balanced consideration of possible outcomes, effectively guiding decision-making in a resource-efficient manner.

The components of MCTS implementation are stated below.
- Selection Phase:
  - The mcts_selection function selects the most promising child node from the current node based on the Upper Confidence Bounds for Trees (UCT) algorithm. It considers the exploration and exploitation of nodes. The exploration term ensures that all possible moves get sampled, while the exploitation term aids in favoring nodes that historically showed higher success rates.

- Expansion Phase:
  - The mcts_expansion function selects a random unvisited child node for expansion. It creates a new node representing a possible future game state given a random unexplored move.

- Simulation Phase:
  - The mcts_simulation function performs a random rollout or simulation of a game from the new node created in the expansion phase to determine a potential outcome. The game is simulated to completion with random moves to estimate the likelihood of success from a given node.

- Backpropagation Phase:
  - The mcts_backpropagation function backpropagates the result obtained from the simulation phase. It updates the statistics of the nodes in the tree, incrementing the visit count and win count, contributing to the exploration/exploitation balance.

The computer_turn function initially creates a tree, explores and expands nodes using selection and expansion, simulates games to evaluate potential outcomes, and then backpropagates the results to update the nodes.

---


##Tic Tac Toe - *using* ***Alpha-Beta Prunning***

Alpha-Beta Pruning significantly minimizes the number of explored nodes by discarding unpromising moves and their subsequent branches. This enhancement improves search efficiency without compromising the accuracy of the decision-making process.

The Alpha-Beta Pruning algorithm optimizes the search process by:

- Minimizing explored nodes:
    -  It prunes unnecessary branches in the search tree where the best moves have been determined. This is achieved by maintaining alpha and beta values, representing the best possible outcomes for the maximizing and minimizing players. These values help discard irrelevant moves, reducing the number of nodes explored.

- Pruning irrelevant subtrees:
  - If a move does not influence the final decision (not changing alpha or beta values), the search in that direction is cut off. This significantly reduces the search space by ignoring branches that won't affect the final decision, boosting efficiency.

- Depth limitation:
  - By limiting the search depth to 3 in this implementation, the algorithm focuses on a subset of possible moves, which reduces the tree size. This strategy helps the algorithm make informed decisions within resource constraints.

---


##**Comparative Analysis**


*   **Efficiency**: *(Number of Nodes Explored)*
  - MCTS:
      - MCTS explores a varied number of nodes and uses random simulations to decide the most promising ones.
      - The number of nodes visited increases with the number of simulations.
      - Can explore a large number of nodes, especially in complex games, requiring more computational resources.
  - Alpha-Beta Pruning:
      - Reduces the number of explored nodes by eliminating unnecessary branches, leading to more efficient exploration.
      - Effectiveness increases with a higher depth search and a lower branching factor.
      - Even though it prunes nodes, it can still explore a substantial number, particularly in games with a vast search space.


*   **Accuracy**: *(Quality of Moves Chosen)*
  - MCTS:
      - Focuses on exploring a wide range of moves, providing high-quality moves with a higher number of simulations.
      - Works well when there's a large number of possible moves.
      - Accuracy depends heavily on the number of simulations, sometimes making suboptimal moves with an insufficient number of simulations.
  - Alpha-Beta Pruning:
      - Aims to choose the best moves by exploring deeper and considering a limited number of nodes due to pruning.
      - Quality of moves depends on the effectiveness of the heuristic evaluation function.
      - May overlook certain good moves due to cutoffs or ineffective evaluation functions.

##**Results and Conclusion**

*   **Insights**:
  - MCTS Insights:
      - Effective in exploring numerous possible moves due to its randomized exploration.
      - Relatively computationally expensive, especially in scenarios with an extensive number of possible moves, requiring more simulations for accurate decisions.

  - Alpha-Beta Pruning Insights:
      - Efficient in reducing the number of nodes explored.
      - Can sometimes overlook potential good moves based on the heuristic evaluation, especially in complex game states.
    
*   **Verdict**:
  - MCTS:
      - Effective in scenarios with numerous possible moves due to its randomized exploration. However, it requires a significant number of simulations for reasonable decisions.
  - Alpha-Beta Pruning:
      - Performs relatively well, especially with a limited number of moves, exploring a smaller subset of nodes.

*   **Conclusion**:
      -  In a nutshell, while both alpha-beta pruning and MCTS could be technically applied to Tic Tac Toe, alpha-beta pruning is more suitable and efficient given the game's simplicity and deterministic nature. MCTS introduces unnecessary computational overhead for a game with a small and manageable decision space like Tic Tac Toe.

---
"""
