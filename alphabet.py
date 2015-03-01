# -*- encoding: UTF-8 -*-
import helpers
import random, pygame, time

class sub(helpers.subBase):
	def OnStart(self):
		self.Sound.SetBGM("sandstorm")
		w, h = self.Game.window.get_size()

		self.s_objective = tuple(helpers.Text.Create("Typing with DORA!", 60, i) for i in helpers.colors)
		self.objW = w/2 - self.s_objective[0].get_width()/2

		self.s_intro = tuple(helpers.Text.Create("dora: I can tyep better than u!", 60, i) for i in helpers.colors)
		self.introW = w/2 - self.s_intro[0].get_width()/2
		self.s_intro2 = tuple(helpers.Text.Create("u: 1v1 me bitch", 60, i) for i in helpers.colors)
		self.intro2W = w/2 - self.s_intro2[0].get_width()/2
		self.s_intro3 = tuple(helpers.Text.Create("dora:I bet you can't even alphabet!", 60, i) for i in helpers.colors)
		self.intro3W = w/2 - self.s_intro3[0].get_width()/2
		self.s_intro4 = tuple(helpers.Text.Create("Type the alphabet forwards and backwards as fast as you can!", 40, i) for i in helpers.colors)
		self.intro4W = w/2 - self.s_intro4[0].get_width()/2
		self.s_finish = tuple(helpers.Text.Create("You REKT Dora", 60, i) for i in helpers.colors)
		self.finishW = w/2 - self.s_finish[0].get_width()/2
		self.s_finish2 = tuple(helpers.Text.Create("dora: ...no...", 60, i) for i in helpers.colors)
		self.finish2W = w/2 - self.s_finish2[0].get_width()/2
		self.s_reminder = tuple(helpers.Text.Create("And backwards again!", 40, i) for i in helpers.colors)
		self.reminderW = w/2 - self.s_reminder[0].get_width()/2
		self.s_rekt = tuple(helpers.Text.Create("REKT", 50, i) for i in helpers.colors)

		self.s_start = tuple(helpers.Text.Create("Start with A!", 140, i) for i in helpers.colors)
		self.startW = w/2 - self.s_start[0].get_width()/2

		self.s_next = tuple(helpers.Text.Create("Click for next challenge", 40, i) for i in helpers.colors)
		self.nextW = w/2 - self.s_next[0].get_width()/2

		self.s_explosion = self.Sprites.LoadImageSequence("explosion.png")#71x100


		self.s_bg = pygame.transform.scale(self.Sprites.LoadImage("chalckboard.jpg"), (w, h)); self.s_bg.set_alpha(128)
		self.s_dora = self.Sprites.LoadImage("dora.png")

		self.progress = ""
		self.target = u"abcdefghijklmnopqrstuvwxyzyxwvutsrqponmlkjihgfedcba"
		#self.target = u"abc"
		self.started = False
		self.finished = False
		self.epoch = None

		self.time = None

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



		for i in events:
			if i.type == pygame.MOUSEBUTTONDOWN:
				if i.button == 1:
					if self.finished:
						w, h = self.Game.window.get_size()
						x, y = i.pos
						nx, ny = self.s_next[0].get_size()
						if -nx/2 < x - w/2 < nx/2 and h-150 < y < h-150+ny:
							self.Sound.mute()
							self.Game.Start(3)

			elif i.type == pygame.KEYDOWN:
				char = i.unicode.lower()
				if not self.finished:
					if char in self.target:
						if not self.started:
							if char == u"a":
								self.epoch = time.time()
								self.started = True
								self.Sound.PlaySound("wow")

						l = len(self.progress)
						if char == self.target[l]:
							self.progress += char
							self.Sound.PlaySFX("hitmarker")

							if self.target == self.progress:
								self.finished = True

								self.time = time.time() - self.epoch
								self.Game.scores["alphabet"] = self.time

								w, h = self.Game.window.get_size()
								self.Sound.PlaySFX("shotgun")
								self.Sound.PlaySFX("AIRHORN")
								self.Sound.PlaySound("get the camera")
								self.Sound.SetBGM("omg")

								self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2-200), loop=False, scale=4))
								self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2, h/2-200), loop=False, scale=3))
								self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2), loop=False, scale=2))

				else:
					pass

		self.stepSprites()
	def draw(self, parent):
		w, h = parent.get_size()
		parent.fill(self.bg_color)
		parent.blit(self.s_bg, (0, 0))

		self.drawSprites(parent)

		parent.blit(self.s_dora, (w-340 + random.randrange(-4, 5), h-500 + random.randrange(-4, 5)))

		if self.finished:
			score = helpers.Text.Create(str(self.time)[:4] + " seconds", 140, helpers.randomcolor())
			parent.blit(score, (w/2-score.get_width()/2 + random.randrange(-4, 5), h/2-60 + random.randrange(-4, 5)))
			parent.blit(random.choice(self.s_finish), (self.finishW + random.randrange(-2, 3), h/2-110 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_finish2), (self.finish2W + random.randrange(-2, 3), h/2+110 + random.randrange(-2, 3)))

			parent.blit(random.choice(self.s_rekt), (w-260 + random.randrange(-4, 5), h-400 + random.randrange(-4, 5)))

			parent.blit(random.choice(self.s_next), (self.nextW + random.randrange(-2, 3), h-150 + random.randrange(-2, 3)))
		elif self.started:
			progress = helpers.Text.Create(self.progress + "_", 30, helpers.randomcolor())
			parent.blit(progress, (w/2 - progress.get_width()/2, h/2-15))

			if len(self.progress) >= 26:
				parent.blit(random.choice(self.s_reminder), (self.reminderW + random.randrange(-2, 3), h/2-80 + random.randrange(-2, 3)))



			time.time() - self.epoch

			count = helpers.Text.Create(str(time.time() - self.epoch)[:4] + " seconds", 60, helpers.randomcolor())
			parent.blit(count, (w/2-count.get_width()/2 + random.randrange(-2, 3), h-100 + random.randrange(-2, 3)))

		else:
			parent.blit(random.choice(self.s_intro), (self.introW + random.randrange(-2, 3), h/2 - 130 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_intro2), (self.intro2W + random.randrange(-2, 3), h/2 -50 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_intro3), (self.intro3W + random.randrange(-2, 3), h/2 + 30 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_intro4), (self.intro4W + random.randrange(-2, 3), h/2 + 130 + random.randrange(-2, 3)))

			parent.blit(random.choice(self.s_start), (self.startW + random.randrange(-4, 5), h - 200 + random.randrange(-4, 5)))



		parent.blit(random.choice(self.s_objective), (self.objW + random.randrange(-2, 3), 10 + random.randrange(-2, 3)))
