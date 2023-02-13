import pygame
from settings import *
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/test/player.png").convert_alpha()
        # Set the rectangle of the player & hit_box slightly smaller than the rectangle.
        self.rect = self.image.get_rect(topleft=position)
        self.hit_box = self.rect.inflate(0, -26)

        # Graphics setup.
        self.import_player_assets()
        # Default status of player for animations.
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15

        # Movement.
        # Create 2d vector for x & y coordinates, for player movement.
        self.direction = pygame.math.Vector2()
        # Initial speed of the player.
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

    # Get animations for player.
    def import_player_assets(self):
        character_path = "graphics/player/"
        # Dictionary of animations to display.
        self.animations = {"up": [], "down": [], "left": [], "right": [],
                           "right_idle": [], "left_idle": [], "up_idle": [], "down_idle": [],
                           "right_attack": [], "left_attack": [], "up_attack": [], "down_attack": []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking:
            # Movement input.
            # Store key press in variable.
            keys = pygame.key.get_pressed()
            # Options for direction change on y axis for up & down arrows.
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0
            # Options for direction change on x-axis for left & right arrows.
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            else:
                self.direction.x = 0

            # Attack input.
            if keys[pygame.K_SPACE]:
                self.attacking = True
                # Get the time of the attack.
                self.attack_time = pygame.time.get_ticks()
                print("attack")

            # Magic input.
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print("magic")

    def get_status(self):
        # Idle status.
        if self.direction.x == 0 and self.direction.y == 0:
            # Check if player is idle or attacking before changing status to idle.
            if "idle" not in self.status and "attack" not in self.status:
                self.status = self.status + "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if "attack" not in self.status:
                if "idle" in self.status:
                    # Overwrite idle.
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        # Player is not attacking, change status to remove attack.
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def move(self, speed):
        # Don't allow player to speed up if pressing multiple directions.
        # Need to check if not 0 to avoid throwing error.
        if self.direction.magnitude() != 0:
            # Normalize the vector back to 1 to not have unwanted speed increase.
            self.direction = self.direction.normalize()

        # Allow movement in all directions while checking for collisions using the hit_box.
        self.hit_box.x += self.direction.x * speed
        self.collision("horizontal")
        self.hit_box.y += self.direction.y * speed
        self.collision("vertical")
        # Center the rectangle with the hit_box.
        self.rect.center = self.hit_box.center

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                # if there is a collision between the player & obstacle rectangles.
                if sprite.hit_box.colliderect(self.hit_box):
                    # If the player is moving to the right.
                    if self.direction.x > 0:
                        # Have the player unable to move past the left of the obstacle.
                        self.hit_box.right = sprite.hit_box.left
                    # If the player is moving to the left.
                    if self.direction.x < 0:
                        self.hit_box.left = sprite.hit_box.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hit_box.colliderect(self.hit_box):
                    # Player moving down.
                    if self.direction.y > 0:
                        self.hit_box.bottom = sprite.hit_box.top
                    # Player moving up.
                    if self.direction.y < 0:
                        self.hit_box.top = sprite.hit_box.bottom

    # Cool downs for attacks and magic.
    def cool_downs(self):
        # Get current time to measure against attack time.
        current_time = pygame.time.get_ticks()

        # Basic timer for cool down on attacks.
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    # Create animations.
    def animate(self):
        # Get animation based on player's status.
        animation = self.animations[self.status]

        # Loop over the frame index, restart at 0 when grows too large.
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Set the image.
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hit_box.center)

    def update(self):
        self.input()
        self.cool_downs()
        self.get_status()
        self.animate()
        self.move(self.speed)
