from typing import Tuple
import random

def select_random_opening() -> Tuple[str, int, str]:
    """Select a random opening"""
    rand_choice = random.choice([0, 1])
    if rand_choice == 0:
        filename = "white.txt"
    elif rand_choice ==1:
        filename = "black.txt"
    myarray = list()

    with open(filename) as file:
        for line in file:
            myarray.append(line.rstrip().split())
    number_of_openings = len(myarray)
    move_sequence = myarray[random.randint(0, number_of_openings - 1)]
    return filename, number_of_openings, move_sequence, rand_choice




def print_moves_white(turn, move_sequence):
    move = input("Enter your move: ")
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
