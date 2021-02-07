from rules import launch_game
from rules.assets import ScrabbleParty
from rules.helpers import get_real_names, clear_screen


def setup():
    players = launch_game.init()
    coordinates_table = launch_game.create_coordinates_table()
    playground_table = launch_game.create_playground_table()
    clear_screen()
    players = get_real_names(players)
    launch_game.welcome_screen(players)
    return dict(players=players,
                coordinates_table=coordinates_table,
                playground_table=playground_table)


def play_game(**kwargs):
    party = ScrabbleParty(**kwargs)
    while True:
        party.turn()


if __name__ == '__main__':
    data_game = setup()
    play_game(**data_game)
