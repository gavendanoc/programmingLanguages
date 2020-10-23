
class NoTerminal:
    def __init__(self, symbol, firsts=[], next=[], rules=[]):
        self.symbol = symbol
        self.firsts = firsts
        self.next = next
        self.rules = rules

    def addNext(self, n):
        if type(n) != list:
            n = [n]
        self.next += n
        temp = set(self.next)
        self.next = sorted(list(temp))

    def addFirst(self, first):
        if type(first) != list:
            first = [first]
        self.firsts += first
        temp = set(self.firsts)
        self.firsts = sorted(list(temp))

    def __repr__(self):
        return f" \n  Firsts: {self.firsts} \n  Next:   {self.next} \n  Rules:  {self.rules}"
