WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

CAR_ACCELERATION = 0.05
CAR_DECELERATION = 0.07 #ajouter pour utiliser les freins et la marche arriere dans brakes
CAR_WIDTH = 30
CAR_HEIGHT = 50
FROTTEMENT = 0.98
BRAQUAGE_MAX = 30 #angle de braquage max des roues
FACTEUR_DE_ROT = 0.02 #un facteur pour ajuster la vitesse de rotation
SEUIL_DERAPAGE = 60 #si la vitesse * braqauge depasse le seuil la voiture derape
ADHERENCE_DERAPAGE = 0.05 #part de la vitesse realignee sur le nez a chaque image en derapage
SEUIL_SORTIE_DERAPAGE = 0.1    # fin du derapage si la vitesse laterale passe sous ce seuil
FROTTEMENT_DERAPAGE = 0.98
CAR_REVERSE_ACCELERATION = 0.03 # acceleration en marche arriere plus faible qu en avant

CAR_COLOR_P1 = (255, 0, 0)       # couleur de la voiture du joueur 1 (rouge)
CAR_COLOR_P2 = (0, 0, 255)     # couleur de la voiture du joueur 2 (bleu)

class GameState:
    MENU = "menu"
    RACING = "racing"


# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)
