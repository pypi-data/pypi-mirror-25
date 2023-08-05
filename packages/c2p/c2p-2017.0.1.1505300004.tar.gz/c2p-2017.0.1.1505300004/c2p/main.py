
class Operations:
    def __init__(self):
        self.name = "Basic Calculator Example"

    def add(self, x: int, y: int)-> int:
        """
        Esta funcion se encargar de sumar dos valores enteros.
        :param x: int. Primer valor de entrada entero
        :param y: int. Segundo valor de entrada entero.
        :return: int. Devuelve la operacion suma x + y
        """
        return  x + y

    def divide(self, x, y):
        pass

    def multiply(self, x, y):
<<<<<<< HEAD
        pass

    def log_e(self, x):
        pass

    def exponencial(self, x, y):
        pass
=======
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

>>>>>>> exponential
