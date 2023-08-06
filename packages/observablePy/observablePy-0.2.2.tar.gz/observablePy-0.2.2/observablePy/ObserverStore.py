#!/usr/bin/python3
# -*- coding: utf-8 -*-
from .ObserverTypeEnum import observerTypeEnum


class ObserverStore():
    def __init__(self):
        self._observers = []

    def add(self, what, call):

        def isCallableFunction(function):
            return hasattr(function, "__call__")

        if not isCallableFunction(call):
                raise TypeError(
                    '"call" parameter must be a callable function.')

        type = observerTypeEnum.typeOf(what)
        if type is observerTypeEnum.unknown:
            raise TypeError(
                    "'what' parameter should be a str or " +
                    " an array of strings. Received '{0}'".format(what))

        self._observers.append(
                                {"observing": what,
                                 "type": type,
                                 "call": call
                                 })

    def remove(self, what, call):
        """
        remove an observer

        what: (string | array) state fields to observe
        call: (function) when not given, decorator usage is assumed.
            The call function should have 2 parameters:
            - previousValue,
            - actualValue

        """
        type = observerTypeEnum.typeOf(what)
        self._observers.remove({
                                    "observing": what,
                                    "type": type,
                                    "call": call
                                 })

    def removeAll(self):
        """
        remove all observers
        """
        del self._observers[:]

    def getObservers(self):
        """
        Get the list of observer to the instance of the class.

        :return: Subscribed Obversers.
        :rtype: Array
        """
        result = []
        for observer in self._observers:
            result.append(
                          {
                              "observing": observer["observing"],
                              "call": observer["call"]
                          })
        return result

    def hasObservers(self):
        """
        Mention if the observable class has observer.

        :return: true if it has observer, otherwise false.
        :rtype: bool
        """
        return self._observers.__len__() > 0

    def iterationGenerator(self, filter=None):
        if filter is None:
            obsersers = self._observers
        else:
            obsersers = self._filter(filter)

        for observer in obsersers:
            yield observer  # , type

    def _filter(self, filter):
        return ([o for o in self._observers if (
                "*" == o["observing"] or filter in o["observing"])])
