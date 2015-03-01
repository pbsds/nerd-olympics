import pygame, os, time, ConfigParser, random
from helpers import ListFolderContent, MakeEpilepsySafe
from sys import argv

class Sprites():
	class sprite:
		def __init__(self, sprite, pos, loop=True, scale=None):
			self.pos = pos
			self.sprite = sprite
			self.length = len(sprite)
			self.cycle = 0
			self.speed = 0.5
			self.loop = loop
			self.scale = scale
		def step(self):
			self.cycle += self.speed
			if self.cycle >= self.length:#loop
				if self.loop:
					self.cycle -= self.length
				else:
					return False
			return True
		def draw(self, parent):
			spr = self.sprite[int(self.cycle)]
			if self.scale:
				w, h = spr.get_size()
				spr = pygame.transform.scale(spr, (int(w*self.scale), int(h*self.scale)))
			parent.blit(spr, self.pos)
	def __init__(self):
		self.sprites = {}
		self.sequences = {}
	def LoadImage(self, path, c=True, s=True):#c:colorkey, s:store
		if s and path in self.sprites:
			return self.sprites[path]
		else:
			ret = pygame.image.load("gfx/" + path).convert()
			if c: ret.set_colorkey((255, 0, 220))
			if s: self.sprites[path] = ret
			return ret
	def LoadImageSequence(self, path, c=True, s=True):
		if s and path in self.sequences:
			return self.sequences[path]
		else:
			#load sequence:
			raw = pygame.image.load("gifs/"+path).convert()
			rw = raw.get_width()
			rh = raw.get_height()

			f = open("gifs/"+path[:-3]+"txt", "r")
			meta = f.read().replace("\r\n", "\n").split("\n")
			f.close()

			hor, vert, length = None, None, None
			for i in meta:
				i = i.split(" ")
				if len(i) > 2: continue

				if i[0] == "horizontal":
					hor = int(i[1])
				elif i[0] == "vertical":
					vert = int(i[1])
				elif i[0] == "length":
					length = int(i[1])
			if None in (hor, vert, length):
				raise "insufficient gif metadata"
			w = rw / hor
			h = rh / vert

			#crop out each segment:
			ret = []
			for i in xrange(length):
				x = i % hor
				y = i // hor
				ret.append(raw.subsurface((x*w,y*h,w,h)).convert())
				if c: ret[-1].set_colorkey((255, 0, 220))

			if s: self.sequences[path] = tuple(ret)
			return tuple(ret)
	def LoadImageAlpha(self, path, s=True):
		if s and path in self.sprites:
			return self.sprites[path]
		else:
			ret = pygame.image.load("gfx/" + path).convert_alpha()
			if s: self.sprites[path] = ret
			return ret
class Sound():
	def __init__(self):
		self.SFX = {}
		self.sounds = {}

		#load
		for i in ListFolderContent("sounds/*.wav"):
			self.sounds[i.split(".")[0]] = pygame.mixer.Sound("sounds/" + i)
		for i in ListFolderContent("sfx/*.wav"):
			self.SFX[i.split(".")[0]] = pygame.mixer.Sound("sfx/" + i)

		self.playing = None
	def PlaySFX(self, sfx):
		self.SFX[sfx].play()
	def PlaySound(self, sound):
		self.sounds[sound].play()
	def SetBGM(self, bgm):
		if bgm:
			if self.playing <> bgm:
				if os.path.exists("bgm/%s.ogg" % bgm):
					pygame.mixer.music.load("bgm/%s.ogg" % bgm)
					pygame.mixer.music.play(-1)
				else:
					print "BGM \"%s\" doesn't exist!" % bgm
					pygame.mixer.music.stop()
				self.playing = bgm
		else:
			pygame.mixer.music.stop()
	def mute(self):
		self.SetBGM(None)
		for i in self.sounds.values():
			i.stop()
		for i in self.SFX.values():
			i.stop()
class Game():
	def __init__(self, Title, resolution, fullscreen):
		#start pygame
		#pygame.mixer.pre_init(44100, buffer=512)#lower the buffer to avoid latency
		pygame.mixer.pre_init(44100)#lower the buffer to avoid latency
		pygame.init()
		pygame.font.init()
		pygame.display.set_caption(Title)
		self.window = pygame.display.set_mode(resolution, pygame.HWSURFACE | (pygame.FULLSCREEN*fullscreen))
		self.resolution = resolution
		self.Timer = pygame.time.Clock()

		#initilize the game components:
		global Sprites, Sound
		Sprites = Sprites()
		Sound = Sound()

		#content
		self.subs = []
		self.current = 0
		self.scores = {"click":5, "quickscoper":1000, "alphabet":1000, "scroll":1000}
	def Play(self):

		#id 0
		import menu as current
		self.subs.append(current.sub(self, Sound, Sprites))

		#id 1
		import quickscoper as current
		self.subs.append(current.sub(self, Sound, Sprites))

		#id 2
		import alphabet as current
		self.subs.append(current.sub(self, Sound, Sprites))

		#id 3
		import illuminati as current
		self.subs.append(current.sub(self, Sound, Sprites))

		#id 4
		import scroll as current
		self.subs.append(current.sub(self, Sound, Sprites))

		#id 5
		import click as current
		self.subs.append(current.sub(self, Sound, Sprites))

		#id 6
		import scores as current
		self.subs.append(current.sub(self, Sound, Sprites))


		self.Start(0)
		self.mainLoop()
	def Start(self, id):
		self.current = id
		self.subs[id].doStart()
	#internal:
	def mainLoop(self):
		while 1:
			#FPS:
			self.Timer.tick(60)

			#input:
			events = pygame.event.get()
			for i in events:
				#Keyboard buttons:
				if i.type == pygame.QUIT:
					sys.exit()
				if i.type == pygame.KEYDOWN:
					if i.key == pygame.K_ESCAPE:
						sys.exit()

			#Do:
			self.subs[self.current].step(events)

			#draw
			self.subs[self.current].draw(self.window)

			#flip:
			pygame.display.flip()


ini = ConfigParser.ConfigParser()
f = open("config.ini", "r")
ini.readfp(f)
f.close()

if ini.getboolean("config", "epilepsy_safe") or "--safe" in argv[1:]:
	MakeEpilepsySafe()
	flash = False
else:
	flash = True

if ini.getboolean("config", "cmdgarb"):
	print "Loading assets..."
	time.sleep(0.7)
	print "Making challenges"
	time.sleep(0.7)
	print "Noscoping 1337 h4x0rz, no botting"
	time.sleep(1.5)
	print "Running for president..."
	time.sleep(0.7)
	print "Hacking for nudes..."
	time.sleep(0.7)
	print "Printing money..."
	time.sleep(0.7)
	print "Entering the matrix..."
	time.sleep(1.5)

	for i in xrange(100):
		print ""
		time.sleep(0.005)
	os.system("color a")
	for i in xrange(800):
		print "".join((random.choice(("1 ","0 ")) for i in xrange(40)))[:-1]
		time.sleep(0.005)
	for i in xrange(100):
		print ""
		time.sleep(0.005)
	os.system("cls")

	print "Now commence the MLG!!!"
	for i in xrange(10):
		for n in xrange(16):
			if flash: os.system("color %x" % n)
			time.sleep(0.025)
	#time.sleep(2)
	os.system("cls")
	#time.sleep(0.01)

res = map(int, ini.get("config", "resolution").split("x"))
full = ini.getboolean("config", "fullscreen")

Game = Game("xXx-MLG_N3rd-0lymp1c5_360-xXx", res, full)
time.sleep(0.2)
Game.Play()
