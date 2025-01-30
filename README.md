# ChessEngine
# Python Chess Engine Development Guide

This guide outlines the core milestones and steps to build a basic chess engine in Python. Follow this roadmap incrementally, testing each component thoroughly before moving to the next step.

---

## **Prerequisites**
- Basic Python knowledge (classes, functions, loops)
- Understanding of chess rules and piece movements
- Recommended libraries: `python-chess` (for validation/testing), `pygame` (for GUI)

---

## **Milestone 1: Board Representation**
### Objective: Create a data structure to represent the chess board and pieces.

#### Steps:
1. **Board Initialization**
   - Use an 8x8 list to represent the board.
   - Assign Unicode characters or abbreviations (`R`, `N`, `B`, `Q`, `K`, `P`) to pieces.

2. **Piece Class (Optional)**
   - Create a `Piece` class with `type`, `color`, and position attributes.

3. **Starting Position**
   - Initialize pieces in their standard positions.

#### Example Code:
```python
class ChessBoard:
    def __init__(self):
        self.board = [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            # ... Add remaining rows for initial setup
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ]
        self.current_turn = 'white'
```

---

## **Milestone 2: Move Validation**
### Objective: Implement rules for legal moves.

#### Steps:
1. **Basic Movement Logic**
   - Create functions like `is_valid_move(piece, start, end)`.
   - Handle special cases: castling, en passant, pawn promotion.

2. **Check Detection**
   - Identify if a player's king is under attack.

3. **Checkmate/Stalemate**
   - Check for no legal moves + king in check (checkmate) or no legal moves + king safe (stalemate).

#### Example Code:
```python
def validate_pawn_move(start, end, color):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    if color == 'white':
        return (dx == -1 and dy == 0) or (start[0] == 6 and dx == -2 and dy == 0)
    # Add black pawn logic
```

---

## **Milestone 3: Text-Based Interface**
### Objective: Create a CLI to play chess manually.

#### Steps:
1. **Board Display**
   - Print the board with ranks/files using ASCII/Unicode.

2. **Move Input**
   - Accept moves in algebraic notation (e.g., "e2-e4").

3. **Turn Management**
   - Alternate between white and black players.

#### Example Output:
```
  a b c d e f g h
8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
...
1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
```

---

## **Milestone 4: Move Generation**
### Objective: Generate all legal moves for a position.

#### Steps:
1. **Per-Piece Logic**
   - Implement functions to generate moves for each piece type.

2. **Filter Illegal Moves**
   - Remove moves that leave the king in check.

#### Example Code:
```python
def generate_knight_moves(position):
    x, y = position
    offsets = [(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2,-1)]
    return [(x+dx, y+dy) for dx, dy in offsets if 0 <= x+dx < 8 and 0 <= y+dy < 8]
```

---

## **Milestone 5: Basic AI (Minimax)**
### Objective: Implement a simple AI opponent.

#### Steps:
1. **Minimax Algorithm**
   - Recursively evaluate future positions.

2. **Alpha-Beta Pruning**
   - Optimize minimax by pruning irrelevant branches.

3. **Evaluation Function**
   - Assign scores based on material balance and positional advantages.

#### Example Code:
```python
def minimax(board, depth, maximizing_player):
    if depth == 0 or game_over:
        return evaluate(board)
    # Recursively evaluate child nodes
```

---

## **Milestone 6: Performance Optimization**
### Objective: Improve search speed and depth.

#### Techniques:
1. **Move Ordering**  
   Prioritize capturing moves and checks.
2. **Transposition Tables**  
   Cache previously evaluated positions.
3. **Bitboard Representation**  
   Use 64-bit integers for faster operations.

---

## **Milestone 7: GUI (Optional)**
### Objective: Create a graphical interface with Pygame.

#### Steps:
1. **Draw Board**  
   Render squares and pieces.
2. **Handle Clicks**  
   Allow selecting and moving pieces visually.
3. **Highlight Legal Moves**  
   Show available moves for selected pieces.

---

## **Advanced Features (Post-MVP)**
1. **UCI Protocol**  
   Enable compatibility with chess GUIs like Arena.
2. **Opening Book**  
   Use common openings for better early-game play.
3. **Endgame Tablebases**  
   Implement perfect endgame play.

---

## **Development Tips**
1. **Test Incrementally**  
   Validate each piece's moves before proceeding.
2. **Use Existing Libraries**  
   `python-chess` can help verify move legality.
3. **Version Control**  
   Use Git to track changes and revert bugs.

---

Start with Milestone 1 and progress sequentially. Break each milestone into smaller tasks, and don’t hesitate to refactor code as your understanding grows. Good luck! ♟️🚀
