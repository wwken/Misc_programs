class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        carry = 0
        allNodes = []
        while True:
            sum = l1.val + l2.val + carry
            if sum > 9:
                sum = sum - 10
                carry = 1
            else:
                carry = 0
            p = ListNode(sum)
            allNodes.append(p)
            if l1.next != None and l2.next != None:
                l1 = l1.next
                l2 = l2.next
            else:
                if l1.next != None:
                    l1 = l1.next
                    l2 = ListNode(0)
                elif l2.next != None:
                    l2 = l2.next
                    l1 = ListNode(0)
                else:
                    if carry > 0:
                        l1 = ListNode(0)
                        l2 = ListNode(0)
                    else:
                        break
        for x in range(0, len(allNodes) - 1):
            allNodes[x].next = allNodes[x+1]

        return allNodes[0]