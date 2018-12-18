#!/usr/bin/python

# Given a NxN matrix which denotes a friend relationship of person A and person B, compute the number of friend circles
# By definition, a person is a friend of him/herself.
# For example, the following matrix contains three friend circles (since everyone is only friend of himself):
#   Y N N
#   N Y N
#   N N Y
# For another example, the following matrix contains two friend circles
# (since person 1 is friend of person 2 and person 2 is friend of person 3 while person 4 is friend of himself):
#   Y Y N N
#   Y Y Y N
#   N Y Y N
#   N N N Y

def friendCircles(friends):
    l = len(friends)
    circles = []
    duplicatedCount = 0
    for i in range(l):
        for j in range(l):
            # print(i, j)
            v = friends[i][j]
            if v == 'Y':
                found = False
                appear_sets = []
                unappear_sets = []
                for c in circles:
                    if i in c or j in c:
                        appear_sets.append(c)
                    else:
                        unappear_sets.append(c)
                if len(appear_sets) > 1:
                    s = appear_sets[0].union(appear_sets[1])
                    # print(i,j,s)
                    unappear_sets.append(s)
                    circles = unappear_sets
                    found = True
                if len(appear_sets) == 1:
                    appear_sets[0].add(i)
                    appear_sets[0].add(j)
                    found = True
                if not found:
                    n = set()
                    n.add(i)
                    n.add(j)
                    circles.append(n)

    return len(circles)


friends = [ 'YYNN',
            'YYYN',
            'NYYN',
            'NNNY']

# friends = ['YNNNY',
#            'NYNNN',
#            'NNYNN',
#            'NNNYY',
#            'YNNYY']

print friendCircles(friends)
