import unittest

from rooms_game.occupant import (
    GameContext,
    ItemOccupant,
    DoorOccupant,
    TeleportHazard,
    TrapHazard,
)
from rooms_game.content.rooms import rooms as rooms_data
from rooms_game.room import Room
from rooms_game.map import Map


class FakeItem:
    def __init__(self, is_storable=True):
        self.display_name = 'shiny thing'
        self.item_description = 'It gleams.'
        self.is_active = False
        self.is_storable = is_storable

    def activate(self):
        self.is_active = True


def make_ctx(answers=None, rooms=None):
    '''Build a GameContext with scripted input and captured output. `answers` is a
       list consumed one per read() call.'''
    answers = list(answers or [])
    output = []

    def fake_read(prompt=''):
        output.append(prompt)
        return answers.pop(0) if answers else ''

    def fake_write(msg=''):
        output.append(msg)

    game_map = Map(rooms or [Room(x) for x in rooms_data])
    ctx = GameContext(game_map, player=None, read=fake_read, write=fake_write)
    ctx.output = output
    return ctx


class FakeClock:
    '''A clock whose reported time only advances when we tell it to, so trap timing
       is deterministic and tests never actually wait.'''
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


class TestItemOccupant(unittest.TestCase):
    def test_activates_and_describes(self):
        item = FakeItem()
        ctx = make_ctx()
        ItemOccupant(item).resolve(ctx)
        self.assertTrue(item.is_active)
        self.assertTrue(any('shiny thing' in line for line in ctx.output))

    def test_storable_item_is_removed_from_room(self):
        item = FakeItem(is_storable=True)
        ctx = make_ctx()
        space = ctx.map.player_current_space
        # Put the item at the player's current space, then pick it up.
        key = ctx.map.current_room.convert_space_dict_to_tuple(space)
        ctx.map.current_room.object_locations[key] = 'shiny thing'
        ItemOccupant(item).resolve(ctx)
        self.assertNotIn(key, ctx.map.current_room.object_locations)

    def test_fixture_item_stays_in_room(self):
        item = FakeItem(is_storable=False)
        ctx = make_ctx()
        space = ctx.map.player_current_space
        key = ctx.map.current_room.convert_space_dict_to_tuple(space)
        ctx.map.current_room.object_locations[key] = 'fixture'
        ItemOccupant(item).resolve(ctx)
        self.assertIn(key, ctx.map.current_room.object_locations)


class TestDoorOccupant(unittest.TestCase):
    def test_walk_through_transitions(self):
        ctx = make_ctx(answers=['y'])
        DoorOccupant('Exit').resolve(ctx)
        self.assertIs(ctx.map.current_room, ctx.map.rooms[1])

    def test_declining_stays_put(self):
        ctx = make_ctx(answers=['n'])
        start = ctx.map.current_room
        DoorOccupant('Exit').resolve(ctx)
        self.assertIs(ctx.map.current_room, start)

    def test_final_gate_escape_wins(self):
        ctx = make_ctx(answers=['y'])
        # Move to the last room, whose Exit has no portal (the real escape gate).
        ctx.map.transition(ctx.map.destination('Exit'))
        DoorOccupant('Exit', is_final_gate=True).resolve(ctx)
        self.assertTrue(ctx.game_over)
        self.assertTrue(ctx.won)


class TestTeleportHazard(unittest.TestCase):
    def test_relocates_player(self):
        ctx = make_ctx()
        dest = {'Row': 1, 'Column': 0}
        TeleportHazard('whoosh', dest_room_index=1, dest_space=dest).resolve(ctx)
        self.assertIs(ctx.map.current_room, ctx.map.rooms[1])
        self.assertEqual(ctx.map.player_current_space, dest)


def make_trap():
    return TrapHazard(
        prompt='what is 2+2?',
        answers={'4'},
        time_limit=10,
        success_message='disarmed',
        fail_message='boom',
    )


class TestTrapHazard(unittest.TestCase):
    def test_correct_in_time_disarms(self):
        ctx = make_ctx(answers=['4'])
        clock = FakeClock()
        make_trap().resolve(ctx, clock=clock)
        self.assertFalse(ctx.game_over)
        self.assertTrue(any('disarmed' in line for line in ctx.output))

    def test_wrong_answer_ends_game(self):
        ctx = make_ctx(answers=['5'])
        clock = FakeClock()
        make_trap().resolve(ctx, clock=clock)
        self.assertTrue(ctx.game_over)
        self.assertFalse(ctx.won)
        self.assertEqual(ctx.end_reason, 'boom')

    def test_too_slow_ends_game(self):
        # Advance the clock past the limit between start and submit.
        clock = FakeClock()
        answers = ['4']
        output = []

        def fake_read(prompt=''):
            output.append(prompt)
            clock.now = 999  # player dawdled well past the limit
            return answers.pop(0)

        def fake_write(msg=''):
            output.append(msg)

        game_map = Map([Room(x) for x in rooms_data])
        ctx = GameContext(game_map, None, read=fake_read, write=fake_write)
        make_trap().resolve(ctx, clock=clock)
        self.assertTrue(ctx.game_over)
        self.assertEqual(ctx.end_reason, 'boom')


if __name__ == '__main__':
    unittest.main(verbosity=2)
