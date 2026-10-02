#experiment zone

# s:list[str] | str

# s = ["abc", "def"]

# print(list(s))

a = [1,2,3,4,5,6,7,8,9,10]
b = [2,3,5,7]

print([n for n in a if n in b])
print([n for n in a if n not in b])