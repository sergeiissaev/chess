import os
import time
from pathlib import Path
import chess
import chess.svg
from helper_functions import select_random_opening, print_moves_white, print_moves_black

import pygame
import sys

# Constants
WIDTH, HEIGHT = 640, 640
SQ_SIZE = WIDTH // 8
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT_RED = (255, 0, 0)
PIECE_IMAGES = {}

def load_images():
    pieces = ['p', 'r', 'n', 'b', 'q', 'k']
    for color in ['w', 'b']:
        for piece in pieces:
            filename = f"assets/{color}{piece}.png"
            image = pygame.image.load(filename)
            PIECE_IMAGES[f"{color}{piece}"] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))

def draw_board(screen, highlighted_square=None):
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            square = chess.square(col, 7 - row)
            if highlighted_square == square:
                color = HIGHLIGHT_RED
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board, color):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            if not color:
                row = 7 - chess.square_rank(square)
                col = chess.square_file(square)
            else:
                row = chess.square_rank(square)
                col = 7 - chess.square_file(square)
            piece_str = f"{'w' if piece.color == chess.WHITE else 'b'}{piece.symbol().lower()}"
            screen.blit(PIECE_IMAGES[piece_str], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def get_square_from_pos(pos, color):
    x, y = pos
    col = x // SQ_SIZE
    row = y // SQ_SIZE
    if color == 0:
        return chess.square(col, 7 - row)
    else:
        return chess.square(7 - col, row)

def main(move_sequence, color: int):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess GUI")
    clock = pygame.time.Clock()
    board = chess.Board()

    load_images()

    running = True
    turn = 0
    selected_square = None
    highlighted_square = None
    move_start = None

    # Play white's first move if user is Black
    if color == 1 and turn == 0:
        try:
            opp_move = move_sequence[0]
            print(f"{turn + 1}.{opp_move}")
            opp_move = board.parse_san(opp_move)
            board.push(opp_move)
        except:
            input("You passed! Press enter to quit")
            pygame.quit()
            sys.exit()

    while running:
        draw_board(screen, highlighted_square)
        draw_pieces(screen, board, color)
        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked_square = get_square_from_pos(pos, color)

                if selected_square is None:
                    if board.piece_at(clicked_square) and board.piece_at(clicked_square).color == (
                            chess.WHITE if color == 0 else chess.BLACK):
                        selected_square = clicked_square
                        move_start = board.copy()
                else:
                    try:
                        move = chess.Move(selected_square, clicked_square)
                        if move in board.legal_moves:
                            move_san = board.san(move)
                            expected_move = move_sequence[(turn * 2) + color]
                            expected_move = expected_move.replace("0", "O")
                            if move_san == expected_move:
                                board.push(move)
                                print(f"{turn + 1}.{move_san}")

                                if color == 0:
                                    if (2 * turn + 1) < len(move_sequence):
                                        try:
                                            opp_move = move_sequence[2 * turn + 1]
                                            print(f"{turn + 1}...{opp_move}")
                                            opp_move = board.parse_san(opp_move)
                                            board.push(opp_move)
                                        except Exception as e:
                                            print(f"Error parsing opponent move: {e}")
                                            pygame.quit()
                                            sys.exit()
                                else:
                                    if (2 * turn + 2) < len(move_sequence):
                                        try:
                                            opp_move = move_sequence[2 * turn + 2]
                                            print(f"{turn + 2}.{opp_move}")
                                            opp_move = board.parse_san(opp_move)
                                            board.push(opp_move)
                                        except Exception as e:
                                            print(f"Error parsing opponent move after black: {e}")
                                            pygame.quit()
                                            sys.exit()

                                turn += 1
                            else:
                                print("Wrong move!")
                                print(f"Right move: {expected_move}")
                                try:
                                    correct_move = board.parse_san(expected_move)
                                    if board.is_castling(correct_move):
                                        # For black: king starts on e8, for white: e1
                                        highlighted_square = chess.E8 if color == 1 else chess.E1
                                    else:
                                        highlighted_square = correct_move.from_square if color == 0 else 63 - correct_move.from_square
                                except Exception as e:
                                    print(f"Error highlighting correct piece: {e}")
                                    highlighted_square = selected_square  # fallback

                                board = move_start.copy()
                                draw_board(screen, highlighted_square)
                                draw_pieces(screen, board, color)
                                pygame.display.flip()
                                pygame.time.wait(1000)
                                highlighted_square = None
                        else:
                            print("Illegal move!")
                    except ValueError:
                        print("Invalid move!")
                    except IndexError:
                        raise ValueError(f"Please complete this opening: {move_sequence}")
                    selected_square = None

        if (color == 0 and (turn * 2 - 1) == len(move_sequence)) or (color == 1 and turn * 2 == len(move_sequence)):
            print("You passed!.")
            draw_board(screen, highlighted_square)
            draw_pieces(screen, board, color)
            pygame.display.flip()
            clock.tick(30)
            input("Press enter to exit: ")
            pygame.time.wait(1000)
            pygame.quit()
            sys.exit()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    version = 1
    filename, number_of_openings, move_sequence, rand_choice = select_random_opening(
        white_file=Path(f"white_{version}.txt"), black_file=Path(f"black_{version}.txt"))

    print("Welcome to the custom chess opening drilling app")
    print("Start drilling now")
    print(f"You are  {str(filename)[:-4]}, make your move")

    for i in range(len(move_sequence) // 2 + 1):
        main(move_sequence, color=rand_choice)
