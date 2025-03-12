from utils.collections import lookupFromDictionaryElseEmptyList, lookupFromDictionaryElseFalse, lookupFromDictionaryElseNone


class GameMessage():
    def __init__(self, payload):
        self.__message = lookupFromDictionaryElseEmptyList(payload, "message")
        self.__messageArgs = lookupFromDictionaryElseEmptyList(payload, "messageArgs")
        self.__pressEnterToContinue = lookupFromDictionaryElseFalse(payload, "pressEnterToContinue")
        self.__style = lookupFromDictionaryElseNone(payload, "style")

    def getMessage(self):
        return self.__message

    def getMessageArgs(self):
        return self.__messageArgs

    def isPressEnterToContinue(self):
        return self.__pressEnterToContinue

    def getStyle(self):
        return self.__style
