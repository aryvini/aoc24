import re
from functools import reduce
from typing import Generator, NewType

coff=NewType('coff',int) #column offset type
roff=NewType('roff',int) #row offset type


lines:list[list[str]]
with open('./day4/input.txt','r') as file:
    lines = [letter for letter in [line.strip() for line in file.readlines()]]

# print(lines[0][3])
# line[i][j]
# i=row, j column



# replace the unecessary words

# def clean_list(input:list[list[str]])->list[list[str]]:
#     safe_letters = ['X','M','A','S']

#     return list(map(lambda x: [char if char in safe_letters else "." for char in x],input))


# mat = clean_list(lines)
# print(lines)


def dir_sequence():
    # [ 1 -1  1]
    # [-1  x  1]
    # [ 1  1  1]
    dirs = {
        # values are of (row,column) indexs
        'l':(0,-1),
        'r':(0,1),
        't':(-1,0),
        'b':(1,0),
        'lt':(-1,-1),
        'rt':(-1,1),
        'br':(1,1),
        'lb':(1,-1)
    }

    for dir in dirs:
        c,r = dirs[dir]
        yield c,r

def dir_sequence_pt2():
    dirs = {
        # values are of (row,column) indexs
        # 'l':(0,-1),
        # 'r':(0,1),
        # 't':(-1,0),
        # 'b':(1,0),
        # 'lt':(-1,-1),
        'rt':(-1,1),
        'br':(1,1),
        # 'lb':(1,-1)
    }

    for dir in dirs:
        c,r = dirs[dir]
        yield c,r



def as_sequence():
    for letter in ['A','S']:
        yield letter

def s_sequence():
    for letter in ['S']:
        yield letter

def search_pt1(matrix:list[list[chr]]):



    matches = []

    def find_dirs(row_start,column_start,matrix,target_letter:chr)->list[tuple[roff,coff]]:
        dir_gen = dir_sequence()
        found_dirs = []
        for row_offset,column_offset in dir_gen:
            # apply offset:
            try:
                target_column = column_start+column_offset
                target_row = row_start+row_offset
                if target_column < 0 or target_row < 0:
                    raise IndexError
                
                found_letter = matrix[target_row][target_column]
                if  found_letter == target_letter:
                    # found direction
                    # store this offset for usage later
                    print(f'M[{target_row+1},{target_column+1}]')
                    found_dirs.append((row_offset,column_offset))
            except IndexError:
                # if index not possible, try next
                continue
        
        return found_dirs


    def find_in_direction(row_start,column_start,row_offset,column_offset,matrix,letter:Generator[chr,None,None]):
        print('FINDING IN DIRECTION')
        print(f'checking dir({row_offset},{column_offset}) from [{row_start+1},{column_start+1}])')
        try:
            target_letter = next(letter, None)
            if(target_letter is None):
                return True
            target_column=column_start+column_offset
            target_row= row_start+row_offset
            found_letter = matrix[target_row][target_column]

            if target_column < 0 or target_row < 0:
                raise IndexError            
            
            if  found_letter == target_letter:
                
                # here we found a match, stablished the direction, we can keep looking into the same
                # recursively until generator letter finishes
                print(f'{target_letter}[{target_row+1},{target_column+1}]')
                return find_in_direction(target_row,
                                target_column,
                                row_offset,
                                column_offset,
                                matrix,
                                letter)
        except IndexError:
            # we ran out of indexes
            return False
        except StopIteration:
            # if there are no letters to be checked, means we have found our letter in this direction 
            return True
    


    
    # find first X in the main flow
    r=0
    c=0
    for r, row in enumerate(matrix):
        for c, char in enumerate(row):
            if char == 'X': #will return the first letter to be matched!
                # first match found, we can search the neighours and find the direction
                # there might be more than 1 match of the direction finder!
                print(f'X[{r+1},{c+1}]')
                found_dirs = find_dirs(r,c,matrix,'M')
                
                target_row=0
                target_column=0
                for index,(row_dir,column_dir) in enumerate(found_dirs):
                    print(f'--found {len(found_dirs)} directions, testing: {index+1}---')
                    as_gen = as_sequence() #reset the generator when we search in each direction
                    target_row=r+row_dir
                    target_column=c+column_dir
                    found_xmas = find_in_direction(target_row,target_column,row_dir,column_dir,matrix,as_gen)
                    if found_xmas:
                        print("FOUND A MATCH")
                        print('-------------')
                        matches.append(True)

            

    return matches

def search_pt2(matrix:list[list[chr]]):

    matches = []

    # find first A in the main flow
    r=0
    c=0
    for r, row in enumerate(matrix):
        for c, char in enumerate(row):
            if char == 'A': #will return the first letter to be matched!
                print(f'A[{r+1},{c+1}]')
                # extract values around A:
                try:

                    tl = (r-1,c-1)
                    br = (r+1,c+1)
                    bl = (r+1,c-1)
                    tr = (r-1,c+1)


                    if any([True if (x[0]<0 or x[1]<0) else False for x in [tl,br,bl,tr]]):
                        continue


                    diag1 = True if (matrix[tl[0]][tl[1]]=='M' and matrix[br[0]][br[1]] == 'S') or (matrix[tl[0]][tl[1]]=='S' and matrix[br[0]][br[1]] == 'M') else False  

                    diag2 = True if (matrix[bl[0]][bl[1]]=='M' and matrix[tr[0]][tr[1]] == 'S') or (matrix[bl[0]][bl[1]]=='S' and matrix[tr[0]][tr[1]] == 'M') else False

                    if diag1 and diag2:
                        print('Found Match')
                        matches.append(True)
                


                except IndexError:
                    continue
    


    return matches



if __name__ == "__main__":
    print(f'Part1: {sum(search_pt1(lines))}')
    print('FINISHED PART1')
    print(f'Part2: {sum(search_pt2(lines))}')
