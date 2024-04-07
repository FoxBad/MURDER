import pygame, os

redcross = pygame.image.load(os.path.join("assets", "redcross.png"))
redcross = pygame.transform.scale(redcross, (60, 60))

class RedCross(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.pos = pos
        self.image = redcross
        self.rect = self.image.get_rect(center = self.pos)
        

