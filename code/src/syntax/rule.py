class Rule:
    def __init__(self, ruleSymbols, pred):
        if isinstance(ruleSymbols, str):
            self.ruleSymbols = ruleSymbols.split()
        else:
            self.ruleSymbols = ruleSymbols
        self.pred = pred

    def __repr__(self):
        return f"<{' '.join(self.ruleSymbols)} : {self.pred}>"
