import random
import time


class Room:
    def __init__(self, name:str, enter_message:str, objects:list) -> None:
        self.name = name
        self.enter_message = enter_message
        self.occupied_spaces = []
        self.shape = self.get_shape()
        self.entrance = self.set_entrance_exit()
        self.exit = self.set_entrance_exit()
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


    def __init__(self, rooms) -> None:
        self.rooms = [Room(room) for room in rooms.rooms]
        self.entrances_and_exits_list = self.get_entrances_and_exits()


    def get_entrances_and_exits(self) -> list:
        entrances_and_exits = []
        for room in self.rooms:
            entrances_and_exits.append(room.entrance, room.exit)
        return entrances_and_exits



class Player:
    def __init__(self, stats:dict) -> None:
        self.backpack = Backpack()
        self.current_space = None
        self.stats = stats


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


    def inspect_item(self):
        pass


    def store_item(self):
        pass


class Backpack:
    def __init__(self) -> None:
        self.total_slots = 3
        self.occupied_slots = 0


class Item:
    def __init__(self, initial_message, inspect_message) -> None:
        self.initial_message = initial_message
        self.inspect_message = inspect_message


class Hazard:
    def __init__(self, initial_message, inspect_message) -> None:
        self.initial_message = initial_message
        self.inspect_message = inspect_message


class Game:
    '''The main class in the game.'''

    def __init__(self, rooms) -> None:
        self.map = Map()
        self.player = Player()
        self.game() 


    def game(self):
        '''The main game loop'''

        game_in_progress = True
        while game_in_progress != False:
            pass


    def display_message(message):
        time.sleep(0.5)
        return message


if __name__ == '__main__':
     room1 = Room(name='Room 1', enter_message='Hello this is room one', objects = ['object 1', 'object 2'])
     breakpoint()
    # pass