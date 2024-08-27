from pathlib import Path
from typing import Tuple
import random

def select_random_opening(white_file: Path, black_file: Path) -> Tuple[str, int, str]:
    """Select a random opening"""
    rand_choice = random.choice([0, 1])
    if rand_choice == 0:
        filename = white_file
    elif rand_choice ==1:
        filename = black_file
    myarray = list()

    with open(filename) as file:
        for line in file:
            myarray.append(line.rstrip().split())

    if filename == black_file:
        unsolved = len([a for a in myarray if len(a)%2==1])
        solved = len([a for a in myarray if len(a)%2==0])
    else:
        unsolved = len([a for a in myarray if len(a)%2==0])
        solved = len([a for a in myarray if len(a)%2==1])
    print(f"Unsolved openings account for: {unsolved} / {solved} = {round(unsolved * 100 / solved)}%")


    number_of_openings = len(myarray)
    move_sequence = myarray[random.randint(0, number_of_openings - 1)]
    return filename, number_of_openings, move_sequence, rand_choice




def print_moves_white(turn, move_sequence):
    move = input("Enter your move: ")
    if turn * 2 == len(move_sequence):
        raise ValueError(f"Incomplete opening! Please find this opening, run stockfish and complete the line. {turn=} {move_sequence=}")
    while move_sequence[turn*2] != move:
        print("Wrong move, try again!")
        print(f"Right move: {move_sequence[turn * 2]}")
        move = input("Enter your move: ")
    print(f"{turn+1}.{move}")
    try:
        print(f"{turn+1}...{move_sequence[2*turn+1]}")
    except:
        print("You passed!")


def print_moves_black(turn, move_sequence):
    if turn * 2 == len(move_sequence) - 1:
        raise ValueError(f"Incomplete opening! Please find this opening, run stockfish and complete the line. {turn=} {move_sequence=}")
    try:
        print(f"{turn + 1}.{move_sequence[2 * turn]}")
        move = input("Enter your move: ")
        while move_sequence[turn * 2 + 1] != move:
            print("Wrong move, try again!")
            print(f"Right move: {move_sequence[turn * 2 + 1]}")
            move = input("Enter your move: ")
        print(f"{turn + 1}.{move}")
    except:
        print("You pass!")
