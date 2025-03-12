from entity.entity import Entity


class Combatant(Entity):
    def __init__(self, state):
        Entity.__init__(self, state)
        self.current_behaviour = "Staying Put"

    def action(self, game_map, targets=None):
        self.is_defending = False
        current_hp = self.stats['Current HP']
        max_hp = self.stats['Max HP']

        # If there are no enemies, thus the entity is not in combat
        if not targets:
            # If current hp is less than max, then heal for 5 and make sure not to go over max hp
            if current_hp < max_hp:
                self.stats['Current HP'] += 5
                if current_hp > max_hp:
                    self.stats['Current HP'] = max_hp

            self.current_behaviour = "Patrolling"
        else:
            # Only defend when you have an ally with more than half health
            if current_hp < (max_hp // 2):
                self.current_behaviour = "Defending"
            # Retreat if alone or all allies are under half health
            elif current_hp < (max_hp // 4):
                self.current_behaviour = "Retreating"
            else:
                self.current_behaviour = "Attacking"

        match self.current_behaviour:
            case "Staying Put":
                pass

            case "Patrolling":
                self.auto_move(game_map)

            case "Retreating":
                return self.escape(targets, game_map)

            case "Attacking":
                self.basic_attack(targets)

            case "Defending":
                self.is_defending = True
