import json 

class GameEnvironment:
    def __init__(
        self,
        player_count,
    ):
        self.player_count = player_count
        self.step_count = 0

    def reset(self):
        self.step_count = 0

    def step(self, actions):
        self.step_count += 1

    def to_json(self):
        pass

class TerritoryTile(GameEnvironment):
    def __init__(
        self,
        grid_size: int = 9,
    ):
        

    def step(self, action):
