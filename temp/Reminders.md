## TODO misc:

    - When Class 102 has been barricated, banish all enemy units there and make it a safe zone.

    - Ensure no enemy units can enter the Teacher's Lounge due to the barrier.

## TODO related to Rebecca:

    - Heal the Player's HP.

## TODO related to Layborn:

    - Regarding below, the logic for checking for unupgraded spells.

    - Response #1 will always be available to the player. Response #2 will only be available if the player has unupgraded spells. Selecting response #1 will send the player back into the hallway. Selecting response #2 will result in the following:

    - Response #1 will always be available to the player. Response #2 will only be available if the player still has unupgraded spells. Selecting response #1 will result in the following:

## TODO Throw error during game init when an entity has an invalid vertexId

# Matthew gives Player a magical necklace (item):    
# Matthew gives Player a magical necklace (duration placeholder):

# Matthew leaves with Player:
    
    - [2] The place is mostly safe now. I went through and stopped most of the zombies.
    Response #2 will only be available to the player if the antagonist has already been defeated.
    Selecting Response #2 will skip straight to Matthew leaving with the player. Suggested implementation: when selecting response #2, don't actually directly print out the line, instead, exit this reaction and go into the Matthew leaving with player reaction. The opening line was carefully written to achieve this kind of thing as smoothly as possible. The discrepancy of suddenly knowing Matthew's name can be solved by making it a placeholder instead of hardcoding the name in.
