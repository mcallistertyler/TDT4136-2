import Map
import sys
open_list = []
closed_list = []

class Node():
    def __init__(self, position, status=None, parent=None, kids=None):
        self.position = position # Position of the node
        self.g = 0 # distance between current node and the start node
        self.h = 0 # the heuristic - estimated cost from the current node to the goal node
        self.f = 0 # f = g + h - estimated total cost
        self.status = status # Open or closed
        self.parent = parent # Pointer to the best parent node
        self.kids = kids # List of all successor nodes

def h_distance():
    # Returns heuristic distance - estimated distance from current node to end goal node
    return 0

def g_distance(start_node, current_node):
    # Returns g distance between current node and starting node
    current_node.g = start_node.g + 1
    return current_node

def look_at_list(nodes):
    for x in range(0, len(nodes)):
        print(vars(nodes[x]))

def best_f_cost(nodes):
    temp_f = sys.maxsize
    best_node = Node([0,0])
    print('Temp f is', temp_f)
    for x in range(0, len(nodes)):
        print(nodes[x].f)
        if nodes[x].f < temp_f:
            temp_f = nodes[x].f
            best_node = nodes[x]
    print(temp_f)
    print(vars(best_node))
    return best_node

def best_g_cost():
    return 0

def traverse(node_start_pos, node_goal_pos):
    start_node = Node(node_start_pos, 0)
    end_goal_node = Node(node_goal_pos)
    open_list.append(start_node)
    while len(open_list) > 0:
        current_node = open_list[0]
        best_f_cost(open_list)
    return 0

if __name__ == "__main__":
    map = Map.Map_Obj()
    traverse(map.get_start_pos(), map.get_end_goal_pos())