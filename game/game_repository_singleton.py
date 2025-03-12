from enum import Enum
from utils.collections import lookupFromDictionaryElseNone


class GameRepositoryTarget(Enum):
    CALLER = "caller"
    CALLEE = "callee"


class AdventureOperation(Enum):
    GET = "get"
    SET = "set"
    IN = "in"
    NOT_IN = "not in"
    APPEND = "append"
    EQUIP = "equip"
    UPDATE = "update"
    PICKUP = "pickup"


# TODO (Bonus) "The game allows the player to save a snapshot of the game session, so that the session can  later be restored to the exact same game state to play from the second time."
class GameRepositorySingleton():  # MVC Model
    # <REFERENCE>
    # The Singleton Pattern
    # Badenhorst, Wessel. Practical Python Design Patterns : Pythonic Solutions to Common Problems, Apress L. P., 2017. ProQuest Ebook Central, http://ebookcentral.proquest.com/lib/ryerson/detail.action?docID=5107901.
    # Created from TMU on 2022-05-25 16:44:28.
    instance = None

    def __new__(cls):
        if not GameRepositorySingleton.instance:
            GameRepositorySingleton.instance = GameRepositorySingleton.__GameRepositorySingleton()
        return GameRepositorySingleton.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)

    # </REFERENCE>
    class __GameRepositorySingleton():
        def __init__(self):
            self.database = ()
            self.indexes = ()

        def __handleMoveOperation(self, targetEntity, nextVertexId):
            vertex = self.indexes[0][targetEntity.getVertexId()]
            nextVertex = self.indexes[0][nextVertexId]
            vertex.removeEntity(targetEntity)
            targetEntity.state['vertexId'] = nextVertexId
            nextVertex.addEntity(targetEntity)
            return True

        def __handleOperation(self, command, operationOverride):
            caller = command.getCaller()
            callee = command.getCallee()
            operation = operationOverride if operationOverride is not None else command.getOperation()
            target = command.getTarget()
            targetState = command.getTargetState()
            targetStats = command.getTargetStats()

            value = command.getValue()
            if value and isinstance(value, str) and value.startswith("id="):
                valueId = value[3:]
                value = self.indexes[1][valueId]

            targetEntity = None
            if target == GameRepositoryTarget.CALLER.value:
                targetEntity = caller
            elif target == GameRepositoryTarget.CALLEE.value:
                targetEntity = callee
            elif target and target.startswith("id="):
                targetEntityId = target[3:]
                targetEntity = self.indexes[1][targetEntityId]

            match operation:
                case AdventureOperation.GET.value:
                    return targetEntity.state[targetState]
                case AdventureOperation.SET.value:
                    if (targetState == "vertexId"):
                        self.__handleMoveOperation(targetEntity, value)
                        return True
                    elif (targetStats and targetStats in targetEntity.stats):
                        value = targetEntity.stats[value] if value in targetEntity.stats else value
                        targetEntity.stats[targetStats] = value
                        return True
                    print("[GameRepository Error] Unsupported AdventureOperation.SET targetState: " + targetState)
                    return False
                case AdventureOperation.IN.value:
                    targetState = targetEntity.state[targetState]
                    return value in targetState
                case AdventureOperation.NOT_IN.value:
                    targetState = targetEntity.state[targetState]
                    return value not in targetState
                case AdventureOperation.APPEND.value:
                    targetState = targetEntity.state[targetState]
                    targetState.append(value)
                    return True
                case AdventureOperation.EQUIP.value:
                    targetState = targetEntity.state[targetState]
                    targetState.append(value)
                    value.equip(targetEntity)
                    if value.type == "Weapon":
                        targetEntity.state["armedWeapon"] = value.name
                    return True
                case AdventureOperation.UPDATE.value:
                    targetEntity.state[targetState] = value
                    return True
                case AdventureOperation.PICKUP.value:
                    value.pick_up(targetEntity)
                    return True

        def handleOperation(self, command):
            return self.__handleOperation(command, None)

        def handleGetOperation(self, command):
            return self.__handleOperation(command, AdventureOperation.GET.value)
