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
		self.color = darkGray
		self.edge = playingWinPos
		self.horizontalMargin = 75
		self.verticalMargin = 35
		

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
			message_to_screen_corner(("Born in Generation : " + str(snake.bornGen)),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 6*self.verticalMargin],white,25)
		else:
			message_to_screen_corner(("Showing Snake    : All"),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 2*self.verticalMargin],white,25)
			message_to_screen_corner(("Num                         : None"),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 3*self.verticalMargin],white,25)
			message_to_screen_corner(("Score                       : None"),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 4*self.verticalMargin],white,25)
			message_to_screen_corner(("GrandFather ID        : None"),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 5*self.verticalMargin],white,25)
			message_to_screen_corner(("Born in Generation : None"),[self.infoBlockPos[0] + self.width/2 +self.edge, self.infoBlockPos[1]+self.edge + 6*self.verticalMargin],white,25)


	def draw_brain(self,snake):
		pygame.draw.rect(self.display, self.color,(self.startPos[0], self.startPos[1], self.width, self.hieght))
		messages = []
		messages.append("U_W: " + str(snake.disToWallUp))
		messages.append("R_W: " + str(snake.disToWallDown))
		messages.append("D_W: " + str(snake.disToWallRight))
		messages.append("L_W: " + str(snake.disToWallLeft))

		messages.append("X_A: " + str(snake.disToAppleX))
		messages.append("Y_A: " + str(snake.disToAppleY))

		messages.append("U_C: " + str(snake.disToCellUp))
		messages.append("R_C: " + str(snake.disToCellDown))
		messages.append("D_C: " + str(snake.disToCellRight))
		messages.append("L_C: " + str(snake.disToCellLeft))
		messages.append("C__: 1")
		#message_to_screen_corner("U_W: " + str(round(snake.disToWallUp,2)), (playingWinWidth + 3*playingWinPos , 2*playingWinPos), white, 25)
		#message_to_screen_corner("R_W: " + str(round(snake.disToWallRight,2)), (playingWinWidth + 3*playingWinPos, 4*playingWinPos), white, 25)
		for i ,msg in enumerate(messages):
			message_to_screen_corner(msg,(self.startPos[0]+self.edge, self.startPos[1]+self.edge + i*self.verticalMargin),white, 20)
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
				circle(self.neural_pos[i][j], calc_neuron_color(snake.brain.layers[i][j]))

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
		self.Pos = [int(random.randrange(0, playingWinWidth- blockSize)/10)*10, int(random.randrange(0, playingWinHieght- blockSize)/10)*10]

	def draw(self):
		rect([playingWinPos+self.Pos[0], playingWinPos+ self.Pos[1], blockSize, blockSize], black)
		rect([playingWinPos+self.Pos[0]+1, playingWinPos+ self.Pos[1]+1, blockSize-2, blockSize-2], red)

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
			self.connections = np.array(self.connections)
			self.imitate()
		else:
			for i in range(len(self.layersNum) -1):
				self.connections.append([])
				for j in range(self.layersNum[i+1]):
					self.connections[i].append([])
					for k in range(self.layersNum[i]+1):
						self.connections[i][j].append(random.random()*2-1)
			self.connections = np.array(self.connections)


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
		newConnections = np.array(newConnections)
		return newConnections






class snake():
	#global numOfDeadSnakes
	global growthRate

	def __init__(self, snakeToCopy = None):	
		brainToCopy=[]
		self.numFitToCount = 5
		self.fitnessSum=0
		self.lastNfitToCount = []
		for i in range(self.numFitToCount):
			self.lastNfitToCount.append(0)

		if snakeToCopy:
			brainToCopy = snakeToCopy.brain.connections
			self.color=snakeToCopy.color
			self.rootID = snakeToCopy.rootID
			self.name = snakeToCopy.name
			self.change_name()
			r=random.randrange(3)
			if r ==3:
				for i in range(3):
					r1=random.randrange(21)-10
					r1=self.color[i] + r1
					r1 = max(0,r1)
					r1 = min(255,r1)
					self.color[i]=r1
					self.fitnessSum	 = snakeToCopy.fitnessSum
					self.lastNfitToCount = snakeToCopy.lastNfitToCount
		else:
			self.color = (random.randrange(256),random.randrange(256),random.randrange(256))
			self.rootID = snakeRootID
			globals()["snakeRootID"] +=1
			self.get_name()
			
		
		self.brain = brain(brainToCopy)	
		self.XSpeed = mainSpeed
		self.YSpeed = 0
		self.minLength = 1
		self.dir = [1, 0]
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
		self.canMove = True
		self.numOfMoves = 0
		self.fitness = 0
		self.posRepetitionNum = 0
		self.show = True
		self.updateEnabled = True
		self.alive = True
		self.movesWithoutApple = 0


	def calc_info(self):
		self.disToWallRight = (playingWinWidth - self.Pos[0] - blockSize)#/playingWinWidth
		self.disToWallLeft = self.Pos[0]#/playingWinWidth
		self.disToWallDown = (playingWinHieght - self.Pos[1] - blockSize)#/playingWinHieght
		self.disToWallUp = self.Pos[1]#/playingWinHieght

		self.disToAppleX = (gameApples[self.score].Pos[0] - self.Pos[0])#/playingWinWidth
		self.disToAppleY = (gameApples[self.score].Pos[1] - self.Pos[1])#/playingWinHieght

		self.disToCellUp = playingWinHieght
		self.disToCellDown = playingWinHieght
		self.disToCellLeft = playingWinWidth
		self.disToCellRight = playingWinWidth

		leadX = self.Pos[0]
		leadY = self.Pos[1]
		for cell in self.cells[:-1]:
			if cell[0] == leadX:
				#if cell[1] > leadY and ((cell[1] - leadY)/playingWinHieght < self.disToCellDown):
				if cell[1] > leadY and ((cell[1] - leadY) < self.disToCellDown):
					self.disToCellDown = (cell[1] - leadY)#/playingWinHieght
				#elif leadY > cell[1] and (leadY - cell[1])/playingWinHieght< self.disToCellUp:
				elif leadY > cell[1] and (leadY - cell[1]) < self.disToCellUp:
					self.disToCellUp = (leadY - cell[1])#/playingWinHieght
			if cell[1] == leadY:
				#if cell[0] > leadX and ((cell[0] - leadX)/playingWinWidth < self.disToCellRight):
				if cell[0] > leadX and ((cell[0] - leadX)< self.disToCellRight):
					self.disToCellRight = (cell[0] - leadX)#/playingWinWidth
				#elif leadX > cell[0] and (leadX - cell[0])'''/playingWinWidth''' < self.disToCellLeft:
				elif leadX > cell[0] and (leadX - cell[0])< self.disToCellLeft:
					self.disToCellLeft = (leadX - cell[0])#/playingWinWidth
	
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
		inputs.append(self.disToWallDown/playingWinHieght)	#	To scale the result to one and the input will be bigger when the snake is closer to the wall
		inputs.append(self.disToWallLeft/playingWinWidth)	#
		inputs.append(self.disToWallUp/playingWinHieght)	#
		inputs.append(self.disToWallRight/playingWinWidth)	#
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
		inputs.append((playingWinHieght-self.disToCellUp)/playingWinHieght)		#	To scale the result to one and the input will be bigger when the snake is closer to another cell
		inputs.append((playingWinWidth-self.disToCellRight)/playingWinWidth)	#
		inputs.append((playingWinHieght-self.disToCellDown)/playingWinHieght)	#
		inputs.append((playingWinWidth-self.disToCellLeft)/playingWinWidth)		#

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
			self.fitness = self.fitness/15
		elif self.deadReason == "self-Crush":
			self.fitness = self.fitness/15
		elif self.deadReason == "Position-Repeting":
			self.fitness = self.fitness/10
		elif self.deadReason == "No-Apple":
			self.fitness = self.fitness/2

		self.lastNfitToCount.append(self.fitness)
		self.lastNfitToCount = self.lastNfitToCount[1:]
		self.fitnessSum=0
		for i in range(self.numFitToCount):
			self.fitnessSum = self.fitnessSum + (i+1)*(i+1)*self.lastNfitToCount[i]
		self.fitnessSum = self.fitnessSum/((self.numFitToCount*(self.numFitToCount+1)*(2*self.numFitToCount+1))/6)


	def update(self):
		if not self.updateEnabled:
			return
		self.Pos = [self.Pos[0] + self.XSpeed, self.Pos[1]+self.YSpeed]
		self.cells.append(self.Pos)
		self.cells = self.cells[max(0,len(self.cells)-self.length):]
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





	def draw(self):
		if not self.show or not self.alive:
			return
		for c in self.cells:
			rect([playingWinPos+c[0], playingWinPos+ c[1], blockSize, blockSize], black)
			rect([playingWinPos+c[0]+1, playingWinPos+ c[1]+1, blockSize-2, blockSize-2], self.color)

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

		if not self.canMove:
			return
		while(not moved):
			if idx==0 and not self.YSpeed == mainSpeed:
				self.XSpeed = 0
				self.YSpeed = -mainSpeed
				moved = True
			elif idx==2 and not self.YSpeed == -mainSpeed:
				self.XSpeed = 0
				self.YSpeed = mainSpeed
				moved = True
			elif idx==1 and not self.XSpeed == -mainSpeed:
				self.YSpeed = 0
				self.XSpeed = mainSpeed
				moved = True
			elif idx==3 and not self.XSpeed == mainSpeed:
				self.YSpeed = 0
				self.XSpeed = -mainSpeed
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
					#	print(lineColor)
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
		newSnakes.append(s)
	for j in range(hugeImitationNum):
		i = random.randrange(numOfSnakesToRepreduce)
		newSnakes[i].brain.imitate(hugeImitationRate)
		newSnakes[i].color=(random.randrange(256),random.randrange(256),random.randrange(256))
		newSnakes[i].rootID = snakeRootID
		newSnakes[i].get_name()
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
		return(int(num*55),int(num*55),int(num*255))
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
	rect([playingWinPos,playingWinPos,playingWinWidth,playingWinHieght],white)

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
	init_display()
	globals()["applesToshow"] = [0 for i in range(maxApplesNum)]
	for s in snakes:
		s.update()
	if showOne:
		if snakes[idOfShownSnake].alive:
			snakes[idOfShownSnake].draw()
		else:
			while(numOfDeadSnakes<genSize and (not snakes[idOfShownSnake].alive)):
				globals()["idOfShownSnake"] = (globals()["idOfShownSnake"] + changeShowDir)%genSize
				if globals()["idOfShownSnake"] < 0:
					globals()["idOfShownSnake"] = genSize-1
	else:
		for s in snakes:
			s.draw()

	globals()["numOfMoves"] +=1
	if numOfMoves>genTestSteps:
		for s in snakes:
			if s.alive:
				s.self_kill("")
		globals()["numOfDeadSnakes"] = genSize
		
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

	clock.tick(FPS)
	if numOfDeadSnakes>genSize-1:
		genNum+=1
		init_gen()

pygame.quit()

quit()

