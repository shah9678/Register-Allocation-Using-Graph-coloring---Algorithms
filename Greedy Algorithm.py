import csv
import time
import networkx as nx
import matplotlib.pyplot as plt
import csv
def color_graph(graph, node_colors):
    # Create a new graph to prevent modification of the original graph
    colored_graph = graph.copy()

    # Assign colors to nodes based on the given dictionary
    for node, color in node_colors.items():
        colored_graph.nodes[node]['color'] = color

    return colored_graph

def addEdge(adj, v, w):
     
    adj[v].append(w)
     
    # Note: the graph is undirected
    adj[w].append(v)  
    return adj
 
# Assigns colors (starting from 0) to all
# vertices and prints the assignment of colors
def greedyColoring(adj, V):
     
    result = [-1] * V
 
    # Assign the first color to first vertex
    result[0] = 0
 
 
    # A temporary array to store the available colors. 
    # True value of available[cr] would mean that the
    # color cr is assigned to one of its adjacent vertices
    available = [False] * V
    chromatic_number = 0
    # Assign colors to remaining V-1 vertices
    for u in range(1,V):
         
        # Process all adjacent vertices and
        # flag their colors as unavailable
        for i in adj[u]:
            if (result[i] != -1):
                available[result[i]] = True
 
        # Find the first available color
        cr = 0
        while cr < V:
            if (available[cr] == False):
                break
             
            cr += 1
             
        # Assign the found color
        result[u] = cr 
 
        # Reset the values back to false 
        # for the next iteration
        for i in adj[u]:
            if (result[i] != -1):
                available[result[i]] = False
    colors=[]
    vertexes = []
    # Print the result
    for u in range(1,V):
        print("Vertex", u, " --->  Register", result[u]+1)
        chromatic_number=max(chromatic_number,result[u]+1)
        colors.append(result[u]+1)
        vertexes.append(u)
    return chromatic_number,vertexes,colors

#Reading data from csv file


with open('Path to dataset', mode='r',encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    u = 'u'
    v = 'v'
    an=0
    # Iterate through each row and access the specified column
    for row in csv_reader:
        an=max(an,max(int(row[u]),int(row[v])))
with open('Path to dataset', mode='r',encoding="utf8") as csv_file:
    #mycie14: vertices 23; edges 71
    csv_reader = csv.DictReader(csv_file)
    
    # Specify the column name you want to loop through
    u = 'u'
    v = 'v'
    g = [[] for i in range(an+1)]
    edges = []
    start_time = time.time()
    for row in csv_reader:
        g = addEdge(g, int(row[u]), int(row[v]))
        x = row[u]
        y = row[v]
        edges.append((int(x),int(y)))
    # print("\nRegister allocation can be done in following manner: ")
    chromatic_number,vertexes, colors = greedyColoring(g, an+1)
    print("Chromatic Number is ", chromatic_number)
print("Running time of the algorithm is --- %s seconds ---" % (time.time() - start_time))





#Draw colored graph after running the greedy algorithm

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
