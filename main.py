from interface import *
from custom_rules import *
from random import randint
from fun_start_states import *
#from queue import Queue
from multiprocessing import Process, Queue


""" To Do
[ ] step_simulation function in its own thead (to increase performance)
[ ] erase yellow cells by clicking on them
[ ] Framerate spinbox actually control framerate

"""

class simulate:
    def __init__(self, rule_function):
        self.queue = Queue()
        self.evaluate = rule_function
        self.thread = Process()

    def add(self, state):
        if not self.thread.is_alive():
            self.thread.close()
            self.thread = Process(target=self._simulate, args=(state,))
            self.thread.start()
        # if not busy, start a thread to step the simulation
        # set busy flag to True

    def get(self):
        if self.queue.qsize():
            try:
                return self.queue.get(0)
            except:
                pass
        return False
        # if there is anything in the queue, return it, else
        # return false

    def _simulate(self, state):        
        # Find all cells (alive and dead) that need to be checked
        cells_to_check = dict.fromkeys(state,1)
        for cell in state:
            for x in range(cell[0]-1,cell[0]+2):
                for y in range(cell[1]-1,cell[1]+2):
                    cells_to_check.setdefault((x,y),False)

        # Loop through every cell, evaluate it according to the rule_class
        alive_cells = []
        for cell in cells_to_check:
            grid = [cells_to_check.get((x,y),False) \
                    for x in range(cell[0]-1,cell[0]+2) \
                    for y in range(cell[1]-1,cell[1]+2)]
                
            if self.evaluate(grid) == True:
                alive_cells.append(cell)
        
        self.queue.put(alive_cells)
        # put result into queue
        # set busy flag to False

def make_random_state(width,center_point,density_percent):
    """Returns list of tuples, each with an x and y coordinate.
    All x an y coordinates are within a square centered at <center_point>
    with a width of <width>.
    The amount of tuples in the list is determined by <density_percent>"""
    
    state = []
    center_x = center_point[0]
    center_y = center_point[1]
    while len(state) < (width**2)*(density_percent/100):
        cell = (randint(center_x-(width//2),center_x+(width//2)),
                randint(center_y-(width//2),center_y+(width//2)))
        if not cell in state:
            state.append(cell)
    return state

def Conways_Rules(cell_data):
    """
    Returns True if cell at center of cell_data survive,
    else False (according to the rules of Conway's Game of Life).
    """
    if cell_data[4] == 1:
        return 3 <= sum(cell_data) <= 4
    else:
        return sum(cell_data) == 3


def step_simulation(state, rule_class):        
    # Find all cells (alive and dead) that need to be checked
    cells_to_check = dict.fromkeys(state,1)
    for cell in state:
        for x in range(cell[0]-1,cell[0]+2):
            for y in range(cell[1]-1,cell[1]+2):
                cells_to_check.setdefault((x,y),False)

    # Loop through every cell, evaluate it according to the rule_class
    state.clear()
    for cell in cells_to_check:
        grid = [cells_to_check.get((x,y),False) \
                for x in range(cell[0]-1,cell[0]+2) \
                for y in range(cell[1]-1,cell[1]+2)]
            
        if rule_class(grid) == True:
            state.append(cell)


def parse_rfe(rfe_string_or_file):
    """Read either a .rfe file, or a string of characters in rfe format.
        Returns a list of coordinates"""
    try:
        file = open(rfe_string_or_file)
        data = file.readlines()
        file.close()

        rfe_string_or_file = ''
        started = False
        for line in data:
            if started:
                rfe_string_or_file+=line
            if line[0] == 'x':
                started = True
    except:
        pass
            
    state = []
    x_pointer = 0
    y_pointer = 0
    digit = ''
    for char in rfe_string_or_file:
        if char.isdigit():
            digit+=char
            continue
        elif char == 'o':
            if digit == '': digit = '1'
            segment = []
            for i in range(int(digit)):
                segment.append((x_pointer,y_pointer))
                x_pointer += 1
            digit = ''
            state.extend(segment)
        elif char == 'b':
            if digit == '': digit = '1'
            x_pointer += int(digit)
            digit = ''
        elif char == '$':
            if digit == '': digit = '1'
            y_pointer+= int(digit)
            x_pointer=0
            digit=''
        elif char == '!':
            break
    return state

def main():    
    def initialize(state):
        state.clear() #for a blank canvas
        state[:] = parse_rfe('/media/wizard/RONAN DRIVE/Documents/Colledge/Fall 2024/Classes/CSE_111/Visual Sudio/CSE111/Final_Project/all/p690bigagun.rle')

    state = []
    initialize(state)
    origional_state = state[:]

    interface = GUI()
    interface.draw(state)

    def runtime_code():
        status = interface.is_simulation_running()
        if status:
            if status == 1:
                step_simulation(state, Conways_Rules)
            elif status == 2:
                state[:] = origional_state[:]
            elif status == 3:
                initialize(state)
                origional_state[:] = state[:]
            interface.draw(state)

        edited_cells = interface.get_edited_cells()
        if edited_cells:
            state.extend(edited_cells)
            origional_state[:] = state[:]
        
        interface.update_framerate(other_data=len(state)) #other_data can be anything you want to display
        interface.schedule(runtime_code)

    runtime_code()
    interface.loop()

if __name__ == '__main__':
    main()

