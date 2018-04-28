#!/usr/bin/python

class MainObj:
    @classmethod
    def friendCircles(cls, friends):
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

    def run_main(self):
        friends = [ 'YYNN',
                    'YYYN',
                    'NYYN',
                    'NNNY']

        friends = ['YNNNY',
                   'NYNNN',
                   'NNYNN',
                   'NNNYY',
                   'YNNYY']

        # friends = ['YY',
        #            'YY']

        a1s = self.friendCircles(friends)
        print a1s


if __name__ == '__main__':
    mainObj = MainObj()
    mainObj.run_main()
