class PlayerNotFound(Exception):
    """Игрок не найден"""
    def __init__(self, player):
        super().__init__(f"Игрок {player} не найден")


class GooseNotFound(Exception):
    """Гусь не найден"""
    def __init__(self, goose):
        super().__init__(f"Игрок {goose} не найден")


class InvalidAmountArgs(Exception):
    """Неверное количество аргументов"""
    def __init__(self):
        super().__init__('Указано неверное количество аргументов')


class InvalidArgs(Exception):
    """Некорректные аргументы"""
    def __init__(self):
        super().__init__('Указаны некорректные аргументы')


class NegativeSteps(Exception):
    """Указано отрицательное количество шагов"""
    def __init__(self):
        super().__init__('Количество шагов в симуляции должно быть > 0')


class NotEnoughMoney(Exception):
    """Недостаточно денег для покупки фишек"""
    def __init__(self, balance: int, amount: int):
        super().__init__(f'Для покупки {amount} фишек необходимо еще {amount - balance}')


class NotEnoughChips(Exception):
    """Недостаточно фишек для обмена на деньги"""
    def __init__(self, amount: int, amount_chips: int):
        super().__init__(f'Невозможно обменять {amount} фишек, так как на баласе {amount_chips} фишек')
