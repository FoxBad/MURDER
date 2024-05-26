import pygame, random, sector, math, redcross, os, bullet

seconds = 4

innocent = pygame.image.load(os.path.join("assets", "innocent.png"))
innocent  = pygame.transform.rotate(innocent, 90)

mage = pygame.image.load(os.path.join("assets", "mage.png"))
mage  = pygame.transform.rotate(mage, 90)

assassin = pygame.image.load(os.path.join("assets", "assassin.png"))
assassin  = pygame.transform.rotate(assassin, 90)

class Player(pygame.sprite.Sprite):
    def __init__(self, allspritegroup, groups, ws ,hs, x, y, main, playerid, role):
        super().__init__(allspritegroup)
        groups.add(self)

        self.main = main

        self.playerid = playerid
        self.currentPlayer = 1
        self.state = "WAIT"

        self.x = x
        self.y = y
        self.pos = (self.x,self.y)

        self.mpos = (0, 0)

        self.sx = 100
        self.sy = 100 
        self.size = (self.sx, self.sy)

        self.vie = 1

        self.vel = 6

        self.role = role

        self.assassinstat = False
        self.magestat = False

        self.etat = True
        
        self.cooldash = False

        self.bulletlist = pygame.sprite.Group()
        self.bullet = 3
        self.isshooting = False

        self.base_img = innocent
        self.image = pygame.transform.scale(self.base_img, (self.sx, self.sy))
        self.rect = self.image.get_rect()

        self.coins = 0

        self.vectsize = pygame.Vector2((ws//2, hs//2))
        self.vpos = pygame.Vector2(self.pos)
        self.sector = sector.Sector(self.vpos, allspritegroup, self)


        self.data = {"state" : self.state, "playerid" : self.playerid, "currentPlayer": self.currentPlayer,"role": self.role, "pos": self.pos, "mpos": self.mpos, "assassinstat" : self.assassinstat, "magestat" : self.magestat, "etat" : self.etat, "isshooting": self.isshooting}


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
       
            for sprite in collisiongroup:
                rect = sprite.rect
                if rect.collidepoint(self.rect.midbottom): 
                    if self.vely > 0: 
                        self.y -= self.vel
                if rect.collidepoint(self.rect.midtop): 
                    if self.vely < 0: 
                        self.y += self.vel
                if rect.collidepoint(self.rect.midright): 
                    if self.velx > 0: 
                        self.x -= self.vel 
                if rect.collidepoint(self.rect.midleft):
                    if self.velx < 0: 
                        self.x += self.vel 

            if self.x < 0 or self.y < 0 or self.x > 9600 or self.y > 9600:
                self.x, self.y = self.prev_x, self.prev_y

            self.vpos = pygame.Vector2(self.pos)
            self.pos = (self.x,self.y)
            self.rect  = self.image.get_rect(center = (self.x, self.y))
         
    def update_data(self):
        self.data = {"state" : self.state, "playerid" : self.playerid, "currentPlayer": self.currentPlayer ,"role": self.role, "pos": self.pos, "mpos": self.mpos, "assassinstat" : self.assassinstat, "magestat" : self.magestat, "etat" : self.etat, "isshooting": self.isshooting}
                   
    def isshoot(self, playergroup, allsprite, ws , hs):
        if self.isshooting == True and self.role == 'Assassin' and self.assassinstat == True:
            otherplayer = playergroup.copy()
            otherplayer.remove(self)
            
            for player2 in otherplayer:
                if pygame.sprite.collide_mask(self.sector, player2):
                    player2.perdre_vie()
            self.isshooting = False
            
        
        if self.isshooting == True and self.role == 'Mage' and self.magestat == True:
            bullet.Bullet(self, allsprite, self.bulletlist, ws ,hs)
            self.bullet -= 1

            self.isshooting = False

    def orientation(self, ws ,hs):
        
        if self.main == True:
            self.mpos = pygame.mouse.get_pos()

        self.x_dist = self.mpos[0] - ws//2
        self.y_dist = -(self.mpos[1] - hs//2)
        self.angle = math.degrees(math.atan2(self.y_dist, self.x_dist))
        self.image  = pygame.transform.rotate(self.image, self.angle)
        self.rect  = self.image.get_rect(center = (self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
    
    def dash(self, ws ,hs):
       
        self.destx, self.desty = self.mpos
        vect = (self.destx - ws//2, self.desty - hs//2)
        angle = math.atan2(vect[1], vect[0])
        self.change_x = math.cos(angle) * 500
        self.change_y = math.sin(angle) * 500

        self.x += self.change_x
        self.y += self.change_y

        self.vpos = pygame.Vector2(self.pos)
        self.pos = (self.x,self.y)
        self.rect  = self.image.get_rect(center = (self.x, self.y))

        self.cooldash = True







    def roles(self, allspritegroup, ws ,hs): 

        if self.role == 'Assassin':
            if self.assassinstat == True:
                self.base_img = assassin
                allspritegroup.add(self.sector)
                self.managesector(ws ,hs)

            else: 
                allspritegroup.remove(self.sector)
                self.base_img = innocent
                

        if self.role == 'Innocent':
            allspritegroup.remove(self.sector)
            self.base_img = innocent
            self.magestat == False
            self.assassinstat == False


        if self.role == 'Mage':
            allspritegroup.remove(self.sector)
            if self.magestat == True:
                self.base_img = mage
            else:
                self.base_img = innocent



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
