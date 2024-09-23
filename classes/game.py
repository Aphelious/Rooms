import logging
import os
import time
from .item import Item

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

    
    def parse_item_instructions(self, raw_item_instructions:str):
        # Preformat the input:
        sanitized_item_instructions = raw_item_instructions.lower()
        tokens = sanitized_item_instructions.split(' ')
        verbs = {'read', 'inspect', 'use', 'combine'}
        prepositions = {'on', 'with', 'and', 'of'}
        descriptive_words = {'side', 'back', 'top', 'bottom', 'inside', 'outside'}

        # If one and only one word in the instructions isn't a predefined verb, reject:
        if not verbs.intersection(tokens) or not len(verbs.intersection(tokens)) == 1:
            print(f'"{raw_item_instructions}" is not possible.')

        # Consider what is actually active for the player:
        active_objects = self.player.get_active_items() # dict
        active_object_names = [x.lower() for x in active_objects.keys()]
        instructions_objects = [x for x in tokens if x not in verbs]
        instructions_objects = [x for x in instructions_objects if x not in prepositions]
        instructions_objects = [x for x in instructions_objects if x not in descriptive_words]

        invalid_objects = [x for x in instructions_objects if x not in active_object_names]
        # breakpoint()
        if invalid_objects:
            print(f'"{raw_item_instructions}" is not possible.')

        if tokens[0] == 'read' and tokens[1] in active_object_names and len(tokens) == 2:
            subject = tokens[1]
            self.clear_screen()
            print(active_objects[subject.title()].item_writing)
            return
        
        elif tokens[0] == 'inspect':
             self.inspect(tokens, prepositions, descriptive_words, active_objects,
                          active_object_names, instructions_objects)
             return

        elif tokens[0] == 'use':
            pass 
        
        elif tokens[0] == 'combine':
            pass 

        else:
            print(f'"{raw_item_instructions}" is not possible.')
            return

        # Read needs: Read, active_object    
        # Inspect needs: Inspect, descriptive word, preposition, active_object to be valid
        # Use needs: Use, active_object, on|with, active_object, on, active_object
        # Combine needs: Combine, active_object, with, active_object, with... n number of times -dont have this funtionality just yet
        # Need a valid combination of verbs and item names, or verbs-item names-attributes to work
        
        
    def inspect(self, tokens, prepositions, descriptive_words, active_objects,
                active_object_names, instructions_objects):

        # If asked to inspect the item itself, print the item description:
        if len(tokens) == 2 and tokens[1] in active_object_names:
            self.clear_screen()
            subject_item = active_objects[tokens[1].title()]
            print(subject_item.item_description)

        # If asked to inspect a part of the item, check to see if there's an attibute associated:
        elif tokens[1] in descriptive_words and tokens[2] in prepositions and tokens[3] in active_object_names:
            subject_item = active_objects[tokens[1].title()]
            result = subject_item.attributes.get([f'{tokens[1]} {tokens[2]} {tokens[3]}'])
            if not result:
                print('There\'s nothing there.')
                return
            elif type(result) == str:
                print(result)
                return
            elif type(result) == Item:
                pass



    def clear_screen(self):
        # check and make call for specific operating system
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    def game(self):
        '''The main game loop'''

        game_in_progress = True

        self.clear_screen()
        print('Welcome to the game!\n')
        print(self.map.current_room.enter_message)
        while game_in_progress != False:
            self.display_menu(self.main_menu)
            selection = input()

            if selection == '1':
                self.clear_screen()
                self.display_menu(self.move_menu)
                selection = input()
                if selection == '8':
                    self.clear_screen()
                    object_name = self.map.move_player('north')
                    if not object_name:
                        continue
                    elif object_name in ('Entrance', 'Exit'):
                        print('You see a door, walk through it?')
                    else:
                        object = self.player.items[object_name]
                        print(f'You found a {object.display_name}!\n{object.item_description}')
                        object.activate()
                if selection == '6':
                    self.clear_screen()
                    object_name = self.map.move_player('east')
                    if not object_name:
                        continue
                    elif object_name in ('Entrance', 'Exit'):
                        print('You see a door, walk through it?')
                    else:
                        object = self.player.items[object_name]
                        print(f'You found a {object.display_name}!\n{object.item_description}')
                        object.activate()
                if selection == '2':
                    self.clear_screen()
                    object_name = self.map.move_player('south')
                    if not object_name:
                        continue
                    elif object_name in ('Entrance', 'Exit'):
                        print('You see a door, walk through it?')
                    else:
                        object = self.player.items[object_name]
                        print(f'You found a {object.display_name}!\n{object.item_description}')
                        object.activate()
                if selection == '4':
                    self.clear_screen()
                    object_name = self.map.move_player('west')
                    if not object_name:
                        continue
                    elif object_name in ('Entrance', 'Exit'):
                        print('You see a door, walk through it?')
                    else:
                        object = self.player.items[object_name]
                        print(f'You found a {object.display_name}!\n{object.item_description}')
                        object.activate()
                    
            if selection == '2':
                self.clear_screen()
                while True:
                    self.player.check_inventory()
                    # self.display_menu(self.inventory_menu)
                    item_instructions = input('\nWhat do you want to do in the inventory? (type "main menu" to go back)\nYou can Read, Inspect, Use, or Combine items.\n\n')
                    if item_instructions == 'main menu':
                        # self.clear_screen()
                        break
                    self.parse_item_instructions(item_instructions)
                    continue

            