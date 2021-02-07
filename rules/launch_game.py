import argparse
from rules.assets import Player
from string import ascii_uppercase
from typing import List, Set
from art import tprint
from rules.helpers import clear_screen, rules, hello, spacing, introduction
from time import sleep


def argument_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', nargs='?', const=2, type=int, default=2)
    # parser.add_argument('--mode', nargs='?', default='n', type=str)
    return parser.parse_args()


def init():
    args = argument_parse()
    players = [Player(f'player-{i}') for i in range(1, args.players + 1)]
    return players


def welcome_screen(players: List[Player]):
    names = [player.name for player in players]
    clear_screen()
    tprint('scrabble', 'rnd-xlarge')
    print(spacing)
    for part in hello.split('\n'):
        print(f'{part.upper():^100}\n')
    print(f"Hello {', '.join(names[:-1])} and {names[-1]} !",
          introduction, sep=f'{spacing}')
    sleep(6)
    print(spacing)
    for part in rules.split('\n'):
        print(f'{part}')
    sleep(10)


def create_coordinates_table() -> List[List[str]]:
    coordinates_table = list()
    for letter in ascii_uppercase[:15]:
        coordinates_table.append([letter + str(value) for letter, value in list(zip(letter * 15, range(1, 16)))])
    return coordinates_table


def create_playground_table() -> List[List[int]]:
    playground_table = list()
    for i in range(15):
        playground_table.append([0 for i in range(15)])
    return playground_table


if __name__ == '__main__':
    pass
