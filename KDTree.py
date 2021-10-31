# Python implementation of the KD Tree
import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Node:
    def __init__(self, point: Point):
        self.point = point
        self.left = None
        self.right = None
    def setLeft(self, node):
        self.left = node
    def setRight(self, node):
        self.right = node


class KDTree:   
    def __init__(self):
        self.root = None
    
    # axis = 0 for x, axis = 1 for y
    def sort_by_axis(self, points: list, axis: int):
        if axis == 0:
            points.sort(key=lambda point: point.x)
        elif axis == 1:
            points.sort(key=lambda point: point.y)
        return points

    def build(self, points: list):
        print("Building tree...")
        print("Points: ", [str(p.x) + "," + str(p.y) for p in points])
        self.root = self.build_tree(points, 0)
        # self.root.setLeft(None)
        # self.root.setRight(None)
    
    def build_tree(self, points, depth):
        print("Points: ", [str(p.x) + "," + str(p.y) for p in points])
        if len(points) == 0:
            return None
        # si solo queda un elemento, ese es el nodo hoja
        if len(points) == 1:
            return Node(points[0])

        # ordenamiento por eje
        points = self.sort_by_axis(points, depth % 2)
        median_idx = len(points) // 2
        median_point = points[median_idx]

        # nodo que se va a retornar
        node = Node(median_point)
        left = self.build_tree(points[:median_idx], depth + 1)
        right = self.build_tree(points[median_idx + 1:], depth + 1)
        node.setLeft(left)
        node.setRight(right)

        return node
    
    def print_tree(self):
        self.print_tree_rec(self.root, 0)
    
    def print_tree_rec(self, node, depth):
        if node is None:
            return
        print(" " * 2*depth, node.point.x, node.point.y)
        self.print_tree_rec(node.left, depth + 1)
        self.print_tree_rec(node.right, depth + 1)
        


        
    
        