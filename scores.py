import helpers
import random, pygame, os

class sub(helpers.subBase):
	def OnStart(self):
		quickscoper = self.Game.scores["quickscoper"]
		alphabet = self.Game.scores["alphabet"]
		scroll = self.Game.scores["scroll"]
		click = self.Game.scores["click"]
		self.score = int((quickscoper*1000./50. + 2000-alphabet*1000./25. + 2000-scroll*1000./30. + 2000-click*1000./40.)*2)

		self.s_text = tuple(helpers.Text.Create("Your score:", 100, i) for i in helpers.colors)
		self.s_text2 = tuple(helpers.Text.Create("%s targets in 25 seconds!" % quickscoper, 60, i) for i in helpers.colors)
		self.s_text3 = tuple(helpers.Text.Create("57 characters in %s seconds!" % str(alphabet)[:4], 60, i) for i in helpers.colors)
		self.s_text4 = tuple(helpers.Text.Create("500 scrolls in %s seconds!" % str(scroll)[:4], 60, i) for i in helpers.colors)
		self.s_text5 = tuple(helpers.Text.Create("420 clicks in %s seconds!" % str(click)[:4], 60, i) for i in helpers.colors)
		self.s_text6 = tuple(helpers.Text.Create("Verdict: %s points" % self.score, 100, i) for i in helpers.colors)
		self.textW  = self.s_text [0].get_width()/2
		self.text2W = self.s_text2[0].get_width()/2
		self.text3W = self.s_text3[0].get_width()/2
		self.text4W = self.s_text4[0].get_width()/2
		self.text5W = self.s_text5[0].get_width()/2
		self.text6W = self.s_text6[0].get_width()/2



		self.s_euphoric = self.Sprites.LoadImageSequence("euphoric.png")
		self.s_frog = self.Sprites.LoadImageSequence("frog.png")
		self.s_explosion = self.Sprites.LoadImageSequence("explosion.png")

		self.sprites.append(self.Sprites.sprite(self.s_euphoric, (1050, 244)))
		self.sprites.append(self.Sprites.sprite(self.s_frog, (470, 541), scale=3))
		w, h = self.Game.window.get_size()
		for _ in xrange(16):
			x = random.randrange(w-70*3)
			y = random.randrange(h-100*3)
			self.sprites.append(self.Sprites.sprite(self.s_explosion, (x, y), loop=False, scale=3))
		self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2-200), loop=False, scale=5))
		self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2, h/2-200), loop=False, scale=4))

		self.name = ""
		self.type = True

		self.s_bg = pygame.transform.scale(self.Sprites.LoadImage("mlg.png"), (w, h)); self.s_bg.set_alpha(200)
		self.bg_color = (0, 0, 0)
		self.bg_step = 30
		self.Sound.SetBGM("fiilis")
		self.Sound.PlaySFX("shotgun")
		self.Sound.PlaySound("OMG NO WAY")
		self.Sound.PlaySound("inception")
	def step(self, events):
		self.bg_step += 1
		if self.bg_step >= 8:
			self.bg_step = 0
			old = self.bg_color
			while self.bg_color == old:
				self.bg_color = helpers.randomcolor()
				self.bg_color = (self.bg_color[0]/3, self.bg_color[1]/3, self.bg_color[2]/3)

		for i in events:
			if i.type == pygame.KEYDOWN:
				if self.type:
					char = i.unicode
					if char in "\r\n\b\t":
						if char == "\b":
							self.name = self.name[:-1]
							self.Sound.PlaySFX("hitmarker")
						elif char in "\r\n" and len(self.name):
							self.type = False

							self.Sound.PlaySFX("shotgun")
							self.Sound.PlaySound("scream")
							w, h = self.Game.window.get_size()
							for _ in xrange(16):
								x = random.randrange(w-70*3)
								y = random.randrange(h-100*3)
								self.sprites.append(self.Sprites.sprite(self.s_explosion, (x, y), loop=False, scale=3))
							self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2-142, h/2-200), loop=False, scale=5))
							self.sprites.append(self.Sprites.sprite(self.s_explosion, (w/2, h/2-200), loop=False, scale=4))

							fname = os.environ.get("HOME") + "/nerd-olympics-scores.txt"
							if os.path.isfile(fname):
								f = open(fname, "r")
								data = f.read()
								f.close()
							else:
								data = None
							if data:
								scores = list((i.split("\t")[0].strip(), int(i.strip().split("\t")[1])) for i in data.split("\n") if i.strip())
							else:
								scores = [
								    ("pbsds",     8972),
								    ("pbsds",     8442),
								    ("pbsds",     7143),
								    ("not pbsds", 6116)
								]


							scores.append((self.name, self.score))
							scores = sorted(scores, key=lambda x: -x[1])

							f = open(fname, "w")
							f.write("\r\n".join("%s\t%i"%i for i in scores))
							f.close()

							self.highscores = []
							for entry in scores[:10]:
								surf = tuple(helpers.Text.Create("%s: %i points" % entry, 50, i) for i in helpers.colors)
								self.highscores.append((surf, surf[0].get_width()))

					else:
						self.name += char
						self.Sound.PlaySFX("hitmarker")
				else:
					if i.unicode in "\r\n":
						self.Sound.mute()
						self.Game.Start(0)

		self.stepSprites()
	def draw(self, parent):
		w, h = parent.get_size()
		parent.fill(self.bg_color)
		parent.blit(self.s_bg, (0, 0))

		self.drawSprites(parent)

		if self.type:
			parent.blit(random.choice(self.s_text ), (w/2-self.textW  + random.randrange(-2, 3), h/2-290 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_text2), (w/2-self.text2W + random.randrange(-2, 3), h/2 -170 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_text3), (w/2-self.text3W + random.randrange(-2, 3), h/2 -100 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_text4), (w/2-self.text4W + random.randrange(-2, 3), h/2 -30  + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_text5), (w/2-self.text5W + random.randrange(-2, 3), h/2 +40 + random.randrange(-2, 3)))
			parent.blit(random.choice(self.s_text6), (w/2-self.text6W + random.randrange(-2, 3), h/2 +110 + random.randrange(-2, 3)))


			name = helpers.Text.Create("Write your name: %s_" % self.name, 40, helpers.randomcolor())
			parent.blit(name, (w/2 - name.get_width()/2, h-100))
		else:
			for i, (surfs, width) in enumerate(self.highscores):
				parent.blit(random.choice(surfs), (w/2 + 400-width  + random.randrange(-2, 3), h/2-300 + 60*i + random.randrange(-2, 3)))
