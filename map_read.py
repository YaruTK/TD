import numpy as np


with open('resources/map', 'r') as map:
    all_lines = map.readlines()
    num_lines = len(all_lines)  # 9
    line_length = len(all_lines[0])-1  # 13

print(all_lines[8][12])
print(str(num_lines))
print(str(line_length))
tf = np.zeros((num_lines, line_length), dtype = "int")
for i in range(0, num_lines):
    for j in range(0, line_length):
        tf[i][j] = int(all_lines[i][j])

print(str(tf))