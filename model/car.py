import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_DECELERATION, 
    FROTTEMENT, BRAQUAGE_MAX, FACTEUR_DE_ROT, SEUIL_DERAPAGE, ADHERENCE_DERAPAGE,
    FROTTEMENT_DERAPAGE, SEUIL_SORTIE_DERAPAGE, CAR_REVERSE_ACCELERATION,
    CAR_BOOST_ACCELERATION, CAR_BOOST_DURATION, TRACTION_DEFAUT
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
        #proprietes du terrain sous la voitue, qui change avec set_grip
        self.seuil_derapage : float = SEUIL_DERAPAGE
        self.adherence_derapage : float = ADHERENCE_DERAPAGE
        self.frottement_derapage : float = FROTTEMENT_DERAPAGE
        #dernier point de passage pour les checkpoints
        self.checkpoint_x : float = self.x
        self.checkpoint_y : float = self.y
        self.checkpoint_angle : float = self.angle
        self.boost_timer : int = 0 # nombre d'images de boost restantes
        self.traction : float = TRACTION_DEFAUT

    def get_tile_position(self) -> tuple[int, int]:
        """ Renvoie la case de la grille ou se trouve la voiture (col, row)"""
        col = int(self.x // TILE_SIZE)
        row = int(self.y // TILE_SIZE)
        return col,row

    def set_grip(self, seuil: float, adherence: float, frottement: float, traction: float) -> None:
        """Donne a la voiture les proprietes du terrain ou elle est pour le derapage et la traction"""
        self.seuil_derapage = seuil
        self.adherence_derapage = adherence
        self.frottement_derapage = frottement
        self.traction = traction

    def set_checkpoint(self) -> None:
        """Retient la position actuel et l angle de la voiture au dernier passage"""
        self.checkpoint_x =self.x
        self.checkpoint_y =self.y
        self.checkpoint_angle =self.angle

    def respawn(self)-> None:
        """Remet la voiture au derniert point de passage"""
        self.x = self.checkpoint_x
        self.y = self.checkpoint_y
        self.angle = self.checkpoint_angle
        self.vx = 0.0 # remet ma voiture a l'arret
        self.vy = 0.0
        self.drifting = False

    def boost(self) -> None:
        """Lance un boost pendant CAR_BOOST_DURATION images"""
        self.boost_timer = CAR_BOOST_DURATION

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
        self.vx += self.traction * CAR_ACCELERATION * math.cos(rad)
        self.vy += self.traction * CAR_ACCELERATION * math.sin(rad)

    # ajout des methodes pour les autres touches et directions
    def brakes(self) -> None:
        """Freine si la voiture avance sinon elle recule"""
        rad = math.radians(self.angle)
        if self.forward_speed()>0 :
            force = CAR_DECELERATION
        else:
            # rendre la marcge arriere plus lente
            force = CAR_REVERSE_ACCELERATION
        
        self.vx -= self.traction * force * math.cos(rad)
        self.vy -= self.traction * force * math.sin(rad)

    def turn_left(self) -> None:
        """Braquage des roues vers la gauche"""
        self.steering_angle = -BRAQUAGE_MAX  # on suit le repere de pygame donc y pointe vers le bas
    
    def turn_right(self) -> None:
        """Braquage des roues vers la droite"""
        self.steering_angle = BRAQUAGE_MAX 

    def update_position(self) -> None:
        """Mets a jour la voiture a chaque image en prenant en compte le frottement, la rotation, derapage et le deplacement"""
        if self.boost_timer > 0 :
            rad = math.radians(self.angle)
            self.vx += CAR_BOOST_ACCELERATION * math.cos(rad)
            self.vy += CAR_BOOST_ACCELERATION * math.sin(rad)
            self.boost_timer -=1
        #frottement de l'air sur les deux composantes
        self.vx = self.vx * FROTTEMENT
        self.vy = self.vy * FROTTEMENT
        #la voiture tourne selon sa vitesse vers l'avant et le braquage
        v = self.forward_speed()
        self.angle += FACTEUR_DE_ROT * v * self.steering_angle
        # l entree en derapage 
        if not self.drifting and abs(v*self.steering_angle) > self.seuil_derapage :
            self.drifting = True
            print(" derapage ")
        rad = math.radians(self.angle)
        if self.drifting:
            self.vx = self.vx * self.frottement_derapage
            self.vy = self.vy * self.frottement_derapage
            v = self.forward_speed()
            self.vx += self.adherence_derapage* (v * math.cos(rad) - self.vx)
            self.vy += self.adherence_derapage * (v * math.sin(rad) - self.vy)
            if abs(self.lateral_speed()) < SEUIL_SORTIE_DERAPAGE and abs(v * self.steering_angle) <= self.seuil_derapage:
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
