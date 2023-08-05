
class Operations:
    def __init__(self):
        self.name = "Basic Calculator Example"

    def add(self, x, y):
        return x + y

    def divide(self, x, y):
        return x/y

    def multiply(self, x, y):
        return x * y

    def exp(self, x: float, y: float) -> float:
        """
        Calculates the exponential of the base "x" given its exponent as "y"
        :param x: base
        :param y: exponent
        :return:
        """
        if y == 0:
            return 1;
        else:
            return x * self.exp(x, y - 1)

