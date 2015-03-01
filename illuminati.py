import helpers
import random, pygame, time

class sub(helpers.subBase):
	def OnStart(self):
		self.Sound.SetBGM("spoopy")
		w, h = self.Game.window.get_size()

		self.s_bg = pygame.transform.scale(self.Sprites.LoadImage("chalckboard.jpg"), (w, h)); self.s_bg.set_alpha(128)
		self.s_dora = pygame.transform.scale(self.Sprites.LoadImage("dora.png"), (340*4, 500*4))
		self.s_spook = self.Sprites.LoadImage("spook.png")
		self.s_illuminati = self.Sprites.LoadImage("illuminati.png"); self.s_illuminati.set_alpha(0)


		self.s_text1 = helpers.Text.Create("Wait, did you catch that?", 70, (255, 255, 255))
		self.s_text2 = helpers.Text.Create("I sense some real paranormal rektivity here", 50, (255, 255, 255))
		self.s_text3 = helpers.Text.Create("Let's look again...", 70, (255, 255, 255))
		self.s_text4 = helpers.Text.Create("Dora comfirmed as one true god", 70, (255, 255, 255))
		self.s_text5 = tuple(helpers.Text.Create("God got REKT!", 140, i) for i in helpers.colors)

		self.epoch = time.time()

		self.soundcue = False
		self.bg_color = (0, 0, 0)
	def step(self, events):
		if time.time() - self.epoch > 12.5:
			if not self.soundcue:
				self.Sound.SetBGM(None)
				self.Sound.PlaySFX("AIRHORN")
				self.Sound.PlaySound("wow")
				self.soundcue = True
			self.bg_color = helpers.randomcolor()
		if time.time() - self.epoch > 13.5:
			self.Game.Start(4)
			return


		self.stepSprites()
	def draw(self, parent):
		w, h = parent.get_size()
		parent.fill(self.bg_color)


		t = time.time() - self.epoch

		if t > 12.5:
			v = self.s_text5[0].get_width()
			parent.blit(random.choice(self.s_text5), (w/2-v/2 + random.randrange(-4, 5), h/2-70 + random.randrange(-4, 5)))
		elif t > 10.5:
			v = self.s_text4.get_width()
			parent.blit(self.s_text4, (w/2-v/2, h/2-30))
		elif t > 7.5:
			parent.blit(self.s_bg, (0, 0))
			parent.blit(self.s_dora, (0, -300))


			self.s_illuminati.set_alpha(int(min((max((t - 8.5, 0)), 2))/2.0*255))
			parent.blit(self.s_illuminati, (526, 341))
		elif t > 6:
			parent.blit(self.s_spook, (0, h-300))
			v = self.s_text3.get_width()
			parent.blit(self.s_text3, (w/2-v/2, h/2-30))
		elif t > 2.5:
			parent.blit(self.s_spook, (0, h-300))
			v = self.s_text2.get_width()
			parent.blit(self.s_text2, (w/2-v/2, h/2-30))
		else:
			v = self.s_text1.get_width()
			parent.blit(self.s_text1, (w/2-v/2, h/2-30))

		self.drawSprites(parent)
