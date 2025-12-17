class Player:
    def __init__(self, name: str, balance: int = 100):
        self.name = name
        self.balance = balance

    def update_balance(self, amount: int):
        if not isinstance(amount, int):
            raise TypeError('Вы можете к балансу прибавлять только целое число')
        self.balance += amount

    def __repr__(self):
        return f"Player(name='{self.name}', balance={self.balance})"
