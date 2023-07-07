# My colors
white = (255,255,255)
controlColor = (60,60,60)
background = (60,60,60)
mapBackgroundColor = (20,80,40)
darkGray = [30,30,30]

black = (0,0,0)
red = (255,0,0)
wallColor = (100,50,30)
green = (0,200,0)
blue = (0,0,255)

FPS = 25

# Width and hight of the full window (with neural network and info)
fullWinWidth = 1400
# fullWinHieght = 800
fullWinHieght = 800
fullWinDimentions =(fullWinWidth, fullWinHieght)

# Width and hight of the game simulation window (without the neural network and info)
playingWinWidth = 750
playingWinHieght = 750
#playingWinDimentions = (playingWinWidth, playingWinHieght)
playingWinPos = 25

horizontalMargin = 75
verticalMargin = 35

# Size of each cell
blockSize = 50
mainSpeed = blockSize
wallThikness = 6
cellEdgeWidth = 1

# Drawing parameters
pathToAppleImage = "drawings/apple.png"
neuronSize = 6
eyesWhiteSize = int(blockSize*0.1)
eyesBlackSize = int(blockSize*0.09)
noseSize = int(eyesBlackSize*0.7)

maxApplesNum = 200
applesToshow = [0 for i in range(maxApplesNum)]
maxScore = 0
numOfDeadSnakes = 0

# The number of cells to add after each point (apple)
growthRate = 4
initialPos = [int(playingWinWidth/(2*blockSize))*blockSize,int(playingWinHieght/(2*blockSize))*blockSize]

# useMidAndLastCells = True
useMidAndLastCells = False
if useMidAndLastCells:
    inputNum = 14
else:
    inputNum = 10
    
outputNum = 4
# initialBrainLyers = [inputNum, 20, 15, outputNum]
# initialBrainLyers = [inputNum, 7, 7, outputNum]
initialBrainLyers = [inputNum, 10, 7, 10, outputNum]
# initialBrainLyers = [inputNum, 10, outputNum]
# initialBrainLyers = [inputNum, outputNum]
initialImitateRate = 0.01
hugeImitationNum = 25
binaryDistToApple = True
hugeImitationRate = 2.5*initialImitateRate
colorShiftRate = int(255*0.06)
neural_pos = []

allowedRepetition = 5
numOfMovesToCheckRepetition = 20
maxMovesWithoutApples = (playingWinWidth + playingWinHieght)/blockSize *3.5

# The size of each generation (num of snakes to test)
genSize = 1000

# Initializing the environment
genNum = 1
numOfMoves = 0
bestScore = 0
bestScoreThisGen = 0
bestFitness = 0
bestFitnessLastGen = 0
genTestSteps = 5000
genKeepRate = 0.2

showOne = False
changeShowDir = 1
idOfShownSnake = 0
snakeRootID = 1

