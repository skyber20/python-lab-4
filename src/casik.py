import random

from src.collections.casino_balance import CasinoBalance
from src.collections.goose_collection import GooseCollection
from src.collections.player_collection import PlayerCollection
from src.entities.goose import Goose, WarGoose, HonkGoose
from src.entities.player import Player


class Casino:
    def __init__(self):
        self.players = PlayerCollection()
        self.geese = GooseCollection()
        self.balances = CasinoBalance()

    def register_player(self, player: Player):
        self.players = self.players + player
        self.balances[player.name] = player.balance

    def register_goose(self, goose: Goose):
        self.geese = self.geese + goose

    def perform_attack(self):
        war_geese = [g for g in self.geese if isinstance(g, WarGoose)]

        if not war_geese:
            print('ДОДЕЛАТЬ')
            return

        if not self.players:
            print('ДОДЕЛАТЬ')
            return

        war_goose = random.choice(war_geese)
        player = random.choice(self.players)

        war_goose.attack(player)
        self.balances[player.name] = player.balance

    def perform_honk(self):
        honk_geese = [g for g in self.geese if isinstance(g, HonkGoose)]

        if not honk_geese:
            print('ДОДЕЛАТЬ')
            return

        if not self.players:
            print('ДОДЕЛАТЬ')
            return

        honk_goose = random.choice(honk_geese)
        player = random.choice(self.players)

        honk_goose(player)
        self.balances[player.name] = player.balance

    def perform_bet(self):
        player = random.choice(self.players)

        if not player:
            print('...')
            return

        if player.balance <= 0:
            print('Дописать')
            return

        max_bet = min(100, player.balance)
        bet_amount = random.randint(1, max_bet)

        if random.choice([True, False]):
            player.balance += bet_amount
            print('дописать')
        else:
            player.balance -= bet_amount
            print('дописать')
        self.balances[player.name] = player.balance

    def perform_steal(self):
        player = random.choice(self.players)
        goose = random.choice(self.geese)

        if not player:
            print('...')
            return

        if not goose:
            print('...')
            return

        if player.balance <= 0:
            print('...')
            return

        max_steal = min(50, player.balance // 2)
        stolen_amount = random.randint(1, max_steal)

        player.balance -= stolen_amount
        self.balances[player.name] = player.balance