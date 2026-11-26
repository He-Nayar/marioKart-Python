from constants import GameState, GRID_ROWS, GRID_COLS,  CAR_COLOR_P1, CAR_COLOR_P2
from model.car import Car
from model.circuit import Circuit
#from model.road_tile import RoadTile
#from model.terrain import Road, Grass, Dirt, Ice, Void
#from model.block import CheckpointBlock, StartBlock, FinishLineBlock, BoostBlock

class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.cars: list[Car] = []  #cars[0] = joueur 1, cars[1] = joueur 2

    def load_circuit(self, path:str="circuits/circuit1.txt") -> None:
        
       # grid = [[RoadTile(col=col_idx, row=row_idx,
                         #  terrain=self._test_terrain(col_idx, row_idx),
                          # block= self._test_block(col_idx, row_idx))
               # for col_idx in range(GRID_COLS)] for row_idx in range(GRID_ROWS)]
       # self.circuit = Circuit(grid=grid)
        """ charger le circuit depuis un fichier texte """
              
        self.circuit = Circuit.from_file(path)
               
        self.spawn_cars()

   # def _test_block(self, col: int, row: int):
       # """Blocs de test,fichiers en attendant les  de circuit."""
       # if (col, row) == (2, 1):
           # return StartBlock(1)
       # if (col, row) == (2, 2):
        #    return StartBlock(2)
        #if col == 5 and 1 <= row <= 3:
         #   return BoostBlock()
        #if (col, row) == (8, 9):
         #   return CheckpointBlock(0)
        #if col == 13 and 1 <= row <= 3:
         #   return FinishLineBlock()
        #return None

    #def _test_terrain(self, col:int, row: int):
     #   """terrain de test en attaensant les fichier text"""
      #  if row==0 or row==GRID_ROWS -1 or col==0 or col== GRID_COLS-1:
       #     return Void()
        #if row <= 3 :
         #   return Road()
        #if row <= 5 :
         #   return Grass()
        #if row <=7:
         #   return Dirt()
        #return Ice()

    def spawn_cars(self) -> None:
        """Cree les deux voitures cote a cote sur la grille"""
        """  place les deux voitures sur les blocs de depart 1&2 """
        col1, row1= self.circuit.find_start(1)
        col2, row2= self.circuit.find_start(2)
        self.cars= [Car(col1, row1, CAR_COLOR_P1), Car(col2, row2, CAR_COLOR_P2)]

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        
        for car in self.cars:
            col, row= car.get_tile_position()
            tile = self.circuit.get_tile(col,row)
            if tile is None:
                car.respawn()
            else:
                """on demande à ce terrain d'agir sur la voiture peut importe le terrain"""
                """ le terrain puis le block agissent sur la voiture"""
                tile.terrain.apply_to(car) 
                if tile.block is not None :
                    tile.block.on_enter(car)
            car.update_position()
