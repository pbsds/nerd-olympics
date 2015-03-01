import random, pygame, glob, os

class Text():
	def __init__(self):
		self.Fonts = {}
	def Create(self, string, size=9, c=(255,255,255)):
		if size not in self.Fonts:
			self.Fonts[size] = pygame.font.Font("comic.ttf", size)
		return self.Fonts[size].render(string, False, c)
	def CreateRune(self, string, size=9, c=(255,255,255)):
		if size not in self.Fonts:
			self.Fonts[size] = pygame.font.Font("comic.ttf", size)
		return self.Fonts[size].render(string, False, c)
Text = Text()

def ListFolderContent(Path):
	if "*" not in Path: Path += os.path.join("l","l")[1]+"*"
	return sorted((i.split(os.path.join("l","l")[1])[-1] for i in glob.glob(Path)))

colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255))
ecolors = ((255, 255, 255),(250, 250, 250))
def randomcolor():
	return random.choice(colors)
def MakeEpilepsySafe():
	global colors, ecolors
	colors = ecolors


class subBase:
	def __init__(self, Game, Sound, Sprites):
		self.Game = Game
		self.Sound = Sound
		self.Sprites = Sprites
		self.Text = Text

		self.sprites = []
	def doStart(self):
		self.sprites = []
		self.OnStart()
	def OnStart(self):
		pass
	def step(self, events):
		pass
	def draw(self, parent):
		pass
	def stepSprites(self):
		for i, s in tuple(enumerate(self.sprites))[::-1]:
			if not s.step():
				del self.sprites[i]
	def drawSprites(self, parent):
		for i in self.sprites:
			i.draw(parent)
