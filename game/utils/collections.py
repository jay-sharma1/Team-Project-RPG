def lookupFromDictionaryElseNone(dictionary, targetKey):
    return None if targetKey not in dictionary else dictionary[targetKey]


def lookupFromDictionaryElseFalse(dictionary, targetKey):
    return False if targetKey not in dictionary else dictionary[targetKey]


def lookupFromDictionaryElseEmptyString(dictionary, targetKey):
    return "" if targetKey not in dictionary else dictionary[targetKey]


def lookupFromDictionaryElseEmptyList(dictionary, targetKey):
    return [] if targetKey not in dictionary else dictionary[targetKey]


def lookupFromDictionaryElseEmptyDictionary(dictionary, targetKey):
    return {} if targetKey not in dictionary else dictionary[targetKey]
