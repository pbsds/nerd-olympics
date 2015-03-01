import helpers
import random, pygame, time

class sub(helpers.subBase):
	def OnStart(self):
		self.Sound.SetBGM("sanic")
		w, h = self.Game.window.get_size()

		self.s_objective = tuple(helpers.Text.Create("Gotta scroll fast!", 60, i) for i in helpers.colors)
		self.objW = w/2 - self.s_objective[0].get_width()/2

		self.s_intro = tuple(helpers.Text.Create("dammit Aggmen! get back here!", 60, i) for i in helpers.colors)
		self.introW = w/2 - self.s_intro[0].get_width()/2
		self.s_intro2 = tuple(helpers.Text.Create("no staph sanic", 60, i) for i in helpers.colors)
		self.intro2W = w/2 - self.s_intro2[0].get_width()/2
		self.s_intro3 = tuple(helpers.Text.Create("I'll fast u hard, Aggmen!", 60, i) for i in helpers.colors)
		self.intro3W = w/2 - self.s_intro3[0].get_width()/2
		self.s_intro4 = tuple(helpers.Text.Create("Scroll down to catch aggmen! Scroll 500 tick as fast as you can!", 40, i) for i in helpers.colors)
		self.intro4W = w/2 - self.s_intro4[0].get_width()/2
		self.s_intro5 = tuple(helpers.Text.Create("SCROLL FAST 2 START!", 60, i) for i in helpers.colors)
		self.intro5W = w/2 - self.s_intro5[0].get_width()/2
		
		self.s_outro1 = tuple(helpers.Text.Create("THE SPEED IS TOO REAL!", 60, i) for i in helpers.colors)
		self.outro1W = w/2 - self.s_outro1[0].get_width()/2
		self.s_outro2 = tuple(helpers.Text.Create("Aggmen: ouchie sanic, u beat me!", 60, i) for i in helpers.colors)
		self.outro2W = w/2 - self.s_outro2[0].get_width()/2
		self.s_outro3 = tuple(helpers.Text.Create("Click to continue", 60, i) for i in helpers.colors)
		self.outro3W = w/2 - self.s_outro3[0].get_width()/2

		self.s_explosion = self.Sprites.LoadImageSequence("explosion.png")#71x100

		self.s_mtdew = self.Sprites.LoadImage("mtdew.png")
		self.s_doritos = self.Sprites.LoadImage("doritos.png")
		self.s_fast = self.Sprites.LoadImageAlpha("fast.png")#255x290
		self.fastSpr = self.Sprites.sprite((pygame.transform.rotate(self.s_fast, 30), pygame.transform.rotate(self.s_fast, 27)), (-1000, 0)); self.sprites.append(self.fastSpr)
		self.s_sanic = self.Sprites.LoadImage("sanic.png")
		self.s_aggmen = self.Sprites.LoadImage("aggmen.png")


		self.s_hitmarker = self.Sprites.LoadImage("hitmarker.png")
		self.hitmarker = [(0, 0), 0]


		self.inIntro = True
		self.epoch = time.time()
		self.hitcount = 0
		self.splodecount = 0
		self.started = False
		self.ready = False
		self.fasts = 0
		self.finished = False
		self.end = False
		self.time = None

		self.s_bg = pygame.transform.scale(self.Sprites.LoadImage("hills.jpg"), (w, h))
		self.s_bg2 = pygame.transform.scale(self.Sprites.LoadImage("sadfast.jpg"), (w, h))
		self.bg_color = (0, 0, 0)
		self.bg_step = 30
	def step(self, events):
		self.hitmarker[1] -= 1
		if self.inIntro:
			t = time.time()-self.epoch
			w, h = self.Game.window.get_size()

			if t > 7.6:
				if not self.ready:
					self.ready = True
					self.Sound.PlaySFX("shotgun")
					self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2-200), loop=False, scale=4))
					self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2, h/2-200), loop=False, scale=3))
					self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2), loop=False, scale=2))
			elif t > 3.5:
				self.s_bg.set_alpha(128)
			else:
				self.fastSpr.pos = (t*w/3 - w/5, h - t*h/3 * 1.15)

				if int(t*9) > self.hitcount:
					self.hitcount = int(t*9)

					self.Sound.PlaySFX("hitmarker")
					self.hitmarker = [(t*w/3 - w/5 + 290, h - t*h/3 * 1.15 + 230), 10]

				if int(t*2) > self.splodecount:
					self.splodecount = int(t*2)
					self.sprites.append(self.Sprites.sprite(self.s_explosion, (t*w/3 - w/5 + 350, h - t*h/3 * 1.15 + 100), loop=False, scale=2))
					self.Sound.PlaySFX("shotgun")

		if self.ready:
			self.bg_step += 1
			if self.bg_step >= 8:
				self.bg_step = 0
				old = self.bg_color
				while self.bg_color == old:
					self.bg_color = helpers.randomcolor()
					self.bg_color = (self.bg_color[0]/2, self.bg_color[1]/2, self.bg_color[2]/2)


			for i in events:
				if i.type == pygame.MOUSEBUTTONDOWN:
					if self.finished:
						if i.button == 1:
							self.end = True
							self.ready = False
							self.Sound.mute()
							self.Sound.PlaySound("sad violin")

							self.epoch = time.time()
					elif i.button == 5:
						if self.inIntro:
							self.inIntro = False
							self.started = True
							self.epoch = time.time()

						self.fasts += 1

						if self.fasts in (100, 800): self.Sound.PlaySFX("AIRHORN")
						if self.fasts == 1: self.Sound.PlaySound("wow")
						if self.fasts == 420: self.Sound.PlaySound("SMOKE WEED EVRYDAY")
						if self.fasts == 100: self.Sound.PlaySound("NEVER DONE THAT")
						if self.fasts == 200: self.Sound.PlaySound("get the camera")
						if self.fasts == 400: self.Sound.PlaySound("wombo combo")

						if self.fasts >= 500:
							self.finished = True
							#self.Sound.mute()
							self.Sound.PlaySFX("shotgun")
							self.Sound.PlaySFX("AIRHORN")
							self.Sound.PlaySound("homuna")
							w, h = self.Game.window.get_size()
							self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2-200), loop=False, scale=4))
							self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2, h/2-200), loop=False, scale=3))
							self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2), loop=False, scale=2))
							self.time = time.time() - self.epoch
							self.Game.scores["scroll"] = self.time
		elif self.end:
			t = time.time() - self.epoch
			if t > 24:
				self.Game.Start(5)
			if t >= 22.2:
				self.s_bg2.set_alpha(0)
			else:
				self.s_bg2.set_alpha(255-(t*255/22.5))


		self.stepSprites()
	def draw(self, parent):
		if self.end:
			parent.fill((0, 0, 0))
			parent.blit(self.s_bg2, (0, 0))
			return

		w, h = parent.get_size()
		parent.fill(self.bg_color)
		parent.blit(self.s_bg, (0, 0))

		self.drawSprites(parent)

		if self.inIntro:
			t = time.time()-self.epoch
			if t > 3.5:
				parent.blit(self.s_sanic, (-150 + random.randrange(-2, 3), random.randrange(-2, 3)))
				if t > 5: parent.blit(self.s_aggmen, (w-400 + random.randrange(-2, 3), 200 + random.randrange(-2, 3)))
				parent.blit(random.choice(self.s_intro), (self.introW + random.randrange(-2, 3), h/2-110 + random.randrange(-2, 3)))
				if t > 5: parent.blit(random.choice(self.s_intro2), (self.intro2W + random.randrange(-2, 3), h/2-30 + random.randrange(-2, 3)))
				if t > 6.5: parent.blit(random.choice(self.s_intro3), (self.intro3W + random.randrange(-2, 3), h/2+50 + random.randrange(-2, 3)))
				if t > 7.6:
					parent.blit(random.choice(self.s_intro4), (self.intro4W + random.randrange(-2, 3), h-200 + random.randrange(-2, 3)))
					parent.blit(random.choice(self.s_intro5), (self.intro5W + random.randrange(-2, 3), h-130 + random.randrange(-2, 3)))

		if self.ready:
			parent.blit(random.choice(self.s_objective), (self.objW + random.randrange(-2, 3), 10 + random.randrange(-2, 3)))
		if self.finished:
			parent.blit(self.s_aggmen, (w-400 + random.randrange(-2, 3), 200 + random.randrange(-2, 3)))

			count = helpers.Text.Create("Time: %s seconds" % str(self.time)[:4], 140, helpers.randomcolor())
			parent.blit(count, (w/2-count.get_width()/2 + random.randrange(-2, 3), h/2-90 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_outro1), (self.outro1W + random.randrange(-2, 3), h/2-140 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_outro2), (self.outro2W + random.randrange(-2, 3), h/2+70 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_outro3), (self.outro3W + random.randrange(-2, 3), h-110 + random.randrange(-2, 3)))
		elif self.started:
			parent.blit(self.s_mtdew, (- 50 + random.randrange(-10, 10), random.randrange(-10, 10)))
			parent.blit(self.s_mtdew, (w-450 + random.randrange(-10, 10), random.randrange(-10, 10)))
			parent.blit(self.s_doritos, (w/2-350 + random.randrange(-20, 20), h/2 - random.randrange(-10, 10)))
			count = helpers.Text.Create("Time: " + str(time.time() - self.epoch)[:4], 60, helpers.randomcolor())
			parent.blit(count, (w/2-count.get_width()/2 + random.randrange(-2, 3), h-90 + random.randrange(-2, 3)))
			count = helpers.Text.Create("rolls: %i/500" % self.fasts, 140, helpers.randomcolor())
			parent.blit(count, (w/2-count.get_width()/2 + random.randrange(-2, 3), h/2-80 + random.randrange(-2, 3)))

		if self.hitmarker[1] > 0:
				parent.blit(self.s_hitmarker, self.hitmarker[0])
