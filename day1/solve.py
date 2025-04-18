import numpy as np

input_file = "input.txt"
num_entries = 0

# number of lines
with open(input_file, "r") as f:
    num_entries = sum(1 for _ in f)

left_arr = np.empty(num_entries, dtype=int)
right_arr = np.empty(num_entries, dtype=int)

# lines to arrays
with open(input_file) as f:
    i = 0
    for line in f:
        arr_line = line.split('   ')
        left_arr[i] = int(arr_line[0])
        right_arr[i] = int(arr_line[1])
        i += 1

# sort
left_arr_sorted = np.sort(left_arr)
right_arr_sorted = np.sort(right_arr)

# part 1
# calc distance
if len(left_arr_sorted) == len(right_arr_sorted):
    diff = left_arr_sorted - right_arr_sorted
    abs_diff = np.abs(diff)
    total_distance = np.sum(abs_diff)
    print(f"sum of distances: {total_distance}")
else:
    print('error in input list')
    
######################################################
# Part 2
######################################################

# assuming arrays are correct
# count number of entries from left_arr_sorted in right_arr_sorted
count_arr = np.empty(num_entries, dtype=int)
similarity_score = 0

for index, value in np.ndenumerate(left_arr_sorted):
    count_arr[index] = (right_arr_sorted == value).sum()
    similarity_score += count_arr[index] * value

print(f"similarity score: {similarity_score}")
