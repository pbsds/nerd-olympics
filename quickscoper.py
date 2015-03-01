import helpers
import random, pygame, time

class sub(helpers.subBase):
	def OnStart(self):
		self.Sound.SetBGM("died this way")
		w, h = self.Game.window.get_size()

		self.s_objective = tuple(helpers.Text.Create("MLG QUICKSCOPING LEAGUE", 60, i) for i in helpers.colors)
		self.objW = self.s_objective[0].get_width()/2

		self.s_intro = tuple(helpers.Text.Create("You ready for some QUICKSCOPING!?!?11", 60, i) for i in helpers.colors)
		self.intoW = self.s_intro[0].get_width()/2
		self.s_intro2 = tuple(helpers.Text.Create("Shoot the targets so quick you can!", 60, i) for i in helpers.colors)
		self.into2W = self.s_intro2[0].get_width()/2

		self.s_finish = tuple(helpers.Text.Create("Your Score:", 60, i) for i in helpers.colors)
		self.finishW = self.s_finish[0].get_width()/2
		self.s_finish2 = tuple(helpers.Text.Create("Elite snipers can't even!", 60, i) for i in helpers.colors)
		self.finish2W = self.s_finish2[0].get_width()/2

		self.s_next = tuple(helpers.Text.Create("Click for next challenge", 40, i) for i in helpers.colors)
		self.nextW = w/2 - self.s_next[0].get_width()/2

		self.s_explosion = self.Sprites.LoadImageSequence("explosion.png")#71x100
		self.s_villains = self.Sprites.LoadImageSequence("villains.png")#180x180
		self.s_villain = self.s_villains[0]

		self.s_bg = pygame.transform.scale(self.Sprites.LoadImage("dedust.jpg"), (w, h)); self.s_bg.set_alpha(128)
		self.s_target = self.Sprites.LoadImage("target.png")
		self.s_mtdew = self.Sprites.LoadImage("mtdew.png")
		self.s_doritos = self.Sprites.LoadImage("doritos.png")
		self.s_hitmarker = self.Sprites.LoadImage("hitmarker.png")
		self.hitmarker = [(0, 0), 0]

		self.target = [-500, -500]
		self.epoch = time.time()
		self.hits = 0
		self.countdown = True
		self.done = False


		self.bg_color = (0, 0, 0)
		self.bg_step = 0
	def step(self, events):
		self.bg_step += 1
		if self.bg_step >= 12:
			self.bg_step = 0
			old = self.bg_color
			while self.bg_color == old:
				self.bg_color = helpers.randomcolor()
				self.bg_color = (self.bg_color[0]/3, self.bg_color[1]/3, self.bg_color[2]/3)

		if self.countdown:
			if 5 - (time.time() - self.epoch) <= 0:
				self.countdown = False
				self.epoch = time.time()#reset epoch

				w, h = self.Game.window.get_size()
				self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2-200), loop=False, scale=4))
				self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2, h/2-200), loop=False, scale=3))
				self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2), loop=False, scale=2))

				self.Sound.PlaySFX("shotgun")
				self.Sound.PlaySFX("AIRHORN")
				self.Sound.PlaySound("homuna")


				self.target[0] = random.randrange(0, w-180)
				self.target[1] = random.randrange(0, h-180)
		elif not self.done:
			if 25 - (time.time() - self.epoch) <= 0:
				self.done = True
				self.Game.scores["quickscoper"] = self.hits
				self.Sound.PlaySFX("shotgun")
				self.Sound.PlaySound("i shot him short")

				w, h = self.Game.window.get_size()
				self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2-200), loop=False, scale=4))
				self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2, h/2-200), loop=False, scale=3))
				self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2), loop=False, scale=2))
		self.hitmarker[1] -= 1

		for i in events:
			#if i.type == pygame.MOUSEMOTION:
			#	x, y = i.pos
			#	w, h = self.Game.window.get_size()

			if i.type == pygame.MOUSEBUTTONDOWN:
				if i.button == 1:
					x, y = i.pos
					tx, ty = self.target

					self.Sound.PlaySFX("hitmarker")
					self.hitmarker = [(x-24, y-24), 5]
					if self.done:
						w, h = self.Game.window.get_size()
						nx, ny = self.s_next[0].get_size()
						if -nx/2 < x - w/2 < nx/2 and h-150 < y < h-150+ny:
							self.Game.Start(2)
						continue
					if tx <= x < tx+180 and ty <= y < ty+180:#REKTangle BITCH!
						w, h = self.Game.window.get_size()

						self.sprites.append(self.Sprites.sprite(self.s_explosion, (tx, ty), loop=False, scale=2))
						self.hits += 1
						self.target[0] = random.randrange(0, w-180)
						self.target[1] = random.randrange(0, h-180)
						self.s_villain = random.choice(self.s_villains)

						if self.hits == 10:
							self.s_villain = self.s_villains[10]#ensure osama
						if self.hits == 11:
							self.Sound.PlaySound("wombo combo")
							self.Sound.PlaySFX("shotgun")
							self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2-200), loop=False, scale=4))
							self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2, h/2-200), loop=False, scale=3))
							self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2), loop=False, scale=2))




		self.stepSprites()
	def draw(self, parent):
		w, h = parent.get_size()
		parent.fill(self.bg_color)
		parent.blit(self.s_bg, (0, 0))

		self.drawSprites(parent)

		if self.countdown:
			count = helpers.Text.Create(str(5 - (time.time() - self.epoch))[:4], 140, helpers.randomcolor())
			parent.blit(count, (w/2-count.get_width()/2 + random.randrange(-2, 3), h/2-90 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_intro), (w/2-self.intoW + random.randrange(-2, 3), h/2+80 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_intro2), (w/2-self.into2W + random.randrange(-2, 3), h/2+150 + random.randrange(-2, 3)))
		elif not self.done:
			parent.blit(self.s_target, self.target)
			if self.hits >= 10: parent.blit(self.s_villain, self.target)

			hits = helpers.Text.Create("Killcount: %i" % self.hits, 60, helpers.randomcolor())
			parent.blit(hits, (random.randrange(-2, 3), h-100+random.randrange(-2, 3)))

			count = helpers.Text.Create("Time left: " + str(25 - (time.time() - self.epoch))[:4], 60, helpers.randomcolor())
			parent.blit(count, (w/2-count.get_width()/2 + random.randrange(-2, 3), h-100 + random.randrange(-2, 3)))
		else:
			parent.blit(random.choice(self.s_finish), (w/2-self.finishW + random.randrange(-2, 3), h/2+-110 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_finish2), (w/2-self.finish2W + random.randrange(-2, 3), h/2+110 + random.randrange(-2, 3)))

			hits = helpers.Text.Create("%i trickshots" % self.hits, 140, helpers.randomcolor())
			parent.blit(hits, (w/2-hits.get_width()/2 + random.randrange(-2, 3), h/2-60 + random.randrange(-2, 3)))


			parent.blit(random.choice(self.s_next), (self.nextW + random.randrange(-2, 3), h-150 + random.randrange(-2, 3)))



		if self.hitmarker[1] > 0:
				parent.blit(self.s_hitmarker, self.hitmarker[0])

		parent.blit(random.choice(self.s_objective), (w/2-self.objW + random.randrange(-2, 3), 30 + random.randrange(-2, 3)))
