from constants import GameState, GRID_ROWS, GRID_COLS,  CAR_COLOR_P1, CAR_COLOR_P2
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.cars: list[Car] = []  #cars[0] = joueur 1, cars[1] = joueur 2

    def load_circuit(self) -> None:
        grid = [[RoadTile(col=col_idx, row=row_idx)
                for col_idx in range(GRID_COLS)] for row_idx in range(GRID_ROWS)]
        self.circuit = Circuit(grid=grid)
        self.spawn_cars()

    def spawn_cars(self) -> None:
        """Cree les deux voitures cote a cote sur la grille"""
        self.cars = [Car(7, 1, CAR_COLOR_P1), Car(7, 2, CAR_COLOR_P2)]

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        for car in self.cars:
            car.update_position()
