import helpers
import random, pygame

class sub(helpers.subBase):
	def OnStart(self):
		self.Sound.SetBGM("bangarang")
		self.scores = {"click":5, "quickscoper":1000, "alphabet":1000, "scroll":1000}

		self.s_duane = self.Sprites.LoadImageSequence("duane.png")
		self.s_snoop = self.Sprites.LoadImageSequence("snoop.png")

		w, h = self.Game.window.get_size()
		self.sprites.append(self.Sprites.sprite(self.s_snoop, (70, h-390), scale = 3))
		self.sprites.append(self.Sprites.sprite(self.s_snoop, (w-228, h-390), scale = 3))
		self.sprites.append(self.Sprites.sprite(self.s_duane, (w/2 - 240, h-320)))

		self.s_logo = self.Sprites.LoadImage("logo.png")
		self.s_mtdew = self.Sprites.LoadImage("mtdew.png")
		self.s_doritos = self.Sprites.LoadImage("doritos.png")

		self.s_start1 = helpers.Text.Create("START CHALLENGE!", 60, (0, 255, 0))
		self.s_start2 = helpers.Text.Create("START CHALLENGE!", 60, (0, 255, 255))
		self.startRes = self.s_start1.get_size()
		self.startActive = False

		self.bg_color = (0, 0, 0)
		self.bg_step = 0
	def step(self, events):
		self.bg_step += 1
		if self.bg_step >= 33:
			self.bg_step = 0
			old = self.bg_color
			while self.bg_color == old:
				self.bg_color = helpers.randomcolor()
				self.bg_color = (self.bg_color[0]/3, self.bg_color[1]/3, self.bg_color[2]/3)

		for i in events:
			if i.type == pygame.MOUSEMOTION:
				x, y = i.pos
				w, h = self.Game.window.get_size()
				if -self.startRes[0]/2 < x - w/2 < self.startRes[0]/2 and h-150 < y < h-150+self.startRes[1]:
					self.startActive = True

				else:
					self.startActive = False
			elif i.type == pygame.MOUSEBUTTONDOWN:
				if i.button == 1:
					if self.startActive:
						self.Sound.PlaySound("get noscoped")
						self.Game.Start(1)


		self.stepSprites()
	def draw(self, parent):
		w, h = parent.get_size()

		parent.fill(self.bg_color)

		parent.blit(self.s_mtdew, (- 50 + random.randrange(-10, 10), random.randrange(-10, 10)))
		parent.blit(self.s_mtdew, (w-450 + random.randrange(-10, 10), random.randrange(-10, 10)))
		parent.blit(self.s_doritos, (w/2-350 + random.randrange(-20, 20), 320 - random.randrange(-10, 10)))

		self.drawSprites(parent)

		parent.blit(self.s_logo, (w/2-300, 80))


		parent.blit(self.s_start2 if self.startActive and random.random() > 0.5 else self.s_start1, (w/2 - self.startRes[0]/2  + random.randrange(-10, 10)*self.startActive, h-150  + random.randrange(-10, 10)*self.startActive))

		self.startRes
