'''
    This file contains the template for Assignment4. For testing it, I will place it
    in a different directory, call the function <min_cost_connecting_edges>, and check its output.
    So, you can add/remove  whatever you want to/from this file. But, don't change the name
    of the file or the name/signature of the following function.

    I will use <python3> to run this code.
'''



def edge_cost(points, point1, point2):
    xCost = abs(points[point1][0] - points[point2][0])
    yCost = abs(points[point1][1] - points[point2][1])
    return xCost + yCost

class vertex:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.marked = False
        self.component = -1

class edge:
    def __init__(self, point1, point2, cost):
        self.point1 = point1
        self.point2 = point2
        self.cost = cost
    

class graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
    
    def getAdjacentVertices(self, id):
        adjVertices = []
        for edge in self.edges:
            if(id == edge.point1 or id == edge.point2):
                if(id != edge.point1):
                    if(not self.vertices[edge.point1].marked and adjVertices.count(edge.point1) == 0):
                        adjVertices.append(edge.point1)
                if(id != edge.point2):
                    if(not self.vertices[edge.point2].marked and adjVertices.count(edge.point2) == 0):
                        adjVertices.append(edge.point2)
        return adjVertices
    
    def containsEdge(self, point1, point2):
        contains = False
        for x in self.edges:
            if((x.point1 == point1 and x.point2 == point2) or (x.point1 == point2 and x.point2 == point1)):
                contains = True
        return contains



    def addEdge(self, edge):
        if(edge != None and not self.containsEdge(edge.point1, edge.point2)):
            self.edges.append(edge)
    
        


    

def countAndLabel(g):
    count = 0
    for i in range(len(g.vertices)):
        g.vertices[i].marked = False

    for i in range(len(g.vertices)):
        if g.vertices[i].marked == False:
            count += 1


            #labels all the vertices in one component
            to_vist = []
            to_vist.append(g.vertices[i].id)
            while(len(to_vist) > 0):
                current = to_vist[len(to_vist) - 1]
                to_vist.pop()
                if(g.vertices[current].marked == False):
                    g.vertices[current].marked = True
                    g.vertices[current].component = count
                    adjVertices = g.getAdjacentVertices(current)
                    for adj in adjVertices:
                        to_vist.append(adj)                   
    return count


def addAllSafeEdges(edges, g, count):
    safe = []
    for i in range(count):
        safe.append(None)
    for i in range(len(edges)):
        point1 = edges[i].point1
        point2 = edges[i].point2
        comp1 = g.vertices[point1].component - 1
        comp2 = g.vertices[point2].component - 1
        
        if(comp1 != comp2):
            if safe[comp1] == None or edges[i].cost < safe[comp1].cost:
                safe[comp1] = edges[i]
            if safe[comp2] == None or edges[i].cost < safe[comp2].cost:
                safe[comp2] = edges[i]
    for i in range(count):
        g.addEdge(safe[i])

def Boruvka(vertices, edges, freeEdges):
    f = graph(vertices, freeEdges)
    count = countAndLabel(f)
    while count > 1:
        addAllSafeEdges(edges, f, count)
        count = countAndLabel(f)
    return f


def min_cost_connecting_edges(
    points: list[tuple[int, int]],
    given_edges: list[tuple[int, int]]
) -> int:
    '''
    Compute the minimum total cost of edges to connect all points if the set of given_edges
    is free.

    @param
        points: list[tuple[int, int]] - set of poins with integer coordinates on the plane.
        given_edges: list[tuple[int, int]] - set of connections between points that are given
            for free.  Each item of the list is a pair of indices (0, ..., n-1)x(0, ...., n-1)

    Output: minimum cost of new edges needed to connect all vertices.
    '''
    #Create a list of points for component search
    Vertices = []
    for i in range(len(points)):
        Vertices.append(vertex(i, points[i][0], points[i][1]))
    Edges = []
    FreeEdges = []
    for i in range(len(Vertices) - 1):
        for j in range(i + 1, len(Vertices)):
            newEdge = edge(Vertices[i].id, Vertices[j].id, -1)
            if(given_edges.count((i,j)) != 0):
                newEdge.cost = 0
                FreeEdges.append(newEdge)
            else:
                newEdge.cost = edge_cost(points, i, j)
                Edges.append(newEdge)
    
    #Steps for the algorithm
    #Construct a list of all edges in the graph, with their cost calculated and all given edges having a cost of 0
    #Use Borkva Algorithm 
    #Adds all safe edges to the graph repeatedly 
    g = Boruvka(Vertices, Edges, FreeEdges)

    
    minCost = 0
    for minEdge in g.edges:
        minCost += minEdge.cost
    








    # Your code here :)
    return minCost




list1 = [(0,0), (1,1), (2,2), (3,3)]
list2 = [(1,2), (1,3), (2,3)]
print(min_cost_connecting_edges(list1, list2))

list1 = [(0,0), (2,2), (3,3), (2,3), (3,2), (5,5)]
list2 = [(2,3), (2,4), (3,4), (2,5)]
print(min_cost_connecting_edges(list1, list2))

list1 = [(0,0), (0,1), (0,2), (0,12), (0,20)]
list2 = [(1,2), (1,3), (3,4)]
print(min_cost_connecting_edges(list1, list2))

list1 = [(0,0), (0,1), (0,2), (0,12), (0,20)]
list2 = []
print(min_cost_connecting_edges(list1, list2))

list1 = [(0,1), (10,901), (8590,2132), (54124,1662), (12124,21341)]
list2 = [(0,1), (0,2), (0,3), (0,4)]
print(min_cost_connecting_edges(list1, list2))