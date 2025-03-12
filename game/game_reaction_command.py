from utils.collections import lookupFromDictionaryElseNone, lookupFromDictionaryElseEmptyList
from game_message import GameMessage
from game_repository_singleton import GameRepositorySingleton


class GameReactionCommand():
    def __init__(self, caller, callee, payload):
        self.__gameRepository = GameRepositorySingleton()
        self.__caller = caller
        self.__callee = callee
        self.__operation = lookupFromDictionaryElseNone(payload, "operation")
        self.__target = lookupFromDictionaryElseNone(payload, "target")
        self.__targetState = lookupFromDictionaryElseNone(payload, "targetState")
        self.__targetStats = lookupFromDictionaryElseNone(payload, "targetStats")
        self.__value = lookupFromDictionaryElseNone(payload, "value")
        self.__messages = []
        prints = lookupFromDictionaryElseEmptyList(payload, "prints")
        for p in prints:
            if lookupFromDictionaryElseEmptyList(p, "message"):
                self.__messages.append(GameMessage(p))

    def execute(self, gameTerminal):
        executed = False
        # Dialogue related:
        if self.__messages:
            formattedMessages = []
            for msg in self.__messages:
                messageArgs = msg.getMessageArgs()
                evaluatedMessageArgs = []
                for messageArg in messageArgs:
                    getCmdWrapper = GameReactionCommand(self.getCaller(), self.getCallee(), messageArg)
                    evaluatedMessageArg = self.__gameRepository.handleGetOperation(getCmdWrapper)
                    evaluatedMessageArgs.append(evaluatedMessageArg)
                formattedMessage = msg.getMessage().format(*evaluatedMessageArgs)
                gameTerminal.printMessage(formattedMessage, msg.isPressEnterToContinue(), msg.getStyle())
            executed = True

        # Game state related:
        if self.getOperation():
            return self.__gameRepository.handleOperation(self)
        return executed

    # Getters

    def getCaller(self):
        return self.__caller

    def getCallee(self):
        return self.__callee

    def getOperation(self):
        return self.__operation

    def getTarget(self):
        return self.__target

    def getTargetState(self):
        return self.__targetState

    def getTargetStats(self):
        return self.__targetStats

    def getValue(self):
        return self.__value

    def getMessages(self):
        return self.__messages
