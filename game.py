from pygame import *
from random import *
import os

init()

#~---------------------------Initial Variables---------------------------~

gMap = [[None, None, None, None, None, None],[None, "start", "forest", "forest", "forest", None],[None, "forest", "forest", "cave", "cave", None],[None, None, "cave", "cave", "bad", None],[None, "bad", "bad", "end", "bad", None],[None, None, None, None, None, None]]
obstacleList = [[None, None, None, None, None, None],[None, None, None, None, None, None],[None, None, None, None, None, None],[None, None, None, None, None, None],[None, None, None, None, None, None],[None, None, None, None, None, None]]
mapx = 1
mapy = 1
width = 800
height = 600
running = True

#~---------------------------Pygame Setup---------------------------~

backdrop = display.set_mode((width,height))
display.set_caption("COOL and EPUC game")
os.chdir("./assets")
display.set_icon(image.load("drgn.png"))
clock = time.Clock()

#~---------------------------Screens---------------------------~

#Super class for all screens to inherit from
class Screen():
	global mapx, mapy, gMap, PC, CP, obstacleList						#Global variables that are needed both inside and outside the classes
	
	def __init__(self, pbg):
		self.listOfButtons = []											#Attribute to contain any buttons on the screen
		self.state = self				
		self.bg = image.load(pbg).convert()								#Attribute used to switch screens
		self.bg = transform.scale(self.bg, (800,600))
	
	#Method for handling mouse input across screens
	def mouseInput(self,pos):
		for b in self.listOfButtons:
			b.checkClick(pos)
		return self.state
		
	#Method for drawing a screen
	def draw(self,pScreen):
		pScreen.blit(self.bg, (0,0))
		for b in self.listOfButtons:
			b.draw(pScreen)

	#Empty methods to be overridden
	def keyEvent(self):
		pass
	
	def collide(self):
		pass
	
	def cTurn(self):
		pass
	
	#Method that always returns to the main menu
	def backScreen(self):
		self.state = MenuScreen()
	
	#Method that switches the screen to the current map screen
	def playGame(self):
		self.state = GameScreen(gMap[mapx][mapy],0,False)
		
	def exitGame(self):
		self.state = None
	
	def placeObstacles(self):
		tempList = []
		y = 1
		while y < 6:
			x = 1
			while x < 6:
				if gMap[y][x] != None:
					potentialCoords = [(505,90),(370,225),(150,350),(100,200),(260,100),(510,350)]
					numbofobs = randint(3,5)
					n = 0
					while n < numbofobs:
						coords = potentialCoords[randint(0,(5-n))]
						potentialCoords.remove(coords)
						obs = Obstacle(0,0,170,90,"rok.png")
						typeob = randint(0,2)
						if gMap[y][x] == "forest" or gMap[y][x] == "start":
							if typeob == 0:
								obs = Obstacle(0,0,170,90,"rok.png")
							elif typeob == 1:
								obs = Obstacle(0,0,100,100,"bsh.png")
							else:
								obs = Obstacle(0,0,120,90,"logg.png")
						elif gMap[y][x] == "cave":
							if typeob == 0:
								obs = Obstacle(0,0,70,140,"stalagmite.png")
							elif typeob == 1:
								obs = Obstacle(0,0,100,100,"cob.png")
							else:
								obs = Obstacle(0,0,70,70,"hol.png")
						elif gMap[y][x] == "bad":
							if typeob == 0:
								obs = Obstacle(0,0,70,140,"stalagmite.png")
							elif typeob == 1:
								obs = Obstacle(0,0,100,100,"cob.png")
							else:
								obs = Obstacle(0,0,70,70,"hol.png")
						obs.giveCoords(coords)
						tempList.append(obs)
						n += 1
					obstacleList[y][x] = tempList
					tempList = []
				x += 1
			y += 1
		
	#Method to set up all of the game screens
	def startGame(self):
		global mapx, mapy, CP
		mapx = 1
		mapy = 1
		PC.x = 100
		PC.y = 100
		CP = CombatPlayer()
		self.placeObstacles()
	
	def startAgain(self):
		self.startGame()
		self.playGame()

#Class for menu screen
class MenuScreen(Screen):
	def __init__(self):
		super().__init__("IMG_0270.png")
		exitButton = Button(20,20,100,50," Exit",[180,40,40],"georgia",40,(255,240,240))
		exitButton.setTask(self.exitGame)
		self.listOfButtons.append(exitButton)
		playButton = Button(280,170,240,70," Play Game",[180,100,40],"georgia",45,(255,250,240))
		playButton.setTask(self.playGame)
		self.listOfButtons.append(playButton)
		resetButton = Button(300,270,200,55," Start Again",[180,100,40],"georgia",35,(255,250,240))
		resetButton.setTask(self.startAgain)
		self.listOfButtons.append(resetButton)
		mixer.music.load("Butterfly Effect.mp3")
		mixer.music.play(-1, 16)
		
	#Method for handling key input, calls mouse input method
	def keyEvent(self):
		for e in event.get(): 	
			if e.type == QUIT: 
				self.state = None  
			elif e.type == MOUSEBUTTONDOWN:
				self.state = self.mouseInput(e.pos)
			elif e.type == KEYDOWN:
				if e.key == K_ESCAPE:
					self.state = None
	
#Class for game screens
class GameScreen(Screen):
	def __init__(self,areaType,tTrack,startMusic):
		self.areaType = areaType										#Attribute that defines the type of the room
		if self.areaType == "forest" or self.areaType == "start":
			pbg = "foresbg.png"
		elif self.areaType == "cave":
			pbg = "cavebg.png"
		elif self.areaType == "bad":
			pbg = "badbg.png"
		elif self.areaType == "end":
			pbg = "badbg.png"
		super().__init__(pbg)
		menuButton = Button(20,20,120,50," Menu",[100,150,200],"georgia",40,(240,250,255))
		menuButton.setTask(self.backScreen)
		self.listOfButtons.append(menuButton)
		self.timeTrack = tTrack
		self.listOfObstacles = obstacleList[mapy][mapx]					#Attribute for any obstacles on the screen
		if startMusic == True:
			mixer.music.load("Butterfly Effect.mp3")
			mixer.music.play(-1, 16)

	
	#Method to draw game screen, adds relevant background
	def draw(self,pScreen):
		pScreen.blit(self.bg, (0,0))
		PC.draw(pScreen)
		for o in self.listOfObstacles:
			o.draw(pScreen)
		for b in self.listOfButtons:
			b.draw(pScreen)
	
	def combatEncounter(self):
		if self.areaType == "forest":
			p = 600
		elif self.areaType == "start":
			p = 0
		elif self.areaType == "cave":
			p = 450
		elif self.areaType == "bad":
			p = 300
		if self.areaType == "end":
			if time.get_ticks() > self.timeTrack + 3000:
				self.state = CombatScreen(self.areaType)
		else:
			x = randint(0,p)
			if x == 69 and time.get_ticks() > self.timeTrack + 3000:
				PC.stop()
				self.state = CombatScreen(self.areaType)
	
	#Method for key input, calls the player character's key input method
	def keyEvent(self):
		self.combatEncounter()
		for e in event.get(): 
			if e.type == QUIT: 
				self.state = None  
			elif e.type == MOUSEBUTTONDOWN:
				self.state = self.mouseInput(e.pos)
			elif e.type == KEYDOWN:
				if e.key == K_ESCAPE:
					self.backScreen()
			PC.keyInput(e)
		PC.update()
	
	#Method to handle player collision with on-screen obstacles
	def collide(self):
		global mapx, mapy
		i = 0
		while i < len(self.listOfObstacles):
			if self.listOfObstacles[i].colliderect(PC):
				PC.stop()
			i += 1
		if PC.x <= 0:
			if gMap[mapy][mapx-1] == None:
				PC.stop()
			else:
				mapx -= 1
				self.state = GameScreen(gMap[mapy][mapx],time.get_ticks()-2500,False)
				PC.x = 715
		elif PC.x >= 720:
			if gMap[mapy][mapx+1] == None:
				PC.stop()
			else:
				mapx += 1
				self.state = GameScreen(gMap[mapy][mapx],time.get_ticks()-2500,False)
				PC.x = 5
		if PC.y <= 0:
			if gMap[mapy-1][mapx] == None:
				PC.stop()
			else:
				mapy -= 1
				self.state = GameScreen(gMap[mapy][mapx],time.get_ticks()-2500,False)
				PC.y = 515
		elif PC.y >= 520:
			if gMap[mapy+1][mapx] == None:
				PC.stop()
			else:
				mapy += 1
				self.state = GameScreen(gMap[mapy][mapx],time.get_ticks()-2500,False)
				PC.y = 5

#Class for combat screens
class CombatScreen(Screen):
	def __init__(self,aType):
		super().__init__("Picture1.png")
		attackButton = Button(20,410,150,60," Attack",[75,130,200],"georgia",40,(255,240,240))
		attackButton.setTask(self.playAttack)
		self.listOfButtons.append(attackButton)
		defendButton = Button(20,500,150,60," Defend",[75,130,200],"georgia",40,(255,250,240))
		defendButton.setTask(self.playDefend)
		self.listOfButtons.append(defendButton)
		fleeButton = Button(630,500,150,60," Flee",[180,40,40],"georgia",40,(255,250,240))
		fleeButton.setTask(self.playFlee)
		self.listOfButtons.append(fleeButton)
		abButton = Button(630,410,150,60," Ability",[230,165,45],"georgia",40,(255,250,240))
		abButton.setTask(self.playAbility)
		self.listOfButtons.append(abButton)
		self.displayText = ""											#Text to be displayed
		self.enemyList = []												#List to store enemies
		self.track = "Capturism.mp3"
		self.addEnemies(aType)											#Calls method to add enemies
		self.arrow = Obstacle(510,self.enemyList[0].y + 10,50,50,"arrow.png")	#Arrow to indicate selected enemy
		self.turn = 0													#Attribute to track whose turn it is
		self.lastabturn = 0												#Attribute to track the last turn the player used their ability
		self.l = 0														#Integer variable of the targeted enemy
		self.timeTrack = 0												#Stores the time that the display text last changed
		self.enmyact = 0												#Stores which enemy is acting
		self.XPgain = 0													#Stores the XP gained during the combat
		CP.currentHealth = CP.health									#Resets player's health
		CP.hbar.change(CP.currentHealth,CP.health)
		mixer.music.load(self.track)
		mixer.music.play(-1, 0)
		
	def keyEvent(self):
		for e in event.get():
			if self.turn % 2 == 0:
				if e.type == KEYDOWN:
					if e.key == K_DOWN:									#Allows the arrow keys to control which enemy is selected, resets to the 1st/last value if the player exceeds the enemyList's bounds
						if self.l >= (len(self.enemyList) - 1):
							self.l = 0
						else:
							self.l += 1
					elif e.key == K_UP:
						if self.l <= 0:
							self.l = len(self.enemyList) - 1
						else:
							self.l -= 1
					self.arrow.giveCoords((510,self.enemyList[self.l].y + 10))		#Makes the arrow follow the player's selection
				if e.type == MOUSEBUTTONDOWN:
					self.state = self.mouseInput(e.pos)
	
	def cTurn(self):													#Method for the enemy turn
		if self.turn % 2 == 1:											#Checks if it is the enemy turn
			for e in self.enemyList:									#Loop to remove any enemies that have died
				if e.alive == False:
					if e.name == "WALRUS":								#If the enemy was the final boss, it will go to the end game screen
						self.state = EndCombatScreen("wong",self.XPgain)
					else:
						self.enemyList.remove(e)
						self.XPgain += 3
						if len(self.enemyList) >= 1:					#Resets the arrow coordinates
							self.l = 0
							self.arrow.giveCoords((510,self.enemyList[self.l].y + 10))
		if len(self.enemyList) == 0:									#Checks if the list of enemies is empty, if so goes to the end combat screen
			while time.get_ticks() < self.timeTrack + 700:
				pass
			self.state = EndCombatScreen("won",self.XPgain)
		elif CP.alive == False:											#Checks if the player has died or fled from combat - if dead, goes to lost game screen. If fled, goes to fled combat screen.
			if CP.currentHealth <= 0:
				while time.get_ticks() < self.timeTrack + 700:
					pass
				self.state = EndCombatScreen("died",self.XPgain)
			else:
				while time.get_ticks() < self.timeTrack + 700:
					pass
				CP.alive = True
				self.state = EndCombatScreen("fled",self.XPgain)
		else:
			if self.enmyact >= len(self.enemyList):						#If the acting enemy is beyond the list length, the value is reset and the turn incremented
				self.timeTrack = time.get_ticks()
				self.enmyact = 0
				self.turn += 1
			else:
				if time.get_ticks() > self.timeTrack + 1500:
					if self.turn % 2 == 1:								#If it's the enemy turn, the current enemy takes its action and enmyact is incremented
						self.displayText = self.enemyList[self.enmyact].action(CP)
						self.timeTrack = time.get_ticks()
						self.enmyact += 1

	#Method to add enemies
	def addEnemies(self,foeType):
		ycoords = 20													#Value to store the y coordinates for each enemy
		enmy = None														#Temporary object
		Rat = Combatant(100,50,10,5,2,"Rat","rat.png")
		Tree = Combatant(60,100,10,5,2,"Tree","tree.png")
		Wolf = Combatant(100,80,10,5,2,"Wolf","wolf.png")
		Spider = Combatant(100,80,8,10,2,"Spider","spoder.png")
		Skeleton = Combatant(60,110,14,8,5,"Skeleton","skele.png")
		Wyrm = Combatant(100,100,10,12,2,"Wyrm","wrrm.png")
		Dragon = Combatant(100,110,20,15,5,"Dragon","daga.png")
		Lava = Combatant(120,60,15,12,5,"Lava","lavsala.png")
		Goblin = Combatant(50,100,10,10,2,"Goblin","gobly.png")
		WALRUS = Walrus()
		leastAmount = 0													#Variables to store the least and most number of enemies a combat can have
		maxAmount = 0
		if foeType == "forest":
			possFoes = [Rat,Tree,Wolf]
			leastAmount = 1
			maxAmount = 2
		elif foeType == "cave":
			possFoes = [Spider,Wyrm,Skeleton]
			leastAmount = 1
			maxAmount = 3
			self.XPgain = 5
		elif foeType == "bad":
			possFoes = [Dragon,Lava,Goblin]
			leastAmount = 2
			maxAmount = 3
			self.XPgain = 10
		elif foeType == "end":
			self.track = "RISING.mp3"
			self.enemyList.append(WALRUS)
			amount = 0
			self.XPgain = 30
		elif foeType == "start":
			possFoes = [Rat]
			leastAmount = 1
			maxAmount = 1
		amount = randint(leastAmount,maxAmount)							#Variable to store the number of enemies in that combat
		while amount > 0:
			x = randint(0,len(possFoes)-1)								#Variable to pick a random type of enemy from the list of possible enemies
			enmy = possFoes[x].again()									#Creates a copy of the enemy type and gives it the y coordinates, then increments the y coordinates by 120
			enmy.giveCoords(ycoords)
			ycoords += 120
			self.enemyList.append(enmy)									#Adds the enemy to the enemy list
			amount -= 1
	
	def draw(self,pScreen):
		pScreen.blit(self.bg, (0,0))
		draw.rect(pScreen,(100,150,200),(10,380,780,210))
		self.arrow.draw(pScreen)
		for b in self.listOfButtons:
			b.draw(pScreen)
		for e in self.enemyList:
			e.draw(pScreen)
		fnot = font.SysFont("georgia",25)
		fond = font.SysFont("georgia",30)
		if len(self.displayText) > 40:									#If the display text is longer than 40 characters, it will split into 2 and display one below the other
			longtxt = fnot.render(self.displayText[40:len(self.displayText)], False, (255,255,255))
			shortxt = fnot.render(self.displayText[0:40], False, (255,255,255))
			pScreen.blit(shortxt,(190,400))
			pScreen.blit(longtxt,(190,430))
		else:
			txt = fnot.render(self.displayText, False, (255,255,255))
			pScreen.blit(txt,(190,400))
		turnxt = fond.render("Turn count: " + str(self.turn), False, (255,255,255))
		if time.get_ticks() > self.timeTrack + 1000:
			if self.turn % 2 == 0:
				self.displayText = "Your turn!"
				self.timeTrack = time.get_ticks()
		pScreen.blit(turnxt,(10,10))
		CP.draw(pScreen)
		
	#Button methods for each player action
	def playAttack(self):
		self.displayText = CP.attack(self.enemyList[self.l])
		self.timeTrack = time.get_ticks()
		self.turn += 1
		
	def playDefend(self):
		self.displayText = CP.defend()
		self.timeTrack = time.get_ticks()
		self.turn += 1
			
	def playFlee(self):
		self.displayText = CP.flee()
		self.timeTrack = time.get_ticks()
		self.turn += 1
			
	def playAbility(self):
		if ((self.turn - self.lastabturn) / 2) > 2:						#If at least 2 turns have passed since the ability was last used, lastabturn is set to the current turn and the player uses their ability
			self.displayText = CP.ability(self.enemyList)
			self.timeTrack = time.get_ticks()
			self.lastabturn = self.turn
			self.turn += 1
		else:															#Otherwise, text is displayed showing how many turns are left until the ability may be used
			self.displayText = "Ability on cooldown! Wait " + str(3 - int((self.turn-self.lastabturn)/2)) + " more turns."
			self.timeTrack = time.get_ticks()

#Class for end combat/game screens	
class EndCombatScreen(Screen):										
	def __init__(self,pWon,pxp):
		super().__init__("Picture1.png")
		mixer.music.stop()
		self.displayText = ""
		menuButton = Button(20,20,120,50," Menu",[100,150,200],"georgia",40,(240,250,255))
		menuButton.setTask(self.backScreen)
		contButton = Button(275,270,250,70," Continue",[100,150,200],"georgia",40,(255,255,255))
		contButton.setTask(self.contGame)
		resetButton = Button(275,270,250,70," Start Again",[100,150,200],"georgia",40,(255,250,240))
		resetButton.setTask(self.startAgain)
		exitButton = Button(20,20,100,50," Exit",[180,40,40],"georgia",40,(255,240,240))
		exitButton.setTask(self.exitGame)
		if pWon == "won" or pWon == "fled":								#Series of decisions which affect the displayed text, buttons and score of the player based on the outcome of their combat
			if CP.levelUp(pxp) == True:
				self.displayText = "Level up! you are now level " + str(CP.level) + "!"
			else:
				self.displayText = "You gained " + str(pxp) + " XP. You need " + str((CP.level * 10) - CP.XP) + " more to level up."
			if pWon == "fled":
				self.displayText = "Coward. No XP for u."
				CP.score -= 3
				if CP.score <= 0:
					CP.score = 0
			else:
				CP.score += 5
			self.listOfButtons.append(contButton)
			self.listOfButtons.append(menuButton)
		else:
			self.listOfButtons.append(resetButton)
			self.listOfButtons.append(exitButton)
			if pWon == "wong":
				CP.score += 10
				self.displayText = "You won da game so cool wow. your score was " + str(CP.score)
			else:
				self.displayText = "You lose! Your score was " + str(CP.score)
			
	
	def keyEvent(self):
		for e in event.get(): 	
			if e.type == QUIT: 
				self.state = None  
			elif e.type == MOUSEBUTTONDOWN:
				self.state = self.mouseInput(e.pos)
			
	def draw(self,pScreen):
		pScreen.blit(self.bg, (0,0))
		for b in self.listOfButtons:
			b.draw(pScreen)
		fnot = font.SysFont("georgia",27)
		txt = fnot.render(self.displayText, False, (255,255,255))
		pScreen.blit(txt,(50,400))
	
	def contGame(self):
		self.state = GameScreen(gMap[mapy][mapx],time.get_ticks()-1000,True)
	
	def startAgain(self):
		self.startGame()
		self.state = GameScreen(gMap[mapy][mapx],0,True)

#~---------------------------Screen Things---------------------------~

#Class for buttons, inheriting from pygame rectangle
class Button(Rect):
	def __init__(self,x,y,w,h,text,colour,fontType,size,textColour):
		super().__init__(x,y,w,h)										#Sets up pygame rectangle
		self.colour = colour
		self.font = font.SysFont(fontType, size)
		self.text = text
		self.textColour = textColour
		
	#Method to draw the button
	def draw(self,pScreen):
		mx,my = mouse.get_pos()
		colour2 = (self.colour[0]+20, self.colour[1]+20, self.colour[2]+20)		#Sets up two colours that are similar to the given one
		colour3 = (self.colour[0]-35, self.colour[1]-35, self.colour[2]-35)
		if self.collidepoint((mx,my)):									#Changes the colour of the button if the mouse is hovering over it - helpful for the user
			draw.rect(pScreen,colour2,self)
		else:
			draw.rect(pScreen,tuple(self.colour),self) 
		draw.rect(pScreen,colour3,self,7)								#Adds a border to the button
		textImage = self.font.render(self.text, True, self.textColour)
		pScreen.blit(textImage,self)
	
	def setTask(self,task):												#Allows a function to be given to the button
		self.task = task
	
	def checkClick(self, pos):											#Checks whether the mouse is over the button or not
		if self.collidepoint(pos):
			self.task()

#Class for obstacles that are added to game screens inheriting from pygame rectangle
class Obstacle(Rect):
	def __init__(self,x,y,w,h,pimage):
		super().__init__(x,y,w,h)
		self.image = image.load(pimage)
		self.image = transform.scale(self.image, (self.w,self.h))
	
	def draw(self,pScreen):												#Method to draw obstacle
		pScreen.blit(self.image,self)
	
	def giveCoords(self,cods):
		self.x, self.y = cods
		
#Class for the health bars
class HealthBar(Button):
	def __init__(self,text,maxWidth):
		super().__init__(0,0,maxWidth,32,text,[60,200,70],"georgia",30,(255,255,255))
		self.mwidth = maxWidth
		
	def draw(self,pScreen):
		draw.rect(pScreen,tuple(self.colour),self)
		textImage = self.font.render(self.text, True, self.textColour)
		pScreen.blit(textImage,self)
		draw.rect(pScreen,(200,40,30),(self.x+self.width,self.y,self.mwidth-self.width,32),False)	#Draws a red rectangle indicating damage
		draw.rect(pScreen,(10,20,60),(self.x,self.y,self.mwidth,32),3)	#Draws a green rectangle beneath
	
	def change(self,h,maxh):
		self.width = self.mwidth * (h/maxh)								#Changes the width of the red rectangle to be proportional to damage taken
		self.text = str(h)
	
	def giveCoords(self,cods):
		self.x,self.y = cods
	
	def task(self):
		pass
		
#~---------------------------Players---------------------------~

#Super class for any 'player' or similar sprite inheriting form pygame rectangle
class Player(Rect):																
	def __init__(self, x, y, w, h, pimage, name):
		super().__init__(x, y, w, h)
		self.image = pimage
		if isinstance(pimage, str):
			self.image = image.load(self.image)
		self.name = name
		self.dx = 0
		self.dy = 0
		
	#Method to update the sprite's position
	def update(self):
		self.move_ip(self.dx, self.dy)
		
	def draw(self, pScreen):
		pScreen.blit(self.image, (self.x, self.y))
	
	def keyInput(self):
		pass
	
	def stop(self):
		if self.dx > 0:
			self.x -= 6
			self.dx = 0
		elif self.dx < 0:
			self.x += 6
			self.dx = 0
		if self.dy > 0:
			self.y -= 6
			self.dy = 0
		elif self.dy < 0:
			self.y += 6
			self.dy = 0

#Class for the player character inheriting from Player
class PlayerCharacter(Player):
	def __init__(self):
		super().__init__(100, 100, 80, 80, "playerImage.png", "Bob")
		self.image = transform.scale(self.image, (80,80))
		
	#Method that takes in 'event' parameter and changes the character's movement based on key input
	def keyInput(self, e):
		if e.type == KEYDOWN:
			if e.key == K_RIGHT or e.key == ord("d"):
				self.dx = 6
			elif e.key == K_LEFT or e.key == ord("a"):
				self.dx = -6
			elif e.key == K_UP or e.key == ord("w"):
				self.dy = -6
			elif e.key == K_DOWN or e.key == ord("s"):
				self.dy = 6
			
		if e.type == KEYUP:
			if e.key == K_RIGHT or e.key == K_LEFT or e.key == ord("a") or e.key == ord("d"):
				self.dx = 0
			elif e.key == K_UP or e.key == K_DOWN or e.key == ord("w") or e.key == ord("s"):
				self.dy = 0

class Combatant(Player):
	def __init__(self, w, h, pHp, pAtk, pDef, pname, pimage):
		super().__init__(600, 0, w, h, pimage, pname)
		self.image = transform.scale(self.image, (self.w,self.h))
		self.health = pHp
		self.strength = pAtk
		self.defense = pDef
		self.currentDef = 0
		self.currentHealth = self.health
		self.alive = True
		self.num = 0
		self.hbar = HealthBar(str(self.currentHealth),self.health * 10)	#Creates a health bar for the object
		
	def giveCoords(self,cods):
		self.y = cods
		self.hbar.giveCoords((self.x - 30,self.y + self.height))
		
	def draw(self,pScreen):
		self.hbar.change(self.currentHealth,self.health)
		self.hbar.draw(pScreen)
		pScreen.blit(self.image,(self.x,self.y))
		
	def attack(self,target):
		self.currentDef = 0
		dmg = self.strength
		if target.currentDef > 0:
			num = randint(0,4)
			if num == 0:
				self.currentHealth = self.currentHealth - target.strength
				displayText = "Parried! " + self.name + " took " + str(target.strength) + " damage!"
				if self.currentHealth <= 0:
					self.alive = False
					displayText = "Parried! " + self.name + " took " + str(target.strength) + " damage and was   killed by " + target.name + "!"
				return displayText
			else:
				dmg -= target.currentDef
		else:
			dmg -= target.defense
		if dmg <= 0:
			dmg = 0
			displayText = self.name + " tried to attack but " + target.name + "'s defense is too high! 0 damage dealt."
		else:
			displayText = self.name + " hit " + target.name + " for " + str(dmg) + " damage!"
		target.currentHealth -= dmg
		if target.currentHealth <= 0:
			target.alive = False
			displayText = self.name +  " hit " + target.name + " for " + str(dmg) + " damage and killed   " + target.name + "!"
		return displayText
		
	def defend(self):
		self.currentDef = self.defense * 2
		if self.currentHealth < self.health:
			self.currentHealth += 1
		displayText = self.name + " is defending. Defense is now: " + str(self.currentDef)
		return displayText
		
	def flee(self):
		displayText = self.name + " fled the fight!"
		self.alive = False
		return displayText
		
	def action(self,target):
		p = 1
		if self.currentHealth < (self.health*0.2):
			p = 2
		num = randint(0,p)
		if num == 0:
			return self.attack(target)
		elif num == 1:
			return self.defend()
		else:
			return self.flee()
		
	def again(self):
		self.num += 1
		return Combatant(self.w, self.h, self.health, self.strength, self.defense, self.name + " " + str(self.num), self.image)
		
class CombatPlayer(Combatant):
	def __init__(self):
		super().__init__(120, 120, 10, 5, 3, "Bob", "playerImage.png")
		self.x = 30
		self.y = 100
		self.XP = 0
		self.level = 1
		self.score = 0
		self.hbar.giveCoords((self.x - 10, self.y + 130))
		
	#Method to level up the player with a gained XP parameter, updates their stats and returns true/false depending on whether they levelled up or not
	def levelUp(self,XPgain):
		self.XP += XPgain
		if self.XP >= self.level * 10:
			self.level += 1
			self.health += 5
			self.strength += 2
			self.defense += 1
			self.XP -= self.level * 10
			self.score += 10
			return True
		else:
			return False
	
	#Method for the player's ability, damages all enemies and reports any killed enemies
	def ability(self,targets):
		displayText = self.name + " used their ability! All enemies took " + str(self.strength // 2) + " damage!"
		aDead = False
		for t in targets:
			t.currentHealth -= (self.strength // 2)
			if t.currentHealth <= 0:
				if aDead == True:
					displayText = displayText + " and " + t.name
				else:
					displayText = self.name + " used their ability and killed " + t.name
				t.alive = False
				aDead = True
		return displayText
			
#Class for the final boss
class Walrus(Combatant):
	def __init__(self):
		super().__init__(300,180,20,5,2,"WALRUS","WALRUS.png")
		self.x = 300
		self.y = 100
		self.hbar.giveCoords((self.x - 10,self.y + 200))
		
	#Overrided methods from Combatant class which are stronger versions of the methods
	def defend(self):
		self.currentHealth += 3
		if self.currentHealth > self.health:
			self.currentHealth = self.health
		self.currentDef = 2 * self.defense
		displayText = self.name + " is defending. Defense is now: " + str(self.currentDef)
		return displayText
	
	def attack(self,target):
		self.currentDef = 0
		dmg = self.strength
		if target.currentDef > 0:
			num = randint(0,6)
			if num == 0:
				self.currentHealth = self.currentHealth - target.strength
				displayText = "Parried! " + self.name + " took " + str(target.strength) + " damage!"
				if self.currentHealth <= 0:
					self.alive = False
					displayText = "Parried! " + self.name + " took " + str(target.strength) + " damage and was   killed by " + target.name + "!"
				return displayText
			else:
				dmg -= target.currentDef // 2
		else:
			dmg -= target.defense // 2
		if dmg <= 0:
			dmg = 0
			displayText = self.name + " tried to attack but " + target.name + "'s defense is too high! 0 damage dealt."
		else:
			displayText = self.name + " smacked " + target.name + " for " + str(dmg) + " damage!"
		target.currentHealth -= dmg
		if target.currentHealth <= 0:
			target.alive = False
			displayText = self.name +  " smashed " + target.name + " for " + str(dmg) + " damage and killed   " + target.name + "! You die to the WALRUS."
		return displayText
	
	#Method for the walrus' ability, which restores it to full health
	def ability(self):
		self.currentHealth = self.health
		displayText = self.name + " used its ability and restored itself to full health! F%$*!"
		return displayText
		
	#Overriden method for action, has a relatively low chance of using its ability
	def action(self,target):
		p = 15
		num = randint(0,p)
		if num < 7:
			return self.attack(target)
		elif num > 7:
			return self.defend()
		else:
			return self.ability()

#~---------------------------Setup---------------------------~

currentScreen = MenuScreen()
PC = PlayerCharacter()
CP = CombatPlayer()
currentScreen.startGame()

#~----------------------------Game Loop---------------------------~

while running:
	
	currentScreen.collide()
	currentScreen.keyEvent()
	currentScreen.cTurn()
	
	if currentScreen.state == None:
		running = False
	else:
		currentScreen.draw(backdrop)
	currentScreen = currentScreen.state
	
	display.update()
	display.flip()
	
	clock.tick(60)
	
quit()
