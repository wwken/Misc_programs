#!/usr/bin/python

# This problem is to find the min number out of the rotating sorted numbers.
#   For example, the input can be: 1, 2, 3, 4, 5, 6, then the min is 1
#               or 4, 5, 6, 1, 2 then the min is 1
#   The running time of it should be o(log n)

def find(ary):
    if len(ary) == 1:
        return ary[0]
    elif len(ary) == 2:
        return min(ary[0], ary[1])
    elif ary[0] < ary[len(ary) - 1]:
        return ary[0]
    else:
        if len(ary) % 2 == 0:   # even number of elements
            mid = len(ary) / 2 - 1
            mid_next = mid + 1
        else:                   # odd number of elements
            mid = len(ary) / 2
            mid_next = mid
        first_half_good = True
        second_half_good = True
        if ary[0] < ary[mid]:
            first_half_good = False
        if ary[mid_next] < ary[len(ary) - 1]:
            second_half_good = False
        if first_half_good:
            return find(ary[0:mid + 1])
        else:
            return find(ary[mid + 1:])

print(find([2, 3, 3, 1]))     # 1
print(find([4, 1, 2, 3]))     # 1
print(find([3, 4, 1, 2]))     # 1
print(find([1, 2, 3]))     # 1
print(find([3, 1, 2]))     # 1
print(find([2, 3, 1]))     # 1
print(find([1, 2, 3, 4, 5, 6]))     # 1
print(find([4, 5, 6, 1, 2]))        # 1
print(find([11, 12, 19, 3, 5]))     # 3
print(find([11, 12, 19, 213, 5]))   # 5
print(find([11, 12, 19, 213, 5, 6]))    # 5
print(find([11, 12, 19, 213, 5, 6, 10]))    # 5
print(find([11, 12, 19, 213, 2, 5, 6, 10])) # 2