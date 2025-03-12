from enums.adventure_command import AdventureCommand
from game_terminal_adapter import GameTerminalAdapter
from game_repository_singleton import GameRepositorySingleton
from entity_mediator import EntityMediator
from combat_engine import begin_combat


class GameEngine():  # MVC Controller
    def __init__(self, gameMap, players, enemies):
        self.gameMap = gameMap
        self.players = players
        self.enemies = enemies
        gameTerminal = GameTerminalAdapter()
        gameRepository = GameRepositorySingleton()
        self.entityMediator = EntityMediator(gameTerminal, gameRepository)
        self.gameTerminal = gameTerminal
        self.gameRepository = gameRepository

    def __checkForEncounter(self, player):
        previousVertexId = player.getVertexId()
        playerVertex = self.gameMap.getVertexById(player.getVertexId())
        vertexEntities = playerVertex.getEntities()
        flee = False
        for entity in vertexEntities:
            if entity.isEnemy() and not entity.isDefeated():
                enemies = [entity]
                begin_combat(player, [entity], self.gameMap)
                if entity.isDefeated():  # defeated
                    self.entityMediator.handleReactions(player, entity)
                else:
                    flee = True
            elif entity is not player and entity.isInteractable() and not flee:
                entity.printGreeting()
                self.entityMediator.handleReactions(player, entity)
                nextVertexId = player.getVertexId()
                if previousVertexId != nextVertexId:
                    self.__checkForEncounter(player)

    def start(self):
        self.gameTerminal.printWelcomeBanner()
        movingPlayers = self.players
        while len(movingPlayers) > 0:
            for player in movingPlayers:
                playerVertex = self.gameMap.getVertexById(player.getVertexId())
                vertexEntities = playerVertex.getEntities()
                vertexEdges = playerVertex.getEdges()
                validDirections = list(map(lambda edge: edge['direction'], vertexEdges))

                self.gameTerminal.printTurn(player.getName(), str(playerVertex.getName()), str(validDirections))

                isValidMove = False
                while not isValidMove:
                    nextCommand = self.gameTerminal.promptUser()
                    nextCommandType = nextCommand[0]
                    nextCommandValue = nextCommand[1]
                    match nextCommandType:
                        case AdventureCommand.MOVE.value:
                            if nextCommandValue in validDirections:
                                isValidMove = True
                                print("")

                                targetEdge = next(filter(lambda edge: edge['direction'] == nextCommandValue, vertexEdges))
                                player.move(self.gameMap, targetEdge['destination'])
                                self.__checkForEncounter(player)
                            else:
                                self.gameTerminal.println("Cannot move: " + nextCommandValue + " from this location")
                            break
                        case AdventureCommand.QUIT.value:
                            return self.gameTerminal.println("Goodbye.")
                        case AdventureCommand.ERROR.value:
                            self.gameTerminal.println("Unrecognized command.")
                            break

            if player.hasEscapedFromHellspawn():
                movingPlayers = list(filter(lambda p: not p.hasEscapedFromHellspawn(), self.players))

            for enemy in self.enemies:
                if enemy.moveSpeed:
                    enemy.move(self.gameMap)
