import pygame,os
from pygame.locals import *

#button class
class Image():
	def __init__(self, x, y, image, scale, surface):
		self.image = pygame.image.load(os.path.join("assets", image))
		width = self.image.get_width()
		height = self.image.get_height()
		self.image = pygame.transform.scale(self.image, (scale[0], scale[1]))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.surface = surface
		self.surface.blit(self.image, (self.rect.x, self.rect.y))

