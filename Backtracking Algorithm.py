import csv
import time
import networkx as nx
import matplotlib.pyplot as plt
def color_graph(graph, node_colors):
    # Create a new graph to prevent modification of the original graph
    colored_graph = graph.copy()

    # Assign colors to nodes based on the given dictionary
    for node, color in node_colors.items():
        colored_graph.nodes[node]['color'] = color

    return colored_graph
class Graph():
 
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
 
    # A utility function to check
    # if the current color assignment
    # is safe for vertex v
    def isSafe(self, v, colour, c):
        for i in range(self.V):
            if self.graph[v][i] == 1 and colour[i] == c:
                return False
        return True
 
    # A recursive utility function to solve m
    # coloring  problem
    def graphColourUtil(self, m, colour, v):
        if v == self.V:
            return True
 
        for c in range(1, m + 1):
            if self.isSafe(v, colour, c) == True:
                colour[v] = c
                if self.graphColourUtil(m, colour, v + 1) == True:
                    return True
                colour[v] = 0
 
    def graphColouring(self, m):
        colour = [0] * self.V
        if self.graphColourUtil(m, colour, 0) == None:
            return False
 
        # Print the solution
        # print("Register allocation can be done in following manner: ")
        temp=1
        chromatic_number=0
        vertexes = []
        colors = []
        for c in colour:
            vertexes.append(temp)
            colors.append(c)
            # print("Vertex", temp, " --->  Register", c)
            chromatic_number=max(chromatic_number,c)
            temp+=1
        
        return chromatic_number,vertexes,colors

with open('Path to the dataset', mode='r',encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    u = 'u'
    v = 'v'
    an=0
    edges=[]
    # Iterate through each row and access the specified column
    for row in csv_reader:
        x=row[u]
        y=row[v]
        edges.append((int(x),int(y)))
        an=max(an,max(int(row[u]),int(row[v])))

with open("Path to the dataset", mode='r',encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    # Specify the column name you want to loop through
    u = 'u'
    v = 'v'
    g1 = Graph(an)
    g = [[0 for x in range(an)] for y in range(an)]
    temp=[0]*(an)
    start_time = time.time()
    for row in csv_reader:
        g[int(row[u])-1][int(row[v])-1]=1
        g[int(row[v])-1][int(row[u])-1]=1
    g1.graph = g
    chromatic_number, vertexes, colors = g1.graphColouring(an)
    print("Chromatic number is ", chromatic_number)
    print("Running time of the algorithm is --- %s seconds ---" % (time.time() - start_time))



#Draws colored graph after running the Backtracking algorithm
G = nx.Graph()
# [(1, 2), (2, 3), (3, 4), (4, 1)]
G.add_edges_from(edges)

# Define node colors
r,g,b=0,0,0
import random

# Function to generate n random RGBA color combinations divided by 255
def generate_random_rgba_colors_normalized(n):
    colors = []
    for _ in range(n):
        # Generate random RGBA values in the range [0, 1] for R, G, B and [0, 1] for A
        red = round(random.uniform(0, 1), 2)
        green = round(random.uniform(0, 1), 2)
        blue = round(random.uniform(0, 1), 2)
        alpha = round(random.uniform(0, 1), 2)
        colors.append((red, green, blue, alpha))  # Append the RGBA tuple to the list
    return colors

temp_colors=generate_random_rgba_colors_normalized(len(vertexes))
node_colors = {}
for i in range(len(vertexes)):
    # print(colors[i])
    if node_colors.get(vertexes[i])==None:
        node_colors[vertexes[i]]=(temp_colors[colors[i]])
    else:
        node_colors[vertexes[i]].append((temp_colors[colors[i]]))
# Color the graph nodes
colored_G = color_graph(G, node_colors)

# Draw the graph with specified node colors
node_color_list = [colored_G.nodes[node]['color'] for node in colored_G.nodes]
pos = nx.spring_layout(colored_G)  # Define a layout for the graph
nx.draw(colored_G, pos, with_labels=True, node_color=node_color_list)
plt.show()
