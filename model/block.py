from abc import ABC, abstractmethod

class Block(ABC):
    """Bloc pose sur une case qui agit lorsque une voiture passe dessus"""
    def __init__(self,letter: str):
        """Enregistrer la mlettre afficher sur la case """
        self.letter=letter 

        @abstractmethod
        def on_enter(self,car) -> None :
            """Effet du bloc sur la voiture"""

class StartBlock(Block):
    """ Bloc de depart : ou demarre le joueur 1 ou 2"""

    def __init__(self, player:int):
        """cree le depart du player """
        super().__init__(str(player))
        self.player=player

    def on_enter(self,car) -> None:
        """ le depart n'a aucun effet sur la voiture"""

class CheckpointBlock(Block):
    """point de passage : la voiture memorise sa position"""
    def __init__(self, number:int):
         """cree le point de passage numero number"""
         super().__init__("C")
         self.number= number

    def on_enter(self,car):
         """on enregistre ce dernier point de passage"""
         car.set_checkpoint()

class FinishLineBlock(Block):
    """ligne d'arriver """
    def __init__(self):
        """cree une ligne d'arrivee"""
        super().__init__("F")
    def on_enter(self,car) -> None:
        """ ya rien qui passe : le comptage des tours est fait par la course"""

class BoostBlock(Block):
    """cree le block boost"""
    def __init__(self):
        super().__init__("B")

    def on_enter(self,car) -> None:
        """lancere le boost de la voiture"""
        car.boost()





