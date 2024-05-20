import pygame, random, sector, math, redcross, os

class Player(pygame.sprite.Sprite):
    def __init__(self, sx, sy, vel, Ku, Kd, Kl, Kr, allspritegroup, groups, base_img, ws ,hs):
        super().__init__(allspritegroup)
        groups.add(self)

        self.x = 2200
        self.y = 2200
        self.pos = pygame.Vector2((self.x,self.y))
        self.sx = sx
        self.sy = sy 
        self.size = (sx, sy)
        self.vie = 1
        self.etat = True
        self.vel = vel
        self.role = self.choisir_role()  # Choix aléatoire du rôle
        self.assassinstat = False
        self.magestat = False
        self.Ku = Ku
        self.Kd = Kd
        self.Kl = Kl
        self.Kr = Kr
        self.bulletlist = pygame.sprite.Group()
        self.bullet = 3
        self.base_img = base_img
        self.image = pygame.transform.scale(self.base_img, (self.sx, self.sy))
        self.coins = 0
        self.rect = pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy)

        self.vectsize = pygame.Vector2((ws//2, hs//2))
        self.vectsect = pygame.Vector2(self.pos)
        self.sector = sector.Sector(self.vectsect, allspritegroup, self)



    def choisir_role(self):
        roles = ['innocent', "assassin", 'mage']
        poids_roles = [10, 1, 1]
        role = random.choices(roles, weights=poids_roles, k=1)[0]
        return role

    def update(self, collisiongroup):

        self.image = pygame.transform.scale(self.base_img, (self.sx, self.sy))

        
        if self.Kl != None:
            
            keys = pygame.key.get_pressed()

            self.prev_x, self.prev_y = self.x, self.y
                    
        
            if keys[self.Kl]:
                self.x -= self.vel
            if keys[self.Kr]:
                self.x += self.vel
            if keys[self.Ku]:
                self.y -= self.vel 
            if keys[self.Kd]:
                self.y += self.vel


            self.velx, self.vely = self.x - self.prev_x, self.y - self.prev_y

            
            #self.rect = pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy)
            #self.rect = pygame.draw.rect(screen, BLACK, pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy)
        

            for sprite in collisiongroup:
                if pygame.sprite.collide_rect(sprite, self):
                    self.x, self.y = self.prev_x, self.prev_y


    def orientation(self, ws ,hs):

        pos = pygame.mouse.get_pos()
        self.x_dist = pos[0] - ws//2
        self.y_dist = -(pos[1] - hs//2)
        self.angle = math.degrees(math.atan2(self.y_dist, self.x_dist))
        self.image  = pygame.transform.rotate(self.image, self.angle)
        self.rect  = self.image.get_rect(center = (self.x, self.y))

        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.Vector2((self.x,self.y))

    def roles(self, allspritegroup, ws ,hs): 
        if self.role == 'assassin':
            if self.assassinstat == True:
                allspritegroup.add(self.sector)
                self.managesector(ws ,hs)

            else: 
                allspritegroup.remove(self.sector)
                self.magestat == False


        if self.role == 'innocent':
            allspritegroup.remove(self.sector)
            self.assassinstat == False
            self.magestat == False

        if self.role == 'mage':
            allspritegroup.remove(self.sector)
            self.assassinstat == False

    def managesector(self, ws ,hs):
        self.vectsize = pygame.Vector2((ws//2, hs//2))
        self.vectsect = pygame.Vector2(self.pos)
        self.sector.update(self.vectsect, self.vectsize)

    def perdre_vie(self):
        self.vie -= 1
        if self.vie <=0:
            self.etat = False
        
    def checkalive(self, group, allspritegroup):
        if self.etat == False:
            redcross.RedCross(self.pos, allspritegroup ,group)
            self.sector.kill()
            self.kill()
