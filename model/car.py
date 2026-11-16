import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_DECELERATION, 
    FROTTEMENT, BRAQUAGE_MAX, FACTEUR_DE_ROT, SEUIL_DERAPAGE, ADHERENCE_DERAPAGE,
    FROTTEMENT_DERAPAGE, SEUIL_SORTIE_DERAPAGE
)


class Car:

    def __init__(self, start_col: int, start_row: int):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        #self.speed: float = 0.0
        self.vx : float = 0.0 # vitesse horizontale
        self.vy : float = 0.0 # vitesse verticale
        self.angle: float = 0.0
        self.sprite = self.build_sprite()
        self.steering_angle : float = 0.0  # braquage des roues (0 = roues droites)
        self.drifting : bool = False #True si la voiture est en train de deraper 

    def forward_speed(self) -> float :
        #vitesse dans le sens du nez de la voiture
        rad = math.radians(self.angle)
        return self.vx * math.cos(rad) + self.vy * math.sin(rad)

    def lateral_speed(self) -> float: 
        # la vitesse sur le cote
        # elle est a 0 quand la voiture ne derape pas
        rad = math.radians(self.angle)
        return -self.vx * math.sin(rad) + self.vy * math.cos(rad)


    def accelerate(self) -> None:
        #self.speed +=  CAR_ACCELERATION
        rad = math.radians(self.angle)
        self.vx += CAR_ACCELERATION * math.cos(rad)
        self.vy += CAR_ACCELERATION * math.sin(rad)
    # ajout des methodes pour les autres touches et directions
    def brakesR(self):
        #self.speed -= CAR_DECELERATION
        rad = math.radians(self.angle)
        self.vx -= CAR_DECELERATION * math.cos(rad)
        self.vy -= CAR_DECELERATION * math.sin(rad)
    def turnLeft(self):
        self.steering_angle = -BRAQUAGE_MAX  # on suit le repere de pygame donc y pointe vers le bas
    def turnRight(self):
        self.steering_angle = BRAQUAGE_MAX 

    def update_position(self) -> None:
        #frottement de l'air sur les deux composantes
        self.vx = self.vx * FROTTEMENT
        self.vy = self.vy * FROTTEMENT
        #la voiture tourne selon sa vitesse vers l'avant et le braquage
        v = self.forward_speed()
        self.angle += FACTEUR_DE_ROT * v * self.steering_angle
        # l entree en derapage 
        if not self.drifting and abs(v*self.steering_angle) > SEUIL_DERAPAGE :
            self.drifting = True
            print(" derapage ")
        rad = math.radians(self.angle)
        if self.drifting:
            self.vx = self.vx * FROTTEMENT_DERAPAGE
            self.vy = self.vy * FROTTEMENT_DERAPAGE
            v = self.forward_speed()
            self.vx += ADHERENCE_DERAPAGE * (v * math.cos(rad) - self.vx)
            self.vy += ADHERENCE_DERAPAGE * (v * math.sin(rad) - self.vy)
            if abs(self.lateral_speed()) < SEUIL_SORTIE_DERAPAGE and abs(v * self.steering_angle) <= SEUIL_DERAPAGE:
                self.drifting = False # sortir de derapage
                print("fin de derapage")
        else:
            # en adherence la vitesse suit exactement le nez
            self.vx = v * math.cos(rad)
            self.vy = v * math.sin(rad)
    
        self.x += self.vx
        self.y += self.vy
        self.steering_angle = 0.0
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
