import random

class SnakeRules:
    """
    Lógica específica de Snake.
    """

    def __init__(self, config_dict: dict):

        self.cfg = config_dict or {}

        self.width = int(self.cfg.get("ancho", 20))
        self.height = int(self.cfg.get("alto", 20))
        self.initial_length = int(self.cfg.get("largo_inicial", 3))
        self.speed = float(self.cfg.get("velocidad", 5.0))
        self.score_per_food = int(self.cfg.get("puntos_por_manzana", 10))

    def initial_state(self):
        cx = self.width // 2
        cy = self.height // 2
        snake = [(cx - i, cy) for i in range(self.initial_length)]

        return {
            "snake": snake,
            "direction": (1, 0),  # derecha
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
        # Las colisiones se comprueban dentro de _advance_snake
        pass

    def apply_rules(self, state):
        # No hay reglas extra aparte de comer / morir
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

    # ----------------- Lógica interna -----------------

    def _advance_snake(self, state):
        snake = state["snake"]
        dx, dy = state["direction"]
        head_x, head_y = snake[0]
        new_head = (head_x + dx, head_y + dy)

        x, y = new_head
        # Colisión con paredes
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            state["is_game_over"] = True
            return

        # Colisión consigo misma
        if new_head in snake:
            state["is_game_over"] = True
            return

        # Añadir nueva cabeza
        snake.insert(0, new_head)

        # ¿Comió la comida?
        if new_head == state["food"]:
            state["score"] += self.score_per_food
            state["food"] = self._spawn_
