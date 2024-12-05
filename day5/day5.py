import re
from functools import reduce
import itertools

from sqlalchemy import false

rules: list[tuple[int, int]]
updates: list[int]

with open('./day5/input.txt', 'r') as file:
    data = file.read()


# Split the data into the two sections
tuple_section, list_section = data.strip().split("\n\n")

# Parse the tuple section
rules= [tuple(map(int, line.split('|'))) for line in tuple_section.splitlines()]

# Parse the list section
updates= [list(map(int, line.split(','))) for line in list_section.splitlines()]


# Output the results
# print("Tuples:", rules)
# print("Lists:", updates)

def check_update(rules: list[tuple[int, int]], update: list[int]) -> bool:
    # Apply the set of rules to a single update
    #check if both rule nums appears in the update:

    checks = []
    for rule in rules:
        l = rule[0] #must appear before r
        r = rule[1] #must be after l

        # search for l and r
        lfound = None
        rfound = None
        for i,n in enumerate(update):
            if n==l:
                lfound = i
            if n==r:
                rfound = i

            if (lfound is not None) and (rfound is not None):
                break

        if (lfound is not None) ^ (rfound is not None):
            #only one was found, then return true
            checks.append(True)
            continue
        if lfound is None and rfound is None:
            checks.append(True)
            continue

        if (lfound is not None) and (rfound is not None):
            # check the index l must be lower than r
            if lfound > rfound:
                # print(f'Not compliant at rule {rule} for {update}. lin:{lfound}, rin:{rfound}')
                checks.append(False)
                continue
            else:
                checks.append(True)
                continue


    # Default return
    return all(checks)


def find_middle_element(input:list) -> int:
    if len(input)%2 == 0:
        # There is no middle element bc len is even
        return False

    target_index = divmod(len(input),2)[0]

    return input[target_index]

def check_update_swap(rules: list[tuple[int, int]], update: list[int]) -> bool:
    # strategy is to swap elements when a rule fails
    new_update = None
    checks = []
    for rule in rules:
        l = rule[0] #must appear before r
        r = rule[1] #must be after l

        # search for l and r
        lfound_index = None
        rfound_index = None
        for i,n in enumerate(update):
            if n==l:
                lfound_index = i
            if n==r:
                rfound_index = i

            if (lfound_index is not None) and (rfound_index is not None):
                break

        if (lfound_index is not None) ^ (rfound_index is not None):
            #only one was found, then return true
            checks.append(True)
            continue
        if lfound_index is None and rfound_index is None:
            checks.append(True)
            continue

        if (lfound_index is not None) and (rfound_index is not None):
            # check the index l must be lower than r
            if lfound_index > rfound_index:
                # print(f'Not compliant at rule {rule} for {update}. lin:{lfound_index}, rin:{rfound_index}')
                checks.append(False)
                # swap elements using the index and check again
                new_update = update.copy()
                new_update[lfound_index] = update[rfound_index]
                new_update[rfound_index] = update[lfound_index]
                # print(f'Swapping. Old update: {update}. New: {new_update}')
                # update = new_update.copy()
                return False,new_update

            else:
                checks.append(True)
                continue


    # Default return
    return all(checks),update

def find_correct_update(rules,update):

    rst,new_update = check_update_swap(rules,update)
    while (rst is not True):
        rst,new_update = check_update_swap(rules,new_update)

    return rst,new_update

if __name__ == "__main__":

    corrects_updates = [x for x in updates if check_update(rules, x) is True]

    print(corrects_updates)

    middles = [find_middle_element(x) for x in corrects_updates]
    print(f'{middles}')
    print(f'Sum:{sum(middles)}')

    falses_updates = [x for x in updates if check_update(rules, x) is False]

    fixes = [find_correct_update(rules,up)[1] for up in falses_updates]
    print(fixes)
    middles = [find_middle_element(x) for x in fixes]
    print(f'Sum:{sum(middles)}')

