import re
import time
from datetime import datetime
from pathlib import Path
from string import ascii_uppercase
from random import sample
from itertools import cycle
from collections import OrderedDict
from . import helpers

letter_values = dict(A=1, E=1, I=1, L=1, N=1, O=1, R=1, S=1, T=1, U=1,
                     D=2, G=2, M=2, B=3, C=3, P=3, F=4, H=4, V=4, J=8, Q=8,
                     K=10, W=10, X=10, Y=10, Z=10, joker=0)


class Player(object):
    letter_pool = dict(A=9, B=2, C=2, D=3, E=5, F=2, G=2, H=2, I=8, J=1, K=1,
                       L=5, M=3, N=6, O=6, P=2, Q=1, R=6, S=6, T=6, U=6, V=2,
                       W=1, X=1, Y=1, Z=1, joker=2)
    prompt = '-> '

    def __init__(self, name: str = 'player_lambda'):
        self.name = str(name)
        self.score = int()
        self.letters = dict(**{letter: 0 for letter in ascii_uppercase}, joker=0)

    @property
    def draw_letters(self):
        missing_letters = 7 - sum(self.letters.values())
        draw = sample(list(self.letter_pool.keys()), counts=self.letter_pool.values(), k=missing_letters)
        self.letters |= {letter: draw.count(letter) for letter in draw}
        self.update_letter_pool(**self.letters)
        return self.letters

    @classmethod
    def update_letter_pool(cls, **draw):
        cls.letter_pool = {key: value - draw[key] for key, value in cls.letter_pool.items()}

    @property
    def unique_id(self):
        return '_'.join([datetime.now().strftime('%Y%m%d%s'), self.name])

    @property
    def screen(self):
        return f'''
#################### your turn ###################
                                           
                {self.name.upper()}            
                                           
###################################################
'''

    def change_name(self, new_name=None):
        if not new_name:
            while not (new_name := input(f'{self.name.title()}, please insert your name.\n{self.prompt}')):
                print("(Q pour rester anonyme)")
            if new_name.casefold() == 'q':
                print(f'Nous n\'avons pas de nom pour vous et continuerons à vous appeler {self.name}')
            else:
                self.name = new_name
                print(f'Merci {new_name.split()[0]}, votre choix est enregistré.')
        else:
            self.name = new_name
            print(f'Merci {new_name.split()[0]}, votre choix est enregistré.')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.unique_id


class ScrabbleParty(object):

    def __init__(self, players, coordinates_table, playground_table):
        self.lexic = Path.cwd() / 'data-ft-par-labs' / 'Projects' / 'Week-1' / 'your-project' / 'scrabble_game' / 'resources' / 'lexique.txt'
        self.players = OrderedDict()
        for one_player, idx in zip(players, range(len(players))):
            self.players[idx] = one_player
        self.coordinates_table = coordinates_table
        self.playground_table = playground_table
        self.valid_propositions = []
        self.turn_cycle = cycle(range(len(players)))
        self.first_turn = True

    def turn(self):
        if self.first_turn:
            for one_player in self.players.values():
                helpers.clear_screen()
                print(one_player.screen, helpers.spacing, helpers.spacing, sep='\n')
                print(f'Here are your first letters, 3 seconds to memorize it :)', '\n')
                helpers.prettify_letter(one_player.draw_letters)
                time.sleep(5)
            self.first_turn = False

        for idx in self.turn_cycle:
            player = self.players[idx]
            endturn = False
            table_mode = self.coordinates_table
            while not endturn:
                helpers.clear_screen()
                helpers.get_pretty_table(table_mode)
                helpers.prettify_letter(player.letters)
                query = input(
                    f"{player.name} please insert your word or the letter 't' to change table mode from playground\n"
                    f"to coordinates or 'h' for the help.{helpers.prompt}").casefold()

                if not (self.regex_compliance(query) and query):
                    helpers.clear_screen()
                    print(f'Word cannot be empyt or contain digit nor punctation or spaces, please try again.')
                    time.sleep(3)
                    continue
                elif query == 't':
                    table_mode = self.playground_table if table_mode != self.playground_table else self.coordinates_table
                    continue
                elif query == 'p':
                    endturn = True
                    continue
                elif query == 'h':
                    answer = str()
                    while answer != 'q':
                        helpers.help_screen()
                        print(helpers.spacing)
                        answer = input(f'Q pour revenir à l\'écran de jeu.{helpers.prompt}').casefold()
                    continue
                elif query == 'r':
                    answer = str()
                    while answer != 'q':
                        helpers.rules_screen()
                        print(helpers.spacing)
                        answer = input(f'Q pour revenir à l\'écran de jeu.{helpers.prompt}').casefold()
                    continue
                elif query == 'q':
                    helpers.exit_game()
                elif not self.check_word_validity(query):
                    print(f'Your word "{query}" is not accepted by our dictionnary. Please correct any typo or swith '
                          f'to another one.')
                    time.sleep(3)
                    continue
                else:
                    from_point, to_point = input('Insert two coordinates, separated with a comma.').split(', ')
                    self.check_the_coordinates(from_point.upper(), to_point.upper())

    @staticmethod
    def regex_compliance(query):
        regex_query = re.compile(r'[^àèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÃÑÕäëïöüÿÄËÏÖÜŸçÇßØøÅåÆæœA-Za-z]')
        return True if not regex_query.findall(query) else False

    @staticmethod
    def command_checker(query):
        return True if len(query) == 1 and query in 'harpta' else False

    @staticmethod
    def check_the_coordinates(from_point, to_point):
        row_f, col_f = from_point
        row_t, col_t = to_point
        conditions_1 = [row_f in ascii_uppercase[:15],
                        row_t in ascii_uppercase[:15],
                        int(col_t) in range(1, 16),
                        int(col_f) in range(1, 16)]
        if False not in conditions_1:
            conditions_2 = [ascii_uppercase[:15].index(row_f) <= ascii_uppercase[:15].index(row_t),
                            int(col_f) <= int(col_t)]
            return True if False not in conditions_2 else False
        else:
            return False

    def get_the_array(self, from_point, to_point):
        # first case : the array is horizontal
        pass

    def check_word_validity(self, query: str):
        with open(self.lexic, 'r') as f:
            for one_word in f:
                if one_word.strip().casefold() == query:
                    return True
        return False

    @staticmethod
    def transpose_the_table(table):
        return list(zip(*table))


if __name__ == '__main__':
    pass
