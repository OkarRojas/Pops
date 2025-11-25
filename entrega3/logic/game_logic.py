# entrega3/logic/game_logic.py

class GameLogic:
    """
    Lógica genérica del juego: recibe un 'rules_engine'
    (TetrisRules o SnakeRules) y lo orquesta.
    """

    def __init__(self, rules_engine):
        """
        :param rules_engine: objeto con los métodos:
            - initial_state()
            - handle_input(game_state, input_handler)
            - update_timers(game_state, delta_time)
            - check_collisions(game_state)
            - apply_rules(game_state)
            - get_game_state(game_state)
            - is_game_over(game_state)
        """
        self.rules_engine = rules_engine
        self.game_state = self.rules_engine.initial_state()
        self._is_game_over = False

    def update(self, delta_time, input_handler):
        """
        Método principal: se llama una vez por frame desde el motor.
        """
        if self._is_game_over:
            return

        # 1) Entrada del usuario (teclas, etc.)
        self.rules_engine.handle_input(self.game_state, input_handler)

        # 2) Actualización según el tiempo (gravedad, movimiento, etc.)
        self.rules_engine.update_timers(self.game_state, delta_time)

        # 3) Comprobar colisiones
        self.check_collisions()

        # 4) Aplicar reglas del juego (puntuación, líneas, crecer, etc.)
        self.apply_rules()

        # 5) Verificar si el juego terminó
        self._is_game_over = self.is_game_over()

    def check_collisions(self):
        """Detecta choques usando las reglas específicas del juego."""
        self.rules_engine.check_collisions(self.game_state)

    def apply_rules(self):
        """Aplica reglas (puntuación, eliminar líneas, etc.)."""
        self.rules_engine.apply_rules(self.game_state)

    def get_game_state(self):
        """
        Devuelve información del estado del juego:
        - tablero o serpiente
        - puntuación
        - si el juego terminó, etc.
        """
        return self.rules_engine.get_game_state(self.game_state)

    def is_game_over(self):
        """Indica si el juego ha terminado."""
        return self.rules_engine.is_game_over(self.game_state)

