import math
from sys import float_info

class Vector:
    def __init__(self, x: float | int, y: float | int) -> None:
        self.x = x
        self.y = y

    @staticmethod
    def getforward(angle: float):
        return Vector(
            math.cos(angle),
            -math.sin(angle)
        )
    
    def distance(self):
        return math.hypot(self.x, self.y)
    
    def squared_distance(self) -> float:
        """
        Compute the squared distance of this vector.
        Very usefull for comparisons
        """
        return self.x*self.x + self.y*self.y

    def normalized(self):
        """Get Vector unit for the current vector"""
        mydistance = self.distance()
        return self/mydistance

    def dot(self, other) -> float:
        """Dot Product"""
        return self.x * other.x + self.y * other.y

    def get_angle_between(self, other):
        """
        Get angle between two vector.
        """
        return math.acos(self.dot(other))

    def get_angle(self):
        """
        Specially for forward vector
        """
        return math.atan2(-self.y, self.x)
    
    def __str__(self): return f'({self.x}, {self.y})'
    
    def __mul__(self, other):
        if isinstance(other, (int, float)): return Vector(self.x * other, self.y * other)
        return Vector(self.x * other.x, self.y * other.y)
    
    def __rmul__(self, scalar: float | int):
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar: float | int):
        if scalar == 0: scalar = float_info.epsilon # To avoid zero division error
        return Vector(self.x/scalar, self.y/scalar)
    
    def __rtruediv__(self, scalar):
        return self.__truediv__(scalar)

    def __add__(self, other):
        if isinstance(other, (int, float)): return Vector(self.x + other, self.y + other)
        return Vector(self.x+other.x, self.y + other.y)
    
    def __sub__(self, other): return Vector(self.x - other.x, self.y - other.y)

    # Comparisons
    def __eq__(self, other): return self.squared_distance() == other.squared_distance()
    def __ne__(self, other): return self.squared_distance() != other.squared_distance()

    def __gt__(self, other): return self.squared_distance() > other.squared_distance()
    def __ge__(self, other): return self.squared_distance() >= other.squared_distance()

    def __lt__(self, other): return self.squared_distance() < other.squared_distance()
    def __le__(self, other): return self.squared_distance() <= other.squared_distance()

todegree = lambda rad: rad * 180/math.pi
toradian = lambda deg: deg * math.pi / 180
