import json
import random
from typing_extensions import override

class GameEnvironment:
    def __init__(self, **kwargs):
        self.current_frame = 0
        self.state = kwargs
        self.player_actions = None
    
    def ready() -> bool:
        return True
    
    def done() -> bool:
        return False
    
    def join(self, player_id: int):
        pass
    
    def leave(self, player_id: int):
        pass
    
    def score(self, player_id) -> int:
        pass        
    
    def state_dict(self) -> dict:
        return {"frame": self.current_frame, "state": self.state}

    def action_dict(self, player_id = None) -> dict:
        if not player_id:
            return {"frame": self.current_frame, "action": self.player_actions}
        return {"frame": self.current_frame, "action": self.player_actions[player_id]}

    def reset(self, **kwargs):
        self.current_frame = 0
        self.set(**kwargs)

    def set(self, **kwargs):
        self.state = kwargs["state"]
        self.current_frame = kwargs["frame"]
        self.player_actions = None

    def step(self, player_actions: dict):
        self.current_frame += 1
        self.player_actions = player_actions

   
class TerritoryTile(GameEnvironment):

    def __init__(
        self,
        n_cols: int = 8,
        n_rows: int = 8,
        min_players: int = 2,
        max_players: int = 2,
        max_frames: int = 60 * 10,
        frequency: int = 10,
    ):
        super().__init__()
        
        self.area_statistics = {}
        
        self.action_map = {
            'up': { "x": 0, "y": -1 },
            'down': { "x": 0, "y": 1 },
            'left': { "x": -1, "y": 0 },
            'right': { "x": 1, "y": 0 },
            'shoot': { "x": 0, "y": 0 },
            'idle': { "x": 0, "y": 0 },
        }
        
        self.candidate_player_state = [
            {
                "position": {
                    "x": 0, "y": (n_rows - 1) // 2,
                },
                "direction": {
                    "x": 1, "y": 0,
                },
            },
            {
                "position": {
                    "x": (n_cols - 1), "y": (n_rows - 1) - (n_rows - 1) // 2
                },
                "direction": {
                    "x": -1, "y": 0
                }
            },
            {
                "position": {
                    "x": (n_cols - 1) // 2, "y": 0
                },
                "direction": {
                    "x": 0, "y": 1,
                },
            },
            {
                "position": {
                    "x": (n_cols - 1) - (n_cols - 1) // 2 , "y": (n_rows - 1)
                },
                "direction": {
                    "x": 0, "y": -1,
                },
            }
        ]
        
        self.state = {
            "settings": {
                "n_cols": n_cols,
                "n_rows": n_rows,
                "min_players": min_players,
                "max_players": max_players,
                "frequency": frequency,
                "cur_frames": 0,
                "max_frames": max_frames,
            },
            "map": [ 0 for _ in range(n_rows * n_cols)],
            "bullets": {},
            "players": {},
        }

    def join(self, player_id: int):
        cur_players = len(self.state["players"])
        player_state = self.candidate_player_state[cur_players].copy()
        
        self.state["players"][player_id] = player_state
        self.state["players"][player_id]["alive"] = 1
        self.state["players"][player_id]["color"] = cur_players
        for id, _ in enumerate(self.state["map"]):
            x, y = self.index_to_vector(id)
            dist = [(abs(x - player["position"]["x"]) + abs(y - player["position"]["y"]), player['color'])
                for player in self.state["players"].values()]
            min_dist = min(dist)
            color = random.choice([color for _, color in dist if _ == min_dist[0]])
            if color == cur_players:
                old_color = self.state["map"][id]
                self.area_statistics[old_color] = self.area_statistics.get(old_color, 1) - 1
                self.state["map"][id] = color
                self.area_statistics[color] = self.area_statistics.get(color, 0) + 1
            
        
    def ready(self) -> bool:
        return len(self.state["players"]) >= self.state["settings"]["min_players"]

    def done(self) -> bool:
        return self.state["settings"]["cur_frames"] >= self.state["settings"]["max_frames"] or len(self.state["players"]) < self.state["settings"]["min_players"]
    
    @override
    def score(self, player_id) -> int:
        print(self.state["players"], player_id)
        if player_id in self.state["players"]:
            return self.area_statistics[self.state["players"][player_id]["color"]]
        return 0
    
    @override
    def state_dict(self) -> dict:
        for id, player in self.state["players"].items():
            assert isinstance(player, dict)
            assert "position" in player
            assert "x" in player["position"]
            assert "y" in player["position"]
            assert "direction" in player
            assert "x" in player["direction"]
            assert "y" in player["direction"]
            assert "alive" in player
            assert "color" in player
        
        for id, bullet in self.state["bullets"].items():
            assert isinstance(bullet, dict)
            assert "position" in bullet
            assert "x" in bullet["position"]
            assert "y" in bullet["position"]
            assert "direction" in bullet
            assert "x" in bullet["direction"]
            assert "y" in bullet["direction"]
            assert "alive" in bullet
            assert "color" in bullet
        
        return super().state_dict()

    @override 
    def action_dict(self, player_id = None) -> dict:
        if player_id:
            assert player_id in self.player_actions
        
        return super().action_dict(player_id)

    def vector_to_index(self, x, y):
        n_cols = self.state["settings"]["n_cols"]
        return y * n_cols + x

    def index_to_vector(self, index):
        n_cols = self.state["settings"]["n_cols"]
        return index % n_cols, index // n_cols

    def step(self, player_actions: dict):
        super().step(player_actions)

        # Update frames
        if not self.state['settings']['cur_frames']:
            self.state['settings']['cur_frames'] = 1
        else:
            self.state['settings']['cur_frames'] += 1

        
        # Remove dead players
        self.state['players'] = {player_id: player for player_id, player in self.state['players'].items() if player['alive'] > 0}

        # Remove bullets out of the map
        self.state["bullets"] = {bullet_id: bullet for bullet_id, bullet in self.state['bullets'].items() if bullet['alive']}

        # Move bullets
        for bullet_id, bullet in self.state['bullets'].items():
            bullet['next_position'] = {
                'x': bullet['position']['x'] + bullet['direction']['x'],
                'y': bullet['position']['y'] + bullet['direction']['y']
            }

        # Move players
        
        for player_id, player in self.state['players'].items():
            action = player_actions.get(player_id, "idle")
            
            direction = {
                'x': self.action_map[action]['x'],
                'y': self.action_map[action]['y']
            }

            if (direction['x'] == player['direction']['x'] and direction['y'] == player['direction']['y']): 
                next_x = player['position']['x'] + direction['x']
                next_y = player['position']['y'] + direction['y']
                
                if next_x < 0 or next_x >= self.state['settings']['n_cols']:
                    direction["x"] = 0
                elif next_y < 0 or next_y >= self.state['settings']['n_cols']:
                    direction["y"] = 0
                elif self.state["map"][next_y * self.state["settings"]["n_cols"] + next_x] != player["color"]:
                    direction["x"] = 0
                    direction["y"] = 0
            elif direction['x'] != 0 or direction['y'] != 0:
                player['direction'] = direction
                direction = { 'x': 0, 'y': 0 }

            player['next_position'] = {
                'x': player['position']['x'] + direction['x'],
                'y': player['position']['y'] + direction['y']
            }

            if action == 'shoot': 
                bullet_id = f"{self.state['settings']['cur_frames']}_{player_id}"
                
                self.state['bullets'][bullet_id] = {
                    'position': {
                        'x': player['position']['x'],
                        'y': player['position']['y'],
                    },
                    'direction': {
                        'x': player['direction']['x'],
                        'y': player['direction']['y'],
                    },
                    'color': player['color'],
                    'alive': True,
                    'next_position': {
                        'x': player['position']['x'],
                        'y': player['position']['y'],
                    }
                }
        
        for player_id in self.state['players']:
            player = self.state['players'][player_id]
            for bullet_id in self.state['bullets']:
                bullet = self.state['bullets'][bullet_id]
                if bullet['color'] != player['color'] and \
                    bullet['position']['x'] == player['position']['x'] and \
                    bullet['position']['y'] == player['position']['y']:
                    player['alive'] -= 1
                    bullet['alive'] = False
                
                elif bullet['color'] != player['color'] and \
                    bullet['position']['x'] == player['next_position']['x'] and \
                    bullet['position']['y'] == player['next_position']['y'] and \
                    bullet['next_position']['x'] == player['position']['x'] and \
                    bullet['next_position']['y'] == player['position']['y']:
                    player['alive'] -= 1
                    bullet['alive'] = False
        
        for bullet_id_a in self.state['bullets']:
            bullet_a = self.state['bullets'][bullet_id_a]
            for bullet_id_b in self.state['bullets']:
                if bullet_id_a == bullet_id_b:
                    continue
                bullet_b = self.state['bullets'][bullet_id_b]
                
                if bullet_a['color'] != bullet_b['color'] and \
                    bullet_a['position']['x'] == bullet_b['position']['x'] and \
                    bullet_a['position']['y'] == bullet_b['position']['y']:
                    bullet_a['alive'] = False
                    bullet_b['alive'] = False
                
                if bullet_a['color'] != bullet_b['color'] and \
                    bullet_a['position']['x'] == bullet_b['next_position']['x'] and \
                    bullet_a['position']['y'] == bullet_b['next_position']['y'] and \
                    bullet_a['next_position']['x'] == bullet_b['position']['x'] and \
                    bullet_a['next_position']['y'] == bullet_b['position']['y']:
                    bullet_a['alive'] = False
                    bullet_b['alive'] = False

        for bullet_id in self.state['bullets']:
            bullet = self.state['bullets'][bullet_id]
            x = bullet['position']['x']
            y = bullet['position']['y']
            
            if bullet['alive']:
                self.state['map'][y * self.state["settings"]["n_cols"] + x] = bullet['color']
            
            if bullet['next_position']['x'] < 0 or \
                bullet['next_position']['x'] >= self.state['settings']['n_cols'] or \
                bullet['next_position']['y'] < 0 or \
                bullet['next_position']['y'] >= self.state['settings']['n_cols']:
                bullet['alive'] = False


        # Update positions
        for player in self.state['players'].values():
            player['position']['x'] = player['next_position']['x']
            player['position']['y'] = player['next_position']['y']
            del player['next_position']

    
        for bullet in self.state['bullets'].values():
            bullet['position']['x'] = bullet['next_position']['x']
            bullet['position']['y'] = bullet['next_position']['y']
            del bullet['next_position']
            
