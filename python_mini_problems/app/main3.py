#!/usr/bin/python

class MainObj:

    def is_this_number_min_up_to(self, ary, n, l):
        for i in xrange(0, l):
            if ary[i] < n:
                return False
        return True

    def swap(self, ary, i, j):
        tmp = ary[i]
        ary[i] = ary[j]
        ary[j] = tmp

    def solution(self, ary):
        l = len(ary)
        for i in xrange(0, l):
            this_num = ary[i]
            if i + i < l:
                next_num = ary[i + 1]
                if this_num > next_num: # Found a digit that is larger than the next number
                    # Now to determine if the next number the min of all the previous numbers
                    is_next_num_min = self.is_this_number_min_up_to(ary, next_num, i+1)
                    # Now loop from the end to find a digit that is smaller than this number and perform swap
                    for j in xrange(0, l):
                        if is_next_num_min:
                            jj = j
                            the_swap_num = ary[jj]
                            if the_swap_num > next_num: # Found, now try to swap it
                                self.swap(ary, i+1, jj)
                                # Now i have swapped the array, now i am looping through to see if it is sorted
                                for z in xrange(0, l-1):
                                    if ary[z] > ary[z+1]:
                                        return False
                                return True     # The array has been sorted already
                        else:
                            jj = l - j - 1
                            the_swap_num = ary[jj]
                            if the_swap_num < this_num: # Found, now try to swap it
                                self.swap(ary, i, jj)
                                # Now i have swapped the array, now i am looping through to see if it is sorted
                                for z in xrange(0, l-1):
                                    if ary[z] > ary[z+1]:
                                        return False
                                return True     # The array has been sorted already

        return True     # The array has been sorted already

    def run_main(self):
        a1 = [1, 5, 3, 3, 7]
        a1s = self.solution(a1)
        print a1s


if __name__ == '__main__':
    mainObj = MainObj()
    mainObj.run_main()
