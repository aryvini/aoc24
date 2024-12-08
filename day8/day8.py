import copy
import os
import re
from functools import reduce
from itertools import combinations
from math import sqrt
from operator import truediv

from setuptools.wheel import unpack

TEST_DATA = '''............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............'''


ANTINODE = '#'



def parse_data(data):

    return [list(line) for line in data.splitlines()]

def find_antennas(field):
    # find any digit or char

    exp = '(\d{1}|[A-Za-z]{1})'
    reg = re.compile(exp)

    antennas:set[tuple[chr,tuple[int,int]]] = set()
    # store in a set the info like this: ('A', (x,y))
    for r,row in enumerate(field):
        for c, char in enumerate(row):
            matches = reg.findall(char)
            if len(matches)>0:
                freq = matches[0]
                pos = (r,c)
                antennas.add((freq,pos))

    return antennas

def find_antinodes_pt1(field, antennas):
    antinode_field = copy.deepcopy(field)
    antinodes:set[tuple[int,int]] = set()

    unique_frequencies:set[tuple[int,int]] = {ant[0] for ant in antennas}
    # find the combination of 2 antennas of same frequency

    for freq in unique_frequencies:
        filtered_antennas = [item[1] for item in antennas if item[0] == freq]

        combs = list(combinations(filtered_antennas,2))

        for comb in combs:
            pos1,pos2 = comb
            dr,dc = get_dist_dir(pos1,pos2)

            # Place antinodes
            an1r = pos2[0] + dr
            an1c = pos2[1] + dc

            an2r = pos1[0] + dr * -1 #invert direction
            an2c = pos1[1] + dc * -1 #inver direction




            if palce_antinode(antinode_field,(an1r,an1c)) is not False:
                antinodes.add((an1r,an1c))
            if palce_antinode(antinode_field,(an2r,an2c)) is not False:
                antinodes.add((an2r,an2c))


            pass

    return antinodes,antinode_field

def find_antinodes_pt2(field, antennas):
    antinode_field = copy.deepcopy(field)
    antinodes:set[tuple[int,int]] = set()

    unique_frequencies:set[tuple[int,int]] = {ant[0] for ant in antennas}
    # find the combination of 2 antennas of same frequency

    for freq in unique_frequencies:
        filtered_antennas = [item[1] for item in antennas if item[0] == freq]

        combs = list(combinations(filtered_antennas,2))

        for comb in combs:
            ant1,ant2 = comb
            dr,dc = get_dist_dir(ant1,ant2)
            palce_antinode(antinode_field,ant1)
            palce_antinode(antinode_field,ant2)
            antinodes.add(ant1)
            antinodes.add(ant2)
                # Place antinodes in multiples of the distance until we fail!
            # try individually for each direction
            fail = False
            atLeast1 = False
            n = 1
            while not fail:
                an1r = ant2[0] + dr*n
                an1c = ant2[1] + dc*n
                if palce_antinode(antinode_field,(an1r,an1c)) is not False:
                    # if this is valid, make the position of the antenna also an antinode
                    antinodes.add((an1r,an1c))
                    atLeast1 = True
                    n += 1
                else:
                    fail = True


            fail = False
            n = 1
            atLeast2 = False
            while not fail:
                an2r = ant1[0] + dr *(n* -1) #invert direction
                an2c = ant1[1] + dc *(n * -1) #inver direction
                if palce_antinode(antinode_field,(an2r,an2c)) is not False:
                    # if this is valid, make the position of the antenna also an antinode
                    antinodes.add((an2r,an2c))
                    n += 1
                    atLeast2 = True
                else:
                    fail = True


            # if atLeast2 or atLeast1:
            #     palce_antinode(antinode_field,ant1)
            #     palce_antinode(antinode_field,ant2)
            #     antinodes.add(ant1)
            #     antinodes.add(ant2)
            pass

    return antinodes,antinode_field





def palce_antinode(antinode_field,pos):
    r,c = pos
    maxr,maxc = len(antinode_field),len(antinode_field[0])
    # check out of bounds
    if (not(0<=r<maxr)) or (not(0<=c<maxc)):
        return False

    antinode_field[r][c] = ANTINODE
    print_field(antinode_field,clear=True)

    return antinode_field


def print_field(field,clear=False):
    # if clear:
    #     os.system('cls')
    # for r,row in enumerate(field):
    #     chars = row
    #     rst = reduce(lambda x,y: str(x)+str(y), row)
    #     print(rst)

    pass
def get_dist_dir(pos1,pos2):

    r1,c1 = pos1
    r2,c2 = pos2

    dr = r2-r1
    dc = c2-c1

    return dr,dc

if __name__ == '__main__':
    print('TEST DATA ---------------------')
    field = parse_data(TEST_DATA)
    antennas = find_antennas(field)
    print(antennas)
    antinodes,antinodes_field = find_antinodes_pt1(field, antennas)
    print(f'Unique antinodes: {len(antinodes)}')
    print_field(antinodes_field)

    print('REAL DATA PT1 ---------------------')
    with open('./day8/input.txt') as file:
        data = file.read()

    field = parse_data(data)
    antennas = find_antennas(field)
    print(antennas)
    antinodes,antinodes_field = find_antinodes_pt1(field, antennas)
    print(f'Unique antinodes: {len(antinodes)}')
    print_field(antinodes_field)



    print('REAL DATA PT2 ---------------------')
    with open('./day8/input.txt') as file:
        data = file.read()

    field = parse_data(data)
    antennas = find_antennas(field)
    # print(antennas)
    antinodes,antinodes_field = find_antinodes_pt2(field, antennas)
    print(f'Unique antinodes: {len(antinodes)}')
    print_field(antinodes_field)