import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

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
#choise = 4 # from 0 to 5

class Street():

	def __init__(self, B, E, name, L):
		self.B = B
		self.E = E
		self.name = name
		self.L = L

street_list = []

# --- PARSING ---
for choise in range(6):
	with open(sources[choise], "r") as f:
		# getting starting info:

		D, I, S, V, P = map(int, f.readline().split())
		intersections = dict.fromkeys(list(map(str, range(I))), None)

		# for each street in the list:
		for i in range(S):
			B, E, street_name, L = f.readline().split()
			
			# def 
			street = Street(int(B), int(E), street_name, int(L))

			if intersections[E]:
				intersections[E].append(street_name)
			else:
				intersections[E] = [street_name]



	with open(outputs[choise], "w+") as f:
		#total libs:
		A = len(intersections.keys())
		f.write(str(A) + "\n")
		# each lib stats:
		for inter, streets in intersections.items():
			f.write(str(inter) + "\n")
			f.write(str(len(streets)) + "\n")
			for street in streets:
				f.write(str(street) + ' ' + str(1) + '\n')