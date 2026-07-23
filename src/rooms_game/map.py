# Direction -> (delta_row, delta_col). Row increases going north.
DIRECTIONS = {
    'north': (1, 0),
    'south': (-1, 0),
    'east': (0, 1),
    'west': (0, -1),
}

# What a door labeled X in one room connects TO in the destination room. A player
# leaving through an 'Exit' arrives at the next room's 'Entrance', and vice-versa.
DOOR_LABELS = ('Entrance', 'Exit')


class Map:
    '''Stores the rooms and the graph of connections between their doors.

    Connections are held as an adjacency dict keyed by (room, door_label) and
    valued by a Portal describing the destination room and the space the player
    lands on. The structure supports arbitrary links, so linear layouts, branching
    graphs, and later 'geography hazard' teleports are all the same primitive.
    '''

    def __init__(self, rooms) -> None:
        self.rooms = rooms
        self.connections = {}  # (room, door_label) -> {'room': Room, 'space': dict}
        self.build_connections()
        self.current_room = self.rooms[0]
        self.player_current_space = self.current_room.entrance

    def build_connections(self):
        '''Seed a linear chain: each room's Exit leads to the next room's Entrance,
           and each room's Entrance leads back to the previous room's Exit. The
           first room's Entrance and the last room's Exit are left unconnected
           (the latter is the eventual escape/final door).'''
        for i, room in enumerate(self.rooms):
            if i + 1 < len(self.rooms):
                next_room = self.rooms[i + 1]
                self.link(room, 'Exit', next_room, next_room.entrance)
                self.link(next_room, 'Entrance', room, room.exit)

    def link(self, room, door_label, dest_room, dest_space):
        '''Create a one-way connection from a door to a destination space in
           another room. Call twice for a two-way passage.'''
        self.connections[(room, door_label)] = {'room': dest_room, 'space': dest_space}

    def destination(self, door_label):
        '''The portal reachable through the given door of the current room, or None
           if that door doesn't lead anywhere (e.g. the final escape door).'''
        return self.connections.get((self.current_room, door_label))

    def transition(self, portal):
        '''Move the player into the destination room, landing on the linked space.'''
        self.current_room = portal['room']
        self.player_current_space = portal['space']
        return self.current_room

    def move(self, direction):
        '''Attempt to step one space in a direction. Returns the name of whatever
           occupies the new space (an item id, 'Entrance', or 'Exit'), or None if
           the step hit a wall or landed on empty floor.'''
        drow, dcol = DIRECTIONS[direction]
        new_space = {
            'Row': self.player_current_space['Row'] + drow,
            'Column': self.player_current_space['Column'] + dcol,
        }
        if not self.current_room.check_space_exists(new_space):
            print(self.current_room.wall_message)
            return None
        self.player_current_space = new_space
        if not self.current_room.check_space_occupied(new_space):
            print(self.current_room.empty_space_message)
            return None
        return self.get_object_name(new_space)

    def get_object_name(self, space):
        return self.current_room.object_locations[
            self.current_room.convert_space_dict_to_tuple(space)
        ]

    def get_entrances_and_exits(self) -> list:
        entrances_and_exits = []
        for room in self.rooms:
            entrances_and_exits.append(room.entrance)
            entrances_and_exits.append(room.exit)
        return entrances_and_exits
