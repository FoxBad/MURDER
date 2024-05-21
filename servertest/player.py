import pygame, random, sector, math, redcross, os

class Player(pygame.sprite.Sprite):
    def __init__(self, allspritegroup, groups, base_img, ws ,hs, main, playerid):
        super().__init__(allspritegroup)
        groups.add(self)

        self.main = main

        self.playerid = playerid

        self.x = 2200
        self.y = 2200
        self.pos = (self.x,self.y)

        self.mpos = (0, 0)

        self.sx = 100
        self.sy = 100 
        self.size = (self.sx, self.sy)

        self.vie = 1

        self.vel = 4

        self.role = self.choisir_role()

        self.assassinstat = False
        self.magestat = False

        self.etat = True
        

        self.bulletlist = pygame.sprite.Group()
        self.bullet = 3

        self.base_img = base_img
        self.image = pygame.transform.scale(self.base_img, (self.sx, self.sy))
        self.rect = self.image.get_rect()

        self.coins = 0

        self.vectsize = pygame.Vector2((ws//2, hs//2))
        self.vpos = pygame.Vector2(self.pos)
        self.sector = sector.Sector(self.vpos, allspritegroup, self)

        self.data = {"state" : "INGAME", "playerid" : self.playerid ,"role": self.role, "pos": self.pos, "mpos": self.mpos, "assassinstat" : self.assassinstat, "magestat" : self.magestat, "etat" : self.etat}



    def choisir_role(self):
        roles = ['innocent', "assassin", 'mage']
        poids_roles = [10, 1, 1]
        role = random.choices(roles, weights=poids_roles, k=1)[0]
        return role

    def update(self, collisiongroup):

        self.image = pygame.transform.scale(self.base_img, (self.sx, self.sy))

        self.x = self.pos[0]
        self.y = self.pos[1]

        if self.main == True:
            
            keys = pygame.key.get_pressed()

            self.prev_x, self.prev_y = self.x, self.y
                    
            if keys[pygame.K_q]:
                self.x -= self.vel
            if keys[pygame.K_d]:
                self.x += self.vel
            if keys[pygame.K_z ]:
                self.y -= self.vel 
            if keys[pygame.K_s]:
                self.y += self.vel


            self.velx, self.vely = self.x - self.prev_x, self.y - self.prev_y
            
            self.pos = (self.x,self.y)
            self.vpos = pygame.Vector2(self.pos)

            
            #self.rect = pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy)
            #self.rect = pygame.draw.rect(screen, BLACK, pygame.Rect(self.x-self.sx/2, self.y-self.sy/2, self.sx, self.sy)
        

            for sprite in collisiongroup:
                if pygame.sprite.collide_rect(sprite, self):
                    self.x, self.y = self.prev_x, self.prev_y
            

    def update_data(self):
        self.data = {"state" : "INGAME", "playerid" : self.playerid ,"role": self.role, "pos": self.pos, "mpos": self.mpos, "assassinstat" : self.assassinstat, "magestat" : self.magestat, "etat" : self.etat}
                   


    def orientation(self, ws ,hs):
        
        if self.main == True:
            self.mpos = pygame.mouse.get_pos()

        self.x_dist = self.mpos[0] - ws//2
        self.y_dist = -(self.mpos[1] - hs//2)
        self.angle = math.degrees(math.atan2(self.y_dist, self.x_dist))
        self.image  = pygame.transform.rotate(self.image, self.angle)
        self.rect  = self.image.get_rect(center = (self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

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
        self.vpos = pygame.Vector2(self.pos)
        self.sector.update(self.vpos, self.vectsize, self.mpos)

    def perdre_vie(self):
        self.vie -= 1
        if self.vie <=0:
            self.etat = False
        
    def checkalive(self, group, allspritegroup):
        if self.etat == False:
            redcross.RedCross(self.pos, allspritegroup ,group)
            self.sector.kill()
            self.kill()
