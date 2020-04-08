import numpy as np


def read(adress):
    with open(adress, 'r') as map:
        all_lines = map.readlines()
        num_lines = len(all_lines)  # 9
        line_length = len(all_lines[0])-1  # 13
    tf = np.zeros((num_lines, line_length), dtype = "str")
    for i in range(0, num_lines):
        for j in range(0, line_length):
            tf[i][j] = all_lines[i][j]
    return tf
