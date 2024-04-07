import pygame, math, os

sector = pygame.image.load(os.path.join("assets", "sectore3.png"))
sector = pygame.transform.scale(sector, (200, 200))
sector  = pygame.transform.rotate(sector, 275)


def rotate_on_pivot(image, angle, pivot, origin):

    surf = pygame.transform.rotate(image, angle)
    
    offset = pivot + (origin - pivot).rotate(-angle)
    rect = surf.get_rect(center = offset)
    
    return surf, rect

class Sector(pygame.sprite.Sprite):
    def __init__(self, pivot):
        self.pivot = pivot
        self.pos = pivot + (70, 0)
        self.image_orig = sector
        self.image = self.image_orig
        self.rect = self.image.get_rect(center = self.pos)

        
    def update(self, surf):
        
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        
        mouse_offset = mouse_pos - self.pivot
        mouse_angle = -math.degrees(math.atan2(mouse_offset.y, mouse_offset.x))
        
        self.image, self.rect = rotate_on_pivot(self.image_orig, mouse_angle, self.pivot, self.pos)

        self.mask = pygame.mask.from_surface(self.image)
    
        surf.blit(self.image, self.rect)