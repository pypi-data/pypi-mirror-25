# -*- coding: utf-8 -*-

"""Main module."""
import math


class Vector:
    def __init__(self, identifier, value):
        self.id = identifier
        self.value = value

    def magnitude(self):
        """This method calculates the magnitude of the vector

        Returns:
            float: The magnitude of the vector object

        """
        if len(self.value) > 0:
            sum_of_squares = sum([value * value for value in self.value.values()])

            return math.sqrt(sum_of_squares)
        else:
            raise ValueError('Calculation error.  Primary vector is empty.')

    def dot_product(self, second_vector):
        """This method returns the dot product of the vector with the supplied comparision vector.

        Args:
            second_vector: (object) A Vector object.

        Returns:
            int: The dot product.

        """

        if len(second_vector.value) <= 0 or len(self.value) <= 0:
            raise ValueError('Calculation error.  One of the vectors is empty.')

        stuff = [value * second_vector.value[key] for key, value in self.value.items() if
                 key in second_vector.value and second_vector.value[key] > 0]
        dot_prod = sum(stuff)
        return dot_prod

    def cosine_of_angle(self, second_vector):
        """This method calculates the cosine of the angle between this instances method and a second vector.

        This is also the 'cosine similarity'.

        Args:
            second_vector: (object) A vector object.

        Returns:
            float: the cosine of the angle between the two vectors.

        """
        return self.dot_product(second_vector) / (self.magnitude() * second_vector.magnitude())

    def __eq__(self, other):
        """Magic method to handle comparing Vector objects.

        Args:
            other: (object) Object to be compared against.

        Returns:
            bool: True or false depending on whether the object id and the value list are identical.

        """
        return self.id == other.id and self.value == other.value
