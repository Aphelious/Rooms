import random

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
            return new_space
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
                object_name = self.get_object_name(new_space)
                return object_name

        if direction == 'east':
            new_space = self.move_east()
            if not new_space:
                return
            if not self.current_room.check_space_occupied(new_space):
                print(self.current_room.empty_space_message)
            else:
                object_name = self.get_object_name(new_space)
                return object_name
            
        if direction == 'west':
            new_space = self.move_west()
            if not new_space:
                return
            if not self.current_room.check_space_occupied(new_space):
                print(self.current_room.empty_space_message)
            else:
                object_name = self.get_object_name(new_space)
                return object_name

        if direction == 'south':
            new_space = self.move_south()
            if not new_space:
                return
            if not self.current_room.check_space_occupied(new_space):
                print(self.current_room.empty_space_message)
            else:
                object_name = self.get_object_name(new_space)
                return object_name


    def get_object_name(self, new_space):
        object_name = self.current_room.object_locations[self.current_room.convert_space_dict_to_tuple(new_space)]
        return object_name


    def get_entrances_and_exits(self) -> list:
        entrances_and_exits = []
        for room in self.rooms:
            entrances_and_exits.append(room.entrance)
            entrances_and_exits.append(room.exit)
        return entrances_and_exits