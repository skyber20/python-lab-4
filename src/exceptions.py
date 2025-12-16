class PlayerNotFound(Exception):
    def __init__(self, player_name):
        super().__init__(f"Игрок '{player_name}' не найден")


class GooseNotFound(Exception):
    def __init__(self, goose_name):
        super().__init__(f"Игрок '{goose_name}' не найден")
