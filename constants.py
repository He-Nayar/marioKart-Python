WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

CAR_ACCELERATION = 0.05
CAR_DECELERATION = 0.07 #ajouter pour utiliser les freins et la marche arriere dans brakesR
#CAR_ROTATION_SPEED = 1.5
CAR_WIDTH = 30
CAR_HEIGHT = 50
FROTTEMENT = 0.98
BRAQUAGE_MAX = 30 #angle de braquage max des roues
FACTEUR_DE_ROT = 0.02 #un facteur pour ajuster la vitesse de rotation
SEUIL_DERAPAGE = 10 #si la vitesse * braqauge depasse le seuil la voiture derape
ADHERENCE_DERAPAGE = 0.01 #part de la vitesse realignee sur le nez a chaque image en derapage
SEUIL_SORTIE_DERAPAGE = 0.1    # fin du derapage si la vitesse laterale passe sous ce seuil
FROTTEMENT_DERAPAGE = 0.995



class GameState:
    MENU = "menu"
    RACING = "racing"


# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)
