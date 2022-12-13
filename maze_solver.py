""" File: maze_solver.py
    Author: Aiden Foster
    Class: CSC 120
    Purpose: To recieve a file from the user, check if it is valid
             and then solve the maze and do what the user asks
"""

class TreeNode:
    """ This class resprsents the logistical processing behind creating
        the objects with the references

        The constructor creates the variables that we can use to know
        if there is a part of maze up, down, left, or right.
    """
    def __init__(self, cords):
        self.val = cords
        self.up = None
        self.down = None
        self.left = None
        self.right = None      

def main():
    """ This file runs all of the functions that support this
        code. It creates the tree then does what the command asks.
    """
    # open the file and check of the maze is correct format
    file = input()
    if not file_map_check(file):
        exit()
        # ask the user for the comamand
    command = input()
    # create the cells list, and keep track of start and end cell
    cells_lst,start,end = cells(file)
    # create tree root and start of set
    root = TreeNode(start)
    done = set()
    done.add(start)
    root = create_tree(cells_lst,start,done,root)
    # run the command check function that will do what the user wants
    command_check(command, cells_lst,start,end,root,file)

def command_check(command,cells_lst,start,end,root,file):
    """ This checks the command and runs what it is supposed to run.
        command: this is the command the user gave
        cells_lst: a list of all the cells
        start: the start cell
        end: the end cell
        root: the start cell as the root of a tree
        file: the file the user gave
    """
    comands_allowed = ['dumpTree','dumpCells','dumpSolution','dumpSize', '']
    if command not in comands_allowed:
        print(f'ERROR: Unrecognized command {command}')
    else:
        # dumpTree
        if command == 'dumpTree':
            print('DUMPING OUT THE TREE THAT REPRESENTS THE MAZE:')
            dump_tree(root,space = '  ')

        # dumpCells
        if command == 'dumpCells':
            print('DUMPING OUT ALL CELLS FROM THE MAZE:')
            dump_cells(cells_lst,start,end)

        # dumpSolution
        if command == 'dumpSolution':
            path = []
            dump_solution(root,start,end,path)
            print('PATH OF THE SOLUTION:')
            for cell in path:
                print(f'  {cell}')

        # dumpSize
        if command == 'dumpSize':
            max_x = 0
            max_y = 0
            for tuples in cells_lst:
                # find max values
                if tuples[0] > max_x:
                    max_x = tuples[0]
                if tuples[1] > max_y:
                    max_y = tuples[1]
            print('MAP SIZE:')
            print(f'  wid: {max_x + 1}')
            print(f'  hei: {max_y + 1}')

        # print out the solution
        if command == '':
            path = []
            # create the cells list that is the path
            dump_solution(root,start,end,path)
            # print new maze with path more clear 
            new_cells(path[1:-1],file)

def dump_solution(root,start,end,path):
    """ This is a recursive function that searches for the path
        to the end.
        root: the root of the tree
        start: the starting cell
        end: the end cell
        path: a list that we will append the path too
        return: this returns the path of the completed maze
    """
    if root is None:
        return
    if root.val == end:
        path.append(root.val)
        return
    else:
        path.append(root.val)
        # check everytime if you hit the end or not, cause 
        # if not then you need to keep recursing
        if path[-1] != end:
            dump_solution(root.up,start,end,path)
        if path[-1] != end:
            dump_solution(root.down,start,end,path)
        if path[-1] != end:
            dump_solution(root.left,start,end,path)
        if path[-1] != end:
            dump_solution(root.right,start,end,path)
        # if you didn't hit the end that get rid of that cell
        if path[-1] != end:
            path.pop(-1)
    return path
    
def dump_cells(cells_lst,start,end):
    """ This prints all of the cells from the maze.
        cells_lst: a list of all the possible cells
        start: the starting cell
        end: the end cell
    """
    # print all the cells in order
    for cell in sorted(cells_lst):
        if cell == start:
            print(f'  {cell}    START')
        elif cell == end:
            print(f'  {cell}    END')
        else:
            print(f'  {cell}')

def dump_tree(root, space):
    """ This prints out the tree in a format that is easy
        to read.
        root: the root of the tree
        space: the amount of space we will change with each
               call
    """
    # print the tree in an easy to visualize way
    if root is None:
        return None
    else:
        print(f'{space}{root.val}')
        dump_tree(root.up,space + '| ')
        dump_tree(root.down,space + '| ')
        dump_tree(root.left,space + '| ')
        dump_tree(root.right,space + '| ')

def create_tree(cells_lst,start,done,root):
    """ A function that creates a tree based on the cells.
        cells_lst: a list of all the cells
        start: the starting cell
        done: a list for the completed cells
        root: the root of the tree we will add too
        return: the root of the tree so we can use it in 
                other functions
    """
    # create tree with root being the cords of start
    x = start[0]
    y = start[1]
    root = TreeNode(start)
    if len(done) != len(cells_lst):
        # up
        # make sure it is in cell list every time
        if (x,y-1) in cells_lst:
            # make sure you haven't done anything with it yet
            if (x,y-1) not in done:
                done.add((x,y-1))
                root.up = create_tree(cells_lst,(x,y-1),done,root)
        # down
        if (x,y+1) in cells_lst:
            if (x,y+1) not in done:
                done.add((x,y+1))  
                root.down = create_tree(cells_lst,(x,y+1),done,root)
        # left
        if (x-1,y) in cells_lst:
            if (x-1,y) not in done:
                done.add((x-1,y))
                root.left = create_tree(cells_lst,(x-1,y),done,root)
        # right
        if (x+1,y) in cells_lst:
            if (x+1,y) not in done:
                done.add((x+1,y))
                root.right = create_tree(cells_lst,(x+1,y),done,root)
        return root
    # return the root node
    return root

def cells(file):
    """ This function obtains all of the cells to make a list.
        file: the name of the file the user gave
    """
    file = open(file, 'r')
    lines = file.readlines()
    cells = []
    x = 0
    y = 0
    start = None
    end = None
    # create the cells and return a list of them
    for line in lines:
        for symbol in line:
            if symbol == '#':
                cells.append((x,y))
            elif symbol == 'S':
                cells.append((x,y))
                start = (x,y)
            elif symbol == 'E':
                cells.append((x,y))
                end = (x,y)
            x += 1
        y += 1
        x = 0
    file.close()
    return cells,start,end

def file_map_check(file):
    """ This ensures the file is one we can use and doesn't
        have any errors.
        file: the name of the file the user gave
        return: this will return a boolean that will determine
                if the file will keep running or not
    """
    # make sure file exists
    try:
        file = open(file, 'r')
    except FileNotFoundError:
        print(f'ERROR: Could not open file: {file}')
        return False
    lines = file.readlines()
    s_count = 0
    e_count = 0
    allowed = ['#','E','S',' ','\n']
    for line in lines:
        for letter in line:
            # check if the letter is allowed
            if letter not in allowed:
                print('ERROR: Invalid character in the map')
                file.close()
                return False
            elif letter == 'E':
                e_count += 1
            elif letter == 'S':
                s_count += 1
    # make sure the start and end is in it once and only once
    if e_count < 1:
        print('ERROR: Every map needs exactly one START \
            and exactly one END position')
        file.close()
        return False
    if s_count < 1:
        print('ERROR: Every map needs exactly one START \
            and exactly one END position')
        file.close()
        return False
    if e_count > 1:
        print('ERROR: The map has more than one END position')
        file.close()
        return False
    if s_count > 1:
        print('ERROR: The map has more than one START position')
        file.close()
        return False
    file.close()
    return True

def new_cells(path,file):
    """ This prints out the new maze with the completed cells.
        path: this is a list of the path to complete the file
        file: the name of the file the user gave us
    """
    file = open(file, 'r')
    lines = file.readlines()
    list = []
    # go through the file, make a new maze, and change the path
    # change them to a '.' so it is easy to see for the user
    for line in lines:
        line = line.strip('\n')
        second = []
        for letter in line:
            second.append(letter)
        list.append(second)
    for cells in path:
        x = cells[0]
        y = cells[1]
        list[y].pop(x)
        list[y].insert(x,'.')
    print()
    # print it 
    print('SOLUTION:')
    for row in list:
        row = ''.join(row)
        print(row)

if __name__=="__main__":
    main()