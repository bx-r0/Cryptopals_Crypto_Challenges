import os

def loadData(extra):
    """
    Concatenates all data lines into one
    """

    lines = loadLines(extra)

    lines = list(map(str.strip, lines))

    return "".join(lines)

def loadLines(extra):
    """
    Returns all data lines in a list
    """

    path = os.path.realpath(__file__)
    pathSections = path.split('/')
    path = "/".join(pathSections[:-1])
    
    lines = []
    with open(path + extra, 'r') as file:
        lines = file.readlines()
        
    return lines