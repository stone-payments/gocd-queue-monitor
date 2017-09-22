class Resource:

    def __init__(self, name):
        self.name = name

    def __str__(self):       
        return self.name

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.name == other.name
