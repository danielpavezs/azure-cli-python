from os import system

#prints the program header to show the selected path made by the user
def printHead(mess):
    if int(mess) == 1:
        system('clear')
        print("\n###################################\n# VMs CREATION & CLONING IN AZURE #\n###################################\n\n1 - Clone an entire VM\n2 - Exit\n")
    elif int(mess) == 2:
        system('clear')
        print("\n##########################################################\n# VMs CREATION & CLONING IN AZURE ## Clone an entire VM ##\n##########################################################\n")
    elif int(mess) == 3:
        system('clear')
        print("\n#########################################################################\n# VMs CREATION & CLONING IN AZURE ## Clone an entire VM ## Using VM Id ##\n#########################################################################\n")
    elif int(mess) == 4:
        system('clear')
        print("\n###########################################################################\n# VMs CREATION & CLONING IN AZURE ## Clone an entire VM ## Without VM Id ##\n###########################################################################\n\n")
    else:
        system('clear')
        print("\n##########################################################\n# VMs CREATION & CLONING IN AZURE ## Clone an entire VM ##\n##########################################################\n")