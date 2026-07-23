import unittest
from rooms_game.content.rooms import rooms as rooms_data
from rooms_game.room import Room
from rooms_game.map import Map, DIRECTIONS


def build_map():
    return Map([Room(x) for x in rooms_data])


class TestMovement(unittest.TestCase):

    def test_direction_table_complete(self):
        self.assertEqual(set(DIRECTIONS), {'north', 'south', 'east', 'west'})

    def test_move_updates_position_within_room(self):
        m = build_map()
        start = dict(m.player_current_space)
        # Find a direction that stays inside the room and assert the position moved.
        moved = False
        for direction, (drow, dcol) in DIRECTIONS.items():
            target = {'Row': start['Row'] + drow, 'Column': start['Column'] + dcol}
            if m.current_room.check_space_exists(target):
                m.move(direction)
                self.assertEqual(m.player_current_space, target)
                moved = True
                break
        self.assertTrue(moved, 'entrance should have at least one in-bounds neighbour')

    def test_move_into_wall_keeps_position(self):
        m = build_map()
        # Force a known position, then step off the grid.
        # Row 0 never exists (rows are 1-indexed), so moving south from row 1 hits a wall.
        m.player_current_space = {'Row': 1, 'Column': 0}
        before = dict(m.player_current_space)
        result = m.move('south')  # row 0 doesn't exist
        self.assertIsNone(result)
        self.assertEqual(m.player_current_space, before)


class TestRoomGraph(unittest.TestCase):

    def test_starts_in_first_room(self):
        m = build_map()
        self.assertIs(m.current_room, m.rooms[0])
        self.assertEqual(m.player_current_space, m.rooms[0].entrance)

    def test_exit_connects_to_next_room_entrance(self):
        m = build_map()
        portal = m.destination('Exit')
        self.assertIsNotNone(portal)
        self.assertIs(portal['room'], m.rooms[1])
        self.assertEqual(portal['space'], m.rooms[1].entrance)

    def test_first_room_entrance_has_no_connection(self):
        m = build_map()
        self.assertIsNone(m.destination('Entrance'))

    def test_last_room_exit_is_unconnected_final_door(self):
        m = build_map()
        # Walk to the last room, then its Exit should lead nowhere (the escape gate).
        portal = m.destination('Exit')
        m.transition(portal)
        self.assertIs(m.current_room, m.rooms[-1])
        self.assertIsNone(m.destination('Exit'))

    def test_transition_moves_player_into_destination(self):
        m = build_map()
        portal = m.destination('Exit')
        room = m.transition(portal)
        self.assertIs(room, m.rooms[1])
        self.assertIs(m.current_room, m.rooms[1])
        self.assertEqual(m.player_current_space, m.rooms[1].entrance)

    def test_entrance_leads_back_after_transition(self):
        m = build_map()
        # Go forward, then the second room's Entrance should lead back to room 1.
        m.transition(m.destination('Exit'))
        back = m.destination('Entrance')
        self.assertIsNotNone(back)
        self.assertIs(back['room'], m.rooms[0])


if __name__ == '__main__':
    unittest.main(verbosity=2)
