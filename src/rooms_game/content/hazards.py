# Hazards are things the player can land on that are neither plain items nor doors.
# Like objects.py, this file is DECLARATIVE data; behavior lives in occupant.py and
# is assembled by occupant_resolver.py. A room lists a hazard's id among its
# 'objects' and the resolver turns that id into the right Occupant.
#
# HAZARD SCHEMA (keyed by id, which is what a room lists in its objects)
#   kind                'trap' or 'teleport'.
#
#   -- trap fields (a timed text puzzle; failure ends the game) --
#   prompt              The puzzle text shown when the player triggers the trap.
#   answers             Iterable of acceptable answers (matched case-insensitively).
#   time_limit          Seconds allowed to answer. A visible countdown ticks down.
#   success_message     Shown when disarmed correctly and in time.
#   fail_message        Shown on a wrong answer or a timeout (then the game ends).
#
#   -- teleport fields (a chutes-and-ladders relocation) --
#   message             Shown as the player is whisked away.
#   dest_room_index     Index into Map.rooms of the destination room.
#   dest_space          {'Row': r, 'Column': c} space the player lands on.

hazards = {
    'Rune Trap': {
        'kind': 'trap',
        'prompt': (
            'The floor lights up with glowing runes. A voice booms: "Speak the number '
            'that completes the sequence, or be entombed: 2, 4, 8, 16, ..."'
        ),
        'answers': {'32'},
        'time_limit': 15,
        'success_message': 'The runes dim and the floor settles. The trap is disarmed.',
        'fail_message': (
            'Stone slabs slam down from the ceiling. The builders\' trap has claimed you.'
        ),
    },

    'Trap Door': {
        'kind': 'teleport',
        'message': (
            'The floor gives way beneath you! You slide down a smooth stone chute '
            'and tumble out somewhere else entirely.'
        ),
        'dest_room_index': 0,
        'dest_space': {'Row': 1, 'Column': 0},
    },
}
