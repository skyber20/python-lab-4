class PlayerNotFound(Exception):
    def __init__(self, player):
        super().__init__(f"Игрок {player} не найден")


class GooseNotFound(Exception):
    def __init__(self, goose):
        super().__init__(f"Игрок {goose} не найден")


class InvalidAmountArgs(Exception):
    def __init__(self):
        super().__init__('Указано неверное количество аргументов')


class InvalidArgs(Exception):
    def __init__(self):
        super().__init__('Указаны некорректные аргументы')


class NegativeSteps(Exception):
    def __init__(self):
        super().__init__('Количество шагов в симуляции должно быть > 0')


class NotEnoughMoney(Exception):
    def __init__(self, balance: int, amount: int):
        super().__init__(f'Для покупки {amount} фишек необходимо еще {amount - balance}')


class NotEnoughChips(Exception):
    def __init__(self, amount: int, amount_chips: int):
        super().__init__(f'Невозможно обменять {amount} фишек, так как на баласе {amount_chips} фишек')
