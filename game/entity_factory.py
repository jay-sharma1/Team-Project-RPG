from utils.collections import lookupFromDictionaryElseEmptyString
from entity.entity import Entity
from entity.player import Player
from entity.enemy import Enemy
from entity.item import Item


class EntityFactory:
    @staticmethod
    def createEntityFromJson(entityJson):
        if lookupFromDictionaryElseEmptyString(entityJson, "isPlayer"):
            anEntity = Player(entityJson)
        elif lookupFromDictionaryElseEmptyString(entityJson, "isEnemy"):
            anEntity = Enemy(entityJson)
        elif lookupFromDictionaryElseEmptyString(entityJson, "isItem"):
            anEntity = Item(entityJson)
        else:
            anEntity = Entity(entityJson)
        return anEntity
