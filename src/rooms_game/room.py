import random

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