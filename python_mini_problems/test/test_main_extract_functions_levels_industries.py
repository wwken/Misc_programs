import unittest
from app.main_extract_functions_levels_industries import MainObj


class TestExtractFunctionsLevelsIndustries(unittest.TestCase):

    def setUp(self):
        self.mainObj = MainObj()

    def test_get_best_level(self):
        keys = ['Senior Director', 'Head', 'Head of']
        eliminated_keys = self.mainObj.eliminate_duplicate_levels(keys)
        self.assertEqual(eliminated_keys, ['Senior Director', 'Head of'])

        keys = ['Senior Director', 'Head of', 'Head']
        eliminated_keys = self.mainObj.eliminate_duplicate_levels(keys)
        self.assertEqual(eliminated_keys, ['Senior Director', 'Head of'])

        keys = ['Director', 'Head of', 'Director of']
        eliminated_keys = self.mainObj.eliminate_duplicate_levels(keys)
        self.assertEqual(eliminated_keys, ['Head of', 'Director of'])

    def test_valid_entry(self):
        func = self.mainObj.valid_entry

        self.assertEqual(func('hello1'), True)
        self.assertEqual(func('| '), False)

    def test_remove_noises(self):
        f = self.mainObj.remove_noises
        self.assertEqual(f('Chief Brand Officer,'), 'Chief Brand Officer')
        self.assertEqual(f('(chief diversity officer)'), 'chief diversity officer')

    def test_remove_noises_for_function(self):
        f = self.mainObj.remove_noises_for_function
        self.assertEqual(f('& of Services'), 'Services')

    def test_try_parse_chief(self):
        f = self.mainObj.try_parse_chief
        self.assertEqual(f('Chief', 'Chief Brand Officer, Google'), 'Chief Brand Officer')
        self.assertEqual(f('chief', 'Global Head of Inclusion & Diversity (chief diversity officer)'), 'chief diversity officer')
        self.assertEqual(f('Chief', 'SVP, Editor in Chief, Content Marketing & Syndication,'), 'Editor in Chief')
        self.assertEqual(f('Chief', 'Executive Vice President & Chief Counsel, Cable Entertainment Legal Affairs'), 'Chief Counsel')
        self.assertEqual(f('Chief', 'Executive Vice President, Cable Entertainment Legal Affairs'), '')
        self.assertEqual(f('Chief', 'SVP & Chief Employment and Corporate Infrastructure Counsel'), 'Chief Employment and Corporate Infrastructure Counsel')
        self.assertEqual(f('Chief', 'Partner, Chief Marketing & Content Officer'), 'Chief Marketing & Content Officer')

    def test_get_best_level(self):
        f = self.mainObj.get_best_level
        self.assertEqual(f('Executive Vice President & , Cable Entertainment Legal Affairs'), 'Executive Vice President')

    def test_parse_function(self):
        self.mainObj.parse_function(' & , Cable Entertainment Legal Affairs')
        self.assertEqual('Cable Entertainment Legal Affairs' in self.mainObj.functions, True)
        self.mainObj.functions = {}

    def test_dedup_titles(self):
        f = self.mainObj.dedup_titles
        self.assertEqual(f({'COO': 1, 'Chief Operating Officer': 1, 'President': 1}), {'Chief Operating Officer': 1, 'President': 1})

    def _test_basic(self, input_file, expected_levels, expected_functions=None, expected_industries=None):
        # a should be of type dict
        def _test(a, b):
            if b:
                if isinstance(b, (list,)):
                    a = a.keys()
            else:
                b = {}
            self.assertEqual(a, b)
        self.mainObj = MainObj()
        self.mainObj.analyze(input_file)
        _test(self.mainObj.levels, expected_levels)
        _test(self.mainObj.functions, expected_functions)
        _test(self.mainObj.industries, expected_industries)

    def test_all_1(self):
        self._test_basic('fixtures/titles_1.txt',
                         {'Head of': 1, 'Senior Director': 1, 'SVP': 1},
                         {'New Ventures': 1},
                         {'Small Business Banking': 1})

    def test_all_2(self):
        self._test_basic('fixtures/titles_2.txt', {'Head of': 1},{'Franchise': 1},{'DreamWorks Classics': 1})

    def test_all_3(self):
        self._test_basic('fixtures/titles_3.txt', {'Chief Brand Officer': 1}, None, {'Google': 1})

    def test_all_4(self):
        self._test_basic('fixtures/titles_4.txt', {'Global Head of': 1, 'chief diversity officer': 1}, {'Inclusion & Diversity': 1}, None)

    def test_all_5(self):
        self._test_basic('fixtures/titles_5.txt', {'SVP': 1, 'Editor in Chief': 1}, None, {'Content Marketing & Syndication': 1})

    def test_all_6(self):
        self._test_basic('fixtures/titles_6.txt', {'Executive Vice President': 1, 'Chief Counsel': 1}, {'Cable Entertainment Legal Affairs': 1}, None)

    def test_1(self):
        self._test_basic('Chief Operating Officer (COO) & President', {'Chief Operating Officer': 1, 'President': 1}, None, None)

    def test_2(self):
        self._test_basic('Vice President of Video Product + Revenue Product & Operations at Vox Media, Inc.',
                         {'Vice President': 1},
                         {'Video Product + Revenue Product & Operations': 1},
                         {'Vox Media, Inc.': 1})

    def test_3(self):
        self._test_basic("Chief Evangelist & Vice President of Services",
                         {'Chief Evangelist': 1, 'Vice President': 1},
                         {'Services': 1},
                         None)

    def test_4(self):
        self._test_basic('Director, Blackstone Launchpad @ NYU',
                         ['Director'],
                         ['Blackstone Launchpad'],
                         ['NYU'])

    def test_5(self):
        self._test_basic('Director, Interactive Marketing - Century 21',
                         ['Director'],
                         ['Interactive Marketing'],
                         ['Century 21'])

    def test_6(self):
        self._test_basic('President - Advertiser Platforms',
                         ['President'],
                         ['Advertiser Platforms'],
                         None)

    def test_7(self):
        self._test_basic('DVP/GM, Global External Sales and Marketing - Kenmore, Craftsman, Diehard Brands',
                         ['GM','DVP'],
                         ['Global External Sales and Marketing'],
                         ['Kenmore, Craftsman, Diehard Brands'])

if __name__ == '__main__':
    unittest.main()