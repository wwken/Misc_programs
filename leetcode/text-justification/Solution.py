class Solution(object):
    def createSpaces(self, n):
        r = ""
        for x in range(int(n)):
            r += " "
        return r

    def addToOutput(self, newLine, maxWidth, output, isLastLine=False):
        newLine = newLine.strip()
        if isLastLine:
            needspaces = maxWidth - len(newLine)
            output.append(newLine + self.createSpaces(needspaces))
            return

        words=newLine.split(" ")
        actualWordsLength=0
        for w in words:
            actualWordsLength += len(w)
        extraWordsLength = maxWidth - actualWordsLength
        # print "newLine: {}, maxWidth: {}, extraWordsLength: {}".format(newLine, maxWidth, extraWordsLength)
        if extraWordsLength > 0:
            modRemain = 0
            div = maxWidth - len(newLine)
            if len(words) > 1:
                modRemain = extraWordsLength % (len(words)-1)
                div = extraWordsLength / (len(words)-1)
            current=0
            nLine=""
            # print "modRemain: {}, div: {}, len(words): {}".format(modRemain, div, len(words))
            while(current < len(words)):
                thisNeededSpace = div
                if modRemain > 0:
                    thisNeededSpace += 1
                    modRemain -= 1
                nLine += words[current] + self.createSpaces(thisNeededSpace)
                current += 1
            if len(nLine) > maxWidth:
                nLine = nLine.rstrip()
            output.append(nLine)
        else:
            output.append(newLine)

    def fullJustify(self, words, maxWidth):
        """
        :type words: List[str]
        :type maxWidth: int
        :rtype: List[str]
        """
        current=0
        thisLineLength=0
        output = []
        thisNewLine = ""
        while(current<len(words)):
            thisLineLength = thisLineLength + len(words[current]) + 1
            if thisLineLength > maxWidth + 1:   # too much
                self.addToOutput(thisNewLine, maxWidth, output)
                thisNewLine = words[current] + " "
                thisLineLength = len(thisNewLine)
            else:
                thisNewLine = thisNewLine + words[current] + " "
            current = current + 1
        self.addToOutput(thisNewLine, maxWidth, output, True)
        return output
