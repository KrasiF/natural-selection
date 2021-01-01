from evoltuion import Organism, Environment

def welcome():
    print("Welcome to my simulation of evolution/natural selection!")
    print("Let's start by creating an environment.")

def successful_creation():
    print("Environment created!")
    print("Press enter to do a single evolutionary step.")
    print("Type \"help\" for all commands.")

def list_commands():
    print("Type \"temp\", \"hum\", \"afsbig\", \"afssmall\", \"vfsbig\" or \"vfssmall\" followed by a number in order to set a new value for the corresponding environment stat. ")
    print("Type \"biome\" followed by either \"plains\", \"mountains\" or \"desert\" in order to change the biome.")
    print("Type \"envir\" in order to see the stats of the environment.")
    print("Type \"showgenome\" in order to see genes of every single organism in the environment.")
    print("Type \"stop\" to terminate the program.")

def get_temp():
    print("Enter the temperature of the environment from -6 to 6")
    return get_number_in_range(-6,6)

def get_humidity():
    print("Enter the humidity of the environment from 0.2 to 8")
    return get_number_in_range(0.2,8)

def get_biome():
    print("Select the biome for the environment: \"plains\", \"desert\" or \"mountains\":")
    inp = input()

    while True:
        if inp == "plains" or inp == "desert" or inp == "mountains":
            return inp
        else:
            print("Invalid input!")
        inp = input()        

def get_vfs_small():
    print("Enter the amount of small vegetation in the environment from 0 to 8.8")
    return get_number_in_range(0,8.8)

def get_vfs_big():
    print("Enter the amount of large vegetation in the environment from 0 to 8.8")
    return get_number_in_range(0,8.8)

def get_afs_small():
    print("Enter the amount of small animals in the environment from 0 to 8.8")
    return get_number_in_range(0,8.8)

def get_afs_big():
    print("Enter the amount of large animals in the environment from 0 to 8.8")
    return get_number_in_range(0,8.8)

def get_number_in_range(lower,upper):
    num = None

    while num is None:
        inp = input()
        try:
            float(inp)
        except:
            print("Invalid input!")
            continue
        num = float(inp)
        if(num < lower or num > upper):
            num = None
            print("Invalid input!")
    return num

def get_environment():
    temp = get_temp()
    hum = get_humidity()
    biome = get_biome()
    vfs_small = get_vfs_small()
    vfs_big = get_vfs_big()
    afs_small = get_afs_small()
    afs_big = get_afs_big()
    environemt = Environment(temp,hum,biome,vfs_small,vfs_big,afs_small,afs_big,100,10)
    return environemt

def loop(environment):
    while(True):
        command = input().split(" ")
        if command[0] == "showgenome":
            environment.show_population_genes()
        elif command[0] == "temp":
            environment.temp = float(command[1])
        elif command[0] == "hum":
            environment.hum = float(command[1])
        elif command[0] == "biome":
            environment.biome = command[1]
        elif command[0] == "envir":
            print("E temp: " + str(environment.temp) + " hum: " + str(environment.hum)+ " biome: " + str(environment.biome) + " afs_big: " + str(environment.afs_big) + " afs_small: " + str(environment.afs_small) + " vfs_big: " + str(environment.vfs_big) + " vfs_small: " + str(environment.vfs_small))
        elif command[0] == "afsbig":
            environment.afs_big = float(command[1])
        elif command[0] == "afssmall":
            environment.afs_small = float(command[1])
        elif command[0] == "vfsbig":
            environment.vfs_big = float(command[1])
        elif command[0] == "vfssmall":
            environment.vfs_big = float(command[1])
        elif command[0] == "stop":
            break
        elif command[0] == "help":
            list_commands()
        else:
            environment.evolution_step()

def run():
    welcome()    
    environment = get_environment()
    successful_creation()
    loop(environment)

run()