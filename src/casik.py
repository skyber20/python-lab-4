import random

from src.collections.casino_balance import CasinoBalance
from src.collections.goose_collection import GooseCollection
from src.collections.player_collection import PlayerCollection
from src.entities.goose import Goose, WarGoose, HonkGoose
from src.entities.player import Player
from src.my_logger import logger


class Casino:
    def __init__(self, players: PlayerCollection = None, geese: GooseCollection = None, name: str = 'Гусиный казик'):
        self.name = name
        self.players = PlayerCollection()
        self.geese = GooseCollection()
        self.balances = CasinoBalance()

        if players is not None:
            for player in players:
                self.register_player(player)

        if geese is not None:
            for goose in geese:
                self.register_goose(goose)

        logger.info(f"Казино '{self.name}' открылось. В нем {len(self.players)} игроков и {len(self.geese)} гусей")

    def register_player(self, player: Player):
        self.players.add(player)
        self.balances[player.name] = player.balance

    def register_goose(self, goose: Goose):
        self.geese.add(goose)

    def random_player(self):
        if not self.players:
            logger.warning('Игроков нема')
            return None
        return random.choice(self.players)

    def random_goose(self, goose_type=None):
        if goose_type is None:
            type_geese = self.geese.filter_by_type(Goose)
        else:
            type_geese = self.geese.filter_by_type(goose_type)

        if not type_geese:
            logger.warning('От вас даже гуси ушли')
            return None
        return random.choice(type_geese)

    def perform_attack(self):
        logger.info("Ивент 'ГУСЬ АТАКУЕТ'")
        war_goose = self.random_goose(WarGoose)
        player = self.random_player()

        if war_goose is None or player is None:
            logger.warning('Так как никого не было, ивент В С Ё')
            return

        logger.info(f'Итак, главные герои этого события')
        logger.info(f'Игрок {player.name} с балансом {player.balance}')
        logger.info(f'Гусь {war_goose.name} со своим ГА-ГА-ГА в {war_goose.honk_volume} МдБ')

        action = war_goose.attack(player)
        logger.info(action)
        self.balances[player.name] = player.balance

    def perform_honk(self):
        logger.info("Ивент 'ОРУЩИЙ КУСЬ'")
        honk_goose = self.random_goose(HonkGoose)
        player = self.random_player()

        if honk_goose is None or player is None:
            logger.warning('Так как никого не было, ивент В С Ё')
            return

        logger.info(f'Итак, главные герои этого события')
        logger.info(f'Игрок {player.name} с балансом {player.balance}')
        logger.info(f'Гусь {honk_goose.name} со своим ГА-ГА-ГА в {honk_goose.honk_volume} МдБ')

        action = honk_goose(player)
        logger.info(action)
        self.balances[player.name] = player.balance

    def perform_bet(self):
        logger.info("Ивент 'Ну эта ставка точно зайдет'")
        player = self.random_player()

        if player is None:
            logger.warning('Так как никого не было, ивент В С Ё')
            return

        logger.info(f'Итак, главный герой этого события')
        logger.info(f'Игрок {player.name} с балансом {player.balance}')

        if player.balance <= 0:
            logger.info(f'У игрока {player.name} баланс стремится к {player.balance}. Ивент закончился')
            return

        bet_amount = random.randint(1, min(100, player.balance))
        logger.info(f'Ставка: {bet_amount}. Игрок крутит рулетку...иииии....')

        if random.choice([True, False]):
            logger.info(f'Игроку {player.name} крупно повезло!')
            player.balance += bet_amount
        else:
            logger.info(f'Игроку {player.name} не фортануло:(')
            player.balance -= bet_amount
        self.balances[player.name] = player.balance

    def perform_steal(self):
        logger.info("Ивент 'Гусь-воришка'")
        player = self.random_player()
        goose = self.random_goose(Goose)

        if player is None or goose is None:
            logger.warning('Так как никого не было, ивент В С Ё')
            return

        logger.info(f'Итак, главные герои этого события')
        logger.info(f'Игрок {player.name} с балансом {player.balance}')
        logger.info(f'Гусь {goose.name} со своим ГА-ГА-ГА в {goose.honk_volume} МдБ')

        if player.balance <= 0:
            logger.info(f"У игрока {player.name} баланс {player.balance}, ему нечего было терять. Ивент закончился")
            return

        stolen_amount = random.randint(1, player.balance // 2)

        logger.info(f"Гусь {goose.name} украл у игрока {player.name} {stolen_amount} валюты")
        player.balance -= stolen_amount
        self.balances[player.name] = player.balance

    def perform_panic(self):
        logger.info("Ивент 'ПАНИКА'")
        goose = self.random_goose(Goose)
        player = self.random_player()

        if player is None or goose is None:
            logger.warning('Так как никого не было, ивент В С Ё')
            return

        logger.info(f'Итак, главные герои этого события')
        logger.info(f'Игрок {player.name} с балансом {player.balance}')
        logger.info(f'Гусь {goose.name} со своим ГА-ГА-ГА в {goose.honk_volume} МдБ')

        if player.balance <= 0:
            logger.info(f'Игроку {player.name} и так не было чего терять')
            return

        logger.info(f'От паники игрок {player.name} выкинул все деньги в окно')
        player.balance = 0
        self.balances[player.name] = 0

    def run_event(self):
        events = [self.perform_attack, self.perform_honk, self.perform_bet, self.perform_steal, self.perform_panic]
        event = random.choice(events)
        event()

    def stats(self):
        logger.info('Чекаем текущую стату')
        total_balance = sum(p.balance for p in self.players)

        return {
            'name': self.name,
            'players': len(self.players),
            'geese': len(self.geese),
            'war_geese': len(self.geese.filter_by_type(WarGoose)),
            'honk_goose': len(self.geese.filter_by_type(HonkGoose)),
            'total_balance': total_balance,
        }

    def get_players(self):
        for player in self.players:
            print(f"{player.name}: {player.balance}")

    def get_geese(self):
        for goose in self.geese:
            print(f"{goose.name}: {goose.honk_volume}")

    def __repr__(self):
        return f"Casino(name={self.name}, players={self.players}, geese={self.geese})"
