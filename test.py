current = [1, 2]
final = []

for i in range(5):
    final.append(current.copy())
    current[0] += 1
    current[1] += 1

print(final)
