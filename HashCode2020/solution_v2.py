import numpy as np

sources = [
  "/nfs/2018/t/tkatolik/Documents/hashcode/source/a_example.txt",
  "/nfs/2018/t/tkatolik/Documents/hashcode/source/b_read_on.txt",
  "/nfs/2018/t/tkatolik/Documents/hashcode/source/c_incunabula.txt",
  "/nfs/2018/t/tkatolik/Documents/hashcode/source/d_tough_choices.txt",
  "/nfs/2018/t/tkatolik/Documents/hashcode/source/e_so_many_books.txt",
  "/nfs/2018/t/tkatolik/Documents/hashcode/source/f_libraries_of_the_world.txt"
  ]

files_to_create = [
  "/nfs/2018/t/tkatolik/Documents/hashcode/results/a.txt",
  "/nfs/2018/t/tkatolik/Documents/hashcode/results/b.txt",
  "/nfs/2018/t/tkatolik/Documents/hashcode/results/c.txt",
  "/nfs/2018/t/tkatolik/Documents/hashcode/results/d.txt",
  "/nfs/2018/t/tkatolik/Documents/hashcode/results/e.txt",
  "/nfs/2018/t/tkatolik/Documents/hashcode/results/f.txt"
  ]

choise = 4 # from 0 to 5

class Library():

  lib_index = 0 # indexing libs
  time_coefficient = 5500 # coefficient in experimental part

  def __init__(self, books_count, signup_time, books_perday, books, nday):
    self.index = Library.lib_index
    Library.lib_index += 1
    self.count = books_count
    self.time = signup_time # sign-up time for the lib
    self.bpd = books_perday # books per day
    self.books = books      # sorted (by cost) dict of books {book: cost}
    self.priority = -1      # number of points lib can gain in N days
    self.potential = []     # potential books to scan
    self.b2p_over_count = self.priority / books_count # number of books to process

  def remove_books(self, book_list):
    for book in book_list:
      if self.count > 0 and book in self.books:
        self.books.pop(book, None)
        self.count -= 1

  def calc_priority(self, nday):
    if nday - self.time <= 0:   # if signup > then rest of days.
      self.priority = -1e-100
      self.potetntial = []
    else:
      b2p = (nday - self.time) * self.bpd # number of books to process
      books = np.array(list(self.books.keys()))
      costs = np.array(list(self.books.values()))
      #self.priority = costs[:b2p].sum() / self.time
      # ----
      if b2p < self.count:
        self.priority = costs[:b2p].sum() / self.time / 0.5
      else:
        self.priority = costs[:b2p].sum() / self.time
      # ----
      # this is experimental
      #self.priority = (costs[:b2p].sum() + self.count * 2) / self.time
      #self.priority = costs[:b2p].sum() - (self.time * Library.time_coefficient)
      self.potential = books[:b2p]

# parcing -------------------------------------------------------------------
print("set: {}".format(choise))
with open(sources[choise], "r") as f:
  # getting starting info:
  NBOOK, NLIB, nday = f.readline().split()
  NBOOK = int(NBOOK)
  NLIB = int(NLIB)
  nday = int(nday)
  COST = np.array(list(map(int, f.readline().split())))
  libs = [] # list of all libs;
  # getting a lib each iteration:
  for i in range(NLIB):
    lib_books_n, signup, book_per_day = f.readline().split()
    # getting dict of books: cost
    lib_books_list = map(int, f.readline().split())
    lib_books_dict = {}
    for book in lib_books_list:
      lib_books_dict[book] = COST[book]
    # sorting dict by value:
    sorted_dict = {k: v for k, v in sorted(\
              lib_books_dict.items(), reverse=True, key=lambda item: item[1])}
    # appending lib:
    lib = Library(int(lib_books_n), int(signup),\
                  int(book_per_day), sorted_dict, nday)
    libs.append(lib)


# solution ------------------------------------------------------------------
# remove all dublicates in advance:
def remove_dublicates(lib1, lib2):
  books = lib1.potential.copy()
  for book in books:
    if book in lib2.books:
      if lib1.b2p_over_count < lib2.b2p_over_count:
        lib1.books.pop(book, None)
      else:
        lib2.books.pop(book, None)
# loop

for lib in libs:
  lib.calc_priority(nday)

for i in range(NLIB):
  for j in range(NLIB):
    if i == j:
      continue
    print("cleaning: {} / {}".format(i, NLIB), "\r", end='') # timing for large inputs
    remove_dublicates(libs[i], libs[j])
print()


result_libs = [] #appending best libs here
while nday > 0:
  print("Days left: ", nday, "\r", end='') # timing for large inputs
  if not libs:
    break
  # calculating priorities and potential books to scan
  for lib in libs:
    lib.calc_priority(nday)
  # getting best priority book
  top_lib = max(libs, key=lambda lib: lib.priority)
  result_libs.append(top_lib)
  libs.pop(libs.index(top_lib))
  # removing all books that chosen lib will be scanning from other libs
#  for lib in libs:
#    lib.remove_books(top_lib.potential)
  # updating remaining days
  nday -= top_lib.time

print()
all_books = set([book for lib in result_libs for book in lib.potential])
result = sum([COST[book] for book in all_books])
print(Library.time_coefficient, " | ", result)

# output --------------------------------------------------------------------
with open(files_to_create[choise], "w+") as f:
  #total libs:
  out_libs = len(result_libs)
  f.write(str(out_libs) + "\n")
  # each lib stats:
  for lib in result_libs:
    if not (lib.potential.shape[0]):
      continue
    f.write(str(lib.index) + ' ' + str(len(lib.potential)) + '\n')
    # each lib sent books:
    for book in lib.potential:
      f.write(str(book) + ' ')
    f.write("\n")
