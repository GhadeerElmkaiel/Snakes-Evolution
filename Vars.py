# My colors
white = (255,255,255)
controlColor = (60,60,60)
background = (60,60,60)
darkGray = (30,30,30)

black = (0,0,0)
red = (255,0,0)
wallColor = (100,50,30)
green = (0,200,0)
blue = (0,0,255)

FPS = 20

# Width and hight of the full window (with neural network and info)
fullWinWidth = 1400
fullWinHieght = 800
fullWinDimentions =(fullWinWidth, fullWinHieght)

# Width and hight of the game simulation window (without the neural network and info)
playingWinWidth = 750
playingWinHieght = 750
#playingWinDimentions = (playingWinWidth, playingWinHieght)
playingWinPos = 25

# Size of each cell
blockSize = 10
mainSpeed = blockSize
wallThikness = 6


maxApplesNum = 200
applesToshow = [0 for i in range(maxApplesNum)]
maxScore = 0
numOfDeadSnakes = 0

# The number of cells to add after each point (apple)
growthRate = 4
initialPos = [int(playingWinWidth/20)*10,int(playingWinHieght/20)*10]

inputNum = 10
outputNum = 4
initialBrainLyers = [inputNum, 20, 15, outputNum]
initialImitateRate = 0.01
hugeImitationNum = 10
hugeImitationRate = 2.5*initialImitateRate
neural_pos = []

allowedRepetition = 5
numOfMovesToCheckRepetition = 20
maxMovesWithoutApples = (playingWinWidth + playingWinHieght)/blockSize *1.2

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
genKeepRate = 0.5

showOne = False
changeShowDir = 1
idOfShownSnake = 0
snakeRootID = 1
