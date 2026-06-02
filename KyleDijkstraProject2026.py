import pygame
from collections import deque
import heapq

# This is the amount of grids I will be using for the pathfinding visualizer which the width is the window screen and rows so it can be even out which make the square grid.
WIDTH = 800
ROWS = 40

"""
This is the color palette which 
White: When the grid is empty which if the user makes a wall which blocks the path, it is untouch which the node will not be able to pass through it meaning it is not discovered.
Black: When the user makes a wall which blocks the path which the node will not be able to pass through it meaning it is not discovered.
Red: The starting point which the node will start from.
Light Blue: The path which the node will take after it reaches the ending point which is pink.
Pink: The ending point which the node will try to reach.
Lavender: When the node is discovered but not yet evaluated which it is in the open set.
Yellow: When the user makes a traffic which is a node that has a higher weight than normal which means it is more costly to pass through it but it is not blocked like a wall.
"""
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 49, 49)
LIGHTBLUE = (4, 217, 255)
PINK = (240, 105, 180)
LAVENDER = (234, 157, 255)
YELLOW = (255, 255, 51)

# It is a mandatory function to initalize all of the pygame modules.
pygame.init()
window = pygame.display.set_mode((WIDTH, WIDTH)) #This will pop out a window after executing it and size of the window and the width and height are the same which is 800 by 800 pixels.
pygame.display.set_caption("Kyle's Summer Project 2026 Pathfinding Visualizer") #Caption when the display is opened.

# This is an interactive function which allows the user to place the starting point first, end point second, and then they can place walls or traffic to make the path more difficult for the node to find the path from start to end. The user can also toggle traffic mode on and off by pressing the "T" key which allows them to place traffic nodes instead of walls. The user can also reset the grid by pressing the "R" key which will clear all walls, traffic, start, and end points. The user can also undo their last action by pressing the "Z" key and redo their last undone action by pressing the "Y" key.
def draw_grid(win, rows, width):
        gap = WIDTH // ROWS

        for i in range(ROWS):                
                # Draw horizontal
                pygame.draw.line(window, BLACK, (0, i * gap), (WIDTH, i * gap))
                # Draw vertical
                pygame.draw.line(window, BLACK, (i * gap, 0), (i * gap, WIDTH))

# This is the implementation of the Breadth-First Search (BFS) algorithm which is a pathfinding algorithm that explores all the neighboring nodes at the present depth before moving on to the nodes at the next depth level. It uses a queue data structure to keep track of the nodes to be explored, ensuring that it explores nodes in the order they were added to the queue. BFS is particularly effective for unweighted graphs and guarantees finding the shortest path in terms of number of edges, but it can be less efficient than other algorithms like Dijkstra's or A* for weighted graphs or larger search spaces which I commented out in the code because it is not as efficient as Dijkstra's algorithm for this particular implementation since we have traffic nodes with different weights which makes it a weighted graph.               
"""
def bfs(draw, grid, start, end):
        queue = deque()
        queue.append(start)

        came_from = {}
        visited = {start}

        while queue:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()

                current = queue.popleft()

                if current == end:
                        reconstruct_path(came_from, end, draw)
                        end.make_end()
                        start.make_start()
                        print("Path found!")
                        return True

                for neighbor in current.neighbors:
                        if neighbor not in visited:
                                visited.add(neighbor)
                                came_from[neighbor] = current
                                queue.append(neighbor)
                                neighbor.make_open()

                draw()

                if current != start:
                        current.make_closed()

        print("No path found.")
        return False
"""

# This is where the Dijkstra's algorithm is implemented which is a pathfinding algorithm that finds the shortest path from a starting node to an ending node in a weighted graph. It uses a priority queue to explore nodes based on their cumulative cost from the start node, ensuring that the first time it reaches the end node, it has found the shortest path. The algorithm continues to explore until it either finds the end node or exhausts all possible paths, making it efficient for graphs with non-negative edge weights.
def dijkstra(draw, grid, start, end):
        count = 0 # This is like a tiebreaker if the same priority (distance) and this is like who came first and the lesser the number, the higher the priority in the open set.
        open_set = [] #It uses a min-heap priority queue to keep track of the nodes to be explored, where the node with the lowest cumulative cost from the start node is given the highest priority.
        heapq.heappush(open_set, (0, count, start)) #The struture we use is heap specfically a min-heap where the parent node is the minimum value which is use for if there is a value that have the same attribututes, we can find who came first so we can remove from the queue and put as the current node.
    
        came_from = {} # This is the dictionary, this remembers how we got each node when we go deep dive to the childrens specfically min-heap
        g_score = {spot: float("inf") for row in grid for spot in row} #This is where the node is intialize with an infinite cost (worse cost) and means that it is undiscovered or not reached yet.
        g_score[start] = 0 
    
        visited = set() #This is a set, where we list of what nodes have we visited.
    
        while open_set: #This is where while we keep track of the queue of the djikstra.
                for event in pygame.event.get(): #This is a for loop making the 2D grapics run, and if window is close, close down the application.
                        if event.type == pygame.QUIT:
                                pygame.quit()
    
                current = heapq.heappop(open_set)[2] #This will remove the third index of the element which represent the attribute of the node. First index is weight of the Dijkstra, second index is the count, whoever got there first in the queue, third is the element of the node object 
    
                if current == end: # If the path find its destination, then it will reconstructed the pathway and display how many steps, the weight, and if it encouter the weight which is traffic.
                        path = reconstruct_path(came_from, end, draw) # This is the path it will reconstrut with its parameters.
                        reconstruct_path(came_from, end, draw)

                        total_cost = g_score[end] # This will add up to the cost of what is the fastest pathway based on the weight
                        path_uses_traffic = any(spot.is_traffic() for spot in path) # This is a boolean if the pathway had to encounter the weight which is traffic.
                        steps = len(path) # This will identify how many units it take to reach with the effiency of the weight.
                        start.make_start() # This call the start method which by default it is None and when you click on the first tile, it is red color.
                        end.make_end() # This call the end method which by default it is None until you click Start first and after you click again to make the end point.
                        print("Path found!")
                        print("Steps:", steps)
                        print("Total  weighted cost:", total_cost) 
                        print("Path uses traffic:", path_uses_traffic) 
                        return True
    
                visited.add(current) # This indiciate if the node is already visited.
    
                for neighbor in current.neighbors:
                        temp_g_score = g_score[current] + neighbor.weight # This calculates the total cost of the weight.
    
                        if temp_g_score < g_score[neighbor]: # It is now comparing to the values of the weight using min-heap and if it is less than, then it will get the smallest value
                                came_from[neighbor] = current # This is where it will saved the value if it is less than
                                g_score[neighbor] = temp_g_score # This will replaced the old path with a cheaper path.
    
                                if neighbor not in visited: #This is if the node is not visited, it will add one and put the incremenet value per node.
                                        count += 1
                                        heapq.heappush(open_set, (g_score[neighbor], count, neighbor))
                                        neighbor.make_open()
    
                draw() # The draw method where it will draw out the fastest pathway.
    
                if current != start:
                        current.make_closed() # It will not start the program if there is no starting node.
    
        print("No path found.") #If it does not reach the end, it will display the message.
        return False # Return false if it did not reach the path.       

def reconstruct_path(came_from, current, draw): #This method will reconstruct the path once it reach start to end.
        
        path = [] #This will rebuild the path once it finds the end.

        while current in came_from: # This process is where it goes to the end node to start node so it can display as start to end.
                path.append(current) # This put the nodes in the list
                current = came_from[current] # This will make the path backwards making it end to start

        path.reverse() # This will make the path from start to end

        for current in path: # This is for each node in the path and store it in current
            current.make_path() # Mark the node    
            draw() # Draw the nodes after it finds the end with the cheapest weight.

        return path # Return the path resulting the display of the path of the shortest weight.

def clear_path(grid): # This is where we clear the path so we can reset the grid, only for the pathway, not the walls nor traffic.
        for row in grid:
                for spot in row:
                        spot.clear_search_color()

class Spot: # This is the spot class where it represents the path and it is attributues which is colored coded
        
        def __init__(self, row, col, width): # This is the constructor  for its colum, rows, weight and the list of the upcoming nodes, etc.
                self.row = row # This is the vectical indicies of the 2D graph (n-1)
                self.col = col # This is the horizontial indicies of the 2D graph (m-1)
                self.x = col * width # It determines the size of the width like, 800 will be 800x800
                self.y = row * width # The amount of rows that grid has
                self.color = WHITE # White for default
                self.width = width # Width of the window size
                self.neighbors = [] # List of the upcoming nodes
                self.weight = 1 # Weight which is 1 be fault the normal pathway (without traffic)
     
        def draw(self, win): # This is the draw method where it draws with its parameter of the attribututes of the method
                pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

        def make_start(self): # Makes the starting point
                self.color = RED

        def make_end(self): # Makes the end point
                self.color = PINK

        def make_wall(self): # Makes the walls
                self.color = BLACK

        def reset(self): # Makes the default path with weight as 1
                self.color = WHITE
                self.weight = 1

        def make_path(self): # This is reconstruct the path
                self.color = LIGHTBLUE

        def is_traffic(self): # This will send a boolean if the pathway did encounter traffic
               return self.weight > 1 # If it is greater than 1, the path did encounter traffic

        def make_traffic(self): # This is where the traffic occurs
                self.color = YELLOW
                self.weight = 10 # If this encounters, it will add 10 to its weight if they believe this is the fastest way to get to the end

        def update_neighbors(self, grid): # This will update by remove the node and putting as the current node and what node the current node now discovered, it is put on the list, and also making the visited nodes shown
                self.neighbors = []

                if self.row < ROWS - 1 and grid[self.row + 1][self.col].color != BLACK: # DOWN
                        self.neighbors.append(grid[self.row + 1][self.col])

                if self.row > 0 and grid[self.row - 1][self.col].color != BLACK: # UP
                        self.neighbors.append(grid[self.row - 1][self.col])

                if self.col < ROWS - 1 and grid[self.row][self.col + 1].color != BLACK: # RIGHT
                        self.neighbors.append(grid[self.row][self.col + 1])

                if self.col > 0 and grid[self.row][self.col - 1].color != BLACK: # LEFT
                        self.neighbors.append(grid[self.row][self.col - 1])
        
        def is_wall(self): # This will return the value as black for the display of the wall
                return self.color == BLACK
        
        def make_closed(self): # This is where it has been explored while looking for the finish spot
                if not self.is_traffic():
                    self.color = LAVENDER

        def make_open(self): # This is where it checks the node but will see it later but once it find the finish spot then it will stop midway leaving some white squares.
                if not self.is_traffic():
                    self.color = LAVENDER

        def make_path(self): # This is where the make the path once it finds the finish spot.
                self.color = LIGHTBLUE

        def clear_search_color(self): # This will clear the make_open and make_close colors and the path color and keep the walls and traffic intact and making weight by 1 since it will reset to white.
            if self. color == LAVENDER or self.color == LIGHTBLUE or self.color == PINK:
                self.color = WHITE
                self.weight = 1   


def make_grid(rows, width): # This makes the struture of the grid
        grid = [] # This will hold all the node's postion starting (0,0) on the top left to downwards and right
        gap = width // rows # This will be how many pixels wide/tall

        for i in range(rows): # This is for the rows
                grid.append([]) # Append for the rows.
                for j in range(rows): # This is for the columns
                        spot = Spot(i, j, gap) # This determines the node with, the row, the column, and the gap (Size of the square in pixel)
                        grid[i].append(spot) # Put that node in row i

        return grid # Return the 2D list of nodes

def draw_grid(win, rows, width): # This is where the user can draw to either make the black walls or yellow traffic tiles.
        gap = width // rows

        for i in range(rows):
                # Draw horizontal
                pygame.draw.line(window, BLACK, (0, i * gap), (WIDTH, i * gap))
                # Draw vertical
                pygame.draw.line(window, BLACK, (i * gap, 0), (i * gap, WIDTH))

def draw(win, grid, rows, width): # This will constatntly keep updating so the display can show about the walls, traffic, etc.
        win.fill(WHITE)

        for row in grid:
                for spot in row:
                        spot.draw(win)

        draw_grid(win, rows, width)
        pygame.display.update()

def get_clicked_pos(pos, rows, width): # This is where the mouse positions are for the grid.
        gap = width // rows
        x,y = pos

        row = y // gap
        col = x // gap

        return row, col

def is_inside_grid(row, col, rows): # This function is important because without it, it will crash the grid window and I had to rerun the program.
        return 0 <= row < rows and 0 <= col < rows


grid = make_grid(ROWS, WIDTH) # This is declaring the grid with the parameters rows and width.

start = None # By default the start tile is nothing unless the user do their first click
end = None # This is the second click after they click their starting position

running = True # Keep the method running
traffic_mode = False # This is where they need to toggle for the traffic mode which starts at false first until the user clicks on the traffic key which is T
undo_stack = [] # This is where if they messed up on a wall or traffic they do not want so they click z
redo_stack = [] # This is if they accidentally delete something, they can redo it when they click y 

while running: # When the python code is executed
    draw(window, grid, ROWS, WIDTH) # Call the draw method

    for event in pygame.event.get(): # For when the even is running
        if event.type == pygame.QUIT: # If the user exits the grid window, it will stop running
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t: # If they user clicks t, that will toggle traffic mode
                traffic_mode = not traffic_mode # This is to toggle true and false for traffic mode
                print("Traffic mode:", "ON" if traffic_mode else "OFF") # Tracing the mode to ensure it is toggle on and off

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: # This is to reset the whole grid
                grid = make_grid(ROWS, WIDTH)
                start = None
                end = None
                print("Grid reset.")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c: # This is to clear the path and the open/closed nodes
                clear_path(grid) # Clear all the visited nodes disregard the walls and traffic
                print("Cleared search/path colors.") # Trace the code to know it is successful        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and undo_stack: # This is the undo feature
                  spot, color, weight = undo_stack.pop() # This will pop from the stack when the undo button is click
                  redo_stack.append((spot, spot.color, spot.weight)) # This will push the redo stack and saved when the redo is trigger

                  spot.color = color # Store the color of the tile's position
                  spot.weight = weight # Store the weight of the tile's position

        if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_y and redo_stack: # This is where the redo feature
                    spot, color, weight = redo_stack.pop() #This will pop after the undo button is click and they want to restore the block that has been undo.
                    undo_stack.append((spot, spot.color, spot.weight)) #This is store on the undo stack after the undo is trigger and they want to pop and restore the tile
                    spot.color = color
                    spot.weight = weight



        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # This is where the Dijkstra is going to occur so it is going to find the pathway based on the distance and the cheapest weight
                """
                for row in grid: 
                    for spot in row:
                        spot.update_neighbors(grid)
                                                        """
                if start and end: # It will update the nodes after start and end is placed
                    
                    for row in grid: # This will update what are the upcoming nodes after each node is visited.
                        for spot in row:
                            spot.update_neighbors(grid)

                    dijkstra(lambda: draw(window, grid, ROWS, WIDTH), grid, start, end) # This is the Algorithm I will be using, Dijkstra
                    #bfs(lambda: draw(window, grid, ROWS, WIDTH), grid, start, end)

        #print("neighbors updated")

        if pygame.mouse.get_pressed()[0]: # Left mouse button
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, WIDTH)

            if is_inside_grid(row, col, ROWS): # This is where when left mouse is click, it will trigger the starting point first, end point last, wall tile and traffic tile
                spot = grid[row][col]

                if not start and spot != end: # This means if there is no start point, the next click will be the start position
                    start = spot
                    start.make_start()

                elif not end and spot != start: #This mean if there is no end point, the next click will be the end point
                    end = spot
                    end.make_end()

                elif spot != end and spot != start: # If the nodes are not an start and end point, so it does think that it is a wall tile or traffic tile

                    if traffic_mode: # This is the traffic where the weight is 10 like goal is to find the cheapest pathway with no traffic if the path can find it.
                        if spot.color != YELLOW: # This is if the tiles are not yellow, we can clear the pathway and the nodes that are open/closed back to white perserving the yellow tiles
                            undo_stack.append((spot, spot.color, spot.weight))
                            redo_stack.clear()
                            spot.make_traffic()
                    else:
                        if spot.color != BLACK: # Same thing when clearing the pathway and nodes that are open/closed back to white perserving the wall tiles.
                            undo_stack.append((spot, spot.color, spot.weight))
                            redo_stack.clear()
                            spot.make_wall()

        elif pygame.mouse.get_pressed()[2]: # Right mouse button
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, WIDTH)

            if is_inside_grid(row, col, ROWS): # This is like the delete feature
                spot = grid[row][col]

                undo_stack.append((spot, spot.color, spot.weight)) # Save current state for undo
                redo_stack.clear() # Clear redo stack on new action
                spot.reset()

                if spot == start: # If the user delete the start tile, the next click will be the start tile
                    start = None
                elif spot == end: # Same thing as if the user delete the end tile, the next click will be the end tile
                    end = None

        
        

pygame.quit()

