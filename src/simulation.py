import random
import string

from src.collections.goose_collection import GooseCollection
from src.collections.player_collection import PlayerCollection
from src.entities.player import Player
from src.entities.goose import Goose, HonkGoose, WarGoose
from src.entities.chip import Chip
from src.my_logger import logger
from src.casik import Casino
from src.exceptions import NegativeSteps


def generate_name():
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for _ in range(8))


def run_simulation(steps: int = 20, seed: int | None = None) -> None:
    if steps <= 0:
        raise NegativeSteps()
    if seed is not None:
        random.seed(seed)

    cnt = max(3, int(steps * 0.5))
    players = PlayerCollection()
    geese = GooseCollection()

    for _ in range(cnt):
        player = Player('P_' + generate_name(), random.randint(0, 500), Chip(random.randint(0, 500)))
        goose = random.choice([Goose, HonkGoose, WarGoose])('G_' + generate_name(), random.randint(1, 10))

        players.add(player)
        geese.add(goose)

    casino = Casino(players, geese)

    for step in range(1, steps + 1):
        print()
        logger.info(f'Шаг: {step}')
        casino.run_event()
