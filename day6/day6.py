import os
import copy

field_raw:list[list[chr]]
with open('./day6/input.txt', 'r') as file:

    lines = [line.strip() for line in file.readlines()]

# print(lines)

field_raw = [list(s) for s in lines]
def find_guard(input:list[list[chr]]) -> tuple[int,int]:
    guards = ['^','>','v','<']
    for r, row in enumerate(input):
        for c, char in enumerate(row):
            if char in guards:
                return (r,c)

    return None

def print_field(field):
    # os.system("cls")
    # for l in field:
    #     print(l)
    #     # print('\n')

    pass


def walk(field:list[list[chr]], start:tuple[int,int]):

    movs = {
        '^':(-1,-0),
        '>':(0,+1),
        'v':(+1,0),
        '<':(0,-1)
    }

    field_size = (len(field),len(field[0]))

    def get_guard_dir(guard_pos:tuple[int,int])-> movs:
        #make sure the guard is here:
        # if guard_pos != find_guard(field):
        #     return False
        r,c = guard_pos
        ch = field[r][c]

        return movs[ch],ch

    def has_conflict(guar_pos:tuple[int,int]):
        r,c = guar_pos
        try:
            if field[r][c] == "#":
                return True
        except Exception:
            return True
        return False

    def rotate(curr:chr)->chr:

        if curr == '^':
            return '>'
        elif curr == '>':
            return 'v'
        elif curr == 'v':
            return '<'
        elif curr == '<':
            return '^'
        else:
            return None


    def out_of_bounds(field,pos)-> bool:
        r,c = pos
        maxr,maxc = field_size
        if (0<=r<maxr) and (0<=c<maxc):
            return False
        return True

    visited_places:set[tuple[int,int]] = set()
    visisted_cycles:set[tuple[tuple[int,int],tuple[int,int]]] = set() #store cycles:

    isCycle:bool = False


    visited_places.add(start)
    leave = False
    curr_pos = start
    walk_dir,char_dir = get_guard_dir(curr_pos)
    field[curr_pos[0]][curr_pos[1]] = 'X'

    visisted_cycles.add((curr_pos,walk_dir))

    while leave is not True:

        # update pos
        new_pos = (curr_pos[0]+walk_dir[0],curr_pos[1]+walk_dir[1])
        # check outofbounds
        leave = out_of_bounds(field,new_pos)
        if leave:
            break
        r,c = new_pos

        # check for cycles:
        # the catch is: if a direction and position has been visited: we are in a cycle!
        # this is the catch!!!
        if (new_pos, walk_dir) in visisted_cycles:
            isCycle = True
            leave = True
            break
        else:
            visisted_cycles.add((new_pos,walk_dir))


        # check for conflicts
        if has_conflict(new_pos):
            # we found a conflict, we need to turn right
            new_gard_char = rotate(char_dir)
            field[curr_pos[0]][curr_pos[1]] = new_gard_char
            walk_dir,char_dir = get_guard_dir((curr_pos[0],curr_pos[1]))
            field[curr_pos[0]][curr_pos[1]] = 'X'
            print_field(field)
            # reset the loop
            continue

        # here there is no conflict, increment position
        visited_places.add(new_pos)
        field[r][c] = 'X'
        print_field(field)
        curr_pos = new_pos



    return visited_places, isCycle

def find_obstacles(field, start):
    field1 = copy.deepcopy(field)
    possible_obstacles,_ = walk(field1,start)
    possible_obstacles.remove(start)

    obstacles = set()
    for candidate in possible_obstacles:
        changed_field = copy.deepcopy(field)
        changed_field[candidate[0]][candidate[1]] = '#'
        _, is_cycle = walk(changed_field, start)

        if is_cycle:
            obstacles.add(candidate)

    return obstacles



if __name__ == '__main__':
    field1 = copy.deepcopy(field_raw)
    print(find_guard(field1))
    vis,_ = walk(field1,find_guard(field1))
    print(f'Part1: {len(vis)}')

    field2 = copy.deepcopy(field_raw)
    obstacles = find_obstacles(field2, find_guard(field2))
    print(f'Part2: {len(obstacles)}')