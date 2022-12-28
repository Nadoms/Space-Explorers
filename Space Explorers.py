# Resolution: 1920x1080

from tkinter import *
from PIL import ImageTk, Image
from random import randrange, uniform
import math

'''
TO DO:
- Convert to PEP8
EXTRAS:
- Powerups
- Instructions
- Cool title
'''
# Spaceship class to move and orient the spaceship properly
class Spaceship:
	# Initialises the spaceship variables
	def __init__(self, tkImage, canvasImage):
		self.tkImage = tkImage
		self.canvasImage = canvasImage

	# Sets the corresponding movement boolean to true when a key is pressed
	def moving(self, event):
		global lefting
		global righting
		global upping
		global downing
		if gameRunning or canvas.itemcget(menuCanvas, "state") == "normal":
			if event.char == leftKey:
				lefting = True
				righting = False
			elif event.char == rightKey:
				righting = True
				lefting = False
			elif event.char == upKey:
				upping = True
				downing = False
			elif event.char == downKey:
				downing = True
				upping = False

	# Sets the corresponding movement boolean to false when a key is released
	def stopMoving(self, event):
		global lefting
		global righting
		global upping
		global downing
		if event.keysym == leftKey:
			lefting = False
		elif event.keysym == rightKey:
			righting = False
		elif event.keysym == upKey:
			upping = False
		elif event.keysym == downKey:
			downing = False

	# Moves spaceship when one or two of the directional booleans are true
	def shmooves(self, fire):
		direction = 0
		if fire == True:
			fire = False
		else:
			fire = True
		if upping and canvas.coords(spaceshipCanvas)[1] > 130:
			canvas.move(self.canvasImage, 0, -shmooveSpeed)
			direction = 1
		elif downing and 700 > canvas.coords(spaceshipCanvas)[1]:
			canvas.move(self.canvasImage, 0, shmooveSpeed/1.5)
			direction = 2
		if lefting and canvas.coords(spaceshipCanvas)[0] > 30:
			canvas.move(self.canvasImage, -(shmooveSpeed), 0)
			direction = 3
		elif righting and 670 > canvas.coords(spaceshipCanvas)[0]:
			canvas.move(self.canvasImage, shmooveSpeed, 0)
			direction = 4
		if not lefting and not righting and not upping and not downing:
			if 700 > canvas.coords(spaceshipCanvas)[1] \
			and canvas.itemcget(optionCanvas, "state") == "hidden" \
			and canvas.itemcget(pauseCanvas, "state") == "hidden" \
			and canvas.itemcget(countCanvas, "state") == "hidden" \
			and canvas.itemcget(bossCanvas, "state") == "hidden":
				canvas.move(self.canvasImage, 0, shmooveSpeed/4)
			direction = 5
		if direction:
			self.orient(direction, fire)
		window.after(10, self.shmooves, fire)

	# Selects the correct spaceship image based on direction
	def orient(self, direction, fire):
		if fire:
			if direction == 1:
				canvas.itemconfigure(spaceshipCanvas, image=spaceshipImg)
			elif direction == 2:
				canvas.itemconfigure(spaceshipCanvas, image=spaceshipImgOff)
			elif direction == 3:
				canvas.itemconfigure(spaceshipCanvas, image=spaceshipImgLeft)
			elif direction == 4:
				canvas.itemconfigure(spaceshipCanvas, image=spaceshipImgRight)
			elif direction == 5:
				canvas.itemconfigure(spaceshipCanvas, image=spaceshipImgOff)
		else:
			if direction == 1:
				canvas.itemconfigure(spaceshipCanvas, image=spaceshipImgOff)
			elif direction == 2:
				canvas.itemconfigure(spaceshipCanvas, image=spaceshipImgOff)
			elif direction == 3:
				canvas.itemconfigure(spaceshipCanvas, image=spaceshipImgLeftOff)
			elif direction == 4:
				canvas.itemconfigure(spaceshipCanvas, image=spaceshipImgRightOff)
			elif direction == 5:
				canvas.itemconfigure(spaceshipCanvas, image=spaceshipImgOff)

# Asteroid class to spawn, move and check collision for each asteroid
class Asteroid:
	# Initialising asteroid variable
	def __init__(self, size):
		self.size = size

	# Debug message to check that an asteroid object is deleted
	def __del__(self):
		print("Asteroid deleted")

	# Creates the asteroid image, starts the move function
	def spawnAsteroid(self):
		if currentCheat == "Shrink":
			asteroidCanvas = canvas.create_image(randrange(50, 651), -50, image=monocleImg, anchor="s")
		else:
			asteroidCanvas = canvas.create_image(randrange(50, 651), -50, image=asteroidSizes[self.size - 1], anchor="s")
		window.after(0, self.moveAsteroid, asteroidCanvas)

	# Moves the asteroid down at a speed based on scaled difficulty and size
	def moveAsteroid(self, asteroidCanvas):
		global asteroids
		if self in asteroids:
			asteroidSpeed = (8 - self.size) * math.pow(scaledDifficulty, 0.7) / 7
			if currentCheat == "Slow":
				asteroidSpeed /= 4
			if canvas.itemcget(pauseCanvas, "state") == "hidden" \
			and canvas.itemcget(countCanvas, "state") == "hidden" \
			and canvas.itemcget(bossCanvas, "state") == "hidden":
				canvas.move(asteroidCanvas, 0, asteroidSpeed)
				if not invincibility:
					self.checkCollision(asteroidCanvas)
			if canvas.coords(asteroidCanvas)[1] < 900:
				window.after(10, self.moveAsteroid, asteroidCanvas)
			else:
				asteroids.remove(self)
		else:
			canvas.move(asteroidCanvas, 0, 900)

	# Checks whether the asteroid hitbox and spaceship hitbox overlap
	def checkCollision(self, asteroidCanvas):
		spaceshipBound = canvas.bbox(spaceshipCanvas)
		asteroidBound = canvas.bbox(asteroidCanvas)
		spaceshipBound = list(spaceshipBound)
		asteroidBound = list(asteroidBound)
		spaceshipBound[0] += 33
		spaceshipBound[1] += 15
		spaceshipBound[2] -= 33
		spaceshipBound[3] -= 20
		asteroidBound[0] += asteroidHitboxesDifference[self.size-1]
		asteroidBound[1] += asteroidHitboxesDifference[self.size-1]
		asteroidBound[2] -= asteroidHitboxesDifference[self.size-1]
		asteroidBound[3] -= asteroidHitboxesDifference[self.size-1]
		if (spaceshipBound[0] < asteroidBound[0] < spaceshipBound[2] \
		or spaceshipBound[0] < asteroidBound[2] < spaceshipBound[2]) \
		and (spaceshipBound[1] < asteroidBound[1] < spaceshipBound[3] \
		or spaceshipBound[1] < asteroidBound[3] < spaceshipBound[3]):
			print("Collided with asteroid number", asteroidCanvas)
			collision()

# Inputs a file and dimensions, returns an ImageTk.PhotoImage
def addImage(file, x, y):
	image = Image.open(file).resize((x, y))
	image = ImageTk.PhotoImage(image)
	return image

# Makes background gif change frame every 0.1 seconds
def updateBg(frameNo):
	star = stars[frameNo]
	frameNo += 1
	frameNo = frameNo % starCount
	canvas.itemconfigure(backgroundCanvas, image=star)
	window.after(50, updateBg, frameNo)

# Main game loop: increases score, calculates difficulty, creates asteroids
def gameLoop():
	global scaledDifficulty
	global score
	if gameRunning:
		scaledDifficulty = math.log(difficulty+1, 2) * math.pow(score + 1000, 0.43) / 2
		score += (7 * difficulty)
		scoreLabel.config(text=("Score:", score))
		if uniform(0, 1000) < scaledDifficulty:
			print("Current difficulty:", int(scaledDifficulty))
			if currentCheat == "Shrink":
				asteroid = Asteroid(1)
			else:
				asteroid = Asteroid(randrange(1,4))
			asteroids.append(asteroid)
			asteroid.spawnAsteroid()
		window.after(20, gameLoop)

# Handles invincibility, lives and the explosion when colliding
def collision():
	setInvincibility(True)
	lostLife()
	explode(6)
	window.after(1000, setInvincibility, False)

# Creates many orange ovals around the spaceship to simulate an explosion
def explode(count):
	coords = canvas.coords(spaceshipCanvas)
	coords[1] += randrange(-120,-20)
	coords[0] += randrange(-30,30)
	explosion = canvas.create_oval(coords[0]-randrange(5,20), coords[1]-randrange(5,20), coords[0]+randrange(5,20), coords[1]+randrange(5,20), fill="#FB8B23", width=0)
	window.after(100, hide, explosion)
	count -= 1
	if count > 0:
		window.after(20, explode, count)

# Removes a life, partially handles the game over
def lostLife():
	global lives
	global gameRunning
	lives -= 1
	if lives == 2:
		heartFlicker(False, 7, lifeLabel1)
	elif lives == 1:
		heartFlicker(False, 7, lifeLabel2)
	else:
		heartFlicker(False, 1, lifeLabel3)
		gameRunning = False
		hide(spaceshipCanvas)
		endScoreLabel.config(text="You explored " + str(score) + "\nkm of space!")
		show(endCanvas)
		gameEnd()

# Makes the selected heart flicker on and off
def heartFlicker(on, flicks, label):
	if on:
		label.config(image=heartImg)
		on = False
	else:
		label.config(image=lostHeartImg)
		on = True
	flicks -= 1
	if flicks > 0:
		window.after(200, heartFlicker, on, flicks, label)

# Sets whether the spaceship is invincible or not
def setInvincibility(value):
	global invincibility
	invincibility = value

# Pause menu that is displayed when pause button is pressed midgame
def pause(event):
	global gameRunning
	if gameRunning:
		show(pauseCanvas)
		gameRunning = False

# Displays work image and hides all menus or vice versa when boss key pressed
def boss(event):
	global gameRunning
	global gameWasRunning
	global canvasesShown
	canvas.tag_raise(bossCanvas)
	if canvas.itemcget(bossCanvas, "state") == "hidden":
		gameWasRunning = gameRunning
		show(bossCanvas)
		gameRunning = False
		for item in canvases:
			if canvas.itemcget(item, "state") == "normal":
				canvasesShown.append(item)
				hide(item)
	else:
		hide(bossCanvas)
		for item in canvasesShown:
			show(item)
		canvasesShown.clear()
		if gameWasRunning:
			show(countCanvas)
			window.after(0, countdown, 3)
		gameWasRunning = False
	print(gameRunning, gameWasRunning, canvasesShown)

# Handles resetting variables and updating the score label when the game ends
def gameEnd():
	global score
	global latestScore
	global asteroids
	global currentCheat
	currentCheat = ""
	asteroids.clear()
	latestScore = score
	score = 0
	scoreLabel.config(text="Latest score: " + str(latestScore))

# Closes main menu, initiates the game
def playGame():
	global gameRunning
	global lives
	gameRunning = True
	lives = 3
	lifeLabel1.config(image=heartImg)
	lifeLabel2.config(image=heartImg)
	lifeLabel3.config(image=heartImg)
	hide(menuCanvas)
	show(livesCanvas)
	window.after(0, gameLoop)

# Loads the game that is stored in savestate.txt
def load():
	global gameRunning
	global score
	global difficulty
	global lives
	global currentCheat
	s = open("savestate.txt", "r")
	score = int(s.readline())
	difficulty = int(s.readline())
	lives = int(s.readline())
	currentCheat = s.readline().strip()
	xCoord = float(s.readline())
	yCoord = float(s.readline())
	xSpaceship = xCoord - canvas.coords(spaceshipCanvas)[0]
	ySpaceship = yCoord - canvas.coords(spaceshipCanvas)[1]
	canvas.move(spaceshipCanvas, xSpaceship, ySpaceship)
	gameRunning = True
	hide(menuCanvas)
	show(livesCanvas)
	window.after(0, gameLoop)

# Opens up the options page
def options():
	hide(menuCanvas)
	hide(spaceshipCanvas)
	hide(scoreCanvas)
	show(optionCanvas)
	leftEntry.delete(0, len(leftEntry.get()))
	rightEntry.delete(0, len(rightEntry.get()))
	upEntry.delete(0, len(upEntry.get()))
	downEntry.delete(0, len(downEntry.get()))
	pauseEntry.delete(0, len(pauseEntry.get()))
	bossEntry.delete(0, len(bossEntry.get()))
	leftEntry.insert(0, leftKey)
	rightEntry.insert(0, rightKey)
	upEntry.insert(0, upKey)
	downEntry.insert(0, downKey)
	pauseEntry.insert(0, pauseKey)
	bossEntry.insert(0, bossKey)

# Opens up the leaderboards page
def leaderboards():
	hide(menuCanvas)
	hide(spaceshipCanvas)
	hide(scoreCanvas)
	show(lbCanvas)
	pass

# Closes the game
def exitToDesktop():
	window.destroy()

# Closes pause screen, opens countdown screen
def resume():
	saveButton["state"] = "normal"
	saveButton.config(text="Save")
	hide(pauseCanvas)
	show(countCanvas)
	window.after(0, countdown, 3)

# Changes the countdown number every second, resumes the game
def countdown(count):
	global gameRunning
	countLabel.config(text=count)
	count -= 1
	if count >= 0:
		window.after(1000, countdown, count)
	else:
		gameRunning = True
		hide(countCanvas)
		window.after(0, gameLoop)

# Saves the current state of the game into a text file
def save():
	saveState = ""
	saveState += str(score) + "\n" + \
				 str(difficulty) + "\n" + \
				 str(lives) + "\n" + \
				 str(currentCheat) + "\n" + \
				 str(canvas.coords(spaceshipCanvas)[0]) + "\n" + \
				 str(canvas.coords(spaceshipCanvas)[1])
	s = open("savestate.txt", "w")
	s.write(saveState)
	s.close()
	saveButton["state"] = "disabled"
	saveButton.config(text="Saved!")

# Exits to the main menu from the pause screen
def exitToMenu():
	saveButton["state"] = "normal"
	saveButton.config(text="Save")
	if canvas.itemcget(pauseCanvas, "state") == "normal":
		hide(pauseCanvas)
		gameEnd()
	else:
		hide(endCanvas)
		show(spaceshipCanvas)
		print("Updating leaderboard")
		addToLb()
	hide(livesCanvas)
	show(menuCanvas)

# Adds a score to the leaderboard if it is in the top 5
def addToLb():
	global currentName
	global lbNames
	global lbScores
	global lbText
	currentName = endNameEntry.get()
	if currentName:
		print(currentName, latestScore)
		lbScores.append(latestScore)
		lbScores.sort(reverse=True)
		index = lbScores.index(latestScore)
		lbNames.insert(index, currentName)
		del lbScores[5]
		del lbNames[5]
		print(lbNames, lbScores)
		lbText = formatLb()
		lbScoreLabel.config(text=lbText)
		writeToLb()

# Returns to the main menu from the options
def back():
	hide(optionCanvas)
	show(scoreCanvas)
	show(menuCanvas)
	show(spaceshipCanvas)

# Increases difficulty of the game
# 1: Easy
# 2: Medium
# 3: Hard
# 4: Expert
# 5: Insane
def difficultyIncrease():
	global difficulty
	global shmooveSpeed
	difficulty += 1
	if difficulty == 4:
		difficulty = 8
	if difficulty == 9:
		difficulty = 1
	shmooveSpeed = 4 + difficulty
	difficultyButton.config(text="Difficulty: " + difficultyArray[difficulty-1])

# Unbinds, changes, and rebinds every possible key
def setKeybinds():
	global leftKey
	global rightKey
	global upKey
	global downKey
	global pauseKey
	global bossKey
	global leftRelease
	global rightRelease
	global upRelease
	global downRelease
	window.unbind(leftKey)
	window.unbind(rightKey)
	window.unbind(upKey)
	window.unbind(downKey)
	window.unbind(pauseKey)
	window.unbind(bossKey)
	window.unbind(leftRelease)
	window.unbind(rightRelease)
	window.unbind(upRelease)
	window.unbind(downRelease)
	leftKey = leftEntry.get()[0]
	rightKey = rightEntry.get()[0]
	upKey = upEntry.get()[0]
	downKey = downEntry.get()[0]
	pauseKey = pauseEntry.get()[0]
	bossKey = bossEntry.get()[0]
	leftRelease = "<KeyRelease-" + leftKey + ">"
	rightRelease = "<KeyRelease-" + rightKey + ">"
	upRelease = "<KeyRelease-" + upKey + ">"
	downRelease = "<KeyRelease-" + downKey + ">"
	window.bind(leftKey, spaceship.moving)
	window.bind(rightKey, spaceship.moving)
	window.bind(upKey, spaceship.moving)
	window.bind(downKey, spaceship.moving)
	window.bind(pauseKey, pause)
	window.bind(bossKey, boss)
	window.bind(leftRelease, spaceship.stopMoving)
	window.bind(rightRelease, spaceship.stopMoving)
	window.bind(upRelease, spaceship.stopMoving)
	window.bind(downRelease, spaceship.stopMoving)

# Returns to the main menu from the leaderboard
def backFromLb():
	hide(lbCanvas)
	show(scoreCanvas)
	show(menuCanvas)
	show(spaceshipCanvas)

# Returns the leaderboard in the format correct for the leaderboard label
def formatLb():
	lbText = ""
	for i in range(0, 5):
		lbText += (lbNames[i] + ": " + str(lbScores[i]))
		if i < 4:
			lbText += "\n-------\n"
	return lbText

# Overwrites the leaderboards file when a top 5 score is achieved
def writeToLb():
	f = open("leaderboards.txt", "w")
	line1 = ""
	line2 = ""
	for i in range(0,5):
		line1 += lbNames[i]
		if i < 4:
			line1 += ","
	for i in range(0,5):
		line2 += str(lbScores[i])
		if i < 4:
			line2 += ","
	f.write(line1 + "\n" + line2)
	f.close()

# Hides selected canvas widget
def hide(widget):
	canvas.itemconfigure(widget, state="hidden")

# Unhides selected canvas widget
def show(widget):
	canvas.itemconfigure(widget, state="normal")

# Handles what happens when the player enters a cheat code
def startCheating(event, cheat):
	global currentCheat
	if gameRunning:
		if not currentCheat:
			currentCheat = cheat
			cheatLabel.config(text=("Cheat activated: " + currentCheat))
		else:
			if currentCheat == cheat:
				cheatLabel.config(text=("Cheat deactivated: " + currentCheat))
				currentCheat = ""
		if cheat == "Regen":
			regen()
		if cheat == "Boost":
			boost()
		cheatFlicker(True, 6)

# Causes the cheat frame to flicker when a cheat is (de)activated
def cheatFlicker(on, flicks):
	if on:
		canvas.itemconfigure(cheatCanvas, state="normal")
		on = False
	else:
		canvas.itemconfigure(cheatCanvas, state="hidden")
		on = True
	flicks -= 1
	if flicks > 0:
		window.after(300, cheatFlicker, on, flicks)

# Regenerates the player one heart every 10 seconds
def regen():
	global lives
	if currentCheat == "Regen":
		if lives == 1:
			heartFlicker(True, 5, lifeLabel2)
			lives += 1
		elif lives == 2:
			heartFlicker(True, 5, lifeLabel1)
			lives += 1
		window.after(10000, regen)

# Doubles player speed
def boost():
	global shmooveSpeed
	if currentCheat == "Boost":
		shmooveSpeed *= 2
	else:
		shmooveSpeed /= 2

# Loading the leaderboard
f = open("leaderboards.txt", "r")
lbNames = f.readline().split(",")
lbNames[4] = lbNames[4].strip()
lbScores = f.readline().split(",")
lbScores = [int(x) for x in lbScores]
lbText = formatLb()
f.close()

# Global variables
score = 0
latestScore = 0
difficulty = 1
difficultyArray = ["Medium", "Hard", "Master", None, None, None, None, "IMPOSSIBLE"]
scaledDifficulty = 0
shmooveSpeed = 5
lives = 3
pauseKey = "p"
bossKey = "b"
leftKey = "a"
rightKey = "d"
upKey = "w"
downKey = "s"
leftRelease = "<KeyRelease-a>"
rightRelease = "<KeyRelease-d>"
upRelease = "<KeyRelease-w>"
downRelease = "<KeyRelease-s>"
lefting = False
righting = False
upping = False
downing = False
invincibility = False
gameRunning = False
gameWasRunning = False
canvasesShown = []
canvases = []
currentName = ""
currentCheat = ""

# Creating and configuring window
window = Tk()
window.title("Space Explorers")
window.resizable(False, False)
centerX = window.winfo_screenwidth() / 2 - 350
centerY = window.winfo_screenheight() / 2 - 350
window.geometry("700x700" + "+" + str(int(centerX)) + "+" + str(int(centerY)))

# Image stuff
starCount = 30
stars = [PhotoImage(file="starry.gif", format = 'gif -index %i' %(i)) for i in range(starCount)]
spaceshipImg = addImage("spaceship.png", 125, 125)
spaceshipImgOff = addImage("spaceshipoff.png", 125, 125)
spaceshipImgLeft = addImage("spaceshipleft.png", 125, 125)
spaceshipImgLeftOff = addImage("spaceshipleftoff.png", 125, 125)
spaceshipImgRight = addImage("spaceshipright.png", 125, 125)
spaceshipImgRightOff = addImage("spaceshiprightoff.png", 125, 125)
heartImg = addImage("heart.png", 40, 40)
lostHeartImg = addImage("lostheart.png", 40, 40)
bossImg = addImage("boss.png", 700, 700)
monocleImg = addImage("monocle.png", 50, 50)
asteroidSizes = [addImage("asteroid.png", 75, 75),
			addImage("asteroid.png", 125, 125),
			addImage("asteroid.png", 150, 150)]
asteroidHitboxesDifference = [15, 25, 30]
asteroids = []

# Canvas making
canvas = Canvas(window,
					bg="#000000",
					width=700,
					height=700,
					cursor="dot",
					highlightthickness=0)
canvas.pack()

# Create various frames for the different menus
menuFrame = Frame(canvas,
					bg="#1D1D23",
					width=300,
					height=620,
					bd=2,
					relief="ridge")
optionsFrame = Frame(canvas,
					bg="#1D1D23",
					width=500,
					height=620,
					bd=2,
					relief="ridge")
lbFrame = Frame(canvas,
					bg="#1D1D23",
					width=500,
					height=620,
					bd=2,
					relief="ridge")
pauseFrame = Frame(canvas,
					bg="#1D1D23",
					width=300,
					height=420,
					bd=2,
					relief="ridge")
countFrame = Frame(canvas,
					bg="#000000",
					width=200,
					height=200,
					bd=2,
					relief="ridge")
scoreFrame = Frame(canvas,
					bg="#000000",
					width=100,
					height=30,
					bd=2,
					relief="ridge")
livesFrame = Frame(canvas,
					bg="#000000",
					width=30,
					height=30,
					bd=2,
					relief="ridge",
					padx=5,
					pady=5)
endFrame = Frame(canvas,
					bg="#000000",
					width=300,
					height=460,
					bd=2,
					relief="ridge")
cheatFrame = Frame(canvas,
					bg="#000000",
					width=200,
					height=50,
					bd=2,
					relief="ridge")

# Create labels and buttons for main menu
welcomeLabel = Label(menuFrame,
					text="Welcome to\nSpace Explorers!",
					bg="#000000",
					fg="#FFFFFF",
					font=("Uroob", 30),
					bd=5,
					relief="ridge",
					pady=10,
					padx=10)
playButton = Button(menuFrame,
					text="Launch!",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 26),
					bd=2,
					relief="ridge",
					pady=10,
					padx=10,
					cursor="X_cursor",
					command=playGame)
loadButton = Button(menuFrame,
					text="Load Game",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 26),
					bd=2,
					relief="ridge",
					pady=10,
					padx=10,
					cursor="X_cursor",
					command=load)
optionsButton = Button(menuFrame,
					text="Options",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 26),
					bd=2,
					relief="ridge",
					pady=10,
					padx=10,
					cursor="X_cursor",
					command=options)
lbButton = Button(menuFrame,
					text="Leaderboards",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 26),
					bd=2,
					relief="ridge",
					pady=10,
					padx=10,
					cursor="X_cursor",
					command=leaderboards)
desktopButton = Button(menuFrame,
					text="Exit to Desktop",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 26),
					bd=2,
					relief="ridge",
					pady=10,
					padx=10,
					cursor="X_cursor",
					command=exitToDesktop)

# Create labels and buttons for options menu
optionsLabel = Label(optionsFrame,
					text="Options",
					bg="#000000",
					fg="#FFFFFF",
					font=("Uroob", 36),
					bd=5,
					relief="ridge",
					pady=10,
					padx=10)
backButton = Button(optionsFrame,
					text="Back",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 26),
					bd=2,
					relief="ridge",
					pady=10,
					padx=10,
					cursor="X_cursor",
					command=back)
difficultyButton = Button(optionsFrame,
					text="Difficulty: Medium",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 26),
					bd=2,
					relief="ridge",
					pady=10,
					padx=10,
					cursor="X_cursor",
					command=difficultyIncrease)
keybindsButton = Button(optionsFrame,
					text="Set Keybinds",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 26),
					bd=2,
					relief="ridge",
					pady=10,
					padx=10,
					cursor="X_cursor",
					command=setKeybinds)
pauseEntryLabel = Label(optionsFrame,
					text="Pause",
					bg="#1D1D23",
					fg="#FFFFFF",
					font=("Uroob", 22))
bossEntryLabel = Label(optionsFrame,
					text="Boss",
					bg="#1D1D23",
					fg="#FFFFFF",
					font=("Uroob", 22))
leftEntryLabel = Label(optionsFrame,
					text="Left",
					bg="#1D1D23",
					fg="#FFFFFF",
					font=("Uroob", 22))
rightEntryLabel = Label(optionsFrame,
					text="Right",
					bg="#1D1D23",
					fg="#FFFFFF",
					font=("Uroob", 22))
upEntryLabel = Label(optionsFrame,
					text="Up",
					bg="#1D1D23",
					fg="#FFFFFF",
					font=("Uroob", 22))
downEntryLabel = Label(optionsFrame,
					text="Down",
					bg="#1D1D23",
					fg="#FFFFFF",
					font=("Uroob", 22))
pauseEntry = Entry(optionsFrame,
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 22),
					bd=2,
					relief="ridge",
					cursor="X_cursor",
					exportselection=0,
					textvariable=pauseKey,
					width=3,
					justify=CENTER)
bossEntry = Entry(optionsFrame,
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 22),
					bd=2,
					relief="ridge",
					cursor="X_cursor",
					exportselection=0,
					textvariable=bossKey,
					width=3,
					justify=CENTER)
leftEntry = Entry(optionsFrame,
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 22),
					bd=2,
					relief="ridge",
					cursor="X_cursor",
					exportselection=0,
					textvariable=leftKey,
					width=3,
					justify=CENTER)
rightEntry = Entry(optionsFrame,
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 22),
					bd=2,
					relief="ridge",
					cursor="X_cursor",
					exportselection=0,
					textvariable=rightKey,
					width=3,
					justify=CENTER)
upEntry = Entry(optionsFrame,
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 22),
					bd=2,
					relief="ridge",
					cursor="X_cursor",
					exportselection=0,
					textvariable=upKey,
					width=3,
					justify=CENTER)
downEntry = Entry(optionsFrame,
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 22),
					bd=2,
					relief="ridge",
					cursor="X_cursor",
					exportselection=0,
					textvariable=downKey,
					width=3,
					justify=CENTER)

# Create labels and buttons for leaderboards screen
lbLabel = Label(lbFrame,
					text="Leaderboards",
					bg="#000000",
					fg="#FFFFFF",
					font=("Uroob", 36),
					bd=5,
					relief="ridge",
					pady=10,
					padx=10)
lbScoreLabel = Label(lbFrame,
					text=lbText,
					bg="#1D1D23",
					fg="#FFD700",
					font=("Uroob", 28),
					width=20,
					height=9,
					pady=10,
					padx=10)
lbBackButton = Button(lbFrame,
					text="Back",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 26),
					bd=2,
					relief="ridge",
					pady=10,
					padx=10,
					cursor="X_cursor",
					command=backFromLb)

# Create labels and buttons for pause menu
pauseLabel = Label(pauseFrame,
					text="Paused",
					bg="#000000",
					fg="#FFFFFF",
					font=("Uroob", 36),
					bd=5,
					relief="ridge",
					pady=10,
					padx=10)
resumeButton = Button(pauseFrame,
					text="Resume",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 26),
					bd=2,
					relief="ridge",
					pady=10,
					padx=10,
					cursor="X_cursor",
					command=resume)
saveButton = Button(pauseFrame,
					text="Save",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 26),
					bd=2,
					relief="ridge",
					pady=10,
					padx=10,
					cursor="X_cursor",
					command=save)
menuButton = Button(pauseFrame,
					text="Exit to Menu",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 26),
					bd=2,
					relief="ridge",
					pady=10,
					padx=10,
					cursor="X_cursor",
					command=exitToMenu)

# Create label for the countdown frame
countLabel = Label(countFrame,
					text="C",
					bg="#000000",
					fg="#FFD700",
					font=("Sawasdee", 100),
					width=2)

# Create labels for the lives frame
lifeLabel1 = Label(livesFrame,
					image=heartImg,
					bg="#000000")
lifeLabel2 = Label(livesFrame,
					image=heartImg,
					bg="#000000")
lifeLabel3 = Label(livesFrame,
					image=heartImg,
					bg="#000000")

# Create label for the score frame
scoreLabel = Label(scoreFrame,
					text="Latest score: " + str(latestScore),
					bg="#000000",
					fg="#FFD700",
					font=("Sawasdee", 13),
					width=16)

# Create labels for end screen
endLabel = Label(endFrame,
					text="Game Over!",
					bg="#000000",
					fg="#FFFFFF",
					font=("Uroob", 36),
					bd=5,
					relief="ridge",
					pady=10,
					padx=10)
endScoreLabel = Label(endFrame,
					text="You explored\nx km of space!",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 24),
					pady=10,
					padx=10)
endNameLabel = Label(endFrame,
					text="Enter your name:",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 24),
					pady=10,
					padx=10)
endNameEntry = Entry(endFrame,
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 22),
					bd=2,
					relief="ridge",
					cursor="X_cursor",
					exportselection=0,
					textvariable=currentName,
					width=10,
					justify=CENTER)
endNoteLabel = Label(endFrame,
					text="(Or nothing to not save score)",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 16))
endExitButton = Button(endFrame,
					text="Exit to Menu",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 26),
					bd=2,
					relief="ridge",
					pady=10,
					padx=10,
					cursor="X_cursor",
					command=exitToMenu)

# Create label for the cheat frame
cheatLabel = Label(cheatFrame,
					text="Cheat activated:",
					bg="#000000",
					fg="#FFD700",
					font=("Uroob", 20),
					pady=5,
					padx=5)

# Placing labels and buttons on the menu frame
welcomeLabel.place(x=150, y=30, anchor="n")
playButton.place(x=150, y=160, anchor="n")
loadButton.place(x=150, y=250, anchor="n")
optionsButton.place(x=150, y=340, anchor="n")
lbButton.place(x=150, y=430, anchor="n")
desktopButton.place(x=150, y=520, anchor="n")

# Placing labels and buttons on the options frame
optionsLabel.place(x=250, y=30, anchor="n")
backButton.place(x=250, y=140, anchor="n")
difficultyButton.place(x=250, y=230, anchor="n")
keybindsButton.place(x=250, y=320, anchor="n")
leftEntryLabel.place(x=100, y=420, anchor="n")
rightEntryLabel.place(x=200, y=420, anchor="n")
upEntryLabel.place(x=300, y=420, anchor="n")
downEntryLabel.place(x=400, y=420, anchor="n")
leftEntry.place(x=100, y=450, anchor="n")
rightEntry.place(x=200, y=450, anchor="n")
upEntry.place(x=300, y=450, anchor="n")
downEntry.place(x=400, y=450, anchor="n")
pauseEntryLabel.place(x=150, y=500, anchor="n")
bossEntryLabel.place(x=350, y=500, anchor="n")
pauseEntry.place(x=150, y=530, anchor="n")
bossEntry.place(x=350, y=530, anchor="n")

# Placing labels and buttons on the leaderboards frame
lbLabel.place(x=250, y=30, anchor="n")
lbScoreLabel.place(x=250, y=130, anchor="n")
lbBackButton.place(x=250, y=520, anchor="n")

# Placing labels and buttons on the pause frame
pauseLabel.place(x=150, y=30, anchor="n")
resumeButton.place(x=150, y=140, anchor="n")
saveButton.place(x=150, y=230, anchor="n")
menuButton.place(x=150, y=320, anchor="n")

# Placing label on the countdown frame
countLabel.pack()

# Placing label on the score frame
scoreLabel.pack()

# Placing labels on the lives frame
lifeLabel1.pack()
lifeLabel2.pack()
lifeLabel3.pack()

# Placing labels and buttons on the end frame
endLabel.place(x=150, y=30, anchor="n")
endScoreLabel.place(x=150, y=130, anchor="n")
endNameLabel.place(x=150, y=210, anchor="n")
endNameEntry.place(x=150, y=260, anchor="n")
endNoteLabel.place(x=150, y=310, anchor="n")
endExitButton.place(x=150, y=360, anchor="n")

# Placing label on the cheats frame
cheatLabel.pack()

# Creating canvas widgets for all the various windows and images used
backgroundCanvas = canvas.create_image(0, 0, image=stars[0], anchor="nw")
spaceshipCanvas = canvas.create_image(100, 680, image=spaceshipImgOff, anchor="s")
bossCanvas = canvas.create_image(0, 0, image=bossImg, anchor="nw", state="hidden")
menuCanvas = canvas.create_window(350, 10, anchor="n", window=menuFrame, state="normal")
optionCanvas = canvas.create_window(350, 30, anchor="n", window=optionsFrame, state="hidden")
lbCanvas = canvas.create_window(350, 30, anchor="n", window=lbFrame, state="hidden")
pauseCanvas = canvas.create_window(350, 140, anchor="n", window=pauseFrame, state="hidden")
countCanvas = canvas.create_window(350, 250, anchor="n", window=countFrame, state="hidden")
scoreCanvas = canvas.create_window(690, 10, anchor="ne", window=scoreFrame, state="normal")
livesCanvas = canvas.create_window(10, 10, anchor="nw", window=livesFrame, state="hidden")
endCanvas = canvas.create_window(350, 125, anchor="n", window=endFrame, state="hidden")
cheatCanvas = canvas.create_window(350, 30, anchor="n", window=cheatFrame, state="hidden")

canvases = [backgroundCanvas,
			spaceshipCanvas,
			menuCanvas,
			optionCanvas,
			lbCanvas,
			pauseCanvas,
			countCanvas,
			scoreCanvas,
			livesCanvas,
			endCanvas,
			cheatCanvas]

# My pitiful attempt at OOP
spaceship = Spaceship(spaceshipImg, spaceshipCanvas)

# Initiates background loop and spaceship movement detection
window.after(0, updateBg, 0)
window.after(0, spaceship.shmooves, True)

# Key bindings
window.bind(leftKey, spaceship.moving)
window.bind(rightKey, spaceship.moving)
window.bind(upKey, spaceship.moving)
window.bind(downKey, spaceship.moving)
window.bind(pauseKey, pause)
window.bind(bossKey, boss)
window.bind(leftRelease, spaceship.stopMoving)
window.bind(rightRelease, spaceship.stopMoving)
window.bind(upRelease, spaceship.stopMoving)
window.bind(downRelease, spaceship.stopMoving)
window.bind(downRelease, spaceship.stopMoving)
window.bind("<Control-Down>", lambda event, a="Slow": startCheating(event, a))
window.bind("<Control-minus>", lambda event, a="Shrink": startCheating(event, a))
window.bind("<Control-plus>", lambda event, a="Regen": startCheating(event, a))
window.bind("<Control-comma>", lambda event, a="Boost": startCheating(event, a))
window.mainloop()