class PlayerNotFound(Exception):
    def __init__(self, player):
        super().__init__(f"Игрок {player} не найден")


class GooseNotFound(Exception):
    def __init__(self, goose):
        super().__init__(f"Игрок {goose} не найден")
