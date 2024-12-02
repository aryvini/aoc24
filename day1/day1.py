
# https://adventofcode.com/2024/day/1

import numpy as np
import pandas as pd




with open('./day1.txt','r') as file:
    lines = file.readlines()


left : list[str]= []
right: list[str] = []

for line in lines:
    l = line.split(',')[0]
    left.append(l)
    
    r = line.split(',')[1]
    r = r.strip('\n')
    right.append(r)



def part1(left:list,right:list) -> int:
    left = np.array(left)
    right = np.array(right)

    left_sort = np.sort(left)
    right_sort = np.sort(right)

    dist = [abs(int(l) - int(r)) for l,r in zip(left_sort,right_sort)]
    dist = np.array(dist)


    print(dist.sum())
    return dist.sum()


def part2(left:list, right:list) -> int:
    left = np.array(left)
    right = np.array(right)

    left_sorted = np.sort(left)
    right_sorted = np.sort(right)
    occur: list = []
    for l in left_sorted:
        matches = 0
        for r in right_sorted:
            if (l == r):
                matches += 1

        occur.append(matches)  

    simi = [int(l)*int(m) for l,m in zip(left_sorted, occur)]
    # print(left_sorted)
    # print(simi)
    print(sum(simi))
    return simi

part1(left=left, right=right)
part2(left=left,right=right)



