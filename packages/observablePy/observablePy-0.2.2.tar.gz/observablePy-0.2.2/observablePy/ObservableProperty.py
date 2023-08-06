#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Decorator to set observable to a property.

It override the python property decorator to specified
    the setter and deleter behaviour, so it can diffuse to observer
    any change.

    warning: If the property does not have a setter or deleter function
    no change will be diffused.

=================
How to use it
=================

.. code-block:: python
from Observable import Observable, observable_property
class Battery(Observable):
def __init__(self):
    super().__init__()
    self.__voltage = 0

@observable_property
def voltage(self):
    return self.__voltage

@voltage.setter
def voltage(self, value):
    self.__voltage = value

@voltage.deleter
def voltage(self):
    self.__voltage = 0

"""


class observable_property(property):
    def __init__(self, *args, **kwargs):
        super(observable_property, self).__init__(*args, **kwargs)
        self.name = args[0].__name__  # The property get function

    def __set__(self, obj, value):
        """
        Override the computed value of the property to
        diffuse the change to observer.

        :param obj: The instance that owns the property.
        :param value: The new value for the property.
        """
        previousValue = getattr(obj, self.name)
        super(observable_property, self).__set__(obj, value)
        obj.diffuse(self.name, previousValue, value)

    def __delete__(self, obj):
        """
        Override the deletion of the property to
        diffuse the change to observer.

        :param obj: The instance that owns the property.
        """
        previousValue = getattr(obj, self.name)
        super(observable_property, self).__delete__(obj)
        obj.diffuse(self.name, previousValue, None)
