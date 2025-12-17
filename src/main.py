import sys

from src.simulation import run_simulation
from src.exceptions import InvalidArgs, InvalidAmountArgs, NegativeSteps


def main():
    while sys.stdin:
        try:
            user_inp = input('> ')

            if user_inp == 'exit':
                print('Пока пока')
                break

            if user_inp == 'help':
                print("run <steps> <seed>  - запустить симуляцию")
                print("help                - хелпа")
                print("exit                - выход из cli")
                continue

            user_inp = user_inp.split()
            if len(user_inp) != 3:
                raise InvalidAmountArgs()

            if user_inp[0] != 'run':
                raise InvalidArgs()

            try:
                steps = int(user_inp[1])
                seed = int(user_inp[2])
            except ValueError:
                raise InvalidArgs()

            print('СИМУЛЯЦИЯ КАЗИКА НАЧИНАЕТСЯ')
            run_simulation(steps, seed)
            print('\nСИМУЛЯЦИЯ КАЗИКА ЗАКОНЧЕНА')
        except (InvalidAmountArgs, InvalidArgs, NegativeSteps) as e:
            print(e)
        except KeyboardInterrupt:
            print('\nПока пока')


if __name__ == "__main__":
    main()
