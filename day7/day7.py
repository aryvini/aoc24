import re
from functools import reduce
from itertools import product

TEST_DATA = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20'''


ADD='+'
TIMES='x'
CONCAT = '||'

def parse_line(line:str):

    expected_result:int

    expected_result=line.split(':')[0]
    operands_text = line.split(':')[1]
    operands = operands_text.strip()
    operands_parsed = []
    reg='(\d*)'
    exp = re.compile(reg)
    matches = exp.findall(operands)

    for match in matches[:-1]:
        # Remove the last None occurence, because we dont need them
        if match == '':
            # None will be the place of our operators
            operands_parsed.append(None)
        else:
            operands_parsed.append(int(match))


    return (int(expected_result),operands_parsed)


def parse_data(data) -> list[tuple[int,list]]:

    return [parse_line(line) for line in data.splitlines()]


def perform_operation(accumulated, current):
    op, value = current

    if op == ADD:
        return accumulated+value
    if op == TIMES:
        return accumulated*value
    if op == CONCAT:
        return int(str(accumulated)+str(value))
    else:
        raise ValueError(f"Unsupported operator: {op}")

def generate_combinations(operands:list,operators=[ADD,TIMES]):

    # Create a list for later create the product:
    options = [operators if x is None else [x] for x in operands]
    # [[1],[ADD,TIMES],[2]...]

    # unpacking this direct at argument will be the same as:
    # a=[1]
    # b = [ADD,TIMES]
    # c = [2]
    # product(a,b,c)
    combinations = list(product(*options))

    return combinations

def isValid(test: tuple[int, list[int]], possible_operators=[ADD,TIMES]) -> bool:

    expected = test[0]
    operands = test[1]

    # generate combinations
    combinations = generate_combinations(operands,possible_operators)
    # combinations are in form of: [(10,'+',19),...]
    # to use reduce we need them like this: (+,10) (+,19)
    # the evaluate function will have a initial value (first combination value) and then takes 2 arguments: operator and operand to make the
    # evaluation


    for comb in combinations:
        # Prepare pairs of (operator, operand)
        pt1 = comb[1::2]
        pt2 = comb[2::2]
        pairs = zip(pt1,pt2) # [('+', 40), ('+', 27)]
        rst = reduce(perform_operation, pairs, comb[0])
        if rst == expected:
            return True
    return False

def check_tests(tests:list,possible_operators = [ADD,TIMES]):

    return [test for test in tests if isValid(test,possible_operators)]

if __name__ == '__main__':
    print('TEST DATA TEST DATA')
    OPERATORS_PT1=[ADD,TIMES]
    parsed_tests = parse_data(TEST_DATA)
    # print(parsed_tests)
    valid_tests = check_tests(parsed_tests,OPERATORS_PT1)
    print(f'Sum Valid tests with {OPERATORS_PT1}: {sum([test[0] for test in valid_tests ])}')

    print('--------------------------------')

    print('INPUT DATA INPUT DATA')
    with open('./day7/input.txt') as file:
        FILE_DATA = file.read()
    parsed_tests = parse_data(FILE_DATA)
    # print(parsed_tests)
    valid_tests = check_tests(parsed_tests,OPERATORS_PT1)
    print(f'Sum Valid tests with {OPERATORS_PT1}: {sum([test[0] for test in valid_tests ])}')

    print('--------------------------------')

    parsed_tests = parse_data(FILE_DATA)
    OPERATORS_PT2=[ADD,TIMES,CONCAT]
    valid_tests = check_tests(parsed_tests,OPERATORS_PT2)
    print(f'Sum Valid tests with {OPERATORS_PT2}: {sum([test[0] for test in valid_tests ])}')