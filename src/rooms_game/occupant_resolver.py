from rooms_game.occupant import (
    ItemOccupant,
    DoorOccupant,
    TrapHazard,
    TeleportHazard,
)


class OccupantResolver:
    '''Turns the string an object space holds (an item id, a hazard id, or a door
       label) into the Occupant that knows how to behave when the player lands
       on it. Content stays declarative strings; this is where they become behavior.

       `hazards` is a mapping of id -> spec dict (see content/hazards.py). Each spec
       has a 'kind' of 'trap' or 'teleport' plus that kind's fields.'''

    def __init__(self, game_map, items, hazards=None):
        self.map = game_map
        self.items = items          # {id: Item}
        self.hazards = hazards or {} # {id: spec dict}

    def is_final_gate(self, door_label):
        '''The one door in the map with no destination is the escape gate.'''
        return door_label == 'Exit' and self.map.destination('Exit') is None

    def resolve(self, occupant_name):
        '''occupant_name is whatever object_locations stored for the landed space.'''
        if occupant_name in ('Entrance', 'Exit'):
            return DoorOccupant(
                occupant_name,
                is_final_gate=self.is_final_gate(occupant_name),
            )
        if occupant_name in self.hazards:
            return self._build_hazard(self.hazards[occupant_name])
        return ItemOccupant(self.items[occupant_name])

    def _build_hazard(self, spec):
        if spec['kind'] == 'trap':
            return TrapHazard(
                prompt=spec['prompt'],
                answers=spec['answers'],
                time_limit=spec['time_limit'],
                success_message=spec['success_message'],
                fail_message=spec['fail_message'],
            )
        if spec['kind'] == 'teleport':
            return TeleportHazard(
                message=spec['message'],
                dest_room_index=spec['dest_room_index'],
                dest_space=spec['dest_space'],
            )
        raise ValueError(f"unknown hazard kind: {spec['kind']!r}")
