
mapping = [4, 5, 6, 7, 0, 2, 1, 3, 8, 9]

data = ["123", "657", "02"]

output = []
for obj in data:
    hold = ''
    for char in obj:
        hold += str(mapping.index(int(char)))
    output += [hold]

print(output)