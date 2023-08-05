import math

class Operations:
    def __init__(self):
        self.name = "Basic Calculator Example"

<<<<<<< HEAD
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
=======
    def add(self, x, y):
        pass

    def divide(self, x: int, y: int)->float:
        """
        Esta función se encarga de dividir dos números enteros, siendo el resultado un float
        :param x: int. Numerador
        :param y: int. Denominador
        :return: float. División entre numerador y denominador
        """
        return x/y

    def multiply(self, x, y):
>>>>>>> Divide
        pass

    def log_e(self, x):
        pass
<<<<<<< HEAD

    def exponencial(self, x, y):
        pass
=======
        return x * y
<<<<<<< HEAD

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
=======
>>>>>>> Divide
=======
    def exponential(self,x):
        """
        Operacion exponencial
        :param x:
        :return:
        """
        return math.exp(x)
>>>>>>> operation_exponential
