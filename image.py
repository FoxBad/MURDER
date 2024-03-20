import pygame,os
from pygame.locals import *

#button class
class Image():
	def __init__(self, x, y, image, scale):
		self.image = pygame.image.load(os.path.join("assets", image))
		width = self.image.get_width()
		height = self.image.get_height()
		self.image = pygame.transform.scale(self.image, (scale[0], scale[1]))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def draw(self, surface):

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

