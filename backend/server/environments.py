import json


class GameEnvironment:
    def __init__(self, **kwargs):
        self.current_frame = 0
        self.state = kwargs
        self.player_actions = None

    def state_dict(self) -> dict:
        return {"frame": self.current_frame, "state": self.state}

    def action_dict(self, player_id) -> dict:
        return {"frame": self.current_frame, "action": self.player_actions[player_id]}

    def reset(self, **kwargs):
        self.current_frame = 0
        self.set(**kwargs)

    def set(self, **kwargs):
        self.state = kwargs
        self.player_actions = None

    def step(self, player_actions: dict):
        self.current_frame += 1
        self.player_actions = player_actions


class TerritoryTile(GameEnvironment):
    def __init__(
        self,
        map_size: int = 9,
        min_players: int = 2,
        max_players: int = 2,
        max_frames: int = 3 * 60 * 6,
    ):
        self.metadata = {
            "map_size": map_size,
            "max_frames": max_frames,
        }
        self.map = [0] * map_size * map_size
        self.bullets = []
        self.players = []

    def vector_to_index(self, x, y):
        map_size = self.metadata.get("map_size", 0)
        return x * map_size + y

    def index_to_vector(self, index):
        map_size = self.metadata.get("map_size", 0)
        return index // map_size, index % map_size

    def step(self, player_actions: dict):
        super().step(player_actions)

        for player, action in player_actions.items():
            pass
