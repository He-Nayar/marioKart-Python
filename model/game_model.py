from constants import GameState, GRID_ROWS, GRID_COLS,  CAR_COLOR_P1, CAR_COLOR_P2
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile
from model.terrain import Road, Grass, Dirt, Ice, Void


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.cars: list[Car] = []  #cars[0] = joueur 1, cars[1] = joueur 2

    def load_circuit(self) -> None:
        grid = [[RoadTile(col=col_idx, row=row_idx, terrain=self._test_terrain(col_idx, row_idx))
                for col_idx in range(GRID_COLS)] for row_idx in range(GRID_ROWS)]
        self.circuit = Circuit(grid=grid)
        self.spawn_cars()

    def _test_terrain(self, col:int, row: int):
        """terrain de test en attaensant les fichier text"""
        if row==0 or row==GRID_ROWS -1 or col==0 or col== GRID_COLS-1:
            return Void()
        if row <= 3 :
            return Road()
        if row <= 5 :
            return Grass()
        if row <=7:
            return Dirt()
        return Ice()

    def spawn_cars(self) -> None:
        """Cree les deux voitures cote a cote sur la grille"""
        self.cars = [Car(7, 1, CAR_COLOR_P1), Car(7, 2, CAR_COLOR_P2)]

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        
        for car in self.cars:
            col, row= car.get_tile_position()
            tile = self.circuit.get_tile(col,row)
            if tile is None:
                car.respawn()
            else:
                """on demande à ce terrain d'agir sur la voiture."""
                tile.terrain.apply_to(car) 
                print(tile.terrain.name, car.traction)
            car.update_position()
