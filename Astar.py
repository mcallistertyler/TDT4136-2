import Map
import sys #lets me escape the program when path is found, really bad practice :)
import math
open_list = []
closed_list = []
class Node():
    def __init__(self, position, skip=False, parent=None, cell_cost=1):
        self.position = position # Position of the node
        self.g = 0 # distance between current node and the start node
        self.h = 0 # the heuristic - estimated cost from the current node to the goal node
        self.f = 0 # f = g + h - estimated total cost
        self.cell_cost = cell_cost
        self.skip = skip # when true the node wont be added to the open list
        self.parent = parent # Pointer to a node's parent node
        if parent != None:
            self.parent_position = parent.position # Keeps track of the position of the node's parent. Sanity check.
        else:
            self.parent_position = None

def manhattan(current_node, end_goal_node):
    return abs(current_node.position[0] - end_goal_node.position[0]) + abs(current_node.position[1] - end_goal_node.position[1])

def diagonal(current_node, end_goal_node):
    return max([abs(current_node.position[0] - end_goal_node.position[0]), abs(current_node.position[1] - end_goal_node.position[1])])

def euclidean(current_node, end_goal_node):
    return math.sqrt(((current_node.position[0] - end_goal_node.position[0])**2) + ((current_node.position[1] - end_goal_node.position[1])**2))

def h_distance(current_node, end_goal_node):
    # Returns heuristic distance - estimated distance from current node to end goal node
    #current_node.h = euclidean(current_node, end_goal_node)
    current_node.h = manhattan(current_node, end_goal_node)
    return current_node

def g_distance(current_node, start_node):
    # Returns g distance between current node and starting node
    current_node.g = start_node.g + 1
    return current_node

# Just makes looking at the open list a little easier - utility
def look_at_list(nodes):
    for x in range(0, len(nodes)):
        print(vars(nodes[x]))

# Gets every adjacent node for a given node provided that their value is walkable (not -1)
# Also stores a node's cell_cost for part 2 of the assignment
def get_adjacent_nodes(node, map):
    adjacent_nodes = []
    if(map.get_cell_value([node.position[0] + 1, node.position[1]]) != -1):
        adjacent_nodes.append(Node([node.position[0] + 1, node.position[1]], parent=node, cell_cost=map.get_cell_value([node.position[0] + 1, node.position[1]])))
    if(map.get_cell_value([node.position[0] - 1, node.position[1]]) != -1):
        adjacent_nodes.append(Node([node.position[0] - 1, node.position[1]], parent=node, cell_cost=map.get_cell_value([node.position[0] - 1, node.position[1]])))
    if(map.get_cell_value([node.position[0], node.position[1] + 1]) != -1):
        adjacent_nodes.append(Node([node.position[0], node.position[1] + 1], parent=node, cell_cost=map.get_cell_value([node.position[0], node.position[1] + 1])))
    if(map.get_cell_value([node.position[0], node.position[1] - 1]) != -1):
        adjacent_nodes.append(Node([node.position[0], node.position[1] - 1], parent=node, cell_cost=map.get_cell_value([node.position[0], node.position[1] - 1])))
    return adjacent_nodes

# Same as the adjacent implementation but gets all diagonal
def get_diagonal_nodes(node, map):
    diagonal_nodes = []
    if(map.get_cell_value([node.position[0] + 1, node.position[1] + 1]) != -1):
        diagonal_nodes.append(Node([node.position[0] + 1, node.position[1] + 1], parent=node, cell_cost=map.get_cell_value([node.position[0] + 1, node.position[1] + 1])))
    if(map.get_cell_value([node.position[0] + 1, node.position[1] - 1]) != -1):
        diagonal_nodes.append(Node([node.position[0] + 1, node.position[1] - 1], parent=node, cell_cost=map.get_cell_value([node.position[0] + 1, node.position[1] - 1])))
    if(map.get_cell_value([node.position[0] - 1, node.position[1] + 1]) != -1):
        diagonal_nodes.append(Node([node.position[0] - 1, node.position[1] + 1], parent=node, cell_cost=map.get_cell_value([node.position[0] - 1, node.position[1] + 1])))
    if(map.get_cell_value([node.position[0] - 1, node.position[1] - 1]) != -1):
        diagonal_nodes.append(Node([node.position[0] - 1, node.position[1] - 1], parent=node, cell_cost=map.get_cell_value([node.position[0] - 1, node.position[1] - 1])))
    return diagonal_nodes

# Can return either adjacent, diagonal or both depending on what you return
def get_surrounding_nodes(node, map):
    adjacent_nodes = get_adjacent_nodes(node, map)
    diagonal_nodes = get_diagonal_nodes(node, map)
    surrounding_nodes = adjacent_nodes + diagonal_nodes
    return adjacent_nodes

# When a path is found this iterates backwards through a node's parents and then reverses the path
# It will also set the value of the map to show that it has been walked on.
def return_path(current_node, map):
    print('Found a path')
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        map.set_cell_value(current.position, ' P ') # P for pink
        current = current.parent
    print(path[::-1])
    print('Path is ', len(path), ' steps.')

# If a node is already in the open list just skip it
def open_list_check(current_node):
    for x in range(0, len(open_list)):
        if(open_list[x].position == current_node.position):
            current_node.skip = True
    return current_node

# If a node is already in the closed list just skip it
def closed_list_check(current_node):
    for x in range(0, len(closed_list)):
        if(closed_list[x].position == current_node.position):
            current_node.skip = True
    return current_node

# Add nodes to the open list that havent been designated to be skipped
def add_to_open_list(surrounding_nodes):
    for x in range(0, len(surrounding_nodes)):
        if surrounding_nodes[x].skip == False:
            open_list.append(surrounding_nodes[x])

# Where most of the path finding happens.
# If we found the goal just stop everything and show the path
# Calculates the overall f distance for nodes and compares them against both lists
def path_find(current_node, surrounding_nodes, end_goal_node, map):
    for x in range(0, len(surrounding_nodes)):
        if(surrounding_nodes[x].position == end_goal_node.position):
            return_path(surrounding_nodes[x], map)
            map.show_map()
            sys.exit('Path found exiting...') #...just exits when a path is found
        surrounding_nodes[x] = g_distance(surrounding_nodes[x], current_node)
        surrounding_nodes[x] = h_distance(surrounding_nodes[x], end_goal_node)
        surrounding_nodes[x].f = (surrounding_nodes[x].g + surrounding_nodes[x].h) * surrounding_nodes[x].cell_cost
        surrounding_nodes[x] = open_list_check(surrounding_nodes[x])
        surrounding_nodes[x] = closed_list_check(surrounding_nodes[x])
    return surrounding_nodes

# Starts the algorithm. Gets the start and end goals for the map
# Finds the best node from the open list
# Adds nodes to the open list that have met the checks defined in path_find()
def astar(node_start_pos, node_goal_pos, map):
    start_node = Node(node_start_pos)
    end_goal_node = Node(node_goal_pos)
    open_list.append(start_node)
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)
        surrounding_nodes = get_surrounding_nodes(current_node, map)
        surrounding_nodes = path_find(current_node, surrounding_nodes, end_goal_node, map)
        add_to_open_list(surrounding_nodes)

if __name__ == "__main__":
    map = Map.Map_Obj(task=2)
    astar(map.get_start_pos(), map.get_end_goal_pos(), map)