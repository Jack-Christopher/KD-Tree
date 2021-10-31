# Python implementation of the KD Tree
# Para su uso es necesario instalar la librería matplotlib
import matplotlib.pyplot as plt
from heapq import heappush, heappop
from random import randint

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5


class Node:
    def __init__(self, point: Point):
        self.point = point
        self.left = None
        self.right = None
        self.bottom_left = None
        self.top_right = None

    def setLeft(self, node):
        self.left = node
    def setRight(self, node):
        self.right = node

    def set_bottom_left(self, node):
        self.bottom_left = node
    def set_top_right(self, node):
        self.top_right = node


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
        # print("Points: ", [str(p.x) + "," + str(p.y) for p in points])
        self.root = self.build_tree(points, 0)
        # self.root.setLeft(None)
        # self.root.setRight(None)
    
    def build_tree(self, points, depth):
        # print("Points: ", [str(p.x) + "," + str(p.y) for p in points])
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

    def prepare_to_plot(self, bottom_left: Point, top_right: Point):
        self.root.set_bottom_left(bottom_left)
        self.root.set_top_right(top_right)
        self.prepare_to_plot_rec(self.root, 0, self.root)

    def prepare_to_plot_rec(self, node, depth, parent: Node):
        if node is None:
            return
        if depth % 2 == 0:
            if node.left is not None:
                node.left.set_bottom_left(parent.bottom_left)
                node.left.set_top_right(Point(parent.point.x, parent.top_right.y))
            if node.right is not None:
                node.right.set_bottom_left(Point(parent.point.x, parent.bottom_left.y))
                node.right.set_top_right(parent.top_right)
        else:
            if node.left is not None:
                node.left.set_bottom_left(parent.bottom_left)
                node.left.set_top_right(Point(parent.top_right.x, parent.point.y))
            if node.right is not None:
                node.right.set_bottom_left(Point(parent.bottom_left.x, parent.point.y))
                node.right.set_top_right(parent.top_right)
        
        self.prepare_to_plot_rec(node.left, depth + 1, node.left)
        self.prepare_to_plot_rec(node.right, depth + 1, node.right)

    
    def print_tree(self):
        self.prepare_to_plot(Point(0, 0), Point(10, 10))
        self.print_tree_rec(self.root, 0)
    
    def print_tree_rec(self, node, depth):
        if node is None:
            return
        print(" " * 2*depth, node.point.x, node.point.y, end=" ")
        if node.left is not None:
            print(": ", node.bottom_left.x, node.bottom_left.y, "--> ", node.top_right.x, node.top_right.y)
        print()
        self.print_tree_rec(node.left, depth + 1)
        self.print_tree_rec(node.right, depth + 1)
    

    def draw(self, point= None, list_points = None):
        self.draw_rec(self.root, 0, list_points)
        
        #draw exterior mark
        plt.plot([0, self.root.top_right.x], [0, 0], 'k-')
        plt.plot([0, 0], [0, self.root.top_right.y], 'k-')
        plt.plot([self.root.top_right.x, self.root.top_right.x], [0, self.root.top_right.y], 'k-')
        plt.plot([0, self.root.top_right.x], [self.root.top_right.y, self.root.top_right.y], 'k-')
        if point is not None:
            plt.scatter(point.x, point.y, color="black")
        
        plt.show()
    
    def draw_rec(self, node, depth, list_points = None):
        if node is None:
            return            
            
        # corte vertical
        if depth % 2 == 0:
            if node.bottom_left is not None and node.top_right is not None:
                # print("ok ==0")
                plt.plot([node.point.x, node.point.x], [node.bottom_left.y, node.top_right.y], 'g')
                if list_points is not None and node.point in list_points:
                    plt.scatter(node.point.x, node.point.y, color="yellow")
                else:
                    plt.scatter(node.point.x, node.point.y, color="red")
                # plt.show()

        # corte horizontal
        else:
            if node.bottom_left is not None and node.top_right is not None:
                # print("ok ==1")
                plt.plot([node.bottom_left.x, node.top_right.x], [node.point.y, node.point.y], 'b')
                if list_points is not None and node.point in list_points:
                    plt.scatter(node.point.x, node.point.y, color="yellow")
                else:
                    plt.scatter(node.point.x, node.point.y, color="red")
                # plt.show()

        self.draw_rec(node.left, depth + 1, list_points)
        self.draw_rec(node.right, depth + 1, list_points)


    def populate(self, n: int, top_x: int, top_y: int):
        # add random points and the build the tree
        points = []
        
        for i in range(n):
            points.append(Point(randint(0, top_x), randint(0, top_y)))
        self.build(points)
        self.prepare_to_plot(Point(0, 0), Point(top_x, top_y))
    
    def KNN(self, point: Point, k: int):
        heap = []  # [ (int distance, Point point), ... ]
        self.KNN_rec(self.root, point, heap, k)
        result = []
        for i in range(k+1):
            result.append(heappop(heap)[1])

        # print("type: ", type(result[0]))

        return result[1:]
    
    def KNN_rec(self, node: Node, point: Point, heap: list, k: int):
        if node is None:
            return
        heappush(heap, [node.point.distance(point), node.point])
        if node.left is not None:
            self.KNN_rec(node.left, point, heap, k)
        if node.right is not None:
            self.KNN_rec(node.right, point, heap, k)

    





# main control

def main():
    # build the tree
    tree = KDTree()
    n = int(input("Numero de puntos: "))
    top_x = int(input("Top x: "))
    top_y = int(input("Top y: "))
    tree.populate(n, top_x, top_y)
    # tree.print_tree()
    tree.draw()
    print("\nKNN")
    x = int(input("X: "))
    y = int(input("Y: "))
    k = int(input("K: "))
    result = tree.KNN(Point(x, y), k)
    print([ "(" + str(p.x) + ", " + str(p.y) + ")" for p in result ])

    tree.draw(Point(x, y), result)

main()