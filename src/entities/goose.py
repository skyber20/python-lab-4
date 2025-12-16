import random

from src.entities.player import Player


class Goose:
    def __init__(self, name: str, honk_volume: int = 1):
        self.name = name
        self.honk_volume = max(1, min(honk_volume, 10))

    def honk(self):
        return f"Гусь {self.name} кричит с громкостью {self.honk_volume}"

    def __repr__(self):
        return f"Goose(name='{self.name}', honk_volume={self.honk_volume})"


class WarGoose(Goose):
    def attack(self, player: Player):
        damage = self.honk_volume * random.randint(1, 10)
        player.update_balance(damage)
        return f"{self.name} атаковал {player.name}! Потеряно {damage}. Баланс: {player.balance}"

    def __repr__(self):
        return f"WarGoose(name='{self.name}', honk_volume={self.honk_volume})"


class HonkGoose(Goose):
    def __call__(self, player: Player):
        unary_sign = random.choice(['-', '+'])
        effect_power = int(f'{unary_sign}{self.honk_volume * random.randint(1, 10)}')
        player.update_balance(effect_power)

        if unary_sign == '-':
            return f"Игрок {player.name} слил {effect_power} из-за орущего гуся {self.name}"
        return f"Игрок {player.name} получил {effect_power} на баланс благодаря орущему гусю {self.name}"

    def __repr__(self):
        return f"HonkGoose(name='{self.name}', honk_volume={self.honk_volume})"
