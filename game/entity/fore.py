import os
os.system("")
class Fore:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    ENDC = '\033[0m'

    @staticmethod
    def getForeByStyleName(styleName):
        if styleName == "important":
            return Fore.RED
        elif styleName == "success":
            return Fore.GREEN
        else:
            return None  # Unrecognized style name
