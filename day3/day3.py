import re
from functools import reduce

# https://adventofcode.com/2024/day/3

lines:str=""
with open('./day3/input.txt','r') as file:
    
    # merge = lambda x: x.strip()
    # for l in file.readlines():
    #     lines+= merge(l)
    
    # this is equivalent
    lines = reduce(lambda a, b: a+b,file.readlines(),"")

print(lines)

pattern = "mul\((\d{1,3}),(\d{1,3})\)"

exp = re.compile(pattern)
matches = exp.findall(lines)
print("part1")
print(sum([int(x)*int(y) for x,y in matches]))


condPattern = "mul\((\d{1,3}),(\d{1,3})\)|(don\'t\(\))|(do\(\))"
expCond = re.compile(condPattern)

matches = expCond.findall(lines)
print(matches)

matchesFilter = []
s=True
for a,b,dont,do in matches:
    

    if dont is not "":
        s=False
    
    if do is not "":
        s=True
    
    if s and (a is not "") and (b is not ""):
        matchesFilter.append((a,b))

print(matchesFilter)
print(sum([int(a)*int(b) for a,b in matchesFilter]))
        


