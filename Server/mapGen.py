__author__ = 'harry'

import random


def generateMap(width, height):
    #Split the screen into 50px blocks
    toplefts_x = [x for x in range(0, width+1, 100)]
    toplefts_y = [x for x in range(150, (height+1)-150, 100)]
    numX = len(toplefts_x)
    numY = len(toplefts_y)
    #Initialise map array
    Map = []

    #We want to have some buildings here and there
    #But we cannot put them over the tanks
    #Tanks spawn in the top and bottom, y=100 and y=700
    #So we cut out ranges 0>y>150 and height-150 > y > height

    #We now want a small chance for a building to gen, and perhaps a tiny chance of a 2x2
    possibleBlocks = len(toplefts_x)
    for i in range(possibleBlocks):
        #Random number generator picks the fill for the block
        toSpawn = random.randint(0,60)
        #Add a single building
        if toSpawn > 50:
            xPos = i % numX
            yPos = i % numY
            Map.append([xPos, yPos, 1])
        #Add a 2x2
        elif toSpawn == 30:
            xPos = i % numX
            yPos = i % numY
            Map.append([xPos, yPos, 2])
    return Map

