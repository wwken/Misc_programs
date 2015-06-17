#!/usr/bin/python

#/*
# 
# Print all permutatiations of a string S.
# 
# For example:
#
# S = "a"
#
# a
# 
# S = "ab"
# 
# ab
# ba
# 
# S = "abc"
# 
# abc
# 
# acb
# 
# bac
# 
# bca
# 
# cab
# 
# cba
# 
# */


def perm(str):
    return perm2(str, 0, [])
    
def perm2(str, i, l):
    if i == len(str):
        return l
    else:
        a = str[i:i+1] 
        l = insertAtEverywhere(a, l)
        return perm2(str, i+1, l)

def insertAtEverywhere(letter, l):
    new_l = []
    if not l:
        return [letter]
    
    for item in l:  #for each words in the list
        for x in range(0, len(item)+1):  
            s = item[0:x] + letter + item[x:]
            new_l.append(s)
    return new_l


#print perm('a')
str='abcd'
print 'The permutations of the string - '+str+' is:'
print perm('abcd')
