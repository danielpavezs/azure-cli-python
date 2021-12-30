import sys
from azVMClone import idOrNot
from printMessage import printHead

def main():
    #prints the main menu, and asks the user for an option
    printHead(1)
    opt = input("Select the number of the task you want to do: ")
    while True:
        #validates the input
        try:
            val = int(opt)
            if 0 < val < 3:
                break
            else:
                opt = input("\nSorry, invalid selection. Try again: ")
        except ValueError:
            opt = input("\nSorry, invalid selection. Try again: ")
    if val == 1:
        #calls the main cloning function
        idOrNot()
    else:
        print("See you around!\n\n")
        sys.exit(0)

if __name__ == "__main__":
    main()