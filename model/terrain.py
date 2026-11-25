class Terrain:
    def __init__(self, name:str, color: tuple, seuil: float,
                  adherence: float, frottement: float,  traction: float):
        self.name = name
        self.color = color 
        self.seuil = seuil
        self.adherence = adherence
        self.frottement= frottement 
        self.traction = traction

    def apply_to(self,car):
        """Donne a la voiture les proprietes de ce terrain """
        car.set_grip(self.seuil,self.adherence,self.frottement,self.traction)

class Road(Terrain):
    def __init__(self):
        super().__init__("route",(80,80,90),60,0.05,0.95,1.0)

class Grass(Terrain):
    """ Herb : facile de deraper"""
    def __init__(self):
        super().__init__("herb", (60,160,60),40,0.04,0.97,0.7)

class Dirt(Terrain):
    """ Terre : tres facile a ce derapper """
    def __init__(self):
        super().__init__("Terre",(140,90,40),25,0.03,0.985,0.7)

class Ice(Terrain):
    """Glace : faible traction, presque aucun frottement en derapage."""
    def __init__(self):
        super().__init__("glace",(170,220,240),10,0.01,0.995,0.4)

class Void(Terrain):
    """Vide : la voiture qui tombe dedans revient au dernier point de passage."""
    def __init__(self):
        super().__init__("vide",(20,20,25),0,0,0,0)
    def apply_to(self,car):
        car.respawn()


