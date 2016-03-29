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

class PeopleRepo:

    idToDataDict = {}
    firstNameToDataDict = {}
    prefixToDataDict = {}
    emailToDataDict = {}
    ageToDataDict = {}

    ID_COLUMN = 0
    FIRST_NAMAE_COLUMN = 1
    LAST_NAMAE_COLUMN = 2
    EMAIL_COLUMN = 3
    AGE_COLUMN = 4

    def __init__(self):
        pass

    def _populate_dict(self, k, v, d):
        if not k in d:
            d[k] = set()
        d[k].add(v)

    def _populate_prefix_dict(self, name, id):
        name = name.lower() #convert the name to lower
        for x in range(0, len(name)+1):
            prefix_name = name[:x]
            self._populate_dict(prefix_name, id, self.prefixToDataDict)

    def _insert_record(self, d):
        id = d[self.ID_COLUMN]
        first_name = d[self.FIRST_NAMAE_COLUMN]
        last_name = d[self.LAST_NAMAE_COLUMN]
        email = d[self.EMAIL_COLUMN]
        age = d[self.AGE_COLUMN]

        self.idToDataDict[id] = d

        self._populate_dict(first_name, id, self.firstNameToDataDict)

        #build the first name prefixs into the dictionary
        self._populate_prefix_dict(first_name, id)

        #build the last name prefixs into the dictionary
        self._populate_prefix_dict(last_name, id)

        self.emailToDataDict[email] = {id}

        self._populate_dict(age, id, self.ageToDataDict)

    def read_from_file(self, file_name):
        with open(file_name) as f:
            lines = f.readlines()
            for line in lines:
                arr = line.split(',')
                id = int(arr[0])
                first_name = arr[1]
                last_name = arr[2]
                email = arr[3].lower()
                age = int(arr[4].replace('\n', ''))
                d = [id, first_name, last_name, email, age]
                #print(d)
                self._insert_record(d)

    def find_by_id(self, id):
        if id in self.idToDataDict:
            return self.idToDataDict[id]
        else:
            return None

    def _retrieve_from_dict(self, k, d):
        r = []
        if k in d:
            ids_to_be_removed = set()
            for id in d[k]:
                p_r = self.find_by_id(id)
                if p_r:
                    r.append(p_r)
                else:
                    #Most likely this id was removed already. so now remove it from the data structure
                    ids_to_be_removed.add(id)
            if(len(ids_to_be_removed)>0):
                for id in ids_to_be_removed:
                    d[k].remove(id)
        if len(r) == 0:
            r = None
        return r

    def find_by_first_name(self, first_name):
        return self._retrieve_from_dict(first_name, self.firstNameToDataDict)

    def find_by_name_prefix(self, prefix):
        prefix = prefix.lower()
        return self._retrieve_from_dict(prefix, self.prefixToDataDict)

    def find_by_email(self, email):
        email = email.lower()
        return self._retrieve_from_dict(email, self.emailToDataDict)

    def find_where_age_between(self, min_age, max_age):
        if min_age > max_age:
            t = max_age
            max_age = min_age
            min_age = t
        r = []
        for x in range(min_age, max_age+1):
            rr = self._retrieve_from_dict(x, self.ageToDataDict)
            if rr:
                for e in rr:
                    r.append(e)
        if len(r) == 0:
            r = None
        return r

    def insert(self, id, first_name, last_name, email, age):
        id = int(id)
        age = int(age)
        d = [id, first_name, last_name, email, age]
        self._insert_record(d)

    def get_size(self):
        return len(self.idToDataDict)

    #This is doing the lazy delete.  For all other data structures, we will remove the id on demand when being retrieved
    def delete(self, id):
        if id in self.idToDataDict:
            self.idToDataDict.pop(id, None)
            return True
        else:
            return False

    def edit_by_email(self, id, email):
        #To do
        pass
