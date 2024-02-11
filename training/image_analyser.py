import cv2
import numpy as np


def board_to_fen(board, active_color='w', castling='-',
                 en_passant_target='-',
                 halfmove_clock='0', fullmove_number='1'):
    empty = 0
    fen = ''
    for i in range(8):
        for j in range(8):
            if board[i][j] is None:
                empty += 1
            else:
                if empty > 0:
                    fen += str(empty)
                    empty = 0
                fen += board[i][j]
        if empty > 0:
            fen += str(empty)
        if i < 7:  # not eight because makes FEN break
            fen += '/'
        empty = 0

    fen += f' {active_color} {castling} {en_passant_target} {halfmove_clock} {fullmove_number}'
    return fen


def detect_pieces(board, pieces, color):
    detections = []
    for piece_name, piece in pieces.items():
        img_piece_clr = cv2.imread(piece, cv2.IMREAD_UNCHANGED)
        img_piece_clr_readable = cv2.cvtColor(img_piece_clr, cv2.COLOR_BGR2GRAY)
        h, w = img_piece_clr_readable.shape
        res = cv2.matchTemplate(img_board_readable, img_piece_clr_readable, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            detections.append((pt, piece_name, h, w))

    # Sort detections by y-coordinate
    detections.sort(key=lambda x: x[0][1])

    for pt, piece_name, h, w in detections:
        cv2.rectangle(board, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        # Update the board state
        row = pt[1] // h
        col = pt[0] // w
        if row < 8 and col < 8:
            if color == 'white':
                board_state[row][col] = piece_name[0].upper()
            else:
                board_state[row][col] = piece_name[0].lower()
    return board


# Load the image
img_board = cv2.imread('train_data/checker.png')

img_board_readable = cv2.cvtColor(img_board, cv2.COLOR_BGR2GRAY)

chessboard_dims = (8, 8)

# I can't believe that CV2 has a built-in function for it...
ret, corners = cv2.findChessboardCorners(img_board_readable, chessboard_dims, None)

if ret:
    # If found, draw corners
    cv2.drawChessboardCorners(img_board, chessboard_dims, corners, ret)
    cv2.imshow('Chessboard', img_board)
    cv2.waitKey(0)
else:
    print("Chessboard not found")

chess_pack = 'usual_chess'

pieces_white = {
    'Pawn': f'train_data/{chess_pack}/white_pawn.png',
    'King': f'train_data/{chess_pack}/white_king.png',
    'Queen': f'train_data/{chess_pack}/white_queen.png',
    'Rook': f'train_data/{chess_pack}/white_rook.png',
    'Bishop': f'train_data/{chess_pack}/white_bishop.png',
    'Night': f'train_data/{chess_pack}/white_knight.png'
}

pieces_black = {
    'Pawn': f'train_data/{chess_pack}/black_pawn.png',
    'King': f'train_data/{chess_pack}/black_king.png',
    'Queen': f'train_data/{chess_pack}/black_queen.png',
    'Rook': f'train_data/{chess_pack}/black_rook.png',
    'Bishop': f'train_data/{chess_pack}/black_bishop.png',
    'Night': f'train_data/{chess_pack}/black_knight.png'
}

# Board that keeps the current state of board
board_state = [[None for _ in range(8)] for _ in range(8)]

img_board = detect_pieces(img_board, pieces_white, 'white')
img_board = detect_pieces(img_board, pieces_black, 'black')

fen = board_to_fen(board_state)
print(fen)

cv2.imwrite('res.png', img_board)