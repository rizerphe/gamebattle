maze = [[]]
maze1 = [["0", "*", "*", "*", "x", "x", "*", "*", "*", "x", "x",\
"x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x"],
["*", "x", "x", "*", "*", "*", "*", "x", "*", "*", "*",\
"*", "*", "*", "x", "x", "x", "x", "x", "x", "x", "x"],
["*", "x", "x", "x", "*", "x", "*", "x", "x", "*", "x",\
"x", "x", "x", "x", "x", "x", "*", "x", "*", "*", "x"],
["*", "x", "x", "x", "*", "x", "*", "x", "x", "*", "x",\
"x", "x", "x", "*", "*", "*", "*", "x", "x", "x", "x"],
["*", "*", "x", "x", "*", "x", "*", "*", "x", "*", "x",\
"x", "x", "x", "*", "x", "x", "*", "x", "x", "x", "x"],
["*", "x", "x", "*", "*", "x", "x", "x", "x", "*", "*",\
"x", "*", "x", "*", "x", "x", "*", "*", "x", "x", "x"],
["*", "x", "x", "x", "x", "x", "x", "x", "x", "x", "*",\
"*", "*", "*", "*", "x", "x", "x", "*", "*", "*", "x"],
["x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "*",\
"x", "x", "x", "x", "x", "x", "x", "*", "x", "*", "1"]]

maze2 = [["0", "*", "x", "x", "x", "x", "x", "x", "x", "x", "x",\
"x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x"],
["x", "*", "x", "x", "*", "x", "*", "*", "*", "*", "*",\
"x", "x", "x", "x", "x", "x", "x", "x", "*", "x", "x"],
["x", "*", "*", "x", "*", "x", "*", "x", "*", "x", "*",\
"*", "x", "x", "*", "*", "x", "x", "x", "*", "x", "x"],
["x", "x", "*", "*", "*", "x", "*", "x", "*", "x", "x",\
"*", "*", "*", "*", "x", "x", "x", "x", "*", "x", "x"],
["*", "*", "*", "x", "*", "*", "*", "x", "*", "x", "x",\
"*", "x", "x", "x", "x", "x", "x", "x", "*", "*", "*"],
["x", "x", "*", "x", "x", "x", "x", "x", "*", "x", "x",\
"*", "x", "x", "x", "*", "*", "*", "*", "*", "x", "*"],
["x", "x", "*", "x", "x", "x", "x", "*", "*", "x", "x",\
"*", "x", "x", "*", "*", "x", "*", "x", "x", "x", "*"],
["x", "x", "*", "*", "*", "x", "x", "x", "x", "x", "x",\
"*", "*", "*", "*", "x", "x", "*", "*", "*", "x", "1"]]
RULES = "––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––\n|\
 Hello, it is the maze! You must lead zero to one,                  \
|\n| using w(up), a(left), s(down), d(right) keyboard keys.             \
|\n| But if zero go to \"x\" or outside the maze, you will lose one live. \
|\n| You can't move zero back to the previous position.                 \
|\n––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––"
print(RULES)

def swap_down(a, b, maze):
    """
    int -> None
    Swaps element[a][b] with element[a+1][b] in list
    """
    temp = maze[a+1][b]
    maze[a+1][b] = maze[a][b]
    maze[a][b] = temp

def swap_right(a, b, maze):
    """
    int -> None
    Swaps element[a][b] with element[a][b+1] in list
    """
    temp = maze[a][b+1]
    maze[a][b+1] = maze[a][b]
    maze[a][b] = temp

def swap_up(a, b, maze):
    """
    int -> None
    Swaps element[a][b] with element[a-1][b] in list
    """
    temp = maze[a-1][b]
    maze[a-1][b] = maze[a][b]
    maze[a][b] = temp

def swap_left(a, b, maze):
    """
    int -> None
    Swaps element[a][b] with element[a][b-1] in list
    """
    temp = maze[a][b-1]
    maze[a][b-1] = maze[a][b]
    maze[a][b] = temp

def swap_start(a, b, maze):
    """
    int -> None
    Swaps element[a][b] with element[0][0] in list
    """
    temp = maze[0][0]
    maze[0][0] = maze[a][b]
    maze[a][b] = temp

def print_maze(maze):
    """
    list -> None
    Prints all elements of list maze
    """
    for i in range(0, 8):
        for j in range(0, 22):
            if j == 21:
                print(maze[i][j], end = '\n')
            else:
                print(maze[i][j], end = '')

def main():
    losing_flag = 0
    previous_position_row = 0
    previous_position_column = 0
    position_row = 0
    position_column = 0
    flag = 1
    while flag == 1:
        num_maze = input("\nPrint \"1\" or \"2\" to choose the maze\n>>> ")
        if num_maze == "1":
            maze = maze1
            flag += 1
        elif num_maze == "2":
            maze = maze2
            flag += 1
        else:
            print("Print the number correctly")

    while losing_flag < 3:
        print("lives: ", 3-losing_flag)
        print_maze(maze)
        temp_direction = input(">>> ")
        if temp_direction == "s":
            if position_row != 7 and maze[position_row + 1][position_column] == "1":
                print("You won!")
                break
            elif position_row != 7 and\
                maze[position_row + 1][position_column] != "x" and\
                position_row + 1 != previous_position_row:
                swap_down(position_row, position_column, maze)
                previous_position_row = position_row
                previous_position_column = position_column
                position_row += 1
                continue
            else:
                swap_start(position_row, position_column, maze)
                losing_flag += 1
                previous_position_row = 0
                previous_position_column = 0
                position_row = 0
                position_column = 0
                continue
        if temp_direction == "d":
            if position_column != 21 and maze[position_row][position_column + 1] == "1":
                print("You won!")
                break
            elif position_column != 21 and\
                maze[position_row][position_column + 1] != "x" and\
                position_column + 1 != previous_position_column:
                swap_right(position_row, position_column, maze)
                previous_position_column = position_column
                previous_position_row = position_row
                position_column += 1
                continue
            else:
                swap_start(position_row, position_column, maze)
                losing_flag += 1
                previous_position_row = 0
                previous_position_column = 0
                position_row = 0
                position_column = 0
                continue
        if temp_direction == "w":
            if position_row != 0 and maze[position_row - 1][position_column] == "1":
                print("You won!")
                break
            elif position_row != 0 and\
                maze[position_row - 1][position_column] != "x" and\
                position_row - 1 != previous_position_row:
                swap_up(position_row, position_column, maze)
                previous_position_row = position_row
                previous_position_column = position_column
                position_row -= 1
                continue
            else:
                swap_start(position_row, position_column, maze)
                losing_flag += 1
                previous_position_row = 0
                previous_position_column = 0
                position_row = 0
                position_column = 0
                continue
        if temp_direction == "a":
            if position_column != 0 and maze[position_row][position_column - 1] == "1":
                print("You won!")
                break
            elif position_column != 0 and\
                maze[position_row][position_column - 1] != "x" and\
                position_column - 1 != previous_position_column:
                swap_left(position_row, position_column, maze)
                previous_position_column = position_column
                previous_position_row = position_row
                position_column -= 1
                continue
            else:
                swap_start(position_row, position_column, maze)
                losing_flag += 1
                previous_position_row = 0
                previous_position_column = 0
                position_row = 0
                position_column = 0
                continue
    else:
        print("You lose)")
if __name__ == "__main__":
    main()
