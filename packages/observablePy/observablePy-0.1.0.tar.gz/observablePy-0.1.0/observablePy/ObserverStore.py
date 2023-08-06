#!/usr/bin/python3
# -*- coding: utf-8 -*-


class ObserverStore():
    def __init__(self):
        self.__observers = []

    def add(self, what, call):

        def isCallableFunction(function):
            return hasattr(function, "__call__")

        if not isCallableFunction(call):
                raise TypeError(
                    '"call" parameter must be a callable function.')

        self.__observers.append({"observing": what, "call": call})

    def remove(self, what, call):
        """
        remove an observer

        what: (string | array) state fields to observe
        call: (function) when not given, decorator usage is assumed.
            The call function should have 2 parameters:
            - previousValue,
            - actualValue

        """
        self.__observers.remove({"observing": what, "call": call})

    def removeAll(self):
        """
        remove all observers
        """
        del self.__observers[:]

    def getObservers(self):
        """
        Get the list of observer to the instance of the class.

        :return: Subscribed Obversers.
        :rtype: Array
        """
        return self.__observers

    def hasObservers(self):
        """
        Mention if the observable class has observer. 

        :return: true if it has observer, otherwise false.
        :rtype: bool
        """
        return self.__observers.__len__() > 0

    def Type(self):
        raise NotImplementedError

    def __iter__(self, filter=None):
        if filter is None:
            return iter(self.__observers)
        else:
            return iter(
                [o for o in self.__observers if (
                    "*" == o["observing"] or filter in o["observing"])])
