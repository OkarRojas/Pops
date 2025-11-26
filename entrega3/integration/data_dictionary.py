from typing import Dict, Any, List

class DataDictionary:
    def __init__(self, ast: Dict[str, Any]):
        self.ast = ast
        self.rules: Dict[str, Any] = {}
        self.parse_rules(ast)
        self.validate_rules()

    def parse_rules(self, ast: Dict[str, Any]) -> None:
        rules = {
            "game_type": "generic",
            "initial_position": [320, 240],
            "rules": {},
            "raw_nodes": ast
        }

        # Busca el tipo de juego
        for key, value in ast.items():
            k = key.strip().lower()
            if k in ("game_type", "tipo_juego", "juego"):
                rules["game_type"] = str(value).strip().lower()
                continue

            # Busca entidad jugador 
            if isinstance(value, dict):
                if value.get("type") == "entity" and "MovableEntity" in str(value.get("class", "")):
                    if "x" in value and "y" in value:
                        rules["initial_position"] = [int(value["x"]), int(value["y"])]

                if "evento" in value and "accion" in value:
                    event = str(value["evento"]).lower().replace(" ", "_")
                    action = str(value["accion"]).lower().replace(" ", "_")
                    rules["rules"][event] = action

                if k.startswith("regla_"):
                    event_name = k[6:].lower()  
                    action = str(value).lower().strip()
                    if action.startswith("<") or "{" in action:
                        if isinstance(value, dict) and "accion" in value:
                            action = str(value["accion"]).lower()
                        else:
                            action = "unknown"
                    rules["rules"][event_name] = action

        self.rules = rules

    def get_rule(self, key: str) -> Any:
        keys = key.split(".")
        current: Any = self.rules
        try:
            for k in keys:
                current = current[k]
            return current
        except (KeyError, TypeError):
            raise KeyError(f"Regla no encontrada: '{key}'")

    def validate_rules(self) -> None:
        game = self.rules["game_type"]

        required = []
        if game == "snake":
            required = ["collision_with_wall", "eat_food"]
        elif game == "tetris":
            required = ["line_completed", "piece_landed"]

        missing = [r for r in required if r not in self.rules["rules"]]
        if missing:
            raise ValueError(f"Para el juego '{game}' faltan reglas obligatorias: {', '.join(missing)}")

    def get_game_type(self) -> str:
        return self.rules["game_type"]

    def get_initial_position(self) -> List[int]:
        return self.rules["initial_position"]