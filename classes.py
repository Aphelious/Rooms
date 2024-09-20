import random
import time
import os
import logging

class Room:
    def __init__(self, room_dict:dict) -> None:
        self.name = room_dict["name"]
        self.enter_message = room_dict["enter_message"]
        self.wall_message = room_dict["wall_message"]
        self.empty_space_message = room_dict["empty_space_message"]
        self.objects = room_dict["objects"]
        self.shape = self.get_shape()
        self.entrance = self.get_random_wall_space()
        self.exit = self.get_random_wall_space()
        self.object_locations = {}  # stores locations of all objects and entrance and exit
        self.set_entrance_and_exit()
        self.place_objects(self.objects)


    def get_shape(self):
        '''Build a dict of lists that represents the shape of a room between 3 and 5 rows, and between 3 and 5 columns.
           Example shape: 
                          {1: [-2, -1, 0, 1, 2], 
                           2: [-2, -1, 0, 1], 
                           3:     [-1, 0, 1], 
                           4: [-2, -1, 0, 1, 2]
                           5: [-2, -1, 0, 1]}'''

        shape = {}
        for row in range(random.randint(3,5)):

            # Generate the random variable row length:
            col_num = random.randint(3,5)
            cols = [-1,0,1]
            if col_num == 4:
                cols.append(random.choice([-2,2]))
            elif col_num == 5:
                cols.extend([-2,2])
            
            # Insert it into the shape dict:
            shape[row+1] = sorted(cols)
        return shape
    

    def get_random_space(self) -> tuple:
        '''Reads in the shape dictionary, returns a tuple of random space (row, col) 
           from the available spaces in the shape.'''    

        row_index = random.randint(1, len(self.shape))  
        row = self.shape[row_index]  
        space = random.choice(row)
        return {"Row":row_index, "Column":space}


    def get_random_wall_space(self) -> tuple:
        '''Reads in the shape dictionary, returns a tuple of random space (row, col) 
           from the available spaces in the shape only if that space is along a wall.'''   

        row_index = random.choice(list(self.shape.keys()))
        # If the randomly-selected row is either the 'bottom' or 'top' of a room, then
        # any space is eligable for selection:
        if row_index == 1 or row_index == list(self.shape.keys())[-1]:
            row = self.shape[row_index]  
            col = random.choice(row)
            space = {"Row":row_index, "Column":col}
            return space
        
        # If the row is in the 'middle' of a room then we need to select a space at either
        # end for it to be a wall space:
        else:
            row = self.shape[row_index]
            eligible_spaces = []
            eligible_spaces.append(row[0])
            eligible_spaces.append(row[-1])
            col = random.choice(eligible_spaces)
            space = {"Row":row_index, "Column":col}
            return space


    def check_space_exists(self, space) -> bool: 
        '''Takes in a space tuple and checks to see if that space is exists in the current room, returning True or False.'''

        row = space["Row"]
        col = space["Column"]
        if row in self.shape.keys() and col in self.shape[row]:
            return True
        return False
    

    def check_space_occupied(self, space:dict) -> bool:
        '''Takes in a space dict and checks to see if that space is already occupied, returning True or False.'''

        if self.convert_space_dict_to_tuple(space) in self.object_locations.keys():
            return True
        else:
            return False


    def convert_space_dict_to_tuple(self, space):
        row = space["Row"]
        col = space["Column"]
        return (row, col)


    def set_entrance_and_exit(self):
        self.object_locations[self.convert_space_dict_to_tuple(self.entrance)] = 'Entrance'
        self.object_locations[self.convert_space_dict_to_tuple(self.exit)]= 'Exit'


    def place_objects(self, objects) -> None:
        '''Takes in a list of all objects supplied when instantiating the room and updates
           the object_locations dictionary to store the location:name of each item, hazard,
           entrance, and exit in the room'''

        for object in objects:
            eligible_space_found = False
            while not eligible_space_found:
                space = self.get_random_space()
                if not self.check_space_occupied(space):
                    self.object_locations.update({self.convert_space_dict_to_tuple(space):object})
                    break
                else:
                    continue


    def __repr__(self) -> str:
        return f'''{self.name} \n Shape: {self.shape} \n Entrance: {self.entrance} \n Exit: {self.exit}
 Objects: {self.objects} \n Object locations: {self.object_locations}\n'''


class Map:
    '''Class to store all the rooms and their connections, which form a graph.'''

    def __init__(self, rooms) -> None:
        self.rooms = rooms
        self.current_room = random.choice(self.rooms)
        self.player_current_space = self.current_room.entrance


    def move_north(self):
        new_space = {"Row":self.player_current_space["Row"] + 1, "Column":self.player_current_space["Column"]}  # change row by add 1
        if self.current_room.check_space_exists(new_space):
            self.player_current_space = new_space
            return new_space
        else:
            print(self.current_room.wall_message)
            return


    def move_east(self):
        new_space = {"Row":self.player_current_space["Row"], "Column":self.player_current_space["Column"] + 1}  # change column by adding 1
        if self.current_room.check_space_exists(new_space):
            self.player_current_space = new_space
            return new_space
        else:
            print(self.current_room.wall_message)
            return


    def move_south(self):
        new_space = {"Row":self.player_current_space["Row"] - 1, "Column":self.player_current_space["Column"]} #  # change row by sub 1
        if self.current_room.check_space_exists(new_space):
            self.player_current_space = new_space
            return new_space
        else:
            print(self.current_room.wall_message)
            return


    def move_west(self):
        new_space = {"Row":self.player_current_space["Row"], "Column":self.player_current_space["Column"] - 1}  # change column by sub 1
        if self.current_room.check_space_exists(new_space):
            self.player_current_space = new_space
        else:
            print(self.current_room.wall_message)
            return


    def move_player(self, direction:str) -> None:
        if direction == 'north':
            new_space = self.move_north()
            if not new_space:
                return
            if not self.current_room.check_space_occupied(new_space):
                print(self.current_room.empty_space_message)
            else:
                ()
                object_name = self.current_room.object_locations[self.current_room.convert_space_dict_to_tuple(new_space)]
                if object_name in ('Entrance', 'Exit'):
                    print('You see a door, walk through it?')
                else:
                    return object_name

        if direction == 'east':
            new_space = self.move_east()
            if not new_space:
                return
            if not self.current_room.check_space_occupied(new_space):
                    print(self.current_room.empty_space_message)
            else:
                ()
                object = self.current_room.object_locations[self.current_room.convert_space_dict_to_tuple(new_space)]
                if object in ('Entrance', 'Exit'):
                    print('You see a door, walk through it?')
                else:
                    return object_name
            
        if direction == 'west':
            new_space = self.move_west()
            if not new_space:
                return
            if not self.current_room.check_space_occupied(new_space):
                print(self.current_room.empty_space_message)
            else:
                ()
                object = self.current_room.object_locations[self.current_room.convert_space_dict_to_tuple(new_space)]
                if object in ('Entrance', 'Exit'):
                    print('You see a door, walk through it?')
                else:
                    return object_name

        if direction == 'south':
            new_space = self.move_south()
            if not new_space:
                return
            if not self.current_room.check_space_occupied(new_space):
                print(self.current_room.empty_space_message)
            else:
                ()
                object = self.current_room.object_locations[self.current_room.convert_space_dict_to_tuple(new_space)]
                if object in ('Entrance', 'Exit'):
                    print('You see a door, walk through it?')
                else:
                    return object_name


    def get_entrances_and_exits(self) -> list:
        entrances_and_exits = []
        for room in self.rooms:
            entrances_and_exits.append(room.entrance)
            entrances_and_exits.append(room.exit)
        return entrances_and_exits



class Player:
    def __init__(self, items_dict) -> None:
        self.name = 'Mike'
        self.items = items_dict


    @staticmethod
    def format_item_name(item_name):
        return item_name.lower().replace(' ', '_')
    

    def get_active_items(self) -> list:
        return [x.name for x in self.items.values() if x.is_active]


    def is_item_active(self, item_name):
        print(self.items[item_name].is_active)


    def validate_item(self, item_name):
        item_name = self.format_item_name(item_name)
        active_items = self.get_active_items()
        if item_name in active_items:
            return True
        return False


    def describe_item(self, item_name):
        if self.validate_item(item_name):
            print(self.items[item_name].print_item_description())
        else:
            print(f'You don\'t have "{item_name.lower()}"')


    def read_item(self, item_name):
        if self.validate_item(item_name):
            print(self.items[item_name].item_writing)
        else:
            print(f'You don\'t have "{item_name.lower()}"')


    def inspect_item_attribute(self, item_name, attribute):
        if attribute in self.items[item_name].attributes.keys():
            attribute_name = self.items[item_name].attributes[attribute]
            print(self.items[attribute_name].item_description)
        else:
            print(f'Cannot inspect "{attribute}"')


    def list_items(self):
        for name,item in self.items.items():
            if item.is_active:
                print(item.name)


    def list_inventory(self):
        print('You have the following items in your sachel:\n')
        for name,item in self.items.items():
            if item.is_active and not item.parent_item:
                print(item.display_name)


    def parse_effects_dict(self, effects_dict):
        # "effects": {'brass_key_piece_1': 'deactivate',  
        #             'brass_key_piece_2': 'deactivate',
        #             'brass_key_full': 'activate'}
        for k,v in effects_dict.items():
            if v == 'deactivate':
                print('parse_effects_dict')
                self.items[k].deactivate()
            if v == 'activate':
                self.items[k].activate()


    def use_item(self, use_item:str, on_item:str):
        active_items = self.get_active_items()
        if not use_item in active_items:
            print(f'You don\'t have "{use_item}"')
        elif not on_item in active_items:
            print(f'You don\'t have "{on_item}"')
        if on_item in self.items[use_item].interactions.keys():
            self.parse_effects_dict(self.items[use_item].interactions[on_item]['effects'])
            print(self.items[use_item].interactions[on_item]["message"])
        else:
            print(f'{use_item} cannot be used on {on_item}.')


    def combine_items(self, item1, item2):
        if item1.name in item2.combinations.keys() and item2.name in item1.combinations.keys():
            print(item1.combinations[item2.name]["message"])
            new_item = self.items[item1.combinations[item2.name]["produces"]]
            new_item.activate()
            new_item.print_item_description()
            item1.deactivate()
            item2.deactivate()
        else:
            return 'There was no effect.'


class Backpack:
    def __init__(self):
        self.total_slots = 3
        self.occupied_slots = 0


class Item:
    def __init__(self, dict):
        self.name = dict.get("name", None)
        self.display_name = dict.get("display_name", None)
        self.parent_item = dict.get("parent_item", None)
        self.is_storable = dict.get("is_storable", None)
        self.is_active = dict.get("is_active", None)
        self.is_hazard = dict.get("is_hazard", None)
        self.item_description = dict.get("item_description", None)
        self.item_writing = dict.get("item_writing", None)
        self.attributes = dict.get("attributes", None)
        self.interactions = dict.get("interactions", None)
        self.combinations = dict.get("combinations", None)
        self.effects = dict.get("effects", None)


    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True

    def print_item_description(self):
        print(self.item_description)


class Hazard:
    def __init__(self, initial_message, inspect_message) -> None:
        self.initial_message = initial_message
        self.inspect_message = inspect_message
        self.attributes = []
        self.interactions = []


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
            '1': 'move',
            '2': 'check inventory',
            '3': 'use item'
        }}
        self.move_menu = {
            'input_message': '\nWhich direction do you want to move?',
            'options': {
            '8': 'north',
            '6': 'east',
            '2': 'south',
            '4': 'west'
        }}
        self.game = self.game()


    def display_message(message):
        time.sleep(0.5)
        return message
    
    @staticmethod
    def display_menu(menu):
        print(menu['input_message'])
        for k,v in menu['options'].items():
            print(f'{k}. {v}')

    def clear_screen(self):
        # check and make call for specific operating system
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    def game(self):
        '''The main game loop'''

        game_in_progress = True

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
                    else:
                        object = self.player.items[object_name]
                        print(f'You found a {object.display_name}!\n{object.item_description}')
                        object.activate()
                if selection == '6':
                    self.clear_screen()
                    object_name = self.map.move_player('east')
                    if not object_name:
                        continue
                    else:
                        object = self.player.items[object_name]
                        print(f'You found a {object.display_name}!\n{object.item_description}')
                        object.activate()
                if selection == '2':
                    self.clear_screen()
                    object_name = self.map.move_player('south')
                    if not object_name:
                        continue
                    else:
                        object = self.player.items[object_name]
                        print(f'You found a {object.display_name}!\n{object.item_description}')
                        object.activate()
                if selection == '4':
                    self.clear_screen()
                    object_name = self.map.move_player('west')
                    if not object_name:
                        continue
                    else:
                        object = self.player.items[object_name]
                        print(f'You found a {object.display_name}!\n{object.item_description}')
                        object.activate()
                    
            if selection == '2':
                self.clear_screen()
                self.player.list_inventory()
                continue
            if selection == '3':
                self.clear_screen()
                print('You chose to use an item but this feature is not implemented yet')
                continue
            
if __name__ == '__main__':
    room = Room('room 1', 'hello', [])
    ()