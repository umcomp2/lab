import numpy as np
superlista = []
superlista += [1] + [2] + [3]
superlista += [4] + [5] + [6]
arr = np.array([superlista])

arr2 = arr.transpose()

print(arr)
print(arr2)