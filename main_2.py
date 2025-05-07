import os
import time
from pathlib import Path
import chess
import chess.svg
from helper_functions import select_random_opening, print_moves_white, print_moves_black


import pygame
import chess
import sys

# Constants
WIDTH, HEIGHT = 640, 640
SQ_SIZE = WIDTH // 8
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
PIECE_IMAGES = {}

# Load local images
def load_images():
    pieces = ['p', 'r', 'n', 'b', 'q', 'k']
    for color in ['w', 'b']:
        for piece in pieces:
            filename = f"assets/{color}{piece}.png"
            image = pygame.image.load(filename)
            PIECE_IMAGES[f"{color}{piece}"] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))

def draw_board(screen):
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
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

def main(move_sequence, color: int):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess GUI")
    clock = pygame.time.Clock()
    board = chess.Board()

    load_images()

    running = True
    turn = 0
    while running:
        draw_board(screen)
        draw_pieces(screen, board, color)
        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        if (color == 0 and turn * 2 == len(move_sequence)) or (color == 1 and turn * 2 == len(move_sequence) - 1):
            raise ValueError(
                f"Incomplete opening! Please find this opening, run stockfish and complete the line. {turn=} {move_sequence=}")
        if color == 1:
            try:
                opp_move = move_sequence[2 * turn]
                print(f"{turn + 1}.{opp_move}")
                opp_move = board.parse_san(opp_move)
                board.push(opp_move)
                draw_board(screen)
                draw_pieces(screen, board, color)
                pygame.display.flip()
            except:
                input("You passed! Press enter to quit")
                pygame.quit()
                sys.exit()

        move_input = input("Enter your move: ")

        while move_sequence[(turn * 2) + color] != move_input:
            print("Wrong move, try again!")
            print(f"Right move: {move_sequence[(turn * 2) + color]}")
            move_input = input("Enter your move: ")
        try:
            move = board.parse_san(move_input)
            board.push(move)
        except ValueError:
            print("Illegal or invalid move.")
        print(f"{turn + 1}.{move_input}")
        if not color:
            try:
                opp_move = move_sequence[2 * turn + 1]
                print(f"{turn + 1}...{opp_move}")
                opp_move = board.parse_san(opp_move)
                board.push(opp_move)
            except:
                if (turn * 2) + 1 != len(move_sequence):
                    raise ValueError(f"{turn=} {len(move_sequence)=}")
                draw_board(screen)
                draw_pieces(screen, board, color)
                pygame.display.flip()
                input("You passed! Press enter to quit")
                pygame.quit()
                sys.exit()
        turn += 1

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    version = 1

    filename, number_of_openings, move_sequence, rand_choice = select_random_opening(white_file=Path(f"white_{version}.txt"), black_file=Path(f"black_{version}.txt"))
    print("Welcome to the custom chess opening drilling app")
    print("Start drilling now")
    print(f"You are  {str(filename)[:-4]}, make your move")

    for i in range(len(move_sequence)//2 + 1):
        main(move_sequence, color=rand_choice)




