import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_DECELERATION, 
    FROTTEMENT, BRAQUAGE_MAX, FACTEUR_DE_ROT, SEUIL_DERAPAGE, ADHERENCE_DERAPAGE,
    FROTTEMENT_DERAPAGE, SEUIL_SORTIE_DERAPAGE, CAR_REVERSE_ACCELERATION,
)


class Car:
    """Voiture du joueur avec sa position, vitesse (vx, vy), orientation, braquage et derapage."""
    def __init__(self, start_col: int, start_row: int, color : tuple):
        """Cree la voiture au centre de la case (start_col, start_row), a l'arret."""
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.vx : float = 0.0 # vitesse horizontale
        self.vy : float = 0.0 # vitesse verticale
        self.angle: float = 0.0
        self.color = color #couleur de la voiture
        self.sprite = self.build_sprite()
        self.steering_angle : float = 0.0  # braquage des roues (0 = roues droites)
        self.drifting : bool = False #True si la voiture est en train de deraper 
        

    def forward_speed(self) -> float :
        """Renvoie la vitesse vers l'avant, elle est négative en marche arriere"""
        rad = math.radians(self.angle)
        return self.vx * math.cos(rad) + self.vy * math.sin(rad)

    def lateral_speed(self) -> float: 
        """Renvoie la vitesse sur le coté perpendiculaire au nez, elle est nulle si la voiture ne glisse pas"""
        rad = math.radians(self.angle)
        return -self.vx * math.sin(rad) + self.vy * math.cos(rad)


    def accelerate(self) -> None:
        """Pousse la voiture vers l'avant"""
        rad = math.radians(self.angle)
        self.vx += CAR_ACCELERATION * math.cos(rad)
        self.vy += CAR_ACCELERATION * math.sin(rad)

    # ajout des methodes pour les autres touches et directions
    def brakes(self) -> None:
        """Freine si la voiture avance sinon elle recule"""
        rad = math.radians(self.angle)
        if self.forward_speed()>0 :
            force = CAR_DECELERATION
        else:
            # rendre la marcge arriere plus lente
            force = CAR_REVERSE_ACCELERATION
        
        self.vx -= force * math.cos(rad)
        self.vy -= force * math.sin(rad)

    def turn_left(self) -> None:
        """Braquage des roues vers la gauche"""
        self.steering_angle = -BRAQUAGE_MAX  # on suit le repere de pygame donc y pointe vers le bas
    
    def turn_right(self) -> None:
        """Braquage des roues vers la droite"""
        self.steering_angle = BRAQUAGE_MAX 

    def update_position(self) -> None:
        """Mets a jour la voiture a chaque image en prenant en compte le frottement, la rotation, derapage et le deplacement"""
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
        """ dessine l image de la voiture"""
        surf = pygame.Surface((CAR_HEIGHT, CAR_WIDTH), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0,CAR_HEIGHT,
                         CAR_WIDTH), border_radius=5)
        nez = 10
        pygame.draw.rect(surf,(255,255,0),(CAR_HEIGHT - nez, 0, nez, CAR_WIDTH))
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        """Renvoie l image de la voiture selon son angle et sa position"""
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
