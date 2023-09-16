import os
import time
import random
from collections import deque

# Constants for game elements
RABBIT = 'r'
RABBIT_WITH_CARROT = 'R'
RABBIT_HOLE = 'O'
CARROT = 'c'
PATHWAY_STONE = '-'

# Initialize the game grid
def initialize_grid(size):
    grid = [['-' for _ in range(size)] for _ in range(size)]
    return grid

# Place game elements (rabbit, rabbit holes, carrots) randomly on the grid
def place_elements(grid, num_carrots, num_rabbit_holes):
    size = len(grid)
    for _ in range(num_rabbit_holes):
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        grid[x][y] = RABBIT_HOLE

    for _ in range(num_carrots):
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        while grid[x][y] != PATHWAY_STONE:
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        grid[x][y] = CARROT

    rabbit_x, rabbit_y = random.randint(0, size - 1), random.randint(0, size - 1)
    while grid[rabbit_x][rabbit_y] != PATHWAY_STONE:
        rabbit_x, rabbit_y = random.randint(0, size - 1), random.randint(0, size - 1)
    grid[rabbit_x][rabbit_y] = RABBIT

    return grid, rabbit_x, rabbit_y

# Display the game grid
def display_grid(grid):
    size = len(grid)
    for x in range(size):
        for y in range(size):
            print(grid[x][y], end='  ')
        print('\n')


# Move the rabbit and update the grid
def move_rabbit(grid, rabbit_x, rabbit_y, direction, size):
    size = len(grid)
    
    # Dictionary of coordinate changes for each direction
    direction_changes = {
        'w': (-1, 0),
        's': (1, 0),
        'a': (0, -1),
        'd': (0, 1),
        'wa': (-1, -1),
        'wd': (-1, 1),
        'sa': (1, -1),
        'sd': (1, 1),
        'aw': (-1, -1),
        'dw': (-1, 1),
        'as': (1, -1),
        'ds': (1, 1),
    }

    # Calculate the new coordinates based on the direction
    dx, dy = direction_changes.get(direction, (0, 0))
    new_x, new_y = (rabbit_x + dx + size) % size, (rabbit_y + dy + size) % size

    # Rabbit doesn't move
    if new_x == rabbit_x and new_y == rabbit_y:
        return rabbit_x, rabbit_y

    # Check if the new cell is a valid move
    if grid[new_x][new_y] != CARROT and grid[new_x][new_y] != RABBIT_HOLE:

        if grid[rabbit_x][rabbit_y] == RABBIT_WITH_CARROT:
            grid[new_x][new_y] = RABBIT_WITH_CARROT
        else:
            grid[new_x][new_y] = RABBIT

        grid[rabbit_x][rabbit_y] = '-'
        rabbit_x, rabbit_y = new_x, new_y

    return rabbit_x, rabbit_y


def findShortestPath(matrix):
    size = len(matrix)
    
    def bfs(start, end):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        diagonals = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        visited = [[False] * size for _ in range(size)]
        parent = [[None] * size for _ in range(size)]  # Store parent coordinates
        queue = deque([(start[0], start[1], 0)])  # (x, y, steps)
        visited[start[0]][start[1]] = True
        
        while queue:
            x, y, steps = queue.popleft()
            
            if (x, y) == end:
                # Reconstruct the path
                path = []
                while (x, y) != start:
                    path.append((x, y))
                    x, y = parent[x][y]
                path.append(start)
                path.reverse()
                return path
            
            for dx, dy in directions:
                nx, ny = (x + dx + size) % size, (y + dy + size) % size  # Wrap around the grid

                # No diagonal movement if diagonal cell is not '-'
                if (dx, dy) in diagonals and matrix[nx][ny] != PATHWAY_STONE:
                    continue

                # Check for Hole, and '-' on the other side
                if matrix[nx][ny] == RABBIT_HOLE:
                    # Coordinates on the other side of the hole
                    nx2, ny2 = (nx + dx + size) % size, (ny + dy + size) % size      
                    if matrix[nx2][ny2] == RABBIT_HOLE and (dx, dy) not in diagonals: 
                        nx, ny = nx2, ny2
                
                if not visited[nx][ny]:
                    queue.append((nx, ny, steps + 1))
                    visited[nx][ny] = True
                    parent[nx][ny] = (x, y)
        
        return [] 
    
    shortest_path = []
    
    start_r = None
    hole_coords = []
    
    for i in range(size):
        for j in range(size):
            if matrix[i][j] == RABBIT:
                start_r = (i, j)
            elif matrix[i][j] == RABBIT_HOLE:
                hole_coords.append((i, j))
    
    if start_r is None or not hole_coords:
        return []
    
    for end_e in hole_coords:
        shortest_rc = []
        shortest_ce = []
        shortest_distance = float('inf')
        
        for i in range(size):
            for j in range(size):
                if matrix[i][j] == CARROT:
                    # Shortest path from 'R' to 'C'
                    current_rc = bfs(start_r, (i, j))
                    
                    if not current_rc:
                        continue
                    
                    # Shortest path from 'C' to 'E'
                    current_ce = bfs((i, j), end_e)
                    
                    if not current_ce:
                        continue
                    
                    current_distance = len(current_rc) + len(current_ce) - 1
                    
                    if current_distance < shortest_distance:
                        shortest_distance = current_distance
                        shortest_rc = current_rc
                        shortest_ce = current_ce[1:]
        
        if shortest_rc and shortest_ce:
            total_path = shortest_rc + shortest_ce
            if len(shortest_path) == 0 or len(total_path) < len(shortest_path):
                shortest_path = total_path
    
    if not shortest_path:
        return []
    
    return shortest_path 

# Clear console
def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear') 

# Function to simulate the shortest path on the grid
def simulateShortestPath(path, matrix, grid_og):
    size = len(matrix)
    new_grid = [['-' for _ in range(size)] for _ in range(size)]

    start_x, start_y = path[0]
    end_x, end_y = path[-1]
    new_grid[start_x][start_y] = 'S'
    new_grid[end_x][end_y] = 'E'


    # Simulate the path step by step
    for step, (x, y) in enumerate(path[1:], start=1):
        new_grid[x][y] = str(step)
        clearConsole()

        print('Initial grid: ')
        display_grid(grid_og) 
        print()

        print("Simulation of shortest path from 'r' to 'c' to '0': \n")
        printGrid(new_grid)
        time.sleep(1)

# Function to print the grid
def printGrid(grid):
    for row in grid:
        print(" ".join(row))
    print()

# Function to print the Instructions
def printInstructions():
    print("\nHow to  play?")
    print("  You are rabbit(r). Collect a carrot(c) and deposit it in a hole(0).")
    print("  Try to achieve this in the minimum steps possible.")
    print("  After the game ends you will get to know the shortest path possible through a simulation.")

    print('\nEnter "w", "s", "a", "d" to move the rabbit(r) up, down, left and right respectively.')
    print('Enter the combination of above keys to move diagonally in the grid.')
    print('Enter "p" to pick a carrot(c), and to deposit in a hole(0) only when you are adjacent to them.')
    print('Enter "j" to jump across a hole(0). You cannot jump diagonally.')
    print('Enter "q" to quit.')


# Function to take input and validate them
def takeValidInput():
    size = int(input("Enter the size of the grid (0 < size <= 30): "))
    if size <= 0 or size > 30:
        print('Please enter valid size value.')
        time.sleep(2)
        clearConsole()
        takeValidInput()

    num_carrots = int(input(f"Enter the number of carrots (0 < num_carrots < {size*size}): "))
    if num_carrots <= 0 or num_carrots >= size * size:
        print('Please enter valid carrots value.')
        time.sleep(2)
        clearConsole()
        takeValidInput()
    
    num_rabbit_holes = int(input(f"Enter the number of rabbit holes (0 < num_holes < {size*size - num_carrots}): "))
    if num_rabbit_holes <= 0 or num_rabbit_holes >= size*size - num_carrots:
        print('Please enter valid holes value.')
        time.sleep(2)
        clearConsole()
        takeValidInput()

    return size, num_carrots, num_rabbit_holes


# Function to pick carrot or deposit carrot
def pickCarrot(grid, rabbit_x, rabbit_y, size, won):
    adjacent_cells = [
        (rabbit_x - 1, rabbit_y),
        (rabbit_x + 1, rabbit_y),
        (rabbit_x, rabbit_y - 1),
        (rabbit_x, rabbit_y + 1),
    ]

    for x, y in adjacent_cells:
        x, y = (x + size) % size, (y + size) % size 
        if grid[x][y] == CARROT and grid[rabbit_x][rabbit_y] != RABBIT_WITH_CARROT:
            grid[x][y] = RABBIT_WITH_CARROT
            grid[rabbit_x][rabbit_y] = PATHWAY_STONE
            rabbit_x = x
            rabbit_y = y
            break
        elif grid[x][y] == RABBIT_HOLE and grid[rabbit_x][rabbit_y] == RABBIT_WITH_CARROT:
            grid[rabbit_x][rabbit_y] = PATHWAY_STONE
            won = True
            break

    return rabbit_x, rabbit_y, won

# Function to jump over the hole
def jumpOverHole(grid, rabbit_x, rabbit_y, size):
    adjacent_cells = [
        (rabbit_x - 1, rabbit_y),
        (rabbit_x + 1, rabbit_y),
        (rabbit_x, rabbit_y - 1),
        (rabbit_x, rabbit_y + 1),
    ]
    
    for x, y in adjacent_cells:
        x, y = (x + size) % size, (y + size) % size 
        nx, ny = (2*x - rabbit_x + size) % size, (2*y - rabbit_y + size) % size
        if grid[x][y] == RABBIT_HOLE and grid[nx][ny] == PATHWAY_STONE:
            grid[nx][ny] = grid[rabbit_x][rabbit_y]
            grid[rabbit_x][rabbit_y] = PATHWAY_STONE
            rabbit_x = nx
            rabbit_y = ny
            break
        
    return rabbit_x, rabbit_y


# Main game loop
def main():
    clearConsole()

    won = False
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    valid_movements = ['w', 's', 'a', 'd', 'wa', 'aw', 'wd', 'dw', 'sa', 'as', 'sd', 'ds']

    #Take and validate input
    size, num_carrots, num_rabbit_holes = takeValidInput()
    print()

    grid, rabbit_x, rabbit_y = place_elements(initialize_grid(size), num_carrots, num_rabbit_holes)
    grid_og = [row[:] for row in grid]
    shortest_path = findShortestPath(grid)

    while not won:
        display_grid(grid)
        
        printInstructions() 
        direction = input("\nEnter an action (a/w/d/s/p/j) :")

        if direction == 'q': 
            print("You Quit the game!")
            exit(0)

        elif direction == 'p':
            # Rabbit tries to pick up a carrot or deposit a carrot into a hole
            rabbit_x, rabbit_y, won = pickCarrot(grid, rabbit_x, rabbit_y, size, won)

        elif direction == 'j':
            # Rabbit tries to jump over a hole
            rabbit_x, rabbit_y = jumpOverHole(grid, rabbit_x, rabbit_y, size)

        elif direction in valid_movements:
            # Rabbit moves in the specified direction
            rabbit_x, rabbit_y = move_rabbit(grid, rabbit_x, rabbit_y, direction, size)


        clearConsole()
        print(f"Enter the size of the grid (0 < size <= 30): {size}")
        print(f"Enter the number of carrots (0 < num_carrots < {size*size}): {num_carrots}")
        print(f"Enter the number of rabbit holes (0 < num_holes < {size*size - num_carrots}): {num_rabbit_holes}\n")

    display_grid(grid) 

    clearConsole()
    print("Game Finished.")
    print("Wait for the answer...")
    time.sleep(3)   

    if not shortest_path:
        print("No valid path")
        exit(0)

    # Simulate the shortest path
    simulateShortestPath(shortest_path, grid, grid_og)
    
    print("Shortest path from 'r' to 'c' to 'O':")
    print('"S" is the starting position of rabbit(r) and "E" is the ending position.')
    for x, y in shortest_path:
        print(f"({x}, {y})", end=" ")
    print(f': {len(shortest_path)-1} steps')


if __name__ == "__main__":
    main()
