import Map
import math
open_list = []
closed_list = []

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        return self.position == other.position
    
def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]

def astar(start, end, map):
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))

    open_list = []
    closed_list = []

    open_list.append(start_node)
    
    outer_iterations = 0
    max_iterations = 10000

    adjacent_squares =  ((0, -1), (0, 1), (-1, 0), (1, 0),)

    while len(open_list) > 0:
        outer_iterations += 1

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        
        if outer_iterations > max_iterations:
            return return_path(current_node)
        
        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            return return_path(current_node)
        
        children = []

        for new_position in adjacent_squares:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if map.get_cell_value(node_position) != 1:
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0:
                continue

            open_list.append(child)

if __name__ == "__main__":
    map = Map.Map_Obj()
    path = astar(map.get_start_pos(), map.get_end_goal_pos(), map)
    print(path)
    print(len(path))
    map.show_map()