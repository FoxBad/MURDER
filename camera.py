import pygame

class Camera(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

        self.offset = pygame.math.Vector2()

        self.floor_rect = pygame.Rect(0, 0, 4400, 4400)

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, player, layer1, layer2, surf, allspritegroup, ):

        self.display_surface = pygame.display.get_surface()

        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.center_target_camera(player)

        for tile in layer1:
            surf.blit(tile.image, tile.rect.topleft - self.offset)
        for tile in layer2:
            surf.blit(tile.image, tile.rect.topleft - self.offset)

        for sprite in allspritegroup:
            offset_pos = sprite.rect.topleft - self.offset
            surf.blit(sprite.image, offset_pos)