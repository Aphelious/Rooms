import time


class GameContext:
    '''Everything an occupant needs to affect the game when the player lands on it,
       without coupling occupants to the Game object itself. Occupants call these
       hooks; the Game owns the actual state.'''

    def __init__(self, game_map, player, read=input, write=print):
        self.map = game_map
        self.player = player
        self.read = read          # how to get a line of input from the player
        self.write = write        # how to show the player a line
        self.game_over = False
        self.won = False
        self.end_reason = None

    def end_game(self, reason, won=False):
        '''Flag the game as finished. The main loop checks this after every space
           is resolved. `won=True` marks an escape; otherwise it's a loss.'''
        self.game_over = True
        self.won = won
        self.end_reason = reason


class Occupant:
    '''Anything the player can land on. Each kind knows how to resolve itself.'''

    def resolve(self, ctx: GameContext) -> None:
        raise NotImplementedError


class ItemOccupant(Occupant):
    '''A discoverable item lying in a space. Landing on it reveals and activates it.'''

    def __init__(self, item):
        self.item = item

    def resolve(self, ctx):
        ctx.write(f'You found a {self.item.display_name}!\n{self.item.item_description}')
        self.item.activate()
        # Storable items are carried away, so remove them from the room; revisiting
        # the space then finds empty floor. Fixtures (e.g. a lock) are not storable
        # and stay in place so the player can return to interact with them.
        if self.item.is_storable:
            ctx.map.current_room.clear_space(ctx.map.player_current_space)


class DoorOccupant(Occupant):
    '''A door between rooms. Walking through is always a choice. A door with no
       portal is a locked gate; if it is the final escape gate, passing wins.'''

    def __init__(self, door_label, is_final_gate=False):
        self.door_label = door_label
        self.is_final_gate = is_final_gate

    def resolve(self, ctx):
        portal = ctx.map.destination(self.door_label)
        if not portal:
            if self.is_final_gate:
                self._attempt_escape(ctx)
            else:
                ctx.write('You have reached a heavy door, but it will not open. Not yet.')
            return
        answer = ctx.read('You see a door. Walk through it? (y/n)\n').strip().lower()
        if answer in ('y', 'yes'):
            room = ctx.map.transition(portal)
            ctx.write(room.enter_message)
        else:
            ctx.write('You step back from the door.')

    def _attempt_escape(self, ctx):
        ctx.write('This is the final door - the way out.')
        answer = ctx.read('Walk through it and escape? (y/n)\n').strip().lower()
        if answer in ('y', 'yes'):
            ctx.end_game('You step through the final door into daylight. You escaped!', won=True)
        else:
            ctx.write('You linger, not ready to leave.')


class TeleportHazard(Occupant):
    '''A geography hazard (chute/ladder): landing here relocates the player to a
       destination space, possibly in another room. Reuses the map's portal move.'''

    def __init__(self, message, dest_room_index, dest_space):
        self.message = message
        self.dest_room_index = dest_room_index
        self.dest_space = dest_space

    def resolve(self, ctx):
        ctx.write(self.message)
        dest_room = ctx.map.rooms[self.dest_room_index]
        ctx.map.transition({'room': dest_room, 'space': self.dest_space})
        ctx.write(dest_room.enter_message)


class TrapHazard(Occupant):
    '''A trap left by the dungeon's builders: a text puzzle under a time limit.
       A correct answer within the limit disarms the trap; a wrong answer or
       taking too long ends the game.

       NOTE: the timer is enforced on submit (elapsed time is checked when the
       player presses enter), and there is deliberately no live on-screen
       countdown. A live ticking display cannot be rendered reliably alongside a
       blocking input() in a plain terminal; that UX is being explored separately
       via a TUI framework. The clock and input are injected so the timing logic
       is testable without real waiting.'''

    def __init__(self, prompt, answers, time_limit, success_message, fail_message):
        self.prompt = prompt
        # Accept a set/list of acceptable answers (compared lowercased/stripped).
        self.answers = {a.lower().strip() for a in answers}
        self.time_limit = time_limit
        self.success_message = success_message
        self.fail_message = fail_message

    def resolve(self, ctx, clock=time.monotonic):
        ctx.write(self.prompt)
        ctx.write(f'(you have {self.time_limit} seconds - answer quickly!)')
        start = clock()
        answer = ctx.read('> ')
        elapsed = clock() - start
        self._judge(ctx, answer, elapsed)

    def _judge(self, ctx, answer, elapsed):
        if elapsed > self.time_limit:
            ctx.end_game(self.fail_message)
            return
        if answer is not None and answer.lower().strip() in self.answers:
            ctx.write(self.success_message)
            return
        ctx.end_game(self.fail_message)
