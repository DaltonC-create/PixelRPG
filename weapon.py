import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        # Drop the _ and chars after to only get the direction for the weapon's view.
        direction = player.status.split("_")[0]

        # Graphic based on the selected weapon and direction of the character.
        full_path = f"graphics/weapons/{player.weapon}/{direction}.png"
        self.image = pygame.image.load(full_path).convert_alpha()

        # Placement of weapon according to direction of character and rectangle of character.
        if direction == "right":
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == "left":
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == "up":
            self.rect = self.image.get_rect(midright=player.rect.midtop + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midright=player.rect.midbottom + pygame.math.Vector2(-10, 0))
