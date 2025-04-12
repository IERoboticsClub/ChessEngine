from var import *

def is_king_in_check(color):
    king_pos = [
        (r, f) for r in range(ROWS)
        for f in range(COLS)
        if game_state.board[r][f] == color + "K"
    ]
    if not king_pos:
        return False
    kr, kf = king_pos[0]
    opp_color = 'b' if color == 'w' else 'w'
    for r in range(ROWS):
        for c in range(COLS):
            piece = game_state.board[r][c]
            if piece and piece[0] == opp_color:
                possible = get_potential_moves(piece, r, c)
                if (kr, kf) in possible:
                    return True
    return False

def can_castle_kingside(color):
    if color == 'w':
        king_start = (7,4)
        rook_start = (7,7)
        rank = 7
    else:
        king_start = (0,4)
        rook_start = (0,7)
        rank = 0

    if game_state.piece_has_moved.get(king_start, False):
        return False
    if game_state.piece_has_moved.get(rook_start, False):
        return False

    if game_state.board[rank][5] != "" or game_state.board[rank][6] != "":
        return False

    ##if is_king_in_check(color):
      ##  return False

    saved_king = game_state.board[king_start[0]][king_start[1]]

    # step on (rank,5)
    saved_5 = game_state.board[rank][5]
    game_state.board[rank][5] = saved_king
    game_state.board[king_start[0]][king_start[1]] = ""
    """if is_king_in_check(color):
        game_state.board[king_start[0]][king_start[1]] = saved_king
        game_state.board[rank][5] = saved_5
        return False"""
    # revert
    game_state.board[king_start[0]][king_start[1]] = saved_king
    game_state.board[rank][5] = saved_5

    # step on (rank,6)
    saved_6 = game_state.board[rank][6]
    game_state.board[rank][6] = saved_king
    game_state.board[king_start[0]][king_start[1]] = ""
    can_castle = True
    ##if is_king_in_check(color):
        ##can_castle = False
    # revert
    game_state.board[king_start[0]][king_start[1]] = saved_king
    game_state.board[rank][6] = saved_6

    return can_castle

def can_castle_queenside(color):
    if color == 'w':
        king_start = (7,4)
        rook_start = (7,0)
        rank = 7
    else:
        king_start = (0,4)
        rook_start = (0,0)
        rank = 0

    if game_state.piece_has_moved.get(king_start, False):
        return False
    if game_state.piece_has_moved.get(rook_start, False):
        return False

    if (game_state.board[rank][1] != "" or
        game_state.board[rank][2] != "" or
        game_state.board[rank][3] != ""):
        return False

    ##if is_king_in_check(color):
       ## return False

    saved_king = game_state.board[king_start[0]][king_start[1]]

    # step on (rank,3)
    saved_3 = game_state.board[rank][3]
    game_state.board[rank][3] = saved_king
    game_state.board[king_start[0]][king_start[1]] = ""
    """if is_king_in_check(color):
        game_state.board[king_start[0]][king_start[1]] = saved_king
        game_state.board[rank][3] = saved_3
        return False"""
    # revert
    game_state.board[king_start[0]][king_start[1]] = saved_king
    game_state.board[rank][3] = saved_3

    # step on (rank,2)
    saved_2 = game_state.board[rank][2]
    game_state.board[rank][2] = saved_king
    game_state.board[king_start[0]][king_start[1]] = ""
    can_castle = True
    ##if is_king_in_check(color):
      ##  can_castle = False
    # revert
    game_state.board[king_start[0]][king_start[1]] = saved_king
    game_state.board[rank][2] = saved_2

    return can_castle

def get_potential_moves(piece, rank, file):
    moves = []
    if not piece:
        return moves
    color = piece[0]
    opponent = 'b' if color == 'w' else 'w'

    if piece[1] == "P":
        direction = -1 if color == 'w' else 1
        start_row = 6 if color == 'w' else 1
        # single step
        if is_valid_position(rank+direction,file) and game_state.board[rank+direction][file] == "":
            moves.append((rank+direction, file))
            # double step
            if rank == start_row and game_state.board[rank+2*direction][file] == "":
                moves.append((rank+2*direction, file))
        # diagonal captures
        for dx in [-1,1]:
            r_cap = rank+direction
            f_cap = file+dx
            if is_valid_position(r_cap,f_cap):
                target = game_state.board[r_cap][f_cap]
                if target and target[0] == opponent:
                    moves.append((r_cap,f_cap))

    elif piece[1] == "R":
        moves.extend(generate_moves_in_directions(rank,file,[(1,0),(-1,0),(0,1),(0,-1)]))

    elif piece[1] == "B":
        moves.extend(generate_moves_in_directions(rank,file,[(1,1),(1,-1),(-1,1),(-1,-1)]))

    elif piece[1] == "Q":
        moves.extend(generate_moves_in_directions(rank,file,[
            (1,0),(-1,0),(0,1),(0,-1),
            (1,1),(1,-1),(-1,1),(-1,-1)
        ]))

    elif piece[1] == "N":
        knight_moves = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for (dr,df) in knight_moves:
            rr = rank+dr
            ff = file+df
            if is_valid_position(rr,ff):
                if game_state.board[rr][ff] == "" or game_state.board[rr][ff][0] == opponent:
                    moves.append((rr,ff))

    elif piece[1] == "K":
        king_moves = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for (dr,df) in king_moves:
            rr=rank+dr
            ff=file+df
            if is_valid_position(rr,ff):
                if game_state.board[rr][ff]=="" or game_state.board[rr][ff][0]==opponent:
                    moves.append((rr,ff))

        # castling squares
        if color=='w' and rank==7 and file==4:
            if can_castle_kingside('w'):
                moves.append((7,6))
            if can_castle_queenside('w'):
                moves.append((7,2))
        if color=='b' and rank==0 and file==4:
            if can_castle_kingside('b'):
                moves.append((0,6))
            if can_castle_queenside('b'):
                moves.append((0,2))

    return moves

def get_legal_moves(piece, rank, file):
    naive_moves = get_potential_moves(piece, rank, file)
    color = piece[0]
    legal = []
    for (r,f) in naive_moves:
        saved_piece = game_state.board[r][f]
        game_state.board[r][f] = piece
        game_state.board[rank][file] = ""

        if not is_king_in_check(color):
            legal.append((r,f))

        game_state.board[rank][file] = piece
        game_state.board[r][f] = saved_piece
    return legal

def promote_pawn(rank, file):
    piece = game_state.board[rank][file]
    if piece and piece[1]=='P' and (rank==0 or rank==7):
        game_state.board[rank][file] = piece[0]+'Q'

def check_game_end():
    if is_king_in_check(game_state.current_turn):
        moves_exist = False
        for r in range(ROWS):
            for c in range(COLS):
                piece = game_state.board[r][c]
                if piece and piece[0] == game_state.current_turn:
                    if get_legal_moves(piece, r, c):
                        moves_exist = True
                        break
            if moves_exist:
                break
        if not moves_exist:
            game_state.winner = 'White' if game_state.current_turn=='b' else 'Black'
            print(f'Checkmate! {game_state.winner} wins!')
            game_state.game_over = True
        else:
            print(f'{game_state.current_turn} is in check!')

def is_valid_position(rank, file):
    return 0 <= rank < ROWS and 0 <= file < COLS

def generate_moves_in_directions(rank, file, directions, max_steps=8):
    moves = []
    curpiece = game_state.board[rank][file]
    if not curpiece:
        return moves
    color = curpiece[0]
    for dr, df in directions:
        for step in range(1, max_steps+1):
            r, f = rank + dr*step, file + df*step
            if not is_valid_position(r, f):
                break
            if game_state.board[r][f] == "":
                moves.append((r, f))
            elif game_state.board[r][f][0] != color:
                moves.append((r, f))
                break
            else:
                break
    return moves