import helpers
import random, pygame, time

class sub(helpers.subBase):
	def OnStart(self):
		self.Sound.SetBGM("cookie")
		#self.Sound.SetBGM("scary")
		w, h = self.Game.window.get_size()
		#pygame.mouse.set_visible(False)
		#pygame.event.set_grab(True)

		self.s_objective = tuple(helpers.Text.Create("Cracky Clicker", 60, i) for i in [(255, 255, 255)] + list(helpers.colors))
		self.objW = w/2 - self.s_objective[0].get_width()/2

		self.s_intro = helpers.Text.Create("Hello there little pumpkin,", 40, (255, 255, 255))
		self.s_intro2 = helpers.Text.Create("Grandma's caught the munchies.", 40, (255, 255, 255))
		self.s_intro3 = helpers.Text.Create("Could you bake me some cookies?", 40, (255, 255, 255))
		self.s_intro4 = helpers.Text.Create("Click the left mousebutton as fast as you can!", 30, (160, 160, 160))
		self.s_intro5 = helpers.Text.Create("Click 2 start cooking!", 40, (160, 160, 160))

		self.s_finish = tuple(helpers.Text.Create("Holy fucking shit! Only", 60, i) for i in helpers.colors)
		self.finishW = self.s_finish[0].get_width()/2
		self.s_finish2 = tuple(helpers.Text.Create("Grandma: 420 cookies maggot. BLAZEIT!", 60, i) for i in helpers.colors)
		self.finish2W = self.s_finish2[0].get_width()/2
		self.s_finish3 = tuple(helpers.Text.Create("Click to continue", 40, i) for i in helpers.colors)
		self.finish3W = self.s_finish3[0].get_width()/2



		self.s_snoop = self.Sprites.LoadImageSequence("snoop.png")
		self.s_explosion = self.Sprites.LoadImageSequence("explosion.png")#71x100
		self.s_grandma = pygame.transform.scale(self.Sprites.LoadImage("grandma.png"), (int(h*0.848), int(h*0.848))); self.s_grandma.set_alpha(0)
		self.s_cookie = self.Sprites.LoadImage("cookie.png")#375x375
		self.s_weed = self.Sprites.LoadImage("weed.png")#260x274
		self.s_hitmarker = self.Sprites.LoadImage("hitmarker.png")
		self.hitmarker = [(0, 0), 0]

		self.started=False
		self.clicks = 0
		self.ready = False
		self.epoch = None
		self.finished = False
		self.time = None

		self.s_bg = pygame.transform.scale(self.Sprites.LoadImage("cooooookie.png"), (w, h))
		self.bg_color = (0, 0, 0)
		self.bg_step = 30
	def step(self, events):
		self.hitmarker[1] -= 1

		p = pygame.mixer.music.get_pos()
		if not self.started:
			if p < 2115:
				self.s_grandma.set_alpha(p*60/2115)
			else:
				self.s_grandma.set_alpha(None)
				self.ready = True
		else:
			self.bg_step += 1
			if self.bg_step >= 12:
				self.bg_step = 0
				old = self.bg_color
				while self.bg_color == old:
					self.bg_color = helpers.randomcolor()
					self.bg_color = (self.bg_color[0]/3, self.bg_color[1]/3, self.bg_color[2]/3)

			if p > 1918:
				self.s_bg.set_alpha(random.randrange(100, 135))

		if self.ready:
			for i in events:
				if i.type == pygame.MOUSEBUTTONDOWN:
					if i.button == 1:
						if self.finished:
							if time.time()-self.epoch > 1.5:
								self.Game.Start(6)
							continue
						if not self.started:
							self.started = True
							self.Sound.SetBGM("scary")
							self.epoch = time.time()
						self.clicks += 1
						x, y = i.pos
						self.Sound.PlaySFX("hitmarker")
						self.hitmarker = [(x-24, y-24), 5]

						if self.clicks == 50: self.Sound.PlaySFX("AIRHORN")
						if self.clicks == 100: self.Sound.PlaySound("NEVER DONE THAT")
						if self.clicks == 160: self.Sound.PlaySound("homuna")
						if self.clicks == 200: self.Sound.PlaySound("wombo combo")
						if self.clicks == 360: self.Sound.PlaySound("get noscoped")

						if self.clicks >= 420:
							w, h = self.Game.window.get_size()
							self.finished = True
							self.time = time.time() - self.epoch
							self.epoch = time.time()
							self.Sound.PlaySFX("shotgun")
							self.Sound.PlaySound("SMOKE WEED EVRYDAY")
							self.sprites.append(self.Sprites.sprite(self.s_snoop, (w-340, h-650), scale = 5))
							for _ in xrange(16):
								x = random.randrange(w-70)
								y = random.randrange(h-100)
								self.sprites.append(self.Sprites.sprite(self.s_explosion, (x, y), loop=False, scale=3))
							self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2-200), loop=False, scale=5))
							self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2, h/2-200), loop=False, scale=4))
							self.Game.scores["click"] = self.time

		self.stepSprites()
	def draw(self, parent):
		w, h = parent.get_size()
		p = pygame.mixer.music.get_pos()
		parent.fill(self.bg_color)

		if not self.started:
			if p >= 2115:
				parent.blit(self.s_bg, (0, 0))
				r = random.randrange(-1, 1) if not p // 300 % 7 else 0
				parent.blit(self.s_grandma, (-50 + r, h-h*0.848))
				self.drawSprites(parent)

				parent.blit(self.s_objective[0], (self.objW, 0))
				parent.blit(self.s_intro , (h*0.848 - 80 , h/2 - 120))
				parent.blit(self.s_intro2, (h*0.848 - 80, h/2-50))
				parent.blit(self.s_intro3, (h*0.848 - 80, h/2+20))
				parent.blit(self.s_intro4, (h*0.848 - 80, h-180))
				parent.blit(self.s_intro5, (h*0.848 - 80, h-130))
			else:
				parent.blit(self.s_grandma, (-50, h-h*0.848))
		elif self.finished:
			parent.blit(self.s_bg, (0, 0))
			parent.blit(self.s_grandma, (-100 + random.randrange(-5, 5), h-h*0.848))

			parent.blit(self.s_weed, (w/2-300 + random.randrange(-5, 5), h/2-400 + random.randrange(-5, 5)))
			parent.blit(self.s_weed, (w/2-500 + random.randrange(-5, 5), h/2-300 + random.randrange(-5, 5)))
			parent.blit(self.s_weed, (w/2-400 + random.randrange(-5, 5), h/2+200 + random.randrange(-5, 5)))
			parent.blit(self.s_weed, (w/2-100 + random.randrange(-5, 5), h/2+100 + random.randrange(-5, 5)))
			parent.blit(self.s_weed, (w/2+300 + random.randrange(-5, 5), h/2-420 + random.randrange(-5, 5)))
			parent.blit(self.s_weed, (w/2+500 + random.randrange(-5, 5), h/2+250 + random.randrange(-5, 5)))

			self.drawSprites(parent)

			x = random.randrange(-5, 5)
			y = random.randrange(-5, 5)
			parent.blit(self.s_cookie, (w/2-185 + x, h/2-185 + y))
			parent.blit(self.s_weed, (w/2-130 + x, h/2-162 + y))

			parent.blit(random.choice(self.s_finish), (w/2-self.finishW + random.randrange(-2, 3), h/2+-110 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_finish2), (w/2-self.finish2W + random.randrange(-2, 3), h/2+110 + random.randrange(-2, 3)))
			if time.time()-self.epoch > 1.5:
				parent.blit(random.choice(self.s_finish3), (w/2-self.finish3W + random.randrange(-2, 3), h-110 + random.randrange(-2, 3)))
			score = helpers.Text.Create(str(self.time)[:4] + " seconds!", 140, helpers.randomcolor())
			parent.blit(score, (w/2-score.get_width()/2 + random.randrange(-2, 3), h/2-60 + random.randrange(-2, 3)))

			parent.blit(random.choice(self.s_objective), (self.objW + random.randrange(-2, 3), random.randrange(-2, 3)))


		else:
			parent.blit(self.s_bg, (0, 0))
			parent.blit(random.choice(self.s_objective), (self.objW + random.randrange(-2, 3), random.randrange(-2, 3)))
			self.drawSprites(parent)

			if p < 1918:
				parent.blit(self.s_grandma, (-100 + random.randrange(-5, 5), h-h*0.848))
				parent.blit(self.s_cookie, (w/2-185 + random.randrange(-5, 5), h/2-185 + random.randrange(-5, 5)))
			else:
				parent.blit(self.s_grandma, (-100 + random.randrange(-60, 10), h-h*0.848))
				parent.blit(self.s_cookie, (w/2-185 + random.randrange(-20, 20), h/2-185 + random.randrange(-20, 20)))


			count = helpers.Text.Create(str(time.time() - self.epoch)[:4] + " seconds", 60, helpers.randomcolor())
			parent.blit(count, (w/2-count.get_width()/2 + random.randrange(-2, 3), h-100 + random.randrange(-2, 3)))

			count = helpers.Text.Create("%i/420 cookies" % self.clicks, 60, helpers.randomcolor())
			parent.blit(count, (w/2-count.get_width()/2 + random.randrange(-2, 3), h/2-40 + random.randrange(-2, 3)))

		if self.hitmarker[1] > 0:
				parent.blit(self.s_hitmarker, self.hitmarker[0])
