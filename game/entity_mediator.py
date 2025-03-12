from enum import Enum
from utils import collections
from game_reaction_command import GameReactionCommand


class EntityMediator():  # MVC Controller
    def __init__(self, gameTerminal, gameRepository):
        self.gameTerminal = gameTerminal
        self.gameRepository = gameRepository

    def handlePreConditions(self, caller, callee, preConditions):
        for cond in preConditions:
            if not GameReactionCommand(caller, callee, cond).execute(self.gameTerminal):
                return False
        return True

    def __handleReaction(self, caller, callee, r):
        preconditions = collections.lookupFromDictionaryElseEmptyList(r, "preconditions")
        meetsPreConditions = self.handlePreConditions(caller, callee, preconditions)
        if meetsPreConditions:
            GameReactionCommand(caller, callee, r).execute(self.gameTerminal)
            postConditions = collections.lookupFromDictionaryElseEmptyDictionary(r, "postconditions")

            actionTarget = ""
            userActions = collections.lookupFromDictionaryElseEmptyList(r, "userActions")
            if userActions:
                userTargets = collections.lookupFromDictionaryElseEmptyList(r, "userTargets")
                userOptions = []
                for index, userAction in enumerate(userActions):
                    userTarget = userTargets[index]
                    userTarget = " " + userTarget if userTarget else ""
                    userOptions.append(userAction + userTarget)
                actionTarget = self.__getActionTarget(userActions, userTargets)
                while not actionTarget or (postConditions and not collections.lookupFromDictionaryElseEmptyString(postConditions, actionTarget)):
                    self.gameTerminal.printlnInvalidAction(userOptions)
                    actionTarget = self.__getActionTarget(userActions, userTargets)

            self.handlePostConditions(caller, callee, postConditions, actionTarget)

    def handleReactions(self, caller, callee):
        reactions = callee.getReactions()
        for r in reactions:
            if isinstance(r, list):  # a chain reaction (one precondition for this list of reactions)
                preconditions = collections.lookupFromDictionaryElseEmptyList(r[0], "preconditions")
                meetsPreConditions = self.handlePreConditions(caller, callee, preconditions)
                if meetsPreConditions:
                    for c in r:
                        self.__handleReaction(caller, callee, c)
            else:
                self.__handleReaction(caller, callee, r)

    def __getActionTarget(self, userActions, userTargets):
        available_actions = set(ua.strip().lower() for ua in userActions)
        available_targets = set()
        for ut in userTargets:
            if ut:
                available_targets.add(ut.strip().lower())
        actionTaken = self.gameTerminal.getActionTaken(input(), {}, available_actions, available_targets)
        actionTarget = (actionTaken[0] + " " + actionTaken[1]).strip()
        return actionTarget

    def __handlePostCondition(self, caller, callee, postConditionAtKey):
        if isinstance(postConditionAtKey, list):
            for postCondition in postConditionAtKey:
                GameReactionCommand(caller, callee, postCondition).execute(self.gameTerminal)
        else:
            GameReactionCommand(caller, callee, postConditionAtKey).execute(self.gameTerminal)

    def handlePostConditions(self, caller, callee, postConditions, actionTarget):
        if not postConditions:
            return None

        if actionTarget:
            self.__handlePostCondition(caller, callee, postConditions[actionTarget])
        else:
            postConditionsKeys = postConditions.keys()
            for postConditionsKey in postConditionsKeys:
                postCondition = postConditions[postConditionsKey]
                self.__handlePostCondition(caller, callee, postCondition)
