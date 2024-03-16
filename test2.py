import pygame
import sys, os

# Initialisation de Pygame
pygame.init()

# Définition de la taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotation d'image avec Pygame")

# Chargement de l'image à faire tourner
image = pygame.image.load(os.path.join("assets", "ino.png"))
image_rect = image.get_rect()

# Point de pivot initial au centre de l'image
pivot = (image_rect.right, image_rect.centery)
# Fonction pour faire tourner l'image autour du pivot en fonction de la position de la souris
def rotate_image(angle):
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=image_rect.center)
    screen.blit(rotated_image, rotated_rect.topleft)

# Boucle principale du jeu
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calcul de l'angle de rotation en fonction de la position de la souris
    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle = pygame.math.Vector2(mouse_x - pivot[0], mouse_y - pivot[1]).angle_to(pygame.math.Vector2(0, 0))

    # Effacement de l'écran
    screen.fill((255, 255, 255))

    # Affichage de l'image tournée
    rotate_image(angle)

    # Rafraîchissement de l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
