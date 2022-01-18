

class Vertex:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.threats = 0

    def __eq__(self, other):
        return other.row == self.row and other.col == self.col

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return f"({self.row},{self.col})"

    def __repr__(self):
        return self.__str__()