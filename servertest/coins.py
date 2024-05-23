
import random, os, pygame

coinsimg = pygame.image.load(os.path.join("assets", "coins.png"))
coinsimg = pygame.transform.scale(coinsimg, (50, 50))

class CoinsC(pygame.sprite.Sprite):
    def __init__(self, allspritegroup, groups, rx ,ry):
        super().__init__(allspritegroup)
        groups.add(self)
        self.x = rx
        self.y = ry
        self.image = coinsimg
        self.rect = self.image.get_rect(center = (self.x,self.y))
    


