#!/usr/bin/python

# Title to function: Let's extract the function and possibly level and industry from titles
#
# Example: Senior VP of Marketing / Vice President of Marketing / SVP of Marketing / Global Head of Marketing / CMO / Chief Marketing Officer -- Function should be marketing. How can we organize and normalize this dataset to help us get a better idea of what people do based on their title? Bonus points for any level and industry normalization
# Input example: data/titles.txt

class MainObj:
    CURRENT = '+-|-|CURRENT|-|-+'

    def __init__(self):
        self.levels = {self.CURRENT: {}}
        self.functions = {self.CURRENT: {}}
        self.industries = {self.CURRENT: {}}

    def reset_all_currents(self):
        self.levels[self.CURRENT] = {}
        self.functions[self.CURRENT] = {}
        self.industries[self.CURRENT] = {}

    @classmethod
    def extract_line(cls, input_file):
        try:
            with open(input_file) as f:
                content = f.readlines()
                # you may also want to remove whitespace characters like `\n` at the end of each line
                content = [x.strip().replace('" ,', '').replace('"', '') for x in content]
                return content
        except IOError as e:
            return [input_file]

    FOLLOW_BY = 'FOLLOW_BY'

    predefined_level_levels = {
        'Executive': 5,
        'Senior': 3
    }

    predefined_levels = {
        'Co-Founder': 101,
        'Founder': 101,
        'CEO': 100,
        'CIO': 90,
        'CTO': 90,
        'COO': 90,
        'CDO': 90,
        'CMO': 90,
        'CFO': 90,
        'Chief of': 80,
        'chief of': 80,
        'Chief': 80,
        'chief': 80,
        'Global Head of': 75,
        'Head': 70,
        'Head of': 70,
        'President': 65,
        'Director': 60,
        'Director of': 60,
        'EVP': 55,
        'SVP': 53,
        'VP': 50,
        'V.P.': 50,
        'Vice President': 50,
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

    predefined_all_levels = None  # this is aggregation of the previous two

    predefined_functions = {
        'Member Board Of Directors': '',
        'Business Development': '',
        'Customer Success': '',
        'Geo Team': ''
    }

    def isalpha(self, s):
        s = s.strip()
        if s:
            for c in s:
                if not (c.isalpha() or c == ' ' or c == '&'):
                    return False
            return True
        else:
            return False

    def remove_noise(self, t):
        t = t.strip()
        if t == ',' or t == ')' or t == '(':
            return ''
        else:
            return t

    def remove_noises(self, t):
        try:
            t = t.replace("()", "").strip()
            if 'of ' == t[0:3]:
                t = t[3:]
            if t:
                tt = t[0: len(t) - 1] + self.remove_noise(t[len(t) - 1])    # beautify the last character
                ttt = self.remove_noise(tt[0:1]) + tt[1:]                   # beautify the first character
                return ttt
            else:
                return ''
        except Exception as e:
            print ('ERRORS! on t: {0}, error: {1}'.format(t, e))
            return ''

    def remove_noises_for_function(self, t):
        if t:
            if t[0:1] == '&':
                t = t[1:].strip()
            if t[0:3].lower() == 'of ':
                t = t[3:]
        return t


    def remove_noises_for_industry(self, t):
        if 'at ' in t.lower():
            t = t.replace('at ', '')
        elif '@' in t:
            t = t.replace('@', '')
        elif '-' in t:
            t = t.replace('-', '')
        return t

    def valid_entry(self, k):
        # so far, it must contain any alpha in the word
        valid = False
        for c in k:
            cc = c + ""
            if cc.isalpha():
                valid = True
        return valid

    def store(self, k, ls, must_contains_all_alpha=True):
        # first make sure it is all if it is required
        if must_contains_all_alpha:
            if not self.valid_entry(k):
                return False
        k = k.strip()
        k = self.remove_noises(k)
        if k in ls:
            ls[k] += 1
            if not k in ls[self.CURRENT]:
                ls[self.CURRENT][k] = 1
            else:
                ls[self.CURRENT][k] += 1
        else:
            ls[k] = 1
            ls[self.CURRENT][k] = 1
        return True

    def level_is_in_title(self, k, title):
        if k in title:
            next_char_pos = title.find(k) + len(k)
            if next_char_pos == len(title):  # end of the string
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

    def retrieve_predefined_levels(self):
        if not self.predefined_all_levels:
            self.predefined_all_levels = {}
            for key, value in self.predefined_levels.items():
                if value < 80:
                    for key1, value1 in self.predefined_level_levels.items():
                        k = key1 + ' ' + key
                        v = value1 + value
                        self.predefined_all_levels[k] = v
                self.predefined_all_levels[key] = value
        return self.predefined_all_levels

    def try_parse_chief(self, key, title):
        n_key = ''
        if (key == 'Chief' or key == 'chief') and key in title:
            alls = title.split(' ')
            word2 = None
            word3 = None
            try:
                for x in range(0, len(alls)):
                    if self.remove_noises(alls[x]) == key:
                        # try to go back to see if it is XXX in chief:
                        if x - 2 >=0:
                            word_p_2 = alls[x - 1]
                            if word_p_2.lower() == 'in':
                                word_p_3 = self.remove_noises(alls[x - 2])
                                return word_p_3 + ' ' + word_p_2 + ' ' + key    # done
                        if x + 2 < len(alls):
                            if ',' in alls[x + 1]:  #if there is a comma, we should just end here
                                word2 = self.remove_noises(alls[x + 1])
                            else:
                                word2 = self.remove_noises(alls[x + 1])
                                word3 = self.remove_noises(alls[x + 2])
                                # if more to parse
                                if not 'officer' in word3.lower() and (word3.isalpha() or word3 == '&'):
                                    for xx in range(3, len(alls) - x):
                                        if alls[x + xx].isalpha() or alls[x + xx] == '&':
                                            word3 = word3 + ' ' + alls[x + xx]
                                        else:
                                            break
            except Exception as e:
                word2 = None  # placeholder
            if word2:
                n_key = key + ' ' + word2
            if word3:
                word3 = self.remove_noises(word3.strip())
                if self.isalpha(word3):
                    title = self.get_best_level(word3)  # see if there is a potential title here, if yes, not going to append it
                    if not title:
                        n_key = n_key + ' ' + word3
        else:
            return ''   # else, nothing returned
        return n_key if n_key else key

    def get_best_level(self, t):
        all_levels = self.retrieve_predefined_levels()
        max = -1
        max_keys = []
        for key, value in all_levels.items():
            if self.level_is_in_title(key, t) > -1:
                if value >= max:
                    max = value
                    max_keys.append(key)

        max_keys = self.eliminate_duplicate_levels(max_keys)
        if len(max_keys) > 1:
            # Now look up again to get the best score
            max = -1
            max_key = None
            max_length = 0
            max_length_key = None
            for key in max_keys:
                if all_levels[key] > max:
                    max = all_levels[key]
                    max_key = key
                if len(key) > max_length:   # i also pick the longest key
                    max_length = len(key)
                    max_length_key = key

            # Greedy algorithm: if ['Vice President', 'Executive Vice President', 'President'], i pick Executive Vice President even President might have highest score
            if max_length_key != max_key:
                # of course, except chief
                if max_key != 'Chief' and max_key != 'CHIEF' and max_key != 'chief':
                    max_key = max_length_key

            try_cheif = self.try_parse_chief(max_key, t)
            return try_cheif if try_cheif else max_key
        elif len(max_keys) == 1:
            try_cheif = self.try_parse_chief(max_keys[0], t)
            return try_cheif if try_cheif else max_keys[0]
        else:
            return None

    def is_this_a_chief_title(self, key):
        splited_keys = key.split(' ')
        if len(splited_keys) > 2 and (splited_keys[0] == 'Chief' or splited_keys[0] == 'chief'):
            return True
        if len(splited_keys) > 2 and (splited_keys[2] == 'Chief' or splited_keys[2] == 'chief'):
            return True
        return False

    def parse_level(self, this_title):
        key = self.get_best_level(this_title)
        if key:
            levels = self.levels
            stored = self.store(key, levels)
            if stored:
                if self.is_this_a_chief_title(key):
                    # it is a chief xxx xxx
                    this_title = this_title.replace(key, '')
                elif ' of' in key:
                    parsed_title = self.parse_function_of(this_title, key)
                    this_title = parsed_title
                else:
                    this_title = this_title.replace(key, '')
                if this_title[0:2] == ', ':
                    this_title = this_title[2:]
                if this_title[0:1] == '&':
                    this_title = this_title[1:]
        else:
            return False
        if len(this_title) > 0:  # if there is still something to parse the level, try it again
            more_to_parse = None
            try:
                more_to_parse = self.parse_level(this_title)
            except RuntimeError as e:
                print ('Running time error: {0} on e: {1}'.format(this_title, str(e)))
            if not more_to_parse:
                if this_title:
                    if not self.functions[self.CURRENT] and not self.industries[self.CURRENT]:
                        # if nothing was parsed into functions nor industries, return the orignal for later stage
                        return this_title
                    else:
                        # This means we are done since beginning was something and returned nothing
                        return ''
                else:
                    return this_title
            if more_to_parse:
                return more_to_parse
        return this_title

    def parse_function_single(self, f):
        if '-in-' in f:
            f = f.replace('-in-', '')
        stored = self.store(f, self.functions)
        if stored:
            f = f.replace(f, '')
        return f

    def parse_function_of(self, that_title, key=None):
        if key:
            pos = that_title.find(key) + len(key)
            function = that_title[pos:]
            industry = ''
            if function.count(',') == 1:
                industry = function[function.find(',') + 1:]
                industry = industry.strip()
                self.parse_industry(industry)
                industry_parsed = True
                function = function[0:function.find(',')]
            stored = self.store(function, self.functions)
            if stored:
                that_title = that_title.replace(key, '')  # eliminate the parsed function by that key
                that_title = that_title.replace(function, '')  # eliminate the parsed function
                if industry:
                    that_title = that_title.replace(industry, '')  # eliminate the parsed function
            return that_title
        else:
            that_title = that_title[3:]
            end_pos = len(that_title)
            if ',' in that_title:
                end_pos = that_title.find(',')
            function = that_title[0:end_pos]
            return self.parse_function_single(function)

    # This function is solely called from the parse_function so far
    def split(self, s, delim=','):
        if ' at ' in s:
            s = s.split(' at ')[0]
        elif '@' in s:
            s = s.split('@')[0]
        elif '-' in s:
            a = s.split('-')
            first_half = self.remove_noises(a[0])
            if self.isalpha(first_half):
                s = first_half  # ok this first half is good to be function!
            else:
                s = self.remove_noises(a[1])
        a = s.split(delim)
        aa = filter(lambda x: self.valid_entry(x), a)
        return aa

    def this_person_has_chief_title(self, current_titles):
        for t in current_titles:
            a = t.lower().split(' ')
            if len(a) == 3:
                if 'chief' == a[0] and 'officer' in a[2]:
                    return True
                if ('chief' == a[0] or 'chief' == a[2]) and 'in' == a[1]:
                    return True
        return False

    def parse_function(self, that_title):
        def function_is_in_title(k, t):
            try:
                if k in t:
                    return 1
            except Exception as e:
                return -1
            return -1

        stored = None
        for key, value in self.predefined_functions.items():
            if function_is_in_title(key, that_title) > -1:
                functions = self.functions
                stored = self.store(key, functions)
                if stored:
                    that_title = that_title.replace(key, '').strip()
        if not stored:
            # Now, just try to store the whole that_title
            that_title = self.remove_noises_for_function(self.remove_noises(that_title.strip()))
            all_functions = self.split(that_title, delim=',')
            if all_functions and len(all_functions) > 0:
                if not self.this_person_has_chief_title(self.levels[self.CURRENT]):
                    up_to = 0
                    if len(all_functions) > 1:
                        up_to = 1   # leave the last one for industries
                    for i in range(0, len(all_functions) - up_to):
                        this_function = all_functions[i]
                        stored = self.store(this_function, self.functions)
                        if stored:
                            that_title = that_title.replace(this_function, '')
        return that_title

    def parse_industry(self, that_title, last_parse=False):
        that_title = self.remove_noises(that_title)
        that_title = self.remove_noises_for_industry(that_title)
        titles = that_title.split('|')
        if titles:
            for t in titles:
                if t.find(',') > 0 and not last_parse:  # if there is a comma in that, the last part is the industry and the first part is function
                    pos = t.find(',')
                    industry = t[pos + 1:len(t)]
                    stored = self.store(industry, self.industries)
                    if stored:
                        that_title = that_title.replace(industry, '').strip()
                    # now parse the function
                    function = t[0:pos]
                    that_title = self.parse_function_single(function)
                else:
                    stored = self.store(t, self.industries)
                    if stored:
                        that_title = that_title.replace(t, '').strip()
        return that_title

    def print_summary(self):
        print ('--- Summary of Levels ----')
        for k, v in self.levels.items():
            print ('L: There are ' + str(v) + ' numbers of ' + k)
        print ('--- Summary of Functions ----')
        for k, v in self.functions.items():
            print ('F: There are ' + str(v) + ' numbers of ' + k)
        print ('--- Summary of Industries ----')
        for k, v in self.industries.items():
            print ('I: There are ' + str(v) + ' numbers of ' + k)

    @classmethod
    def dedup_titles(cls, titles):
        # if i see 'COO' and 'Chief Operating Officer' in the keys, remove COO
        s = None
        l = None
        for k in titles:
            if len(k) == 3:
                s = k
            if len(k.split(' ')) == 3:
                ws = k.split(' ')
                if 'chief' == ws[0].lower():
                    l = k
        if s and l:
            matched = True
            for i in range(0, len(s)):
                if s[i].lower() != ws[i][0:1].lower():
                    matched = False
            if matched:
                del titles[s]
        return titles


    def analyze(self, input_file):
        titles = self.extract_line(input_file)
        for tit in titles:
            self.reset_all_currents()
            t = tit
            t = self.parse_level(t)
            if t == False:
                if not self.levels[self.CURRENT]:
                    # if nothing parsed in the current levels, pass the original to the down stream
                    t = tit
            t = self.parse_function(t)
            if t:
                t = self.parse_industry(t, last_parse=True)
                # print ('Processed title: ' + t)

        # remove all current
        del self.levels[self.CURRENT]
        del self.functions[self.CURRENT]
        del self.industries[self.CURRENT]

        # dedup the titles if duplicate in logics
        self.levels = self.dedup_titles(self.levels)
        self.print_summary()

    def run_main(self):
        input_file = 'data/titles.txt'
        # input_file = 'data/titles_1.txt'
        self.analyze(input_file)


if __name__ == '__main__':
    mainObj = MainObj()
    mainObj.run_main()
