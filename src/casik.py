import random

from src._collections.casino_balance import CasinoBalance
from src._collections.goose_collection import GooseCollection
from src._collections.player_collection import PlayerCollection
from src.entities.goose import Goose, WarGoose, HonkGoose
from src.entities.player import Player
from src.entities.chip import Chip
from src.my_logger import logger


class Casino:
    def __init__(self, players: PlayerCollection = None, geese: GooseCollection = None, name: str = 'Гусиный казик'):
        """
        Класс Казино
        :param players: игроки
        :param geese: гуси
        :param name: наименование подпольного гусиного логова
        """
        self.name = name
        self.players = PlayerCollection()
        self.geese = GooseCollection()
        self.balances = CasinoBalance()

        if players is not None:
            for player in players:
                self.register_player(player)

        if geese is not None:
            logger.info(f'А это наши гуси')
            for goose in geese:
                self.register_goose(goose)

        logger.info(f"Казино '{self.name}' открылось. В нем {len(self.players)} игроков и {len(self.geese)} гусей")

    def __repr__(self):
        return f"Casino(name={self.name}, players={self.players}, geese={self.geese})"

    def register_player(self, player: Player) -> None:
        """
        Зарегистрировать игрока, добавив его баланс в коллекцию балансов
        :param player: игрок
        :return:
        """
        if player.is_bankrupt:
            logger.warning('Этого не впускаем. Он банкрот')
            return
        self.players.add(player)
        self.balances[player.name] = player.balance
        logger.info(str(player))

    def register_goose(self, goose: Goose) -> None:
        """
        Регистрация гуся
        :param goose: гусь
        :return:
        """
        self.geese.add(goose)
        logger.info(str(goose))

    def random_player(self) -> Player | None:
        """Рандомный игрок из коллекции игроков"""
        if not self.players:
            logger.warning('Игроков нема')
            return None
        return random.choice(self.players)

    def random_goose(self, goose_type=None) -> Goose | None:
        """Рандомный гусь из коллекции гусей"""
        if goose_type is None:
            type_geese = self.geese
        else:
            type_geese = self.geese.filter_by_type(goose_type)

        if not type_geese:
            logger.warning('От вас даже гуси ушли')
            return None
        return random.choice(type_geese)

    def player_defeated(self, player: Player) -> None:
        """
        Игрок - банкрот -> выгоняем и стираем баланс
        :param player: игрок
        :return:
        """
        self.players.remove_player(player)
        del self.balances[player.name]

    def plus_money(self, player: Player, need) -> bool:
        """
        Если денег не хватает, то происходит обмен фишек на деньги
        :param player: игрок
        :param need: сколько требуется
        :return: True - игрок остается в игре, False - банкрот и нужно выгнать из игры
        """
        logger.info(f'Игроку {player.name} следует пополнить баланс (на {need})')
        if player.amount_chips >= need:
            logger.info(
                f'Игрок пополнил баланс. Количество фишек {player.amount_chips.amount} -> {player.amount_chips.amount - need}')
            player.sell_chips(need)
            self.balances[player.name] = player.balance
        elif player.amount_chips > 0:
            logger.info(
                f'Игрок не может пополнить баланс, так как ему не хватает {need - player.amount_chips.amount} фишек, но пока они есть, оставим его в живых')
        else:
            logger.warning('Пу-пу-пу')
            self.player_defeated(player)
            return False
        return True

    def perform_attack(self) -> None:
        """Атака гуся WarGoose. Отбирает у жертвы сколько то денег на балансе"""
        logger.info("Ивент 'ГУСЬ АТАКУЕТ'")
        war_goose = self.random_goose(WarGoose)
        player = self.random_player()

        if war_goose is None or player is None:
            logger.warning('Так как никого не было, ивент В С Ё')
            return

        logger.info(f'Итак, главные герои этого события')
        logger.info(str(player))
        logger.info(str(war_goose))

        if player.is_bankrupt:
            logger.warning('Пу-пу-пу')
            self.player_defeated(player)
            return

        action = war_goose.attack(player)
        logger.info(action)

        self.balances[player.name] = player.balance
        if player.balance < 0:
            self.plus_money(player, -player.balance)


    def perform_honk(self) -> None:
        """Орущий гусь. Может как помочь своим криком (пололнить баланс), так и ухудшить ситуацию игроку (отобрать деньги)"""
        logger.info("Ивент 'ОРУЩИЙ КУСЬ'")
        honk_goose = self.random_goose(HonkGoose)
        player = self.random_player()

        if honk_goose is None or player is None:
            logger.warning('Так как никого не было, ивент В С Ё')
            return

        logger.info(f'Итак, главные герои этого события')
        logger.info(str(player))
        logger.info(str(honk_goose))

        if player.is_bankrupt:
            logger.warning('Пу-пу-пу')
            self.player_defeated(player)
            return

        action = honk_goose(player)
        logger.info(action)

        self.balances[player.name] = player.balance
        if player.balance < 0:
            self.plus_money(player, -player.balance)

    def perform_bet(self) -> None:
        """Делаем ставочки. Игрок делает ставку и если она зашла, получает эти деньги, если не зашла - отдает из своего кармана"""
        logger.info("Ивент 'Ну эта ставка точно зайдет'")
        player = self.random_player()

        if player is None:
            logger.warning('Так как никого не было, ивент В С Ё')
            return

        logger.info(f'Итак, главный герой этого события')
        logger.info(str(player))

        if player.is_bankrupt:
            logger.warning('Пу-пу-пу')
            self.player_defeated(player)
            return

        if player.balance <= 0:
            logger.info(f'У игрока {player.name} недостаточно средств. Если ему хватит фишек, то он сможет поучаствовать')
            if -player.balance + 1 <= player.amount_chips:
                self.plus_money(player, random.randint(-player.balance + 1, player.amount_chips.amount))
            else:
                logger.info(f'Увы, игроку не хватило {-player.balance + 1 - player.amount_chips.amount} фишек')
                return

        bet_amount = random.randint(1, player.balance)
        logger.info(f'Ставка: {bet_amount}. Игрок крутит рулетку...иииии....')

        if random.choice([True, False]):
            logger.info(f'Игроку {player.name} крупно повезло!')
            player.balance += bet_amount
            self.balances[player.name] = player.balance
        else:
            logger.info(f'Игроку {player.name} не фортануло:(')
            player.balance -= bet_amount

            self.balances[player.name] = player.balance
            if player.balance < 0:
                self.plus_money(player, -player.balance)

    def perform_steal(self) -> None:
        """Робин Гусь. Гусь будет отбирать фишки у богатых игроков и отдавать их бедным"""
        logger.info("Ивент 'Робин Гусь'")
        poor_player, rich_player = self.players.poor_player(), self.players.rich_player()
        goose = self.random_goose(Goose)

        if poor_player is None or goose is None:
            logger.warning('Так как никого не было, ивент В С Ё')
            return

        if poor_player == rich_player:
            logger.warning('Для этого ивента нужно 2 разных игрока')
            return

        logger.info(f'Итак, главные герои этого события')
        logger.info(f'Богатый игрок {rich_player.name} с балансом {rich_player.balance} и {rich_player.amount_chips.amount} фишками')
        logger.info(f'Бедный игрок {poor_player.name} с балансом {poor_player.balance} и {poor_player.amount_chips.amount} фишками')
        logger.info(f'Робин Гусь {goose.name} со своим ГА-ГА-ГА в {goose.honk_volume} МдБ')

        if poor_player.is_bankrupt:
            logger.warning('Пу-пу-пу')
            self.player_defeated(poor_player)
            if rich_player.is_bankrupt:
                logger.warning('Пу-пу-пу')
                self.player_defeated(rich_player)
            return

        if rich_player.balance > 0:
            logger.info(f'Количество фишек богатого игрока {rich_player.amount_chips.amount} -> {rich_player.amount_chips.amount + rich_player.balance}')
            rich_player.amount_chips = rich_player.amount_chips + Chip(rich_player.balance)
            rich_player.balance = 0
            self.balances[rich_player.name] = 0

        if poor_player.balance > 0:
            logger.info(f'Количество фишек бедного игрока {poor_player.amount_chips.amount} -> {poor_player.amount_chips.amount + poor_player.balance}')
            poor_player.amount_chips = poor_player.amount_chips + Chip(poor_player.balance)
            poor_player.balance = 0
            self.balances[poor_player.name] = 0

        logger.info('Робин гусь перевел деньги наших подопытных в фишки для удобства')

        stolen_amount = random.randint(1, rich_player.amount_chips.amount)
        logger.info(f"Робин Гусь украл у богатого игрока {rich_player.name} {stolen_amount} фишек")
        logger.info(f"Количество фишек богатого игрока (уже не очень): {rich_player.amount_chips.amount} -> {rich_player.amount_chips.amount - stolen_amount}")
        rich_player.amount_chips = rich_player.amount_chips - Chip(stolen_amount)

        logger.info(f"Робин гусь отдал эти фишки бедному игроку {poor_player.name}")
        logger.info(f"Количество фишек бедного игрока (уже чуть богаче): {poor_player.amount_chips.amount} -> {poor_player.amount_chips.amount + stolen_amount}")
        poor_player.amount_chips = poor_player.amount_chips + Chip(stolen_amount)

        if rich_player.is_bankrupt:
            logger.info(f'"богатый" игрок {rich_player.name} всё потерял')
            self.player_defeated(rich_player)

    def perform_panic(self) -> None:
        """Словил паничку. У игрока обнуляется весь баланс или он падает со стула, если баланс был <= 0"""
        logger.info("Ивент 'НЕ НАДО ПАНИКИ'")
        goose = self.random_goose(Goose)
        player = self.random_player()

        if player is None or goose is None:
            logger.warning('Так как никого не было, ивент В С Ё')
            return

        logger.info(f'Итак, главные герои этого события')
        logger.info(str(player))
        logger.info(str(goose))

        if player.is_bankrupt:
            logger.warning(f'Пу-пу-пу')
            self.player_defeated(player)
            return

        if player.balance > 0:
            logger.info(f'От паники игрок {player.name} выкинул все деньги в окно')
            player.balance = 0
            self.balances[player.name] = 0

            if player.amount_chips == 0:
                logger.warning(f'Пу-пу-пу')
                self.player_defeated(player)
                return
        else:
            logger.info(f'От паники игрок {player.name} упал со стула')

    def perform_spin(self) -> None:
        """Рулетка. Если выпадает 2, 4, 6 - то у игрока в два раза увеличивается количество фишек и баланс. Если 1, 3, 5 - он банкрот и его выгоняют из игры"""
        logger.info("Ивент 'Удвой или обанкроться")
        player = self.random_player()

        if player is None:
            logger.warning('Так как никого не было, ивент В С Ё')
            return

        logger.info(f'Итак, главный герой этого события')
        logger.info(str(player))

        if player.is_bankrupt:
            logger.warning(f'Пу-пу-пу')
            self.player_defeated(player)
            return

        n = random.randint(1, 6)
        if n % 2 == 0:
            logger.info(f'ИГРОК {player.name} УДВАИВАЕТ СВОЙ БЮДЖЕТ')

            if player.balance > 0:
                logger.info(f'По деньгам: {player.balance} -> {player.balance * 2}')
                player.balance *= 2
                self.balances[player.name] = player.balance

            logger.info(f'По фишкам: {player.amount_chips.amount} -> {player.amount_chips.amount * 2}')
            player.amount_chips = player.amount_chips + player.amount_chips
        else:
            logger.info(f'ИГРОК {player.name} ОБАНКРОТИЛСЯ')
            player.balance = 0
            player.amount_chips = Chip(0)
            logger.warning('Пу-пу-пу')
            self.player_defeated(player)

    def run_event(self) -> None:
        """Запускается случайное событие"""
        events = [self.perform_attack, self.perform_honk, self.perform_bet, self.perform_steal, self.perform_panic, self.perform_spin]
        event = random.choice(events)
        event()

    def stats(self) -> dict:
        """Небольшая статистика"""
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

    def get_players(self) -> None:
        """Текущие игроки с их балансом"""
        for player in self.players:
            print(f"{player.name}: {player.balance}")

    def get_geese(self) -> None:
        """Имена гусей в казино"""
        for goose in self.geese:
            print(f"{goose.name}: {goose.honk_volume}")
