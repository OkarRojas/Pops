import random

class TetrisRules:

    TETROMINOS = {
        "I": [(0, 0), (1, 0), (2, 0), (3, 0)],
        "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
        "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
        "L": [(0, 0), (0, 1), (0, 2), (1, 2)],
        "J": [(1, 0), (1, 1), (1, 2), (0, 2)],
        "S": [(1, 0), (2, 0), (0, 1), (1, 1)],
        "Z": [(0, 0), (1, 0), (1, 1), (2, 1)],
    }

    def __init__(self, config_dict: dict):

        self.cfg = config_dict or {}

        self.width = int(self.cfg.get("ancho", 10))
        self.height = int(self.cfg.get("alto", 20))
        self.gravity = float(self.cfg.get("gravedad", 1.0))
        self.score_per_line = int(self.cfg.get("puntos_por_linea", 100))

        pieces_from_cfg = self.cfg.get("pieces")
        if isinstance(pieces_from_cfg, list):
            self.available_pieces = [
                p for p in pieces_from_cfg if p in self.TETROMINOS
            ] or list(self.TETROMINOS.keys())
        else:
            self.available_pieces = list(self.TETROMINOS.keys())

    def initial_state(self):
        board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        state = {
            "board": board,
            "current_piece": None,
            "piece_pos": [self.width // 2 - 2, 0],
            "rotation": 0,
            "score": 0,
            "lines_cleared": 0,
            "gravity_timer": 0.0,
            "is_game_over": False,
        }
        self._spawn_new_piece(state)
        return state

    def handle_input(self, state, input_handler):
        if state["is_game_over"]:
            return

        get = getattr(input_handler, "is_action_active", None)
        if get is None:
            left = right = rotate = soft_drop = False
        else:
            left = get("left")
            right = get("right")
            rotate = get("rotate")
            soft_drop = get("soft_drop")

        if left:
            self._try_move(state, dx=-1, dy=0)
        if right:
            self._try_move(state, dx=1, dy=0)
        if rotate:
            self._try_rotate(state)
        if soft_drop:
            moved = self._try_move(state, dx=0, dy=1)
            if not moved:
                self._lock_piece(state)
                self._clear_lines(state)
                self._spawn_new_piece(state)

    def update_timers(self, state, delta_time):
        if state["is_game_over"]:
            return

        fall_interval = 1.0 / self.gravity
        state["gravity_timer"] += delta_time

        while state["gravity_timer"] >= fall_interval:
            state["gravity_timer"] -= fall_interval
            moved = self._try_move(state, dx=0, dy=1)
            if not moved:
                self._lock_piece(state)
                self._clear_lines(state)
                self._spawn_new_piece(state)

    def check_collisions(self, state):
        pass

    def apply_rules(self, state):
        pass

    def get_game_state(self, state):
        return {
            "board": state["board"],
            "current_piece": state["current_piece"],
            "piece_pos": tuple(state["piece_pos"]),
            "rotation": state["rotation"],
            "score": state["score"],
            "lines_cleared": state["lines_cleared"],
            "is_game_over": state["is_game_over"],
        }

    def is_game_over(self, state):
        return state["is_game_over"]

    # ---- helpers internos ----

    def _spawn_new_piece(self, state):
        piece_name = random.choice(self.available_pieces)
        state["current_piece"] = piece_name
        state["rotation"] = 0
        state["piece_pos"] = [self.width // 2 - 2, 0]

        if not self._can_place_piece(state, state["piece_pos"], state["rotation"]):
            state["is_game_over"] = True

    def _try_move(self, state, dx, dy):
        new_pos = [state["piece_pos"][0] + dx, state["piece_pos"][1] + dy]
        if self._can_place_piece(state, new_pos, state["rotation"]):
            state["piece_pos"] = new_pos
            return True
        return False

    def _try_rotate(self, state):
        new_rot = (state["rotation"] + 1) % 4
        if self._can_place_piece(state, state["piece_pos"], new_rot):
            state["rotation"] = new_rot

    def _lock_piece(self, state):
        board = state["board"]
        for x, y in self._get_piece_coords(state):
            if 0 <= y < self.height and 0 <= x < self.width:
                board[y][x] = 1

    def _clear_lines(self, state):
        board = state["board"]
        new_board = []
        lines_cleared = 0

        for row in board:
            if all(cell != 0 for cell in row):
                lines_cleared += 1
            else:
                new_board.append(row)

        for _ in range(lines_cleared):
            new_board.insert(0, [0 for _ in range(self.width)])

        if lines_cleared > 0:
            state["board"] = new_board
            state["lines_cleared"] = state.get("lines_cleared", 0) + lines_cleared
            state["score"] += lines_cleared * self.score_per_line

    def _get_piece_coords(self, state, pos=None, rotation=None):
        if pos is None:
            pos = state["piece_pos"]
        if rotation is None:
            rotation = state["rotation"]

        piece_name = state["current_piece"]
        base_shape = self.TETROMINOS[piece_name]
        coords = []
        for x, y in base_shape:
            rx, ry = self._rotate_point(x, y, rotation)
            coords.append((pos[0] + rx, pos[1] + ry))
        return coords

    @staticmethod
    def _rotate_point(x, y, rotation):
        if rotation == 0:
            return x, y
        if rotation == 1:
            return -y, x
        if rotation == 2:
            return -x, -y
        if rotation == 3:
            return y, -x
        return x, y

    def _can_place_piece(self, state, pos, rotation):
        board = state["board"]
        for x, y in self._get_piece_coords(state, pos, rotation):
            if x < 0 or x >= self.width or y >= self.height:
                return False
            if y < 0:
                continue
            if board[y][x] != 0:
                return False
        return True

