import sys
from prettytable import PrettyTable
from typing import List, Union, Dict
import os
import time

prompt = '\n-> '

rules = '''In this game the goal is to find words from letters you have. Each player begin to pick
7 letters randomly and each time he succeed to pu a word on the board he must draw letters to
to reach 7.

    BASIC PRINCIPLES
    Each letter have its own value and a valid word give points to the player, the amount being the sum of
    the letters of that word. 
    
    WIN THE GAME
    • the minimum of letters for a word is 2
    • the plurals are accepted
    • the first word should have a letter placed in the center cell
    • the following ones should have at least one letter already in place on the board
    • the sum of the letter includes the letter already on the board
    • if a player create a word by using a letter AND modiying another word, all values are added
    • the word must be place from left to right or from up to down
    • when needed, a player can refuse to play. He will wait his turn without any penalty
    
    ENDGAME
    • no more letters : a player have no letter at his disposal an can not draw (no more letter avalaible)
    • no more ideas : nobody can play, the value of each remaining letters are subtracted of each score  
    • all players refuse to play tree times in a row : it's a draw'''

hello = '''Hi and welcome to this OG game
    the mighty ol' school
    s c r a b b l e

    _______________
    _______________'''

introduction = f"We'll briefly present you the rules of the game. You need to know few commands\nto swith between " \
               f"display modes. No need to memorize all of it, you can display\nthis help at any time by inserting " \
               f"the letter 'h'. Good game!"

spacing = '\n\n'

aide = '''
################# Insert q to quit ################
####                                           ####
####                AIDE SCRABBLE              ####
####                                           ####
###################################################

        h -> afficher aide
        r -> afficher les règles
        p -> passer son tour
        t -> changer mode affichage de la table

#################################################
'''

exiting = '''
###################################################
####                                           ####
####                 AU REVOIR                 ####
####                                           ####
###################################################
'''


def help_screen():
    clear_screen()
    for one_line in aide.split('\n'):
        print(f'{one_line}')


def rules_screen():
    clear_screen()
    for part in rules.split('\n'):
        print(f'{part}')


def exit_game():
    clear_screen()
    for part in exiting.split('\n'):
        print(f'{part}')
    time.sleep(4)
    clear_screen()
    sys.exit()


def clear_screen():
    os.system('clear')


def prettify_letter(player_letters: Dict):
    board = PrettyTable()
    letters_to_display = [key for key, value in player_letters.items() if value]
    entries = [entry for key in letters_to_display if (entry := player_letters[key])]
    board.field_names = letters_to_display
    board.add_row(entries)
    print(board)
    return None


def get_pretty_table(coordinates: List[List[Union[int, str]]]):
    pretty_table = PrettyTable(header=False)
    for one_row in coordinates:
        pretty_table.add_row(one_row)
    print(pretty_table)
    return None


def get_real_names(players):
    out = list()
    for one_player in players:
        one_player.change_name()
        out.append(one_player)
        time.sleep(2)
        clear_screen()
    return out


if __name__ == '__main__':
    pass
