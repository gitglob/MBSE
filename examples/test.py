from operator import itemgetter
a = [1, 4, 2, 1, 5]
index_min = min(range(len(a)), key=a.__getitem__)

print(index_min)