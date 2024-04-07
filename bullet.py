import pygame, math, os

fireball = pygame.image.load(os.path.join("assets", "fireball.png"))
fireball = pygame.transform.scale(fireball, (20, 20))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, tireur, groups):
        super().__init__(groups)
        self.tireur = tireur
        self.x = tireur.x
        self.y = tireur.y
        self.image = fireball
        self.destx, self.desty = pygame.mouse.get_pos()
        self.speed = 20  
        
        vect = (self.destx - self.x, self.desty - self.y)
        angle = math.atan2(vect[1], vect[0])
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed


    def update(self, surf):

        self.x += self.change_x
        self.y += self.change_y

        self.rect = self.image.get_rect(center=(self.x,self.y))        
        surf.blit(self.image, self.rect)