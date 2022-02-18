import random


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
move_sequence = myarray[random.randint(0, number_of_openings-1)]


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
    except:
        print("You pass!")
    move = input("Enter your move: ")
    while move_sequence[turn*2 + 1] != move:
        print("Wrong move, try again!")
        print(f"Right move: {move_sequence[turn * 2 + 1]}")
        move = input("Enter your move: ")
    print(f"{turn+1}.{move}")



print("Welcome to the custom chess opening drilling app")
print("Press enter to start drilling")
input()
print(f"You are  {filename[:-4]}, make your move")
for i in range(len(move_sequence)//2 + 1):
    if rand_choice == 0:
        print_moves_white(i, move_sequence)
    elif rand_choice == 1:
        print_moves_black(i, move_sequence)



