rec1 = { 'x': 1, 'w': 1, 'y': 4, 'h': 1 }
rec2 = { 'x': 1, 'w': 3, 'y': 1, 'h': 3 }
rec3 = { 'x': 2, 'w': 5, 'y': 1, 'h': 1 }
rec4 = { 'x': 3, 'w': 2, 'y': 3, 'h': 2 }
rec5 = { 'x': 5, 'w': 1, 'y': 1, 'h': 2 }
rec6 = { 'x': 6, 'w': 1, 'y': 4, 'h': 1 }

recs = [rec1, rec2, rec3, rec4, rec5, rec6]
from rectangle_overlap.check import findAllOverlaps

overlaps = findAllOverlaps(recs)
print (overlaps)
