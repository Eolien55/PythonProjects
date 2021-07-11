class SpecialForm:
    def __init__(self, sub):
        self.sub = sub

    def __getitem__(self, parameters, *args, **kwargs):
        self.sub.parameters = parameters
        self.sub.__getitem__ = self.sub.__getitem__
        return self.sub
