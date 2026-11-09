import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_DECELERATION, CAR_ROTATION_SPEED
)


class Car:

    def __init__(self, start_col: int, start_row: int):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
        self.speed += CAR_ACCELERATION
    # ajout des methodes pour les autres touches et directions
    def brakesR(self):
        self.speed -= CAR_DECELERATION
    def turnLeft(self):
        self.angle -= CAR_ROTATION_SPEED # on suit le repere de pygame donc y pointe vers le bas
    def turnRight(self):
        self.angle += CAR_ROTATION_SPEED

    def update_position(self) -> None:
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

    def build_sprite(self) -> pygame.Surface:
        surf = pygame.Surface((CAR_HEIGHT, CAR_WIDTH), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0,CAR_HEIGHT,
                         CAR_WIDTH), border_radius=5)
        nez = 10
        pygame.draw.rect(surf,(255,255,0),(CAR_HEIGHT - nez, 0, nez, CAR_WIDTH))
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
