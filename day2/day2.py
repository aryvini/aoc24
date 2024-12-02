
import numpy as np


with open('./day2/input.txt','r') as file:
    reports = [list(map(int,line.split())) for line in file]
          

def check_level(report:list[int])->bool:
    levels = report
    status:bool = False
    # 7 6 4 2 1

    
    all_increasing: list[bool] = []
    for prev, curr in zip(levels,levels[1:]):
        if (abs(curr-prev)>3):
            status = False
            print(f'Big increase or decrease, returning')
            return status
        elif (curr == prev):
            status = False
            print(f'No changes, returning')
            return status
        

        if((curr-prev)>0):
            all_increasing.append(True)
        else:
            all_increasing.append(False)
    

    # check all increasing
    if all(all_increasing):
        print(f'Everything increasing: {all_increasing}')
        status = True
        return status
    elif all([x==False for x in all_increasing]):
        print(f'Everything decreasing: {all_increasing}')
        status = True
        return status
    else:
        print(f'Not everything decreasing or increasing: {all_increasing}')
        status=False
        return status


results :list[bool] = list()
for report in reports:
    print(f'checking: {report}--------------')
    status = check_level(report)
    print(f'status: {status}')
    results.append(status)

print(f'total of valid reports: {sum(results)}')

def check_level_permutations(report:list[int]) -> bool:
    
    permutations_rst:list[bool] = []
    for i in range(0, len(report)):
        report_copy = report.copy()
        report_copy.pop(i)
        report_updated = report_copy
        print(f' {report} permutation {report_updated}')
        permutations_rst.append(check_level(report_updated))
    
    return any(permutations_rst)

results :list[bool] = list()
for report in reports:
    print(f'checking: {report}--------------')
    status = check_level_permutations(report)
    print(f'status: {status}')
    results.append(status)

print(f'total of valid reports after permutation: {sum(results)}')



