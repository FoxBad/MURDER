import pygame,os
from pygame.locals import *


#button class
class Button():
	def __init__(self, x, y, image, scale):
		self.image = pygame.image.load(os.path.join("assets", image))
		width = self.image.get_width()
		height = self.image.get_height()
		self.image = pygame.transform.scale(self.image, (scale[0], scale[1]))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action