#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .Diffusible import Diffusible
from .ObservableProperty import observable_property
from .ObservableStore import ObservableStore
from .ObserverStore import ObserverStore

"""
Implement the observable behaviour to a class.

Observable property:
The property of an observable class that have the
@observable_property decorator is an observable property.

refer to ObservableProperty to set a property observable

Observer:
An Observer is a function that will be called, when the specified
observable element change.

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
    self.__voltage = None

"""


class Observable(Diffusible):
    def __init__(self):
        super(Observable, self).__init__()
        self.__observers = ObserverStore()
        # build the list of observable element.
        self.__observables = ObservableStore(self.__getTaggedProperties())

    @classmethod
    def __getTaggedProperties(cls):
        return [p for p in dir(cls) if isinstance(
                    getattr(cls, p), observable_property)]

    def getObservableElements(self):
        """
        get the list of properties that have observable decoration

        :return: list of observable properties.
        :rtype: Array
        """
        return self.__observables.getObservableElements()

    def hasObservableElements(self):
        """
        Mention if class has observable element.

        :return: true if have observable element, otherwise false.
        :rtype: bool
        """
        return self.__observables.hasObservableElements()

    def isObservableElement(self, ElementNames):
        """
        Mention if an element is an observable element.

        :param ElementNames: the element name to evaluate
        :ElementNames Type: (str | Array of strings)
        :return: true if is an observable element, otherwise false.
        :rtype: bool
        """
        return self.__observables.isObservableElement(
            ElementNames)

    def addObservableElement(self, elementName):
        """
        Add an observale element.

        :param str elementName: the element name to add
        :raises RuntimeError: if elementName already exist
        """
        self.__observables.add(elementName)

    def removeObservableElement(self, elementName):
        """
        Remove an observale element.

        :param str elementName: the element name to remove
        """
        self.__observables.remove(elementName)

    def getObservers(self):
        """
        Get the list of observer to the instance of the class.

        :return: Subscribed Obversers.
        :rtype: Array
        """
        return self.__observers.getObservers()

    def getObserversIter(self, filter=None):
        return self.__observers.__iter__(filter)

    def hasObservers(self):
        """
        Mention if the observable class has observer. 

        :return: true if it has observer, otherwise false.
        :rtype: bool
        """
        return self.__observers.hasObservers()

    # def isObserved(cls, fieldName):
    #     return true when exist other false

    def observeState(self, call=None):
        """
        Registers an observer to the any changes.
            The called function should have 2 parameters:
            - previousState,
            - actualState

        :param func call: The function to call.
                          When not given, decorator usage is assumed.
        :return: the function to call once state change.
        :rtype: func
        :raises TypeError: if the called function is not callable

        =================
        How to use it
        =================
        -----------------
        1. Calling the function
        -----------------
            .. code-block:: python
                instance.observeState(functionName)
                instance.observeState(functionName)

                ...
                def functionName(previousState, actualState):

        -----------------
        2. Using Decoration
        -----------------
            .. code-block:: python
                @instance.observeState()
                def functionName(previousState, actualState):

                @instance.observeState()
                def functionName(previousState, actualState):
        """
        def _observe(call):
            self.__observers.add("*", call)
            return call

        if call is not None:
            return _observe(call)
        else:
            return _observe

    def observeElement(self, what, call=None):
        """
        Alias of observeElements method
        """
        return self.observeElements(what, call)

    def observeElements(self, what, call=None):
        """
        Registers an observer function to a specific state field or
            list of state fields.
            The function to call should have 2 parameters:
            - previousValue,
            -actualValue

        :param what: name of the state field or names of the
                     state field to observe.
        :type what: str | array
        :param func call: The function to call. When not given, 
                          decorator usage is assumed.
        :return: the function to call once state change.
        :rtype: func
        :raises TypeError: if the called function is not callable

        =================
        How to use it
        =================
        -----------------
        1. Calling the function
        -----------------
        .. code-block:: python
            instance.observeFields("FieldName", functionName)
            instance.observeFields(["FieldName1","FieldName2"], functionName)

            ...
            def functionName(previousState, actualState):

        -----------------
        2. Using Decoration
        -----------------
        .. code-block:: python
            @instance.observeFields("FieldName")
            def functionName(previousValue, actualValue):

            @instance.observeFields(["FieldName1","FieldName2"])
            def functionName(previousValue, actualValue): 
        """
        def _observe(call):
            self.__observers.add(what, call)
            return call

        if not self.isObservableElement(what):
            msg = 'Could not find observable element named "{0}" in {1}'
            raise ValueError(msg.format(what, self.__class__))

        if call is not None:
            return _observe(call)
        else:
            return _observe

    def unObserve(self, what, call):
        """
        unregisters an observer

        what: (string | array) state fields to observe
        call: (function) when not given, decorator usage is assumed.
            The call function should have 2 parameters:
            - previousValue,
            - actualValue

        """
        self.__observers.remove(what, call)
