class Player:
    def __init__(self, name: str, balance: int = 100):
        self.name = name
        self.balance = balance

    def update_balance(self, amount: int):
        self.balance += amount
        return f'Баланс игрока {self.name} составляетс {self.balance}'

    def __repr__(self):
        return f"Player(name='{self.name}', balance={self.balance})"
