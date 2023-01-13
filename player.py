import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

        # Create 2d vector for x & y coordinates, for player movement.
        self.direction = pygame.math.Vector2()
        # Initial speed of the player.
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        # Store key press in variable.
        keys = pygame.key.get_pressed()
        # Options for direction change on y axis for up & down arrows.
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        # Options for direction change on x-axis for left & right arrows.
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, speed):
        # Don't allow player to speed up if pressing multiple directions.
        # Need to check if not 0 to avoid throwing error.
        if self.direction.magnitude() != 0:
            # Normalize the vector back to 1 to not have unwanted speed increase.
            self.direction = self.direction.normalize()

        # Allow movement in all directions while checking for collisions.
        self.rect.x += self.direction.x * speed
        self.collision("horizontal")
        self.rect.y += self.direction.y * speed
        self.collision("vertical")

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                # if there is a collision between the player & obstacle rectangles.
                if sprite.rect.colliderect(self.rect):
                    # If the player is moving to the right.
                    if self.direction.x > 0:
                        # Have the player unable to move past the left of the obstacle.
                        self.rect.right = sprite.rect.left
                    # If the player is moving to the left.
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    # Player moving down.
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    # Player moving up.
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.move(self.speed)
