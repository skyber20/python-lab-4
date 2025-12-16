class Chip:
    def __init__(self, amount: int):
        if amount < 0:
            raise ValueError('Номинал фишек может быть только > 0')
        self.amount = amount

    def __add__(self, other):
        if not isinstance(other, Chip):
            raise TypeError('Можно складывать только Chip и Chip')

        return Chip(self.amount + other.amount)

    def __repr__(self):
        return f'Chip(amount={self.amount})'
