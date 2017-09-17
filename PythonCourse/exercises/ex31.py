"""Implement the higher order functions map(), filter() and reduce(). 
(They are built-in but writing them yourself may be a good exercise.)"""

def map(function, sequence):
  pass
# filter() implementation  
def filter(function, sequence):
  pass

# reduce() implementation
def reduce(function, sequence, initial=None):
  pass

#test
print(map(lambda x: 2 * x, [1,2,3,4]))
print(filter(lambda x: x.endswith('in'), ('lapin', 'cretin', 'ah', 'oui')))
print(reduce(lambda x, y: x+y, [1, 2, 3, 4, 5], 0))