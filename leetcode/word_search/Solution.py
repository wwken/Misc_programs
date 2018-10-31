class Solution(object):
    def isValidPos(self, board, x, y, letter, history_board):
        if x < 0 or x >= len(board[0]) or y < 0 or y >= len(board):
            return False
        else:
            if history_board[y][x]:
                return False
            if board[y][x] == letter:
                return True
            else:
                return False

    def _exist(self, board, word, history_board, curX, curY, i):
        this_letter = word[i]
        if this_letter != board[curY][curX]:
            return False
        else:
            if i >= len(word) - 1:  # Last character to valid, we are done
                return True
            else:
                # this letter is equal to to this curY curX in the board
                history_board[curY][curX] = True

                #Now look for the next valid move:
                nextLetterToLookFor = word[i+1]
                ans = False
                if self.isValidPos(board, curX+1, curY, nextLetterToLookFor, history_board):
                    ans = self._exist(board, word, history_board[:], curX+1, curY, i+1)
                    if ans:
                        return True
                if self.isValidPos(board, curX, curY+1, nextLetterToLookFor, history_board):
                    ans = self._exist(board, word, history_board[:], curX, curY+1, i+1)
                    if ans:
                        return True
                if self.isValidPos(board, curX-1, curY, nextLetterToLookFor, history_board):
                    ans = self._exist(board, word, history_board[:], curX-1, curY, i+1)
                    if ans:
                        return True
                if self.isValidPos(board, curX, curY-1, nextLetterToLookFor, history_board):
                    ans = self._exist(board, word, history_board[:], curX, curY-1, i+1)
                    if ans:
                        return True
                return False



    def exist(self, board, word):
        """
        :type board: List[List[str]]
        :type word: str
        :rtype: bool
        """
        history_board = []
        for y in range(len(board)):
            b = []
            for x in range(len(board[0])):
                b.append(False)
            history_board.append(b)

        for y in range(len(board)):
            for x in range(len(board[0])):
                ans = self._exist(board, word, history_board, x, y, 0)
                if ans:
                    return True

        return False

