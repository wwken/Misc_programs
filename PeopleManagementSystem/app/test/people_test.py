# Copyright (c) 2016 Ken Wu
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# -----------------------------------------------------------------------------
#
# Author: Ken Wu

import unittest
from app.main.people import PeopleRepo


class PeopleTest(unittest.TestCase):

    def setUp(self):
        self.p = PeopleRepo()
        self.p.read_from_file('app/resources/people.csv')
        print("now at setup")

    def test_find_by_id_01(self):
        o = self.p.find_by_id(1)
        self.assertEquals(o[PeopleRepo.FIRST_NAMAE_COLUMN], 'John')

        o = self.p.find_by_id(4)
        self.assertEquals(o[PeopleRepo.EMAIL_COLUMN], 'janedoe@wwken.com')

        o = self.p.find_by_id(99)   #non exist entry
        self.assertEquals(o, None)

    def test_find_by_first_name_02(self):
        o = self.p.find_by_first_name('John')
        self.assertEquals(len(o), 2)
        self.assertEquals(o[0][PeopleRepo.LAST_NAMAE_COLUMN], 'Smith')

        o = self.p.find_by_first_name('Jane')
        self.assertEquals(len(o), 1)
        self.assertEquals(o[0][PeopleRepo.AGE_COLUMN], 40)

    def test_find_by_email_03(self):
        o = self.p.find_by_email('JSmith@wwken.com')
        self.assertEquals(o[0][PeopleRepo.LAST_NAMAE_COLUMN], 'Smith')

        o = self.p.find_by_email('jsmith@wwken.com')       #lower case of email should be able to find too
        self.assertEquals(o[0][PeopleRepo.LAST_NAMAE_COLUMN], 'Smith')

        o = self.p.find_by_email('dummy@wwken.com')       #lower case of email should be able to find too
        self.assertEquals(o, None)

    def test_find_by_name_prefix_04(self):
        o = self.p.find_by_name_prefix('j')
        print(o)
        self.assertEquals(len(o), 4)    #it should have everyone

        o = self.p.find_by_name_prefix('jo')
        print(o)
        self.assertEquals(len(o), 3)    #it should have only 3 people

        o = self.p.find_by_name_prefix('joh')
        print(o)
        self.assertEquals(len(o), 2)    #it should have only 2 people   - John Smith and John Jones

        o = self.p.find_by_name_prefix('ja')
        print(o)
        self.assertEquals(len(o), 1)    #it should have only 1 people   - Jane Doe

        o = self.p.find_by_name_prefix('d')
        print(o)
        self.assertEquals(len(o), 1)    #it should have only 1 people   - Jane Doe

    def test_find_where_age_between_05(self):
        o = self.p.find_where_age_between(29, 35)
        self.assertEquals(len(o), 2)    #it should have two people
        self.assertEquals(o[0][PeopleRepo.AGE_COLUMN], 29)
        self.assertEquals(o[1][PeopleRepo.AGE_COLUMN], 30)

        o = self.p.find_where_age_between(45, 50)
        self.assertEquals(o[0][PeopleRepo.AGE_COLUMN], 45)

        o = self.p.find_where_age_between(50, 45)
        self.assertEquals(o[0][PeopleRepo.AGE_COLUMN], 45)

        o = self.p.find_where_age_between(60, 75)
        self.assertEquals(o, None)

    def test_insert_07(self):
        self.p.insert(6, 'Ken', 'Wu', 'Ken@wwken.com', 25)
        s = self.p.get_size()
        self.assertEquals(s, 5)

    def test_delete_08(self):
        id_to_be_removed = 1
        self.p.delete(id_to_be_removed)
        o = self.p.find_by_id(id_to_be_removed)
        self.assertEquals(o, None)

        o = self.p.find_by_first_name('John')   #should only one left
        self.assertEquals(len(o), 1)
        o = self.p.find_where_age_between(29, 35)
        self.assertEquals(len(o), 1)            #should only one left