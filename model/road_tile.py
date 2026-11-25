import pygame
from constants import TILE_SIZE
from model.terrain import Terrain 


class RoadTile:

    def __init__(self, col: int, row: int, terrain:Terrain):
        self.col = col
        self.row = row
        self.terrain = terrain
        self.sprite: pygame.Surface | None = None

    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        if self.sprite and self.sprite.get_width() == tile_size:
            return self.sprite
        surface = pygame.Surface((tile_size, tile_size))
        surface.fill(self.terrain.color)
        r, g, b = self.terrain.color
        border = (max(r - 20, 0), max(g - 20, 0), max(b - 20, 0))
        pygame.draw.rect(surface, border, surface.get_rect(), 1)
    
        self.sprite = surface
        return self.sprite
