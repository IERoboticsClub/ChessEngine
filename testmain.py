import pygame
from var import *
from initi import *
from basfunc import *

MaxDepth=2
piece_value={'P':10,'N':30,'B':30,'R':50,'Q':90,'K':1000}
fenrecord= 10 * ["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/"]


def GetFen():
    maherstr=""
    global fenrecord
    for rank in range(ROWS):
        space_count=0
        for file in range(COLS):
      
            curpiece = game_state.board[rank][file]
            if curpiece=="":
                space_count+=1
            else:
                piece_colorizer=(curpiece[1] if curpiece[0]=='w' else curpiece[1].lower())
                maherstr+=(str(space_count) +  piece_colorizer) if space_count else piece_colorizer
                space_count=0
        maherstr+=str(space_count) if space_count else ""
        maherstr+='/'
    fenrecord=fenrecord[1:]+[maherstr]
    print(fenrecord)
            
def DeFenalizer():
    future_board=[]
    global fenrecord
    refboard=fenrecord[-1]
    fenrecord=[""]+fenrecord[:-1]
    s=0
    for k in range(0,8):
    
        i=s
        line=[]
        while refboard[i]!='/':
            line+=(int(refboard[i])*"") if (refboard[i]<='8' and refboard[i]>='0') else refboard[i]
            i+=1
            s=i+1
        
        
        
    

def state_copy(current_turn):
    board_copy = game_state.board.copy()
    for i in range(len(board_copy)):
        board_copy[i] = board_copy[i][:]
    
    piece_moved_copy = game_state.piece_has_moved.copy()
    return {
        'board': board_copy,
        'current_turn': current_turn,
        'piece_has_moved': piece_moved_copy
    }    
        
def undo_move1(state):
    game_state.board = state['board']
    game_state.current_turn = state['current_turn']
    game_state.piece_has_moved = state['piece_has_moved']
    
def board_score():
    score = 0
    
    for rank in range(ROWS):
        for file in range(COLS):
            curpiece = game_state.board[rank][file]
            if curpiece != "":
                value = piece_value[curpiece[1]]
                score += (value if curpiece[0] == 'w' else -value)
                
    return score
    
def basicMinMax(depth, current_turn,alpha,beta):
    if depth == 0 or game_state.game_over:
        return board_score()
    
    if current_turn == 'w':
        max_score = -5000
        
        for rank in range(ROWS):
            for file in range(COLS):
                piece = game_state.board[rank][file]
                if piece != "" and piece[0] == 'w':
                    moves = get_legal_moves(piece, rank, file)
                    for move_rank, move_file in moves:
                        state = state_copy('w')
                        
                        game_state.board[move_rank][move_file] = piece
                        game_state.board[rank][file] = ""
                        
                        
                        move_value = basicMinMax(depth-1, 'b',alpha,beta)
                        
                        undo_move1(state)
                        max_score = max(max_score, move_value)
                        alpha=max(alpha,max_score)
                        if beta<=alpha:
                            return max_score
                        
                        
        return max_score
    
    else:
        min_score = 5000
        
        for rank in range(ROWS):
            for file in range(COLS):
                piece = game_state.board[rank][file]
                
                if piece != "" and piece[0] == 'b':
                    moves = get_legal_moves(piece, rank, file)
                    
                    for move_rank, move_file in moves:
                        state = state_copy('b')
                        
                        game_state.board[move_rank][move_file] = piece
                        game_state.board[rank][file] = ""
                        
                        move_value = basicMinMax(depth-1, 'w',alpha,beta)
                        undo_move1(state)
                        
                        min_score = min(min_score, move_value)
                        beta=min(beta,min_score)
                        if beta<=alpha:
                            return min_score
                        
                        
                        
        return min_score
    
def bMMbestmove(current_turn):
    best_score = -5000 if current_turn == 'w' else 5000
    best_move = None
    
    for rank in range(ROWS):
        for file in range(COLS):
            piece = game_state.board[rank][file]
            if piece != "" and piece[0] == current_turn:
                moves = get_legal_moves(piece, rank, file)
                for move_rank, move_file in moves:
                    state = state_copy(current_turn)
                    game_state.board[move_rank][move_file] = piece
                    game_state.board[rank][file] = ""
                    old_turn = current_turn
                    next_turn = 'b' if current_turn == 'w' else 'w'
       
                    score = basicMinMax(MaxDepth, next_turn,-5000,5000)  
                    if (old_turn == 'w' and score > best_score) or (old_turn == 'b' and score < best_score):
                        best_score = score
                        best_move = ((rank, file), (move_rank, move_file))
                    
                    undo_move1(state)
    
    if best_move:
        (orig_r, orig_c), (dest_r, dest_c) = best_move
        piece_to_move = game_state.board[orig_r][orig_c]
        
        if piece_to_move[1] == 'K':
            # black short castle
            if orig_r == 0 and orig_c == 4 and dest_r == 0 and dest_c == 6:
                # move rook from (0,7)->(0,5)
                game_state.board[0][5] = 'bR'
                game_state.board[0][7] = ''
            # black long castle
            elif orig_r == 0 and orig_c == 4 and dest_r == 0 and dest_c == 2:
                game_state.board[0][3] = 'bR'
                game_state.board[0][0] = ''

        # 4) do the move
        game_state.board[dest_r][dest_c] = piece_to_move
        game_state.board[orig_r][orig_c] = ""
        game_state.last_move = [(orig_r, orig_c), (dest_r, dest_c)]

        # 5) Mark if King/Rook moved from original square
        if (orig_r, orig_c) in game_state.piece_has_moved:
            game_state.piece_has_moved[(orig_r, orig_c)] = True
        if piece_to_move[1] in ['K','R']:
            game_state.piece_has_moved[(dest_r, dest_c)] = True

        # 6) Pawn promotion (rare for black but can happen)
        promote_pawn(dest_r, dest_c)
        GetFen()
    
    return best_move
                            
    
def switch_turn():
    game_state.current_turn = 'b' if game_state.current_turn == 'w' else 'w'

def main():
    load_piece_images()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        # If it's black's turn AND the game isn't over, black does a random move automatically.
        if game_state.current_turn == 'b' and not game_state.game_over:
            best_move = bMMbestmove('b')
            if best_move: 
                switch_turn()
                check_game_end()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_state.game_over:
                # only let user move if it's White's turn
                if game_state.current_turn == 'w':
                    rank = mouse_pos[1] // SQUARE_SIZE
                    file = mouse_pos[0] // SQUARE_SIZE
                    if is_valid_position(rank, file):
                        piece = game_state.board[rank][file]
                        # Only allow selection if it's White's piece with legal moves
                        if piece and piece[0] == 'w':
                            possible_legal_moves = get_legal_moves(piece, rank, file)
                            if possible_legal_moves:
                                game_state.selected_piece = piece
                                game_state.selected_pos = (rank, file)
                                game_state.legal_moves = possible_legal_moves

            elif event.type == pygame.MOUSEBUTTONUP and not game_state.game_over:
                if game_state.current_turn == 'w' and game_state.selected_piece:
                    rank = mouse_pos[1] // SQUARE_SIZE
                    file = mouse_pos[0] // SQUARE_SIZE
                    orig_rank, orig_file = game_state.selected_pos
                    if is_valid_position(rank, file) and (rank, file) in game_state.legal_moves:
                        # handle castling for White
                        if game_state.selected_piece[1] == 'K':
                            # White short
                            if (game_state.selected_piece[0] == 'w' and orig_rank == 7 and orig_file == 4
                                    and rank == 7 and file == 6):
                                game_state.board[7][5] = 'wR'
                                game_state.board[7][7] = ''
                            # White long
                            elif (game_state.selected_piece[0] == 'w' and orig_rank == 7 and orig_file == 4
                                    and rank == 7 and file == 2):
                                game_state.board[7][3] = 'wR'
                                game_state.board[7][0] = ''

                        game_state.board[rank][file] = game_state.selected_piece
                        game_state.board[orig_rank][orig_file] = ""
                        game_state.last_move = [(orig_rank, orig_file), (rank, file)]

                        # Mark if King/Rook moved
                        if (orig_rank, orig_file) in game_state.piece_has_moved:
                            game_state.piece_has_moved[(orig_rank, orig_file)] = True
                        if game_state.selected_piece[1] in ['K','R']:
                            game_state.piece_has_moved[(rank, file)] = True

                        promote_pawn(rank, file)
                        switch_turn()
                        check_game_end()

                    game_state.selected_piece = None
                    game_state.selected_pos = None
                    game_state.legal_moves = []

        screen.fill((0,0,0))
        draw_board()

        # if a White piece is selected, let user drag
        if game_state.current_turn == 'w' and game_state.selected_piece and not game_state.game_over:
            piece_image = PIECE_IMAGES[game_state.selected_piece]
            piece_rect = piece_image.get_rect(center=mouse_pos)
            screen.blit(piece_image, piece_rect.topleft)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()