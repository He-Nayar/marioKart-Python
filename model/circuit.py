from model.road_tile import RoadTile
from constants import TILE_SIZE
from model.terrain import Road, Grass, Dirt, Ice, Void
from model.block import StartBlock, CheckpointBlock, FinishLineBlock, BoostBlock

TERRAIN_LETTRES = {"R":Road, "G": Grass, "D": Dirt, "I": Ice,"V":Void}
CHECKPOINT_LETTRES = "abcdefjhig"

def make_block(letter:str):
    """Renvoie le bloc correspondant a une lettre ou fichier ou None"""
    if letter in "12":
        return StartBlock(int(letter))
    if letter == "B":
        return BoostBlock()
    if letter == "F":
        return FinishLineBlock()
    if letter in CHECKPOINT_LETTRES:
        return CheckpointBlock(CHECKPOINT_LETTRES.index(letter))
    return None

class Circuit:

    def __init__(self,  grid: list[list[RoadTile]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    @classmethod
    def from_file(cls, path:str) -> "Circuit":
        """ cree un circuit apartire du fichier text"""
        with open(path, encoding="utf-8")as file:
            text = file.read()
        terrain_part, block_part = text.strip().split("\n\n")
        terrain_lines= terrain_part.splitlines()
        block_lines = block_part.splitlines()

        grid=[]
        for row in range (len(terrain_lines)):
            tiles =[]
            for col in range(len(terrain_lines[row])):
                terrain = TERRAIN_LETTRES[terrain_lines[row][col]]()
                block = make_block(block_lines[row][col])
                tiles.append(RoadTile(col, row, terrain, block))
            grid.append(tiles)
        return cls(grid)


    def get_tile(self, col: int, row: int) -> RoadTile | None:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile | None:
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)

    def pixel_width(self) -> int:
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        return self.rows * TILE_SIZE

    def find_start(self,player:int) -> tuple[int,int] | None:
        """renvoie la case (col, row) du block de depart du joeur ou none """
        for row in self.grid:
            for tile in row:
                if isinstance(tile.block, StartBlock) and tile.block.player == player:
                    return tile.col , tile.row
        return None
