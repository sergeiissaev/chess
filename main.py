
from helper_functions import select_random_opening, print_moves_white, print_moves_black

if __name__ == "__main__":

    filename, number_of_openings, move_sequence, rand_choice = select_random_opening()
    print("Welcome to the custom chess opening drilling app")
    print("Start drilling now")
    print(f"You are  {filename[:-4]}, make your move")

    for i in range(len(move_sequence)//2 + 1):
        if rand_choice == 0:
            print_moves_white(i, move_sequence)
        elif rand_choice == 1:
            print_moves_black(i, move_sequence)



