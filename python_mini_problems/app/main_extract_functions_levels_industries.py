#!/usr/bin/python
from docutils.nodes import title
import operator

class MainObj:
    @classmethod
    def extract_line(cls, input_file):
        with open(input_file) as f:
            content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            content = [x.strip().replace('" ,', '').replace('"', '') for x in content]
            return content

    FOLLOW_BY = 'FOLLOW_BY'

    predefined_levels = {
        'Co-Founder': 101,
        'Founder': 101,
        'CEO': 100,
        'CIO': 90,
        'CTO': 90,
        'CDO': 90,
        'CMO': 90,
        'CFO': 90,
        'Chief of': 80,
        'Chief': 80,
        'Head': 70,
        'Head of': 70,
        'President': 65,
        'Senior Director': 62,
        'Director': 60,
        'Director of': 60,
        'Executive Vice President': 55,
        'EVP': 55,
        'Senior Vice President': 50,
        'SVP': 50,
        'VP': 49,
        'Vice President': 49,
        'Sr Manager': 23,
        'General Manager': 20,
        'HR Manager': 20,
        'GM': 20,
        'Senior': 15,
        'Sr.': 15,
        'Junior': 14,
        'Jr.': 14,
        'Associate': 10,
    }

    predefined_functions = {
        'Member Board Of Directors': '',
        'Business Development': '',
        'Customer Success': '',
        'Geo Team': ''
    }

    levels = {

    }

    functions = {

    }

    industries = {

    }

    def store(self, k, ls):
        if k in ls:
            ls[k] += 1
        else:
            ls[k] = 1

    def level_is_in_title(self, k, title):
        if k in title:
            next_char_pos = title.find(k) + len(k)
            if next_char_pos == len(title): # end of the string
                return next_char_pos
            next_char = title[next_char_pos:next_char_pos + 1]
            if next_char == ' ' or next_char == ',' or next_char == ')' or next_char == '/':
                return next_char_pos
            else:
                return -1
        return -1

    def eliminate_duplicate_levels(self, levels):
        to_be_remove = None
        pos = -1
        for l in levels:
            for r in levels:
                if l != r:
                    if l in r:
                        if ' of' in r:
                            to_be_remove = l
                            break
                    if r in l:
                        if ' of' in l:
                            to_be_remove = r
                            break
        if to_be_remove:
            levels.remove(to_be_remove)
        return levels



    def get_best_level(self, t, predefined_levels):
        max = -1
        max_keys = []
        for key, value in self.predefined_levels.items():
            if self.level_is_in_title(key, t) > -1:
                if value >= max:
                    max = value
                    max_keys.append(key)

        max_keys = self.eliminate_duplicate_levels(max_keys)
        if len(max_keys) > 1:
            # Now look up again to get the best score
            max = -1
            max_key = None
            for key in max_keys:
                if predefined_levels[key] > max:
                    max = predefined_levels[key]
                    max_key = key
            return max_key
        elif len(max_keys) == 1:
            return max_keys[0]
        else:
            return None

    def parse_level(self, this_title):
        key = self.get_best_level(this_title, self.predefined_levels)
        if key:
            levels = self.levels
            self.store(key, levels)
            this_title = this_title.replace(key, '').strip()
            if this_title[0:2] == ', ':
                this_title = this_title[2:]
            if this_title[0:1] == '&':
                this_title = this_title[1:]

            # Now, if i see the first characters is "of xxx", parse the function afterwards up to ,
            if this_title[0:3] == 'of ':
                this_title = self.parse_function_of(this_title)

        return this_title.strip()

    def parse_function_of(self, that_title):
        that_title = that_title[3:]
        end_pos = len(that_title)
        if ',' in that_title:
            end_pos = that_title.find(',')
        function = that_title[0:end_pos]
        self.store(function, self.functions)
        that_title = that_title.replace(function, '')
        return that_title

    def parse_function(self, that_title):
        def function_is_in_title(k, t):
            if k in t:
                return 1
            return -1

        for key, value in self.predefined_functions.items():
            if function_is_in_title(key, that_title) > -1:
                functions = self.functions
                self.store(key, functions)
                that_title = that_title.replace(key, '').strip()
        return that_title.strip()

    def parse_industry(self, that_title):
        if '|' in that_title:
            pos = that_title.find('|')
            industry = that_title[pos + 1:len(that_title)]
            self.store(industry, self.industries)
            that_title = that_title.replace(industry, '').strip()
        return that_title

    def print_summary(self):
        print ('--- Summary of Levels ----')
        for k, v in self.levels.items():
            print ('There are ' + str(v) + ' numbers of ' + k)
        print ('--- Summary of Functions ----')
        for k, v in self.functions.items():
            print ('There are ' + str(v) + ' numbers of ' + k)
        print ('--- Summary of Industries ----')
        for k, v in self.industries.items():
            print ('There are ' + str(v) + ' numbers of ' + k)

    def analyze(self, input_file):
        titles = self.extract_line(input_file)
        for t in titles:
            t = self.parse_level(t)
            t = self.parse_function(t)
            t = self.parse_industry(t)
            # print ('Processed title: ' + t)

        self.print_summary()

    def run_main(self):
        input_file = 'data/titles_1.txt'
        self.analyze(input_file)


if __name__ == '__main__':
    mainObj = MainObj()
    mainObj.run_main()
