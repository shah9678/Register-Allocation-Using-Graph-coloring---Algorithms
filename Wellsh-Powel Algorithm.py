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

def color_nodes(graph):
  # Order nodes in descending degree
  nodes = sorted(list(graph.keys()), key=lambda x: len(graph[x]), reverse=True)
  color_map = {}
  chromatic_number=-1
  for i in range(len(nodes)):
    available_colors = [True] * len(nodes)
    for neighbor in graph[nodes[i]]:
      if neighbor in color_map:
        color = color_map[neighbor]
        available_colors[color] = False
    for color, available in enumerate(available_colors):
      if available:
        color_map[nodes[i]] = color
        break
  colors = []
  vertexes = []
  for i in color_map:
    colors.append(color_map[i])
    vertexes.append(i)
    if color_map[i] > chromatic_number:
       chromatic_number = color_map[i]
  chromatic_number += 1
  return color_map, chromatic_number, colors, vertexes

with open('Path to the dataset', mode='r',encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    # Specify the column name you want to loop through
    u = 'u'
    v = 'v'
    last_val=0
    graph={}
    start_time = time.time()
    edges = []
    for row in csv_reader:
        x=row[u]
        y=row[v]
        edges.append((int(x),int(y)))
        if graph.get(int(row[u]))==None:
            graph[int(row[u])]=[int(row[v])]
        else:
            graph[int(row[u])].append(int(row[v]))
        if graph.get(int(row[v]))==None:
            graph[int(row[v])]=[int(row[u])]
        else:
            graph[int(row[v])].append(int(row[u]))
    s,chromatic_number, colors, vertexes = color_nodes(graph)
    print("Chromatic Number is: ", chromatic_number)
    print("Running time of the algorithm is --- %s seconds ---" % (time.time() - start_time))

  
#Draws colored graph after running the Wellsh-Powell algorithm
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
