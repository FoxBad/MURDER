import pygame, os

redcross = pygame.image.load(os.path.join("assets", "redcross.png"))
redcross = pygame.transform.scale(redcross, (60, 60))

class RedCross(pygame.sprite.Sprite):
    def __init__(self, pos, allspritegroup, groups):
        super().__init__(allspritegroup)
        groups.add(self)
        self.pos = pos
        self.image = redcross
        self.rect = self.image.get_rect(center = self.pos)
        

