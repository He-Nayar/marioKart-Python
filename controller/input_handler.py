import pygame

MAPPING_P1 = {
    pygame.K_z: "accelerate",   # clavier AZERTY
    pygame.K_w: "accelerate",   # clavier QWERTY
    pygame.K_s: "brakes",
    pygame.K_q: "turn_left",    # clavier AZERTY
    pygame.K_a: "turn_left",    # clavier QWERTY
    pygame.K_d: "turn_right",
}

MAPPING_P2 = {

    pygame.K_UP:     "accelerate",
    pygame.K_DOWN:     "brakes",
    pygame.K_RIGHT:    "turn_right",
    pygame.K_LEFT:    "turn_left"

}

class InputHandler:

    def __init__(self, mapping : dict):
        self.mapping = mapping

    def get_inputs(self) -> dict:
        keys = pygame.key.get_pressed()
        p = {action: False for action in self.mapping.values()}

        for key, action in self.mapping.items():
            if keys[key]:
                p[action] = True

        return p
