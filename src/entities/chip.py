class Chip:
    def __init__(self, amount: int):
        if amount < 0:
            raise ValueError('Номинал фишек может быть только > 0')
        self.amount = amount

    def __add__(self, other):
        if not isinstance(other, Chip):
            raise TypeError('Можно прибавлять только Chip')
        return Chip(self.amount + other.amount)

    def __sub__(self, other):
        if not isinstance(other, Chip):
            raise TypeError('Можно вычитать только Chip')
        return Chip(self.amount - other.amount)

    def __lt__(self, other):
        """Меньше (<)"""
        if isinstance(other, Chip):
            return self.amount < other.amount
        elif isinstance(other, int):
            return self.amount < other
        return NotImplemented

    def __le__(self, other):
        """Меньше или равно (<=)"""
        if isinstance(other, Chip):
            return self.amount <= other.amount
        elif isinstance(other, int):
            return self.amount <= other
        return NotImplemented

    def __eq__(self, other):
        """Равно (==)"""
        if isinstance(other, Chip):
            return self.amount == other.amount
        elif isinstance(other, int):
            return self.amount == other
        return NotImplemented

    def __ne__(self, other):
        """Не равно (!=)"""
        if isinstance(other, Chip):
            return self.amount != other.amount
        elif isinstance(other, int):
            return self.amount != other
        return NotImplemented

    def __gt__(self, other):
        """Больше (>)"""
        if isinstance(other, Chip):
            return self.amount > other.amount
        elif isinstance(other, int):
            return self.amount > other
        return NotImplemented

    def __ge__(self, other):
        """Больше или равно (>=)"""
        if isinstance(other, Chip):
            return self.amount >= other.amount
        elif isinstance(other, int):
            return self.amount >= other
        return NotImplemented

    def __repr__(self):
        return f'Chip(amount={self.amount})'

    def __str__(self):
        return f'Фишка с номиналом {self.amount}'
