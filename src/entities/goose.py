import random

from src.entities.player import Player


class Goose:
    def __init__(self, name: str, honk_volume: int = 1):
        """
        Класс Гусь
        :param name: имя
        :param honk_volume: громкость крика
        """
        self.name = name
        self.honk_volume = max(1, min(honk_volume, 10))

    def __repr__(self):
        return f"Goose(name='{self.name}', honk_volume={self.honk_volume})"

    def __str__(self):
        return f'Дэфолтный гусь {self.name} со своим ГА-ГА-ГА в {self.honk_volume} МдБ'

    def honk(self):
        """ГА-ГА-ГА"""
        return f"Гусь {self.name} кричит с громкостью {self.honk_volume}"


class WarGoose(Goose):
    def __repr__(self):
        return f"WarGoose(name='{self.name}', honk_volume={self.honk_volume})"

    def __str__(self):
        return f'Боевой гусь {self.name} со своим ГА-ГА-ГА в {self.honk_volume} МдБ'

    def attack(self, player: Player):
        """
        Атакует игрока, отбирая у него деньги
        :param player: игрок
        :return: сообщение о проделанном действии
        """
        damage = self.honk_volume * (random.randint(1, 25))
        player.update_balance(-damage)
        return f"Гусь {self.name} атаковал игрока {player.name}! Потеряно {damage} валюты"


class HonkGoose(Goose):
    def __call__(self, player: Player):
        unary_sign = random.choice(['-', '+'])
        effect_power = int(f'{unary_sign}{self.honk_volume * random.randint(1, 25)}')
        player.update_balance(effect_power)

        if unary_sign == '-':
            return f"Игрок {player.name} слил {abs(effect_power)} валюты из-за орущего гуся {self.name}"
        return f"Игрок {player.name} залутал {effect_power} валюты на баланс благодаря орущему гусю {self.name}"

    def __repr__(self):
        return f"HonkGoose(name='{self.name}', honk_volume={self.honk_volume})"

    def __str__(self):
        return f'Орущий гусь {self.name} со своим ГА-ГА-ГА в {self.honk_volume} МдБ'
