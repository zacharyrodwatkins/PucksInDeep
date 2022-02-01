current_data = [1,2,3,4,5,6,7,8,9,10]

bin_size = 5
cur_avg_data = []

for i in range(len(current_data)):
        lower_bound = max([i - int(bin_size/2), 0])
        upper_bound = min([i + int(bin_size/2), len(current_data) -1])
        print(lower_bound)
        print(upper_bound)
        actual_bin_size = 1 + upper_bound - lower_bound
        avg = sum(current_data[lower_bound:upper_bound+1])/float(actual_bin_size)
        cur_avg_data.append(avg)

print(cur_avg_data)