import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

sources = [
    "./source/a.txt",
    "./source/b.txt",
    "./source/c.txt",
    "./source/d.txt",
    "./source/e.txt",
    "./source/f.txt"
]
outputs = [
    "./results/a.txt",
    "./results/b.txt",
    "./results/c.txt",
    "./results/d.txt",
    "./results/e.txt",
    "./results/f.txt"
]
choise = 0 # from 0 to 5

# 6 4 5 2 1000
# 2 0 rue-de-londres 1
# 0 1 rue-d-amsterdam 1
# 3 1 rue-d-athenes 1
# 2 3 rue-de-rome 2
# 1 2 rue-de-moscou 3
# 4 rue-de-londres rue-d-amsterdam rue-de-moscou rue-de-rome
# 3 rue-d-athenes rue-de-moscou rue-de-londres


class CarNode():

	def __init__(self, P, Path):
		self.P = P
		self.path = Path

class StreetNode():

	def __init__(self, B, E, street_name, L):
		self.B = B
		self.E = E
		self.name = street_name
		self.L = L

#class IntersectionNode():

class Graph():

	def __init__(self, N_nodes):
		self.graph = dict.fromkeys(range(N_nodes), [])
		self.G = nx.DiGraph()
		self.G.add_nodes_from(list(range(N_nodes)))




# --- PARSING ---

street_node_map = {}
list_of_connections = []





with open(sources[choise], "r") as f:
	# getting starting info:

	D, I, S, V, P = map(int, f.readline().split())

	city = Graph(I)

	# for each street in the list:
	for i in range(S):
		B, E, street_name, L = f.readline().split()
		B = int(B)
		E = int(E)
		L = int(L)

		street_node_map[street_name] = (B, E, L)
		list_of_connections.append((B, E))
		if B in city.graph:
			city.graph[B].append(E)
		else:
			city.graph[B] == [E]

		city.G.add_edge(B, E, weight=L)
		city.

	print(city.graph)
	print(city.G.nodes(data=True))
	print(city.G.edges(data=True))
	# create streetNode
#	city.G.add_nodes_from(L)
#	city.G.add_edges_from(list_of_connections)
	# draw? -------
	pos = nx.spring_layout(city.G)
	nx.draw_networkx_nodes(city.G, pos, node_size=500)
	nx.draw_networkx_edges(city.G, pos, edgelist=city.G.edges(), edge_color='black')
	nx.draw_networkx_labels(city.G, pos)
#	plt.show()
#

	# for each car in the list
#	for i in range(V):
#		Path = list(f.readline().split())
#		P = Path.pop(0)
#		# create CarNode




#	COST = np.array(list(map(int, f.readline().split())))
#	libs = [] # list of all libs;
#	# getting a lib each iteration:
#	for i in range(NLIB):
#	lib_books_n, signup, book_per_day = f.readline().split()
#	# getting dict of books: cost
#	lib_books_list = map(int, f.readline().split())
#	lib_books_dict = {}
#	for book in lib_books_list:
#		lib_books_dict[book] = COST[book]
#	# sorting dict by value:
#	sorted_dict = {k: v for k, v in sorted(\
#				lib_books_dict.items(), reverse=True, key=lambda item: item[1])}
#	# appending lib:
#	lib = Library(int(lib_books_n), int(signup),\
#					int(book_per_day), sorted_dict)
#	libs.append(lib)


	# --- SOLUTION ---


	# --- OUTPUT ---

#	with open(outputs[choise], "w+") as f:
#	#total libs:
#	out_libs = len(result_libs)
#	f.write(str(out_libs) + "\n")
#	# each lib stats:
#	for lib in result_libs:
#	if not (lib.potential.shape[0]):
#		continue
#	f.write(str(lib.index) + ' ' + str(len(lib.potential)) + '\n')
#	# each lib sent books:
#	for book in lib.potential:
#		f.write(str(book) + ' ')
#	f.write("\n")