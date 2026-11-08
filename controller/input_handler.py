import pygame


MAPPING = {
    pygame.K_UP:     "accelerate",
    # rajouter les autres touches pour bouger
    pygame.K_DOWN:     "brakesR"
}


class InputHandler:

    def __init__(self):
        self.mapping = MAPPING

    def get_inputs(self) -> dict:
        keys = pygame.key.get_pressed()
        p = {action: False for action in self.mapping.values()}

        for key, action in self.mapping.items():
            if keys[key]:
                p[action] = True

        return p
