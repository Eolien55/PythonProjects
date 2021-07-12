class SpecialForm:
    def __init__(self, sub):
        self.sub = sub

    def __getitem__(self, params):
        self.sub.params = params
        return self.sub
