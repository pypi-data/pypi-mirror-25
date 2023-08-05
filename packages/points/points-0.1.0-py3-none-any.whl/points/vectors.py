"""Contains the Vector class."""

from math import sqrt, acos, degrees
from .checks import are_numeric, is_numeric
from .geometry import degree_angle

class Vector:
    """A vector is a sequence of numbers. They can represent a point in space,
    or the attributes of an object.

    Vectors can be added and subtracted with ``+`` and ``-``, but ``*`` is
    reserved for scalar multiplication - you can use it to multiply the vector
    by a number but not by another vector (there are special methods for this).

    :param values: The numbers that make up the Vector. If a single sequence is\
    given, that sequence will be unpacked to make the vector.
    :raises TypeError: if the values given are not numeric."""

    def __init__(self, *values):
        values_ = values
        if len(values) == 1:
            try:
                values_ = list(values[0])
            except TypeError: pass
        if not are_numeric(*values_):
            raise TypeError("{} contains non-numeric values".format(values_))
        self._values = list(values_)


    def __repr__(self):
        return "<Vector {}>".format(self._values)


    def __contains__(self, item):
        return item in self._values


    def __getitem__(self, index):
        return self._values[index]


    def __len__(self):
        return len(self._values)


    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Cannot add {} - not a Vector".format(other))
        if self.length() != other.length():
            raise ValueError("Cannot add {} - unequal length".format(other))
        return Vector(v1 + v2 for v1, v2 in zip(self._values, other._values))


    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Cannot add {} - not a Vector".format(other))
        if self.length() != other.length():
            raise ValueError("Cannot add {} - unequal length".format(other))
        return Vector(v1 - v2 for v1, v2 in zip(self._values, other._values))


    def __mul__(self, other):
        if isinstance(other, Vector):
            raise TypeError("'*' is reserved for scalar multiplication")
        else:
            return Vector([v * other for v in self._values])


    def __rmul__(self, other):
        return self * other


    def length(self):
        """Returns the length of the Vector. This is the number of values it
        contains, not its :py:meth:`magnitude`.

        :rtype: ``int``"""

        return len(self)


    def values(self):
        """Returns the values in the Vector.

        :rtype: ``tuple``"""

        return tuple(self._values)


    def add(self, value):
        """Adds a value to the end of the Vector.

        :param value: the value to add.
        :raises TypeError: if the value is non-numeric."""

        if not is_numeric(value):
            raise TypeError("{} is not numeric".format(value))
        self._values.append(value)


    def insert(self, index, value):
        """Insertes a value into the Vector.

        :param int index: The location to insert to.
        :param value: the value to add.
        :raises TypeError: if the value is non-numeric."""

        if not is_numeric(value):
            raise TypeError("{} is not numeric".format(value))
        self._values.insert(index, value)


    def remove(self, value):
        """Removes a value from the Vector.

        :param value: the value to remove."""

        self._values.remove(value)


    def pop(self, index=-1):
        """Removes a value from the Vector and returns it.

        :param index: the index to remove, default being ``-1``.
        :returns: the removed value."""

        return self._values.pop(index)


    def magnitude(self):
        """Returns the magnitude of the Vector - the length of the line it
        represents.

        :rtype: ``float``"""

        return sqrt(sum([x**2 for x in self._values]))


    def dot(self, other):
        """Returns the dot product between this vector and another.

        :param Vector other: The other Vector.
        :raises TypeError: If a non-Vector is given.
        :rtype: ``float``"""

        if not isinstance(other, Vector):
            raise TypeError("{} is not a Vector".format(other))
        if self.length() != other.length():
            raise ValueError("{} and {} not equal length".format(self, other))
        return sum([u_i * v_i for u_i, v_i in zip(self._values, other._values)])


    @degree_angle
    def angle_with(self, other):
        """Returns the angle between this vector and another, in radians.

        :param Vector other: The other Vector.
        :param bool degrees: If ``True`` the angle will be returned in degrees.
        :raises TypeError: If a non-Vector is given.
        :rtype: ``float``"""

        if not isinstance(other, Vector):
            raise TypeError("{} is not a Vector".format(other))
        if self.length() != other.length():
            raise ValueError("{} and {} not equal length".format(self, other))
        return acos(self.dot(other) / (self.magnitude() * other.magnitude()))
