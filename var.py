
import pygame

# Screen setup
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")

# Fonts
pygame.font.init()
SMALL_FONT = pygame.font.SysFont("Arial", 36, bold=True)

# Colors
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)
HIGHLIGHT_COLOR_LIGHT = (246, 246, 105)
HIGHLIGHT_COLOR_DARK = (180, 180, 30)
LAST_MOVE_COLOR = (255, 223, 88)
SELECTED_COLOR = (255, 160, 122)
CHECK_COLOR = (255, 99, 71)

# Chessboard setup
class GameState:
    def __init__(self):
        self.board= [
        ["bR","bN","bB","bQ","bK","bB","bN","bR"],
        ["bP","bP","bP","bP","bP","bP","bP","bP"],
        ["",  "",  "",  "",  "",  "",  "",  "" ],
        ["",  "",  "",  "",  "",  "",  "",  "" ],
        ["",  "",  "",  "",  "",  "",  "",  "" ],
        ["",  "",  "",  "",  "",  "",  "",  "" ],
        ["wP","wP","wP","wP","wP","wP","wP","wP"],
        ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]   
        self.piece_has_moved={
            (0,4): False,  # Black King (e8)
            (0,0): False,  # Black Rook a8
            (0,7): False,  # Black Rook h8
            (7,4): False,  # White King (e1)
            (7,0): False,  # White Rook a1
            (7,7): False   # White Rook h1
        }
        self.current_turn='w'
        self.selected_piece = None
        self.selected_pos = None
        self.legal_moves = []
        ##current_turn = 'w'
        self.last_move = None
        self.game_over = False
        self.winner = None  # "White" or "Black"



# Keep track of King and Rook movement for castling

game_state=GameState()