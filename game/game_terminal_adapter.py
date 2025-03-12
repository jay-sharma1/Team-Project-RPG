from enums.adventure_movement import AdventureMovement
from enums.adventure_command import AdventureCommand
from entity.fore import Fore
import sys
import re
import string
import os
os.system("")

# DONE (Bonus) "Perhaps your room description data  text could allow special placeholders (akin  to %s and  other  format codes in printf)  that  the game engine  then dynamically fills in with names  and such to describe some particular part of the current moment."
# TODO (Bonus) "Alternatively to above, how about: 'was thinking it would be more like print description, moving entities and items on newlines'"
# DONE (Bonus) "Make sure that your paragraphs of output are neatly printed within the assumed line width  so that the lines won't look all ragged and such, whether a placeholder in some sentence is  filled  with  the  value  "book"   or  with  the  value  "revised edition of the  collected works of Aloysius T. Snuffleupagus, with commentary by  professor P. P. Weisenheimer". It would be nice if your printing logic worked for  arbitrary line lengths, formatting the output into neat paragraphs regardless of whether the  lines are capped to 60, 80 or however many n characters."
# TODO (Bonus) the help command.


class GameTerminalAdapter():  # MVC View

    def __init__(self, numCharsPerLine=80):
        self.numCharsPerLine = numCharsPerLine

    # Take a string and return a list containing every group of alphabetical characters that is separated by whitespace.
    # All words are reduced to lowercase.
    def __parse(self, sentence: str):
        return re.sub('[' + string.punctuation + ']', '', sentence.lower()).split()

    # Takes a string input by the user, all individual actions, all valid verbs, and all valid targets
    # in order to return an array containing only the useful strings.
    # This helps determine what action needs to be taken.
    # Solo actions examples are individual words (e.g. inventory, N, S, etc)
    # Available actions are a verb/target (e.g. grab sword, open chest, etc)
    def getActionTaken(self, user_input: str, solo_actions: set[str], available_actions: set[str], available_targets: set[str]):
        list_words = self.__parse(user_input)
        action = ""
        target = ""

        for word in list_words:
            if word in solo_actions:
                action = word
                break
        if action:
            return [action, ""]

        for word in list_words:
            if word in available_actions:
                action = word
                break

        for word in list_words:
            if word in available_targets:
                target = word
                break

        return [action, target]

    def promptUser(self):
        command = input()
        command = command.strip()
        lenCommand = len(command)
        if 0 < lenCommand <= 2:
            if command == AdventureCommand.QUIT.value:
                return (AdventureCommand.QUIT.value, None)

            movement = next(filter(lambda m: m.value == command, list(AdventureMovement)), None)
            if movement is not None:
                return (AdventureCommand.MOVE.value, movement.value)

        return (AdventureCommand.ERROR.value, None)

    def printWelcomeBanner(self):
        print("")
        self.println("**************************************************")
        print(("Welcome to ") + Fore.RED + "Escape from Hellspawn!" + Fore.ENDC)
        print(("Supported verbs are ") + Fore.GREEN + "read, greet, introduce, agree, go, thank, ask, request, equip, take, use, hesitate, ease, criticize, fight, leave" + Fore.ENDC)
        print("")
        print("          During the past few months, there have been news reports of large numbers of people acting strangely. These people are irritable and become liable to physically aggressive behaviour when irritated. In addition, there has been a noticeable increase in the amount of internet blogs complaining about their friend (who just happens to have visited their doctor recently) suddenly becoming very rude, more than usual. Experts have dismissed this trend as a coincidence. But the number of people reporting greater irritation than usual has been continuing to climb higher and higher. In addition, during the second month of this trend, those who have been prescribed psychiatric drugs have reported no change in their mood, and city morgues have reported self-moving behaviour in corpses, but have been able to terminate the self-movement by beheading them. There have been no news from remote town and rural morgues. Possible links between these self-moving corpses and the irritability trend have been claimed by various people, but experts have not confirmed anything yet. For now, out of concerns for national work productivity, work has commenced on attempting to produce a new suppressant for the strangely resistant mental disorder, now called hyper-irritation.  The objective is to get out of the school using any one of several paths.")
        print("")
        self.println("**************************************************")

    def printTurn(self, playerName, playerVertexName, validDirections):
        print("")
        print(Fore.CYAN + playerName + "'s turn." + Fore.ENDC)
        print(Fore.CYAN + "Current location: " + playerVertexName + Fore.ENDC)
        print(Fore.CYAN + "Move choices: " + validDirections + Fore.ENDC)

    def printMessage(self, message, pressEnterToContinue, style):
        if style:
            fore = Fore.getForeByStyleName(style)
            print(fore + message + Fore.ENDC)
        else:
            self.println(message)
        if pressEnterToContinue:
            self.println("Press enter to continue.")
            while True:
                text = input("")
                if text == AdventureCommand.QUIT.value:
                    if input("Are you sure you want to quit? [Y/N]").strip().upper() == "Y":
                        self.println("Goodbye.")
                        sys.exit(0)
                elif text:
                    self.println("Press Enter to continue")
                else:
                    break

    def println(self, message):
        numCharsInMessage = len(message)
        if not numCharsInMessage:
            return None

        lastIndex = numCharsInMessage - 1
        startIndex = 0
        endIndex = startIndex + self.numCharsPerLine - 1

        while startIndex <= lastIndex:
            if endIndex > lastIndex:
                endIndex = lastIndex
            else:
                # Backtrack to word-boundary (if needed):
                newEndIndex = endIndex
                try:
                    while newEndIndex > 0 and not message[newEndIndex].isspace() and not message[newEndIndex + 1].isspace():
                        newEndIndex -= 1
                    endIndex = newEndIndex if newEndIndex else lastIndex
                except IndexError:
                    newEndIndex = None

            line = message[startIndex:(endIndex + 1)]
            print(line)

            startIndex = endIndex + 1
            endIndex = startIndex + self.numCharsPerLine - 1
        print("")  # Newline

    def printlnInvalidAction(self, userOptions):
        self.println("Invalid action. Available actions:")
        for userOption in userOptions:
            print(Fore.GREEN + " * " + userOption + Fore.ENDC)
        print("")  # Reset colour
