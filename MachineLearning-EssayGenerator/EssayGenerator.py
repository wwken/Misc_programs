#!/usr/bin/python
import random
import re
import sys
from os import listdir
from os.path import isfile, join


# Author: Ken Wu
#
# This program first reads the directory and parse and learn all articles inside and then it will random generate an essay based on what it learns
# 
# To run the program: ./EssayGenerator.py input/

PUNCT = [',', '.', ';']

class EssayGenerator:
    def __init__(self):
        self.transition = {}
        
    
    def study(self, article):
        words = re.findall(r"[\w|']+|[^\s]", article)
        self.transition['^'] = [words[0]]
        self.transition[words[-1]] = ['$']
        for i in xrange(len(words) - 1):
            if words[i] not in self.transition:
                self.transition[words[i]] = []
            self.transition[words[i]].append(words[i + 1])

    def generate(self):
        result = ""
        word = "^"
        while True:
            word = self.transition[word][random.randint(0, len(self.transition[word]) - 1)]
            if word is '$':
                break
            result += word in PUNCT and word or " " + word
        return result


aG = EssayGenerator()
inputPath = sys.argv[1]
onlyfiles = [ f for f in listdir(inputPath) if isfile(join(inputPath,f)) ]
for f in onlyfiles:
	f = join(inputPath,f)
	#print f
	with open(f, 'r') as f:
		aG.study(f.read())

print aG.generate()


