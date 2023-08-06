#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
from .ObserverStore import ObserverStore
from .ObserverTypeEnum import observerTypeEnum
from .DiffusingModeEnum import diffusingModeEnum


class Diffusible(object):
    __diffuseActionsMatrix = {
        diffusingModeEnum.element: {
            observerTypeEnum.element: "_diffuseElement",
            observerTypeEnum.listOfElements: "_diffuseElementsOrState",
            observerTypeEnum.state: "_diffuseElementsOrState",
        },
        diffusingModeEnum.elements: {
            observerTypeEnum.element: "_diffuseElementIn",
            observerTypeEnum.listOfElements: "_diffuseElementsIn",
            observerTypeEnum.state: "_diffuseStateIn",
        }
    }

    def __init__(self):
        self.__observers = {}

    def getObservableElements(self):
        raise NotImplementedError(
            'subclasses must override getObservableElements()!')

    def getObserversIterationGenerator(self, filter=None):
        raise NotImplementedError(
            'subclasses must override __getObserversIter()!')

    def diffuse(self, *args):
        """
        this is a dispatcher of diffuse implementation.
        Depending of the arguments used.
        """

        mode = diffusingModeEnum.unknown
        if (isinstance(args[0], str) and (len(args) == 3)):
            # reveived diffuse(str, any, any)
            mode = diffusingModeEnum.element

        elif (hasattr(args[0], "__len__") and (len(args) == 2)):
            # reveived diffuse(dict({str: any}), dict({str: any}))
            mode = diffusingModeEnum.elements

        else:
            raise TypeError(
                "Called diffuse method using bad argments, receive this" +
                " '{0}', but expected 'str, any, any' or" +
                " 'dict(str: any), dict(str: any)'."
                .format(args))

        self._diffuse(mode, *args)

    def _diffuse(self, mode, *args):
        # Iteration using the diffusing element name.
        #  When None, use all observers
        diffusing = None
        if mode == diffusingModeEnum.element:
            diffusing = args[0]

        observers = self.getObserversIterationGenerator(diffusing)
        for observer in observers:
            type = observer['type']
            actionName = Diffusible.__diffuseActionsMatrix[mode][type]
            action = getattr(self, actionName)

            action(observer, *args)

    def _diffuseElement(self, observer, *args):
        call = observer['call']
        diffusing = args[0]
        previousValue = args[1]
        value = args[2]

        call(previousValue, value)

    def _diffuseElementsOrState(self, observer, *args):
        call = observer['call']
        diffusing = args[0]
        previousValue = args[1]
        value = args[2]

        values = {}
        if observer['observing'] == "*":
            values = self._getValues(self.getObservableElements())
        else:
            values = self._getValues(observer['observing'])

        previousValues = copy.deepcopy(values)
        previousValues[diffusing] = previousValue

        call(previousValues, values)

    # TODO: get none attribute observable element
    def _getValues(self, observableElements):
        values = {}
        for observableElement in observableElements:
            values[observableElement] = getattr(self, observableElement)

        return values

    def _diffuseElementIn(self, observer, *args):
        call = observer['call']
        previousValues = args[0]
        values = args[1]

        call(
            previousValues[observer["observing"]],
            values[observer["observing"]])

    def _diffuseElementsIn(self, observer, *args):
        call = observer['call']
        previousValues = args[0]
        values = args[1]

        subValues = {}
        previousSubValues = {}
        for element in observer['observing']:
            subValues[element] = values[element]
            previousSubValues[element] = previousValues[element]

        call(previousSubValues, subValues)

    def _diffuseStateIn(self, observer, *args):
        call = observer['call']
        previousValues = args[0]
        values = args[1]

        call(previousValues, values)
