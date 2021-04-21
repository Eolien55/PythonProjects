class Graph:
    def __init__(self, name, **kwargs):
        self.name = name
        self.points = {eval(i): kwargs[i] for i in kwargs}
        for i in kwargs:
            eval(i)._add({self: kwargs[i]})

    def add(self, point=None, **kwargs):
        if not point:
            point = {eval(i): kwargs[i] for i in kwargs}
        self.points.update(
            {list(point.keys())[i]: list(point.values())[i] for i in range(len(point))}
        )
        for i in point:
            i._add({self: point[i]})

    def _add(self, point):
        self.points.update({i: point[i] for i in point})

    def __repr__(self):
        return self.name
