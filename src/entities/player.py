from src.entities.chip import Chip
from src.exceptions import NotEnoughMoney, NotEnoughChips


class Player:
    def __init__(self, name: str, balance: int = 100, amount_chips: Chip = Chip(0)):
        self.name = name
        self.balance = balance
        self.amount_chips = amount_chips

    @property
    def is_bankrupt(self):
        return self.amount_chips == 0 and self.balance <= 0

    def update_balance(self, amount: int):
        if not isinstance(amount, int):
            raise TypeError('К балансу можно прибавлять целые числа')
        self.balance += amount

    def buy_chips(self, amount: int):
        if self.balance < amount:
            raise NotEnoughMoney(self.balance, amount)
        self.amount_chips = self.amount_chips + Chip(amount)
        self.balance -= amount

    def sell_chips(self, amount: int):
        if self.amount_chips < amount:
            raise NotEnoughChips(amount, self.amount_chips.amount)
        self.amount_chips = self.amount_chips - Chip(amount)
        self.balance += amount

    def __eq__(self, other):
        if not isinstance(other, Player):
            raise TypeError('Можно сравнивать Player с Player')
        return self.name == other.name and self.balance == other.balance

    def __repr__(self):
        return f"Player(name='{self.name}', balance={self.balance}), amount_chips={self.amount_chips.amount}"

    def __str__(self):
        return f"Игрок {self.name} с балансом {self.balance} и {self.amount_chips.amount} фишками"
