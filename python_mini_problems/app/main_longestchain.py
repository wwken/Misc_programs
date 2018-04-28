#!/usr/bin/python

class MainObj:
    @classmethod
    def longestChain(cls, words):

        def remove(oldstr, i):
            return oldstr[:i] + oldstr[i+1:]

        def process(w, d, current_points, previous_calculations):
            max = current_points
            for i in range(0, len(w)):
                s = remove(w, i)
                if s in d:
                    all_points = -1
                    if s in previous_calculations:
                        all_points = previous_calculations[s]
                    else:
                        all_points = process(s, d, current_points + 1, previous_calculations)
                        previous_calculations[s] = all_points
                    if all_points > max:
                        max = all_points
            return max


        max= 0
        d={}
        for w in words:
           d[w] = 1

        for w in words:
            answer = process(w, d, 1, {})
            if answer > max:
                max = answer

        return max

    def run_main(self):
        words = [   'a',
                    'b',
                    'ba',
                    'bca',
                    'bda',
                    'bdca']

        a1s = self.longestChain(words)
        print a1s


if __name__ == '__main__':
    mainObj = MainObj()
    mainObj.run_main()
