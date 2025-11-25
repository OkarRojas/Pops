# entrega3/logic/snake_rules.py

import random

class SnakeRules:
    """
    Lógica específica de Snake.
    """

    def __init__(self, config_dict: dict):
        """
        config_dict viene del .dnm, algo como:

        dpop snake <
            width : 20,
            height : 20,
            initial_length : 3,
            speed : 5
        >
        """
        self.cfg = config_dict or {}

        self.width = int(self.cfg.get("width", 20))
        self.height = int(self.cfg.get("height", 20))
        self.initial_length = int(self.cfg.get("initial_length", 3))
        self.speed = float(self.cfg.get("speed", 5.0))

    def initial_state(self):
        cx = self.width // 2
        cy = self.height // 2
        snake = [(cx - i, cy) for i in range(self.initial_length)]

        return {
            "snake": snake,
            "direction": (1, 0),
            "food": self._spawn_food(snake),
            "score": 0,
            "is_game_over": False,
            "move_timer": 0.0,
            "move_interval": 1.0 / self.speed,
        }

    def handle_input(self, state, input_handler):
        if state["is_game_over"]:
            return

        get = getattr(input_handler, "is_action_active", None)
        if get is None:
            up = down = left = right = False
        else:
            up = get("up")
            down = get("down")
            left = get("left")
            right = get("right")

        dx, dy = state["direction"]

        if up and dy != 1:
            state["direction"] = (0, -1)
        elif down and dy != -1:
            state["direction"] = (0, 1)
        elif left and dx != 1:
            state["direction"] = (-1, 0)
        elif right and dx != -1:
            state["direction"] = (1, 0)

    def update_timers(self, state, delta_time):
        if state["is_game_over"]:
            return

        state["move_timer"] += delta_time
        while state["move_timer"] >= state["move_interval"]:
            state["move_timer"] -= state["move_interval"]
            self._advance_snake(state)

    def check_collisions(self, state):
        pass

    def apply_rules(self, state):
        pass

    def get_game_state(self, state):
        return {
            "snake": list(state["snake"]),
            "food": state["food"],
            "score": state["score"],
            "is_game_over": state["is_game_over"],
            "width": self.width,
            "height": self.height,
        }

    def is_game_over(self, state):
        return state["is_game_over"]

    def _advance_snake(self, state):
        snake = state["snake"]
        dx, dy = state["direction"]
        head_x, head_y = snake[0]
        new_head = (head_x + dx, head_y + dy)

        x, y = new_head
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            state["is_game_over"] = True
            return

        if new_head in snake:
            state["is_game_over"] = True
            return

        snake.insert(0, new_head)

        if new_head == state["food"]:
            state["score"] += 1
            state["food"] = self._spawn_food(snake)
        else:
            snake.pop()

    def _spawn_food(self, snake):
        free_cells = [
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if (x, y) not in snake
        ]
        if not free_cells:
            return (-1, -1)
        return random.choice(free_cells)

