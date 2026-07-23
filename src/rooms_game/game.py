import logging
import os
import time
from rooms_game.item import Item

class Game:
    '''The main class in the game.'''

    def __init__(self, map, player, debug=False) -> None:
        if debug: 
            self.logger = logging.Logger('debug_logger')
        self.map = map
        self.player = player
        self.main_menu = {
            'input_message': '\nWhat do you want to do?',
            'options': {
            '1': 'Move',
            '2': 'Enter inventory',
            'x': 'Exit game'
        }}
        self.move_menu = {
            'input_message': '\nWhich direction do you want to move?',
            'options': {
            '8': 'North',
            '6': 'East',
            '2': 'South',
            '4': 'West',
            'm': 'Main menu'
        }}
        # self.inventory_menu = {
        #     'input_message': '\nWhat do you want to do in the inventory?\nYou can Read, Inspect, Use, or Combine items.',
        #     'options': {
        #     '1': 'Read item',
        #     '2': 'Inspect item',
        #     '3': 'Use item',
        #     '4': 'Combine items'
        # }}
        self.game = self.game()


    def display_message(message):
        time.sleep(0.5)
        return message

     
    def construct_current_items_menu(self, input_message:str='\nWhich item?'):
        items_menu = {
            'input_message': input_message,
            'options': {}
        }
        for i, item_tuple in enumerate(self.player.items.items()):
            item_name = item_tuple[0]
            item_object = item_tuple[1]
            if item_object.is_active and not item_object.parent_item:
                items_menu['options'][str(i+1)] = item_object
        return items_menu

    
    @staticmethod
    def display_menu(menu):
        print(menu['input_message'])
        for k,v in menu['options'].items():
            if type(v) == Item:
                print(f'{k}. {v.display_name}')
            else:
                print(f'{k}. {v}')

    @staticmethod
    def display_move_menu():
        '''Render the movement options as a compass, matching the numpad layout.'''
        print('\nWhich direction do you want to move?\n')
        print('       8. North')
        print('4. West       6. East')
        print('       2. South')
        print('\nm. Main menu')

    
    # Vocabulary the parser understands. Verbs map to handler methods; the
    # connector words split a command into separate noun phrases. Adding a new
    # verb is a one-line change here plus its handler - no branching sprawl.
    VERBS = {'read', 'inspect', 'use', 'combine'}
    CONNECTORS = {'on', 'with', 'and'}

    def parse_item_instructions(self, raw_item_instructions: str):
        tokens = raw_item_instructions.lower().strip().split()
        if not tokens:
            self.reject(raw_item_instructions)
            return

        verb, rest = tokens[0], tokens[1:]
        if verb not in self.VERBS:
            self.reject(raw_item_instructions)
            return

        handler = {
            'read': self.handle_read,
            'inspect': self.handle_inspect,
            'use': self.handle_use,
            'combine': self.handle_combine,
        }[verb]
        handler(rest, raw_item_instructions)

    @staticmethod
    def reject(raw):
        print(f'"{raw}" is not possible.')

    @classmethod
    def split_phrases(cls, tokens):
        '''Split a token list into noun phrases around connector words
           (on/with/and), dropping the connectors. Multi-word item names survive
           because we only break on connectors, never on plain spaces.'''
        phrases, current = [], []
        for token in tokens:
            if token in cls.CONNECTORS:
                if current:
                    phrases.append(' '.join(current))
                    current = []
            else:
                current.append(token)
        if current:
            phrases.append(' '.join(current))
        return phrases

    def handle_read(self, rest, raw):
        self.clear_screen()
        if not self.player.read_item(' '.join(rest)):
            self.reject(raw)

    def handle_inspect(self, rest, raw):
        self.clear_screen()
        # "inspect <part> of <item>" -> inspect a named part.
        if 'of' in rest:
            idx = rest.index('of')
            part = ' '.join(rest[:idx])
            item = ' '.join(rest[idx + 1:])
            if self.player.inspect_attribute(item, part):
                return
            print('There\'s nothing there.')
            return
        # "inspect <item>" -> print the item description.
        if self.player.describe_item(' '.join(rest)):
            return
        self.reject(raw)

    def handle_use(self, rest, raw):
        phrases = self.split_phrases(rest)
        if len(phrases) < 2:
            self.reject(raw)
            return
        self.clear_screen()
        self.player.combine_items(*phrases)

    def handle_combine(self, rest, raw):
        phrases = self.split_phrases(rest)
        if len(phrases) < 2:
            self.reject(raw)
            return
        self.clear_screen()
        self.player.combine_items(*phrases)



    def clear_screen(self):
        # check and make call for specific operating system
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    # Numpad-style movement keys -> direction names understood by Map.move().
    MOVE_KEYS = {'8': 'north', '6': 'east', '2': 'south', '4': 'west'}

    def handle_move(self, direction):
        '''Step one space, then resolve whatever the player landed on.'''
        self.clear_screen()
        occupant = self.map.move(direction)
        if occupant is None:
            return
        self.resolve_space(occupant)

    def resolve_space(self, occupant):
        '''Single place where landing on an occupied space is interpreted:
           a door (Entrance/Exit) or an item. Hazards will slot in here too.'''
        if occupant in ('Entrance', 'Exit'):
            self.handle_door(occupant)
        else:
            item = self.player.items[occupant]
            print(f'You found a {item.display_name}!\n{item.item_description}')
            item.activate()

    def handle_door(self, door_label):
        '''Offer to walk through a door. Passing through is always a choice.'''
        portal = self.map.destination(door_label)
        if not portal:
            print('You have reached a heavy door, but it will not open. Not yet.')
            return
        answer = input('You see a door. Walk through it? (y/n)\n').strip().lower()
        if answer in ('y', 'yes'):
            room = self.map.transition(portal)
            self.clear_screen()
            print(room.enter_message)
        else:
            print('You step back from the door.')

    def game(self):
        '''The main game loop'''

        game_in_progress = True

        self.clear_screen()
        print('Welcome to the game!\n')
        print(self.map.current_room.enter_message)
        while game_in_progress:
            self.display_menu(self.main_menu)
            selection = input()

            if selection == 'x':
                self.clear_screen()
                print('You give up on escaping. Goodbye.')
                game_in_progress = False

            elif selection == '1':
                self.clear_screen()
                self.display_move_menu()
                selection = input()
                if selection in self.MOVE_KEYS:
                    self.handle_move(self.MOVE_KEYS[selection])
                # 'm' (or anything else) simply falls back to the main menu.

            elif selection == '2':
                self.clear_screen()
                while True:
                    self.player.check_inventory()
                    item_instructions = input('\nWhat do you want to do in the inventory? (type "main menu" to go back)\nYou can Read, Inspect, Use, or Combine items.\n\n')
                    if item_instructions == 'main menu':
                        break
                    self.parse_item_instructions(item_instructions)

            