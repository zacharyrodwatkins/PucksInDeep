file_name = "Current_tests/21-01/run-1.txt"

with open(file_name, 'r') as f:
    lines = f.read_lines()


with open("fixed.txt", "w") as f:
    f.write(lines[0])
    vals = lines[1].split(",")
    for i in range(len(vals))
        new_line = 
