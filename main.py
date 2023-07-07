import pygame
from Vars import *
import random
import numpy as np
import math
import time
import os

# Create a folder to save generation in, if they were needed to load afterwards
def create_folder(dir):
	try:
		if not os.path.exists(dir):
			os.makedirs(dir)
	except:
		pass


# Init Pygame paraeters
pygame.init()
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode(fullWinDimentions)
pygame.display.set_caption('Snake')

appleImage = pygame.image.load(pathToAppleImage).convert_alpha()
appleImage = pygame.transform.scale(appleImage, (blockSize, blockSize))

# Create a folder for this simulation
startTime=int(time.time()%100000000)
create_folder("./TestGens/"+str(startTime)+"/")

class control_panel():
	"""
	A class for the panel on the right side of the window
	
	Attributes
	__________
	display	: pygame.display
		the game display window
	starPos	: [int,	int]
		the start position of the panel
	Width	: int
		the width of the panel
	Hieght	: int
		the hieght ofthe panel
	color	: (int, int, int)
		the color of the panel
	edge	: int
		the distance between the edge of the window and the edge of the panel
	horizontalMargin: int
		the horizontal margin between the elements in the panel
	verticalMargin	: int
		the vertical margin between the elements in the panel

	Methods
	_______
	draw(snake)
		draws the banel and the elements inside it.
	draw_brain(snake)
		draws the neural network inside the brain of the selected snake.
	
	"""
	def __init__(self, snake=None):
		self.display = gameDisplay
		self.startPos = [playingWinWidth	 + 2*playingWinPos, playingWinPos]
		self.width = fullWinWidth - 3 * playingWinPos - playingWinWidth
		self.hieght = fullWinHieght - 2* playingWinPos
		self.color = np.array(darkGray)
		self.edge = playingWinPos
		self.horizontalMargin = horizontalMargin
		self.verticalMargin = verticalMargin
		

		if snake == None:
			self.layersNum = initialBrainLyers
			self.brainHight = self.verticalMargin*(initialBrainLyers[0])
		else:
			self.layersNum = snake.brain.layersNum
			self.brainHight = self.verticalMargin*(snake.brain.layersNum[0])
		self.brainWidth = self.width - 2*self.edge - self.horizontalMargin
		self.calc_neural_newtwork_pos()
		self.infoBlockPos = [self.startPos[0], self.startPos[1]+2*self.edge+self.brainHight]

	def draw(self, snake):
		self.draw_brain(snake)
		message_to_screen_corner(("Gen num       : " + str(genNum)),[self.infoBlockPos[0]+self.edge, self.infoBlockPos[1]+self.edge],white,25)
		message_to_screen_corner(("Best Score    : " + str(bestScore)),[self.infoBlockPos[0]+self.edge, self.infoBlockPos[1]+self.edge + self.verticalMargin],white,25)
		message_to_screen_corner(("Best Fitness : " + str(int(bestFitness))),[self.infoBlockPos[0]+self.edge, self.infoBlockPos[1]+self.edge + 2*self.verticalMargin],white,25)
		message_to_screen_corner(("Num of Moves: " + str(numOfMoves)),[self.infoBlockPos[0]+self.edge, self.infoBlockPos[1]+self.edge + 3*self.verticalMargin],white,25)
		message_to_screen_corner(("Num of alive: " + str(genSize- numOfDeadSnakes)),[self.infoBlockPos[0]+self.edge, self.infoBlockPos[1]+self.edge + 4*self.verticalMargin],white,25)
		

		message_to_screen_corner(("Best Score This Gen  : " + str(bestScoreThisGen)),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge],white,25)
		message_to_screen_corner(("Best Fitness Last Gen: " + str(int(bestFitnessLastGen))),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge+ self.verticalMargin],white,25)
		
		if showOne:
			message_to_screen_corner(("Showing Snake    : " + str(snake.name)),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 2*self.verticalMargin],white,25)
			message_to_screen_corner(("Num                         : " + str(idOfShownSnake)),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 3*self.verticalMargin],white,25)
			message_to_screen_corner(("Score                       : " + str(snake.score)),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 4*self.verticalMargin],white,25)
			message_to_screen_corner(("GrandFather ID        : " + str(snake.rootID)),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 5*self.verticalMargin],white,25)
			# message_to_screen_corner(("Born in Generation : " + str(snake.bornGen)),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 6*self.verticalMargin],white,25)
			message_to_screen_corner(("Born in Generation : " + str(snake.bornGen)),[self.infoBlockPos[0] + self.edge, self.infoBlockPos[1]+self.edge + 5*self.verticalMargin],white,25)
		else:
			message_to_screen_corner(("Showing Snake    : All"),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 2*self.verticalMargin],white,25)
			message_to_screen_corner(("Num                         : None"),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 3*self.verticalMargin],white,25)
			message_to_screen_corner(("Score                       : None"),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 4*self.verticalMargin],white,25)
			message_to_screen_corner(("GrandFather ID        : None"),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 5*self.verticalMargin],white,25)
			# message_to_screen_corner(("Born in Generation : None"),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 6*self.verticalMargin],white,25)
			message_to_screen_corner(("Born in Generation : None"),[self.infoBlockPos[0] +self.edge, self.infoBlockPos[1]+self.edge + 5*self.verticalMargin],white,25)


	def draw_brain(self,snake):
		pygame.draw.rect(self.display, self.color,(self.startPos[0], self.startPos[1], self.width, self.hieght))
		messages = []
		# messages.append("U_W: " + str(snake.disToWallUp))
		# messages.append("R_W: " + str(snake.disToWallDown))
		# messages.append("D_W: " + str(snake.disToWallRight))
		# messages.append("L_W: " + str(snake.disToWallLeft))

		# messages.append("X_A: " + str(snake.disToAppleX))
		# messages.append("Y_A: " + str(snake.disToAppleY))

		# messages.append("U_C: " + str(snake.disToCellUp))
		# messages.append("R_C: " + str(snake.disToCellDown))
		# messages.append("D_C: " + str(snake.disToCellRight))
		# messages.append("L_C: " + str(snake.disToCellLeft))

		messages.append("U_W: " + "{:.3f}".format(snake.disToWallUp))
		messages.append("R_W: " + "{:.3f}".format(snake.disToWallDown))
		messages.append("D_W: " + "{:.3f}".format(snake.disToWallRight))
		messages.append("L_W: " + "{:.3f}".format(snake.disToWallLeft))

		messages.append("X_A: " + "{:.3f}".format(snake.disToAppleX))
		messages.append("Y_A: " + "{:.3f}".format(snake.disToAppleY))

		messages.append("U_C: " + "{:.3f}".format(snake.disToCellUp))
		messages.append("R_C: " + "{:.3f}".format(snake.disToCellDown))
		messages.append("D_C: " + "{:.3f}".format(snake.disToCellRight))
		messages.append("L_C: " + "{:.3f}".format(snake.disToCellLeft))

		if useMidAndLastCells:
			messages.append("MC_X: " + "{:.3f}".format(snake.disToMidCellX))
			messages.append("MC_Y: " + "{:.3f}".format(snake.disToMidCellY))
			messages.append("LC_X: " + "{:.3f}".format(snake.disToLastCellX))
			messages.append("LC_Y: " + "{:.3f}".format(snake.disToLastCellY))

		messages.append("C__: 1")
		#message_to_screen_corner("U_W: " + str(round(snake.disToWallUp,2)), (playingWinWidth + 3*playingWinPos , 2*playingWinPos), white, 25)
		#message_to_screen_corner("R_W: " + str(round(snake.disToWallRight,2)), (playingWinWidth + 3*playingWinPos, 4*playingWinPos), white, 25)
		for i ,msg in enumerate(messages):
			message_to_screen_corner(msg,(self.startPos[0]+self.edge-9, self.startPos[1]+self.edge + i*self.verticalMargin),white, 20)
		for i in range(len(snake.brain.connections)):
			#print(len(snake.brain.layers[i]))
			#print(len(neural_pos[i]))
			for j in range(len(snake.brain.connections[i])):
				for k in range(len(snake.brain.connections[i][j])):
					lineColor= calc_connection_color(float(snake.brain.connections[i][j][k]*snake.brain.layers[i][k]))
					thikness = int(abs(4*snake.brain.connections[i][j][k]))
					line([self.neural_pos[i][k], self.neural_pos[i+1][j]],lineColor, thikness)

		

		## drawing neurons
		
		for i in range(len(snake.brain.layers)):
			#print(len(snake.brain.layers[i]))
			#print(len(neural_pos[i]))
			for j in range(len(snake.brain.layers[i])):
				neuronColor = calc_neuron_color(snake.brain.layers[i][j])
				circle(self.neural_pos[i][j], (min(neuronColor[0]*1.5,255), min(neuronColor[1]*1.5,255),min(neuronColor[2]*1.5,255)), R=neuronSize+1)
				circle(self.neural_pos[i][j], neuronColor , R=neuronSize)

	def calc_neural_newtwork_pos(self):
		self.neural_pos = []
		HM = int(self.brainWidth /(len(self.layersNum)-1))
		for i in range(len(self.layersNum)):
			newA = []
			if i == len(self.layersNum)-1:
				VM = int(self.brainHight/(self.layersNum[i]-1))
			else:
				VM = int(self.brainHight/(self.layersNum[i]))
			for j in range(self.layersNum[i]+1):
				newA.append([self.startPos[0]+self.edge+self.horizontalMargin+ i*HM,self.startPos[1]+self.edge+ j*VM +7])
			self.neural_pos.append(newA)
		self.neural_pos[-1]=self.neural_pos[-1][:-1]


controlPanel = control_panel()

class apple():
	"""
	A class for apples for each snake
	
	Attributes
	__________
	Pos	: [int, int]
		the game display window

	Methods
	_______
	draw()
		draws the apple on the window.
	
	"""
	def __init__(self):
		# self.Pos = [int(random.randrange(0, playingWinWidth- blockSize)/10)*10, int(random.randrange(0, playingWinHieght- blockSize)/10)*10]
		self.Pos = [int(random.randrange(0, playingWinWidth- blockSize)/blockSize)*blockSize, int(random.randrange(0, playingWinHieght- blockSize)/blockSize)*blockSize]

	def draw(self):
		gameDisplay.blit(appleImage, [playingWinPos+self.Pos[0], playingWinPos+self.Pos[1]])
		# rect([playingWinPos+self.Pos[0], playingWinPos+ self.Pos[1], blockSize, blockSize], black)
		# rect([playingWinPos+self.Pos[0]+1, playingWinPos+ self.Pos[1]+1, blockSize-2, blockSize-2], red)

gameApples = []
for i in range(maxApplesNum):
	gameApples.append(apple())


class brain():
	"""
	A class for the Brain of the snake, which contains a neural network that define how it 
	reacts with the environments
	
	Attributes
	__________
	display	: pygame.display
		the game display window
	starPos	: [int,	int]
		the start position of the panel
	Width	: int
		the width of the panel
	Hieght	: int
		the hieght ofthe panel
	color	: (int, int, int)
		the color of the panel
	edge	: int
		the distance between the edge of the window and the edge of the panel
	horizontalMargin: int
		the horizontal margin between the elements in the panel
	verticalMargin	: int
		the vertical margin between the elements in the panel

	Methods
	_______
	init_layers()
		initialize the initial values of the neural network.
	activate(num, activationFunc='relu')
		the activation funciton for neurons.
	calc_output(inputs)
		calculates the outputs of the neural network given the inputs.
	imitate(imitateRate=None)
		imitate the brain of the snake to create new snakes a bit different than the original.
	copy()
		copy the brain of the snake to use it for a snake in the next generation.
	
	"""
	def __init__(self, copyBrain= [], layers = initialBrainLyers):
		self.layersNum = layers
		self.imitateRate = initialImitateRate
		self.connections=[]
		self.copyBrain = copyBrain
		self.layers = []
		self.init_layers()


	def init_layers(self):
		if len(self.copyBrain) > 0:
			for i in range(len(self.layersNum) -1):
				self.connections.append([])
				for j in range(self.layersNum[i+1]):
					self.connections[i].append([])
					for k in range(self.layersNum[i]+1):
						self.connections[i][j].append(self.copyBrain[i][j][k])
			self.connections = np.array(self.connections, dtype=object)
			self.imitate()
		else:
			for i in range(len(self.layersNum) -1):
				self.connections.append([])
				for j in range(self.layersNum[i+1]):
					self.connections[i].append([])
					for k in range(self.layersNum[i]+1):
						self.connections[i][j].append(random.random()*2-1)
			self.connections = np.array(self.connections, dtype=object)


	def activate(self, num, activationFunc='relu'):
		if activationFunc == "step":
			if num < 0:
				return -1
			else:
				return 1

		elif activationFunc =='relu':
			return math.atan(num) /math.pi *2

	def calc_output(self, inputs):
		self.layers = []
		inLayer = inputs
		inLayer.append(1)
		self.layers.append(inputs)
		for i in range(len(self.connections)):
			newArray  =[]
			#print("len(self.connections[{}]):".format(i),len(self.connections[i]))
			for j in range(len(self.connections[i])):
				sumFunc = sum([(self.layers[i][k]*connect) for k,connect in enumerate(self.connections[i][j])])
				newArray.append(self.activate(sumFunc))
			newArray.append(1)

			self.layers.append(newArray)
		self.layers[-1] = self.layers[-1][:-1] 
		return(self.layers[-1])

		

	def imitate(self, imitateRate=None):
		if imitateRate:
			IR = imitateRate
		else:
			IR = self.imitateRate
		for i in range(len(self.connections)):
			for j in range(len(self.connections[i])):
				for k in range(len(self.connections[i][j])):
					r = random.random()

					if r < IR:
						self.connections[i][j][k]=random.random()*2-1

	def copy(self):
		newConnections = []
		for i in range(len(self.connections)):
			newConnections.append([])
			for j in range(len(self.connections[i])):
				newConnections[i].append([])
				for k in range(len(self.connections[i][j])):
					newConnections[i][j].append(self.connections[i][j][k])
		newConnections = np.array(newConnections, dtype=object)
		return newConnections






class snake():
	#global numOfDeadSnakes
	global growthRate

	def __init__(self, snakeToCopy = None):	
		brainToCopy=[]
		self.numFitToCount = 5
		self.fitnessSum=0
		self.lastNfitToCount = np.array([0 for _ in range(self.numFitToCount)])
		# for i in range(self.numFitToCount):
		# 	self.lastNfitToCount.append(0)

		if snakeToCopy:
			brainToCopy = snakeToCopy.brain.connections
			self.color=snakeToCopy.color.copy()
			self.rootID = snakeToCopy.rootID
			self.name = snakeToCopy.name
			self.change_name()
			# r=random.randrange(2)
			# if r ==1:
			for i in range(3):
				r0 = random.randrange(3)
				if r0<1:
					r=random.randrange(colorShiftRate+1)-int(colorShiftRate/2)
					r1=self.color[i] + r
					r1 = max(0,r1)
					r1 = min(255,r1)
					self.color[i]=r1

			self.fitnessSum	 = snakeToCopy.fitnessSum
			self.lastNfitToCount = snakeToCopy.lastNfitToCount.copy()
		else:
			self.color = np.array([random.randrange(256),random.randrange(256),random.randrange(256)])
			self.rootID = snakeRootID
			globals()["snakeRootID"] +=1
			self.get_name()
			
		
		self.brain = brain(brainToCopy)	
		self.XSpeed = mainSpeed
		self.YSpeed = 0
		self.minLength = 1
		# self.dir = [1, 0]
		self.dir = "Up"
		self.nextDir = "Up"
		allowedRepetition = 5
		numOfMovesToCheckRepetition = 20
		self.reset_values()

		self.disToWallUp = 1
		self.disToWallDown = 1
		self.disToWallLeft = 1
		self.disToWallRight = 1

		self.disToCellUp = 1
		self.disToCellDown = 1
		self.disToCellLeft = 1
		self.disToCellRight = 1

		self.disToMidCellX = 1
		self.disToMidCellY = 1
		self.disToLastCellX = 1
		self.disToLastCellY = 1

		self.disToAppleX = 1
		self.disToAppleY = 1
		self.bestScore = 0
		self.bornGen = genNum

	def reset_values(self):
		self.Pos = initialPos
		self.length = self.minLength
		self.deadReason = ""
		self.lastNMoves = []
		self.score = 0
		self.cells = [self.Pos]
		self.breviousCellPos = []
		self.canMove = True
		self.numOfMoves = 0
		self.fitness = 0
		self.posRepetitionNum = 0
		self.show = True
		self.updateEnabled = True
		self.alive = True
		self.movesWithoutApple = 0


	def calc_info(self):
		self.disToWallRight = (playingWinWidth - self.Pos[0] - blockSize)/playingWinWidth
		self.disToWallLeft = self.Pos[0]/playingWinWidth
		self.disToWallDown = (playingWinHieght - self.Pos[1] - blockSize)/playingWinHieght
		self.disToWallUp = self.Pos[1]/playingWinHieght

		self.disToAppleX = (gameApples[self.score].Pos[0] - self.Pos[0])/playingWinWidth
		self.disToAppleY = (gameApples[self.score].Pos[1] - self.Pos[1])/playingWinHieght

		self.disToCellUp = 1.0
		self.disToCellDown = 1.0
		self.disToCellLeft = 1.0
		self.disToCellRight = 1.0

		leadX = self.Pos[0]
		leadY = self.Pos[1]
		for cell in self.cells[:-1]:
			if cell[0] == leadX:
				#if cell[1] > leadY and ((cell[1] - leadY)/playingWinHieght < self.disToCellDown):
				if cell[1] > leadY and ((cell[1] - leadY) < self.disToCellDown*playingWinHieght):
					self.disToCellDown = (cell[1] - leadY)/playingWinHieght
				#elif leadY > cell[1] and (leadY - cell[1])/playingWinHieght< self.disToCellUp:
				elif leadY > cell[1] and (leadY - cell[1]) < self.disToCellUp*playingWinHieght:
					self.disToCellUp = (leadY - cell[1])/playingWinHieght
			if cell[1] == leadY:
				#if cell[0] > leadX and ((cell[0] - leadX)/playingWinWidth < self.disToCellRight):
				if cell[0] > leadX and ((cell[0] - leadX)< self.disToCellRight*playingWinHieght):
					self.disToCellRight = (cell[0] - leadX)/playingWinWidth
				#elif leadX > cell[0] and (leadX - cell[0])'''/playingWinWidth''' < self.disToCellLeft:
				elif leadX > cell[0] and (leadX - cell[0])< self.disToCellLeft*playingWinHieght:
					self.disToCellLeft = (leadX - cell[0])/playingWinWidth

		l = len(self.cells)
		if l > 1:
			self.disToLastCellX = (self.cells[0][0] - leadX)/playingWinWidth
			self.disToLastCellY = (self.cells[0][1] - leadY)/playingWinHieght

		if l > 2:
			midCell = int(l/2)
			self.disToMidCellX = (self.cells[midCell][0] - leadX)/playingWinWidth
			self.disToMidCellY = (self.cells[midCell][1] - leadY)/playingWinHieght


	
	def get_name(self):
		name = ""
		r = 65+random.randrange(26)
		name += chr(r)

		nameLength = 4+random.randrange(4)
		for i in range(nameLength):
			r = 97+random.randrange(26)
			name += chr(r)
		self.name = name

	def change_name(self):
		r = random.randrange(25*len(self.name))
		if r < 1:
			r = 97+random.randrange(26)
			self.name += chr(r)
		nameList = list(self.name)
		i = random.randrange(len(self.name)-2)
		r = 97+random.randrange(26)
		nameList[i+2] = chr(r)
		self.name="".join(nameList)

	def calc_output(self):
		inputs = []

		# inputs.append(self.disToWallDown/playingWinHieght)	#	To scale the result to one and the input will be bigger when the snake is closer to the wall
		# inputs.append(self.disToWallLeft/playingWinWidth)	#
		# inputs.append(self.disToWallUp/playingWinHieght)	#
		# inputs.append(self.disToWallRight/playingWinWidth)	#

		inputs.append(self.disToWallDown)	#	To scale the result to one and the input will be bigger when the snake is closer to the wall
		inputs.append(self.disToWallRight)	#
		inputs.append(self.disToWallUp)	#
		inputs.append(self.disToWallLeft)	#

		if binaryDistToApple:
			# Binary distance to apple
			if self.disToAppleX>0:								#	To scale the result to one and the input will be bigger when the snake is far away from the apple
				inputs.append(1)								#
			elif self.disToAppleX<0:							#
				inputs.append(-1)								#
			else:												#
				inputs.append(0)								#							
			if self.disToAppleY>0:								#
				inputs.append(1)								#
			elif self.disToAppleY<0:							#
				inputs.append(-1)								#
			else:												#
				inputs.append(0)								#
		else:
			inputs.append(self.disToAppleX)
			inputs.append(self.disToAppleY)

		
		# inputs.append((playingWinHieght-self.disToCellUp)/playingWinHieght)		#	To scale the result to one and the input will be bigger when the snake is closer to another cell
		# inputs.append((playingWinWidth-self.disToCellRight)/playingWinWidth)	#
		# inputs.append((playingWinHieght-self.disToCellDown)/playingWinHieght)	#
		# inputs.append((playingWinWidth-self.disToCellLeft)/playingWinWidth)		#

		# inputs.append((playingWinHieght/playingWinHieght-self.disToCellUp))		#	To scale the result to one and the input will be bigger when the snake is closer to another cell
		# inputs.append((playingWinWidth/playingWinWidth-self.disToCellRight))	#
		# inputs.append((playingWinHieght/playingWinHieght-self.disToCellDown))	#
		# inputs.append((playingWinWidth/playingWinWidth-self.disToCellLeft))		#
		
		inputs.append((self.disToCellUp))		#	To scale the result to one and the input will be bigger when the snake is closer to another cell
		inputs.append((self.disToCellRight))	#
		inputs.append((self.disToCellDown))		#
		inputs.append((self.disToCellLeft))		#

		
		if useMidAndLastCells:
			inputs.append((self.disToMidCellX))			#	To scale the result to one and the input will be bigger when the snake is closer to another cell
			inputs.append((self.disToMidCellY))			#
			inputs.append((self.disToLastCellX))		#
			inputs.append((self.disToLastCellX))		#

		newMove = [0, 0, 0, 0]
		#return self.brain.calc_output(inputs)
		outs = self.brain.calc_output(inputs)
		# idx = outs.index(max(outs))
		# newMove[idx] = 1
		# return(newMove)
		return(outs)

	def self_kill(self,reason = ""):
		self.alive = False
		self.updateEnabled = False
		self.deadReason = reason
		globals()["numOfDeadSnakes"] = globals()["numOfDeadSnakes"]+1
		self.calc_fitness()

	def check_repetition(self):
		for p in self.lastNMoves:
			if self.Pos == p:
				self.posRepetitionNum =self.posRepetitionNum + 1
				if self.posRepetitionNum > allowedRepetition:
					self.self_kill("Position-Repeting")
				return
		self.posRepetitionNum = 0

	def check_collision(self):
		
		## wall collision
		if self.Pos[0]<0:
			self.self_kill("Wall-Crush")
			return True
		if self.Pos[0]>playingWinWidth-blockSize:
			self.self_kill("Wall-Crush")
			return True
		if self.Pos[1]<0:
			self.self_kill("Wall-Crush")
			return True
		if self.Pos[1]>playingWinHieght-blockSize:
			self.self_kill("Wall-Crush")
			return True


		## collision with snake cell
		for i in range(len(self.cells)-1):
			if self.Pos[0] == self.cells[i][0] and self.Pos[1] == self.cells[i][1]: 
				self.self_kill("self-Crush")
				return True

		## apple collision
		if self.score < len(gameApples):
			if self.Pos[0] == gameApples[self.score].Pos[0] and self.Pos[1] == gameApples[self.score].Pos[1]:
				self.score +=1
				self.length += growthRate
				self.movesWithoutApple = 0
				if self.score > globals()["bestScoreThisGen"]:
					globals()["bestScoreThisGen"]= self.score
				if self.score > globals()["bestScore"]:
					globals()["bestScore"]= self.score
				if self.score > self.bestScore:
					self.bestScore = self.score
				
		

	def calc_fitness(self):
		if genNum > 5:
			self.fitness = (self.score**2)*1000 - globals()["numOfMoves"]*2
		else:
			self.fitness = (self.score**2)*1000 + globals()["numOfMoves"]/2
		if self.fitness < 0:
			self.fitness = 0
		if self.deadReason == "Wall-Crush":
			self.fitness = self.fitness/25
		elif self.deadReason == "self-Crush":
			self.fitness = self.fitness/25
		elif self.deadReason == "Position-Repeting":
			self.fitness = self.fitness/40
		elif self.deadReason == "No-Apple":
			self.fitness = self.fitness/10

		self.lastNfitToCount = np.append(self.lastNfitToCount, self.fitness)
		self.lastNfitToCount = self.lastNfitToCount[1:]
		self.fitnessSum=0
		for i in range(self.numFitToCount):
			# self.fitnessSum = self.fitnessSum + (i+1)*(i+1)*self.lastNfitToCount[i]
			self.fitnessSum = self.fitnessSum + self.lastNfitToCount[-1*self.numFitToCount+i]*((i+1)*(i+1))
		self.fitnessSum = self.fitnessSum/((self.numFitToCount*(self.numFitToCount+1)*(2*self.numFitToCount+1))/6)


	def update(self):
		if not self.updateEnabled:
			return
		self.Pos = [self.Pos[0] + self.XSpeed, self.Pos[1]+self.YSpeed]
		self.cells.append(self.Pos)
		self.cells = self.cells[max(0,len(self.cells)-self.length):]
		self.breviousCellPos.append(self.nextDir)
		self.breviousCellPos = self.breviousCellPos[max(0,len(self.breviousCellPos)-self.length):]
		self.canMove = True
		self.check_collision()
		globals()["applesToshow"][self.score] = 1
		self.calc_info()
		self.check_repetition()
		moves = self.calc_output()
		self.move(moves)
		if self.movesWithoutApple >= maxMovesWithoutApples:
			self.self_kill("No-Apple")
		#	print(self.Pos)

	
	def calc_head_drawing_info(self, pos):
		# Define the positions of the face elements
		eps = 1e-2
		if self.dir=="Up":
			xPoints = [0, 0, 0.3, 0.7, 1-eps, 1-eps]
			yPoints = [1-eps, 0.5, 0, 0, 0.5, 1-eps]
			eyes_relative_pos = [[0.3, 0.7], [0.7, 0.7]]
			nosePosRelative = [[0.4, 0.3], [0.6, 0.3]]
			
		if self.dir=="Down":
			xPoints = [0, 0, 0.3, 0.7, 1-eps, 1-eps]
			yPoints = [0, 0.5, 1-eps, 1-eps, 0.5, 0]
			eyes_relative_pos = [[0.3, 0.3], [0.7, 0.3]]
			nosePosRelative = [[0.4, 0.7], [0.6, 0.7]]
			
		if self.dir=="Right":
			xPoints = [0, 0, 0.5, 1-eps, 1-eps, 0.5]
			yPoints = [1-eps, 0, 0, 0.3, 0.7, 1-eps]
			eyes_relative_pos = [[0.3, 0.3], [0.3, 0.7]]
			nosePosRelative = [[0.7, 0.4], [0.7, 0.6]]
			
		if self.dir=="Left":
			xPoints = [0, 0, 0.5, 1-eps, 1-eps, 0.5]
			yPoints = [0.7, 0.3, 0, 0, 1-eps, 1-eps]
			eyes_relative_pos = [[0.7, 0.3], [0.7, 0.7]]
			nosePosRelative = [[0.3, 0.4], [0.3, 0.6]]

		xPointsFixed_size = [int(x*blockSize) for x in xPoints]
		yPointsFixed_size = [int(y*blockSize) for y in yPoints]
		xPointsInPos = [x+playingWinPos+pos[0] for x in xPointsFixed_size]
		yPointsInPos = [y+playingWinPos+pos[1] for y in yPointsFixed_size]
		# inside_ration = (blockSize-2)/blockSize
		# # To calculate a 1 pixel smaller polygon for the inside
		# inside_xPoints = [int(x*inside_ration)+playingWinPos+pos[0]+1 for x in xPointsFixed_size]
		# inside_yPoints = [int(y*inside_ration)+playingWinPos+pos[1]+1 for y in yPointsFixed_size]
		points = list(zip(xPointsInPos, yPointsInPos))
		# inside_points = list(zip(inside_xPoints, inside_yPoints))
		
		
		eyesPos = [[int(x[0]*blockSize)+playingWinPos+pos[0], int(x[1]*blockSize)+playingWinPos+pos[1]] for x in eyes_relative_pos]
		nosePos = [[int(x[0]*blockSize)+playingWinPos+pos[0], int(x[1]*blockSize)+playingWinPos+pos[1]] for x in nosePosRelative]
		return points, eyesPos, nosePos


	def calc_tail_drawing_info(self, pos):
		eps = 1e-2
		if self.breviousCellPos[1]=="Up":
			xPoints = [0, 0.25, 0.5, 0.75, 1-eps]
			yPoints = [0, 0.8, 1-eps, 0.8, 0]
			
		if self.breviousCellPos[1]=="Down":
			xPoints = [0, 0.25, 0.5, 0.75, 1-eps]
			yPoints = [1-eps, 0.2, 0, 0.2, 1-eps]
			
		if self.breviousCellPos[1]=="Right":
			xPoints = [1-eps, 0.2, 0, 0.2, 1-eps]
			yPoints = [0, 0.25, 0.5, 0.75, 1-eps]
			
		if self.breviousCellPos[1]=="Left":
			xPoints = [0, 0.8, 1-eps, 0.8, 0]
			yPoints = [0, 0.25, 0.5, 0.75, 1-eps]
			
		xPointsFixedSize = [int(x*blockSize) for x in xPoints]
		yPointsFixedSize = [int(y*blockSize) for y in yPoints]
		xPointsInPos = [x+playingWinPos+pos[0] for x in xPointsFixedSize]
		yPointsInPos = [y+playingWinPos+pos[1] for y in yPointsFixedSize]
		# inside_ration = (blockSize-2)/blockSize
		# # To calculate a 1 pixel smaller polygon for the inside
		# inside_xPoints = [int(x*inside_ration)+playingWinPos+pos[0]+1 for x in xPointsFixed_size]
		# inside_yPoints = [int(y*inside_ration)+playingWinPos+pos[1]+1 for y in yPointsFixed_size]

		points = list(zip(xPointsInPos, yPointsInPos))
		# inside_points = list(zip(inside_xPoints, inside_yPoints))
		
		return points

	def draw(self):
		if not self.show or not self.alive:
			return
		for c in self.cells[1:-1]:
			rect([playingWinPos+c[0], playingWinPos+ c[1], blockSize, blockSize], self.color)
			rect([playingWinPos+c[0], playingWinPos+ c[1], blockSize, blockSize], black, width = cellEdgeWidth)
			# rect([playingWinPos+c[0]+1, playingWinPos+ c[1]+1, blockSize-2, blockSize-2], self.color, width=5)

		points, eyesPos, nosePosition = self.calc_head_drawing_info(self.cells[-1])
		pygame.draw.polygon(gameDisplay, self.color, points)
		pygame.draw.polygon(gameDisplay, black, points, cellEdgeWidth)
		
		# Draw the eyes
		circle(eyesPos[0], white, eyesWhiteSize)
		circle(eyesPos[1], white, eyesWhiteSize)
		circle(eyesPos[0], black, eyesBlackSize)
		circle(eyesPos[1], black, eyesBlackSize)
		
		circle(nosePosition[0], black, noseSize, width = cellEdgeWidth+1)
		circle(nosePosition[1], black, noseSize, width = cellEdgeWidth+1)

		# Draw the mouth as an arc
		# pygame.draw.arc(gameDisplay, black, mouthArcInfo[0], mouthArcInfo[1], mouthArcInfo[2], mouthArcInfo[3])
		
		# Draw tail
		if len(self.cells)>1:
			tailPoints = self.calc_tail_drawing_info(self.cells[0])
			pygame.draw.polygon(gameDisplay, self.color, tailPoints)
			pygame.draw.polygon(gameDisplay, black, tailPoints, width=cellEdgeWidth)

	def increase(self, num):
		self.length+= num

	def decrease(self, num):
		self.length = max(self.minLength, self.length - num)

	def move(self, dirs):
		# array for checking repetition
		idx = dirs.index(max(dirs)) 
		moved = False
		self.lastNMoves.append(self.Pos)
		if len(self.lastNMoves) > numOfMovesToCheckRepetition:
			self.lastNMoves = self.lastNMoves[1:]

		self.movesWithoutApple = self.movesWithoutApple+1

		self.dir = self.nextDir
		if not self.canMove:
			return
		while(not moved):
			
			if idx==0 and not self.YSpeed == mainSpeed:
				self.XSpeed = 0
				self.YSpeed = -mainSpeed
				self.nextDir = "Up"
				moved = True
			elif idx==2 and not self.YSpeed == -mainSpeed:
				self.XSpeed = 0
				self.YSpeed = mainSpeed
				self.nextDir = "Down"
				moved = True
			elif idx==1 and not self.XSpeed == -mainSpeed:
				self.YSpeed = 0
				self.XSpeed = mainSpeed
				self.nextDir = "Right"
				moved = True
			elif idx==3 and not self.XSpeed == mainSpeed:
				self.YSpeed = 0
				self.XSpeed = -mainSpeed
				self.nextDir = "Left"
				moved = True
			dirs[idx] = -5
			idx = dirs.index(max(dirs))

		self.canMove = False
		
			


'''
Function that creates a text object that return the msg after rendering and the rect of the text border.
'''
def text_objects(msg, color, font):
	textSurface = font.render(msg, True, color)
	return textSurface , textSurface.get_rect()


'''
Print a msg to the screen positioning the center of the text.
'''
def message_to_screen(msg, pos, color = black, fontSize = 25):
	font = pygame.font.SysFont(None, fontSize)
	textSurf, textRect = text_objects(msg, color, font)
	textRect.center = pos[0], pos[1]
	gameDisplay.blit(textSurf, textRect)


'''
Print a msg to the screen positioning the corner of the text.
'''
def message_to_screen_corner(msg, pos, color=black, fontSize=25):
	font = pygame.font.SysFont(None, fontSize)
	screenText = font.render(msg, True, color)
	gameDisplay.blit(screenText, pos)


####
# No need for this if you are using control panel class
####
def drow_control(snake):
	leadX = snake.Pos[0]
	leadY = snake.Pos[1]

	pygame.draw.rect(gameDisplay, darkGray,(2*playingWinPos + playingWinWidth, playingWinPos, fullWinWidth -  playingWinWidth -3* playingWinPos , fullWinHieght- 2*playingWinPos))
	#display_buttons()
	
	if showMsgs:
		#for i,msg in enumerate(messages):
		#	message_to_screen_corner(msg,())	
		message_to_screen_corner("U_W: " + str(round(snake.disToWallUp,2)), (playingWinWidth + 3*playingWinPos , 2*playingWinPos), white, 25)
		message_to_screen_corner("R_W: " + str(round(snake.disToWallRight,2)), (playingWinWidth + 3*playingWinPos, 4*playingWinPos), white, 25)
		message_to_screen_corner("D_W: " + str(round(snake.disToWallDown,2)), (playingWinWidth + 3*playingWinPos, 6*playingWinPos), white, 25)
		message_to_screen_corner("L_W: " + str(round(snake.disToWallLeft,2)), (playingWinWidth + 3*playingWinPos, 8*playingWinPos), white, 25)

		message_to_screen_corner("X_A: " + str(round(snake.disToAppleX,2)), (playingWinWidth + 3*playingWinPos, 10*playingWinPos), white, 25)
		message_to_screen_corner("Y_A: " + str(round(snake.disToAppleY,2)), (playingWinWidth + 3*playingWinPos, 12*playingWinPos), white, 25)

		message_to_screen_corner("U_C: " + str(round(snake.disToCellUp,2)), (playingWinWidth + 3*playingWinPos, 14*playingWinPos), white, 25)
		message_to_screen_corner("R_C: " + str(round(snake.disToCellRight,2)), (playingWinWidth + 3*playingWinPos, 16*playingWinPos), white, 25)
		message_to_screen_corner("D_C: " + str(round(snake.disToCellDown,2)), (playingWinWidth + 3*playingWinPos, 18*playingWinPos), white, 25)
		message_to_screen_corner("L_C: " + str(round(snake.disToCellLeft,2)), (playingWinWidth + 3*playingWinPos, 20*playingWinPos), white, 25)
		message_to_screen_corner("C__:  1", (playingWinWidth + 3*playingWinPos, 22*playingWinPos), white, 25)

		## drawing neurons
		
		for i in range(len(snake.brain.connections)):
			#print(len(snake.brain.layers[i]))
			#print(len(neural_pos[i]))
			for j in range(len(snake.brain.connections[i])):
				for k in range(len(snake.brain.connections[i][j])):
					lineColor= calc_connection_color(float(snake.brain.connections[i][j][k]*snake.brain.layers[i][k]))
					#if j == 1:
					#	print(lineColor)brain.layers
					thikness = int(abs(4*snake.brain.connections[i][j][k]))
					line([neural_pos[i][k], neural_pos[i+1][j]],lineColor, thikness)

		

		## drawing neurons
		
		for i in range(len(snake.brain.layers)):
			#print(len(snake.brain.layers[i]))
			#print(len(neural_pos[i]))
			for j in range(len(snake.brain.layers[i])):
				circle(neural_pos[i][j], calc_neuron_color(snake.brain.layers[i][j]))



def calc_fitness_array(snakes):
	fitnessArray = []
	for i,s in enumerate(snakes):
		if i == 0:
			fitnessArray.append(s.fitness)
		else:
			fitnessArray.append(s.fitness + fitnessArray[-1])
	return fitnessArray


def generate_new_snakes(numOfSnakesToRepreduce, snakes, fitnessArray):
	newSnakes = []
	maxFit = int(fitnessArray[-1])+1
	N = len(snakes)
	for i in range(numOfSnakesToRepreduce):
		r = random.randrange(maxFit)
		for j in range(N):
			if r < fitnessArray[j]:
				break
		s = snake(snakes[j])
		# s.brain.imitate(initialImitateRate)
		newSnakes.append(s)
	for j in range(hugeImitationNum):
		i = random.randrange(numOfSnakesToRepreduce)
		newSnakes[i].brain.imitate(hugeImitationRate)
		newSnakes[i].color=np.array([random.randrange(256),random.randrange(256),random.randrange(256)])
		newSnakes[i].rootID = snakeRootID
		newSnakes[i].get_name()
		if newSnakes[i].color[1]>mapBackgroundColor[1]-10 and newSnakes[i].color[1]<mapBackgroundColor[1]+10 and newSnakes[i].color[2]>mapBackgroundColor[2]-10 and newSnakes[i].color[2]<mapBackgroundColor[2]+10:
			newSnakes[i].color=np.array([random.randrange(256),random.randrange(256),random.randrange(256)])
		globals()["snakeRootID"]+=1
	return newSnakes


def imitate_generation(snakes):
	snakes= sorted(snakes, key=lambda x:x.fitnessSum, reverse=True)
	globals()["bestFitnessLastGen"] = snakes[0].fitnessSum
	if snakes[0].fitnessSum	> globals()["bestFitness"]:
		globals()["bestFitness"] = snakes[0].fitnessSum
	np.save("./TestGens/{}/Gen-{}-Name-{}-BestScore-{}.npy".format(startTime,genNum-1,snakes[0].name,snakes[0].bestScore),snakes[0].brain.connections)
	numOfSnakesToKeep = int(genKeepRate*len(snakes))
	numOfSnakesToRepreduce = len(snakes) - numOfSnakesToKeep
	snakes = snakes[:numOfSnakesToKeep]
	fitnessArray=calc_fitness_array(snakes)
	newSnakes = generate_new_snakes(numOfSnakesToRepreduce, snakes, fitnessArray)
	snakes = snakes+newSnakes
	return snakes

####
# No need for this if you are using control panel class
####
def calc_neural_network_pos():
	for i in range(len(initialBrainLyers)):
		newA = []
		if i > 0:
			x = playingWinPos 
		else:
			x = 2*playingWinPos
		for j in range(initialBrainLyers[i]+1):
			newA.append([playingWinWidth + 9*playingWinPos + 3*playingWinPos*i, int(2.5*playingWinPos) + x*j])
		neural_pos.append(newA)
	neural_pos[-1]=neural_pos[-1][:-1]


def calc_neuron_color(num):
	if num < -1:
		num = -1

	if num>1:
		num =1
	if num > 0:
		return(int(num*55),int(num*255),int(num*55))
	else:
		num = -1*num
		return(int(num*255),int(num*55),int(num*55))

def calc_connection_color(num):
	if num < 0:
		num=min(-1*num,1)
		return(20+int(num*235),0,0)
	if num == 0:
		return(10,10,10)
	elif num>1:
		num =1
	return(0,20+int(num*235),0)
	


def init_display():
	gameDisplay.fill(controlColor)
	rect([playingWinPos-wallThikness,playingWinPos-wallThikness,playingWinWidth+2*wallThikness,playingWinHieght+2*wallThikness],wallColor)
	rect([playingWinPos,playingWinPos,playingWinWidth,playingWinHieght],mapBackgroundColor)

def rect(rList, color=red, width=0, surface=gameDisplay):
	pygame.draw.rect(surface, color, rList, width)

def circle(center, color=red, R = 6, width=0, surface=gameDisplay):
	pygame.draw.circle(surface, color, center, R, width)

def line(Points, color=red, thikness = 1 , surface=gameDisplay):
	pygame.draw.line(surface, color, [Points[0][0]+3,Points[0][1]], [Points[1][0]-3,Points[1][1]], thikness)





############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
snakes = []
for i in range(genSize):
	s = snake()
	snakes.append(s)
showMsgs = True
gamePause = False
gameExit = False

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################


def init_gen():
	globals()["numOfMoves"] = 0
	globals()["numOfDeadSnakes"] = 0
	globals()["bestScoreThisGen"] = 0
	globals()["idOfShownSnake"] = 0
	globals()["changeShowDir"] = 1
	for s in snakes:
		s.calc_fitness()
	globals()["snakes"] = imitate_generation(snakes)
	for s in snakes:
		s.reset_values()
	globals()["gameApples"] = []
	for i in range(maxApplesNum):
		globals()["gameApples"] .append(apple())



def event_handling():
	global gamePause
	global gameExit
	global s
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
		else:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					gamePause = not gamePause
				else:
					if event.key == pygame.K_UP:
						globals()["changeShowDir"] = 1
						globals()["idOfShownSnake"] +=1
						if globals()["idOfShownSnake"] >= genSize:
							globals()["idOfShownSnake"] = 0
					elif event.key == pygame.K_DOWN:
						globals()["changeShowDir"] = -1
						globals()["idOfShownSnake"] -=1
						if globals()["idOfShownSnake"] < 0:
							globals()["idOfShownSnake"] = genSize-1
					elif event.key == pygame.K_q:
						gameExit=True
					elif event.key == pygame.K_w:
						s.increase(growthRate)
					elif event.key == pygame.K_s:
						s.decrease(growthRate)
					elif event.key == pygame.K_p:
						gamePause = True
					elif event.key == pygame.K_t:
						print(s.calc_output())
					#elif event.key == pygame.K_c:
					#	showMsgs = not showMsgs
					elif event.key == pygame.K_n:
						globals()["numOfMoves"] = genTestSteps
					elif event.key == pygame.K_o:
						globals()["showOne"] = not globals()["showOne"] 


def game_update():
	# init_display()
	globals()["applesToshow"] = [0 for i in range(maxApplesNum)]
	for s in snakes:
		s.update()
	# if showOne:
	# 	if snakes[idOfShownSnake].alive:
	# 		snakes[idOfShownSnake].draw()
	# 	else:
	# 		while(numOfDeadSnakes<genSize and (not snakes[idOfShownSnake].alive)):
	# 			globals()["idOfShownSnake"] = (globals()["idOfShownSnake"] + changeShowDir)%genSize
	# 			if globals()["idOfShownSnake"] < 0:
	# 				globals()["idOfShownSnake"] = genSize-1
	# else:
	# 	for s in snakes:
	# 		s.draw()

	globals()["numOfMoves"] +=1
	if numOfMoves>genTestSteps:
		for s in snakes:
			if s.alive:
				s.self_kill("")
		globals()["numOfDeadSnakes"] = genSize
		
	# if showOne:
	# 	gameApples[snakes[idOfShownSnake].score].draw()
	# else:
	# 	for i in range(bestScore+1):
	# 		if applesToshow[i] >0:
	# 			gameApples[i].draw()
	# s = snakes[idOfShownSnake]
	# controlPanel.draw(s)
	# pygame.display.update()


def display_update():
	init_display()
	if showOne:
		if snakes[idOfShownSnake].alive:
			snakes[idOfShownSnake].draw()
		# else:
		# 	while(numOfDeadSnakes<genSize and (not snakes[idOfShownSnake].alive)):
		# 		globals()["idOfShownSnake"] = (globals()["idOfShownSnake"] + changeShowDir)%genSize
		# 		if globals()["idOfShownSnake"] < 0:
		# 			globals()["idOfShownSnake"] = genSize-1
	else:
		for s in snakes:
			s.draw()

			
	while(numOfDeadSnakes<genSize and (not snakes[idOfShownSnake].alive)):
		globals()["idOfShownSnake"] = (globals()["idOfShownSnake"] + changeShowDir)%genSize
		if globals()["idOfShownSnake"] < 0:
			globals()["idOfShownSnake"] = genSize-1
		
	if showOne:
		gameApples[snakes[idOfShownSnake].score].draw()
	else:
		for i in range(bestScore+1):
			if applesToshow[i] >0:
				gameApples[i].draw()
	s = snakes[idOfShownSnake]
	controlPanel.draw(s)
	pygame.display.update()



while not gameExit:
	
	event_handling()
	if not gamePause:
		game_update()
	display_update()

	clock.tick(FPS)
	if numOfDeadSnakes>genSize-1:
		genNum+=1
		init_gen()

pygame.quit()

quit()

