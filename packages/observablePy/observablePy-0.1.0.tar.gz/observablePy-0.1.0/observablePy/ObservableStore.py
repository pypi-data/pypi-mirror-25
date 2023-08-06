#!/usr/bin/python3
# -*- coding: utf-8 -*-


class ObservableStore():
    def __init__(self, observables):
        self.__observables = observables

    def getObservableElements(self):
        """
        get the list of properties that have observable decoration

        :return: list of observable properties.
        :rtype: Array
        """
        return self.__observables

    def hasObservableElements(self):
        """
        Mention if class has observable element.

        :return: true if have observable element, otherwise false.
        :rtype: bool
        """
        return self.__observables.__len__() > 0

    def isObservableElement(self, ElementNames):
        """
        Mention if an element is an observable element.

        :param str ElementNames: the element name to evaluate
        :ElementNames Type: (str | Array of strings)
        :return: true if is an observable element, otherwise false.
        :rtype: bool
        """
        def _evaluateString():
            if (ElementNames in self.__observables):
                return True
            return False

        def _evaluateArray():
            if set(ElementNames).issubset(self.__observables):
                return True
            return False

        if (ElementNames == "*"):
            return True
        else:
            if (isinstance(ElementNames, str)):
                return _evaluateString()

            elif (hasattr(ElementNames, "__len__")):
                return _evaluateArray()

            else:
                raise TypeError(
                    "Element name should be a string of an array of string." +
                    "I receive this {0}"
                    .format(ElementNames))

    def add(self, observableElement):
        if observableElement not in self.__observables:
            self.__observables.append(observableElement)
        else:
            raise RuntimeError(
                "{0} is already an observable element"
                .format(observableElement))

    def remove(self, observableElement):
        if observableElement in self.__observables:
            self.__observables.remove(observableElement)
