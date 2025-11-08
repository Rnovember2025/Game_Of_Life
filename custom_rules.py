"""Some other fun alternative rules to run in Game of Life Simulator"""

def Maze_Rules(cell_data):
    total_alive = sum(cell_data)
    
    if (not cell_data[4]) and total_alive == 3:
        return True
    elif cell_data[4] and (1 <= total_alive-1 <= 5):
        return True
    else:
        return False

def Gavins_Rules(cell_data):
    total_alive = sum(cell_data)
    if (not cell_data[4]) and total_alive == 4:
        return True
    elif (not cell_data[4]) and total_alive == 0:
        return True
    elif cell_data[4] and total_alive > 5:
        return False
    elif cell_data[4]:
        return True
    else: return False

def Kenons_Rules(cell_data):
    total_alive = sum(cell_data)
    if cell_data[4]:
        if total_alive == 1:
            return False
        elif 2 <= total_alive <= 3:
            return True
        elif total_alive > 3:
            return False
        else:
            return False
    else:
        if total_alive == 2:
            return True
       
