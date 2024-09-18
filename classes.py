import random
import time


class Room:
    def __init__(self, name:str, enter_message:str, objects:list) -> None:
        self.name = name
        self.enter_message = enter_message
        self.occupied_spaces = []
        self.shape = self.get_shape()
        self.entrance = self.get_random_wall_space()
        self.exit = self.get_random_wall_space()
        self.objects = objects
        self.object_locations = {}
        self.place_objects(objects)
        # super.display_message(self.enter_message)


    def get_shape(self):
        '''Build a list of lists that represents the shape of a room between 3 and 5 rows, and between 3 and 5 columns.
           Example shape: [[-2, -1, 0, 1, 2], 
                           [-2, -1, 0, 1], 
                               [-1, 0, 1], 
                           [-2, -1, 0, 1, 2]]'''
    
        shape = list()
        for row in range(random.randint(4,6)):
            col_num = random.randint(3,5)
            cols = [-1,0,1]
            if col_num == 4:
                cols.append(random.choice([-2,2]))
            elif col_num == 5:
                cols.extend([-2,2])
            if row == 1:
                shape.append(sorted(cols))
            if row == 2:
                shape.append(sorted(cols))
            if row == 3:
                shape.append(sorted(cols))
            if row == 4:
                shape.append(sorted(cols))
            if row == 5:
                shape.append(sorted(cols))
        return shape
    

    def get_random_space(self) -> tuple:
        '''Reads in the shape dictionary, returns a tuple of random space (row, col) 
           from the available spaces in the shape.'''    

        row_index = random.randint(0, len(self.shape) - 1)  
        row = self.shape[row_index]  
        space = random.choice(row)
        return row_index, space


    def get_random_wall_space(self) -> tuple:
        '''Reads in the shape dictionary, returns a tuple of random space (row, col) 
           from the available spaces in the shape only if that space is along a wall.'''   

        row_index = random.randint(0, len(self.shape) - 1)  
        if row_index == 0 or row_index == len(self.shape) - 1:
            row = self.shape[row_index]  
            col = random.choice(row)
            space = (row_index, col)
            return space
        else:
            row = self.shape[row_index]
            eligible_spaces = []
            eligible_spaces.append(row[0])
            eligible_spaces.append(row[-1])
            col = random.choice(eligible_spaces)
            space = (row_index, col)
            return space


    def get_space_exists(self, space) -> bool: 
        '''Takes in a space tuple and checks to see if that space is exists in the current room, returning True or False.'''

        row = space[0]
        col = row[space[1]]
        if row in self.shape and col in self.shape[row]:
            return True
        return False
    

    def is_occupied_space(self, space:tuple) -> bool:
        '''Takes in a space tuple and checks to see if that space is already occupied, returning True or False.'''

        if space in self.occupied_spaces:
            return True
        else:
            return False
    

    def set_occupied_space(self, space) -> None:
        '''Appends the given space to the occupied spaces list of the room.'''

        self.occupied_spaces.append(space)


    def set_entrance_exit(self) -> tuple:
        '''Calls the get_random_wall_space function, updates the occupied space list with the result, and returns the space.'''

        eligible_space_found = False
        while not eligible_space_found:
            space = self.get_random_wall_space()
            if not self.is_occupied_space(space):
                self.set_occupied_space(space)
                return space
            else:
                continue


    def place_objects(self, objects) -> None:
        '''Takes in a list of all objects supplied when instantiating the room and updates
           the object_locations dictionary to store the name and location of each item or hazard in the room'''

        for object in objects:
            eligible_space_found = False
            while not eligible_space_found:
                space = self.get_random_space()
                if not self.is_occupied_space(space):
                    self.set_occupied_space(space)
                    self.object_locations.update({object:space})
                    # self.object_locations.update({object.name , space}) # We'll have to use this line in the end product
                    break
                else:
                    continue


    def __repr__(self) -> str:
        return f'''{self.name} \n Shape: {self.shape} \n Entrance: {self.entrance} \n Exit: {self.exit}
 Objects: {self.objects} \n Occupied spaces: {self.occupied_spaces} \n Object locations: {self.object_locations}'''



class Map:
    '''Class to store all the rooms and their connections, which form a graph.'''

    def __init__(self, rooms) -> None:
        self.rooms = rooms
        self.room_connections_list = self.get_entrances_and_exits()
        self.room_graph = self.build_room_graph()

    #[{'room1': (1,2), 'room2': (2,3)}
    # Need a way of connecting the rooms together that we'll be able to retieve data from later as the player moves through
    # the map. Specifically I'm wondering if the connection between rooms is better stored at the space level
    # 

    def build_room_graph(self) -> dict:
        room_number = len(self.rooms)


    def get_entrances_and_exits(self) -> list:
        entrances_and_exits = []
        for room in self.rooms:
            entrances_and_exits.append(room.entrance)
            entrances_and_exits.append(room.exit)
        return entrances_and_exits



class Player:
    def __init__(self, items) -> None:
        # self.backpack = Backpack()
        self.name = 'Mike'
        self.items = items
        self.current_space = None


    def move(self, direction:str, wall_message) -> None:
        if direction.lower() == 'east':
            new_space = self.current_space - 1
            if self.check_space_exists(new_space):
                self.current_space = new_space
            else:
                return wall_message
        if direction.lower() == 'west':
            new_space = self.space + 1
            if self.check_space_exists(new_space):
                self.space = new_space
            else:
                return wall_message
        if direction.lower() == 'north':
            new_space = self.space - 1
            if self.check_space_exists(new_space):
                self.space = new_space
            else:
                return wall_message
        if direction.lower() == 'south':
            new_space = self.space # something that changes the letter 
            if self.check_space_exists(new_space):
                self.space = new_space
            else:
                return wall_message

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
            # new_item = on_item.interactions[use_item.name]['produces']
            # if new_item:
            #     something?
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

    def __init__(self, map, player) -> None:
        self.map = map
        self.player = player
        # self.game() 
        breakpoint()


    def display_message(message):
        time.sleep(0.5)
        return message
    

    def game(self):
        '''The main game loop'''

        game_in_progress = True
        while game_in_progress != False:
            self.player.current_space = self.map.current_room.entrance
            pass 


if __name__ == '__main__':
    room1 = Room(name='Room 1', enter_message='Hello this is room one', objects=['object 1', 'object 2'])
    room2 = Room(name='Room 2', enter_message='Hello this is room two', objects=['object 3', 'object 4'])
    map = Map([room1, room2])
    player = Player()
    game = Game(map, player)
    # breakpoint()
    # pass