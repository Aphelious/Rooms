# This file contains the descriptions of all objects in the game that a player can
# interact with, including items as well as hazards. The game reads this file to
# randomly populate each room with objects.
#
# ITEM SCHEMA
#   name             Canonical display name (also the dict key here).
#   display_name     What the player sees in the inventory (defaults to name).
#   parent_item      If this item only exists as a revealed part of another, its parent id.
#   is_storable      Whether the player can carry it.
#   is_active        Whether it currently exists/is available to the player.
#   is_hazard        Reserved for hazards.
#   item_description What 'inspect <item>' prints.
#   item_writing     What 'read <item>' prints.
#   attributes       Inspectable PARTS of the item (the discovery axis). Each part maps
#                    a phrase the player might inspect to:
#                       {"text": <what they see>,
#                        "reveals": {<item id>: "activate"} | None}
#
# All cross-item logic (using/combining items together) lives in recipes.py, NOT here.
# Items describe themselves; recipes describe what happens when items meet.

items = {
    'Lighter': {
    'name': 'Lighter',
    'display_name': 'lighter',
    'parent_item': None,
    'is_storable': True,
    'is_active': True,
    'is_hazard': False,
    'item_description': 'A brass lighter. It works, but it\'s not clear how much fuel is left.',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {
        'flame': {'text': 'A small, steady flame. Hot enough to burn - or to melt metal, given the right materials.',
                  'reveals': None},
    },
    },

    'Torn Paper 1': {
    'name': 'Torn Paper 1',
    'display_name': 'torn paper (top half)',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'is_hazard': False,
    'item_description': 'An old, stained piece of parchment; a section is torn away along the bottom.',
    'item_writing': 'It reads: "I don\'t have enough time to explain everything, just know this: '
                    'the Paxilon-487 is not safe, it" - but the rest has been torn off.',
    'attributes': {
        'back': {'text': 'The back reads "3490" in hand-written ink, but the sequence may continue on the torn section.',
                 'reveals': None},
    },
    },

    'Torn Paper 2': {
    'name': 'Torn Paper 2',
    'display_name': 'torn paper (bottom half)',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'is_hazard': False,
    'item_description': 'An old, stained piece of parchment; a section is torn away along the top.',
    'item_writing': 'It reads: "causes an aggressive change in the bio-chemistry of the test subjects. '
                    'Consider them extremely dangerous!"',
    'attributes': {
        'back': {'text': 'The back reads "77" in hand-written ink, continuing a sequence from another fragment.',
                 'reveals': None},
    },
    },

    'Full Paper': {
    'name': 'Full Paper',
    'display_name': 'reassembled parchment',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'is_hazard': False,
    'item_description': 'An old, stained piece of parchment; the torn halves have been reunited.',
    'item_writing': 'It reads:\n'
                    '"I don\'t have enough time to explain everything, just know this: '
                    'the Paxilon-487 is not safe, it causes an aggressive change in the '
                    'bio-chemistry of the test subjects. Consider them extremely dangerous!"',
    'attributes': {
        'back': {'text': 'The back reads "349077" in hand-written ink.',
                 'reveals': None},
    },
    },

    'Ash': {
    'name': 'Ash',
    'display_name': 'a pile of ash',
    'parent_item': None,
    'is_storable': False,
    'is_active': False,
    'is_hazard': False,
    'item_description': 'A small heap of grey ash - all that remains of whatever was burned.',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {},
    },

    'Metal Key Fragment 1': {
    'name': 'Metal Key Fragment 1',
    'display_name': 'broken key (bow end)',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'is_hazard': False,
    'item_description': 'The bow end of a metal key. The teeth section has snapped clean off.',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {
        'teeth': {'text': 'The break is clean, as if it were meant to be rejoined with heat and solder.',
                  'reveals': None},
    },
    },

    'Metal Key Fragment 2': {
    'name': 'Metal Key Fragment 2',
    'display_name': 'broken key (teeth end)',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'is_hazard': False,
    'item_description': 'The teeth section of a metal key, snapped off from its bow.',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {
        'teeth': {'text': 'The break matches the other fragment exactly. Fusing them would need heat and something to solder with.',
                  'reveals': None},
    },
    },

    'Metal Wire': {
    'name': 'Metal Wire',
    'display_name': 'coil of metal wire',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'is_hazard': False,
    'item_description': 'A short coil of soft metal wire. It looks like it could melt and flow if heated.',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {},
    },

    'Metal Key': {
    'name': 'Metal Key',
    'display_name': 'metal key',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'is_hazard': False,
    'item_description': 'A metal key. The teeth have been fused back to the bow with a bead of solder.',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {
        'teeth': {'text': 'The repaired teeth look solid enough to turn a lock.',
                  'reveals': None},
    },
    },

    'Metal Lock': {
    'name': 'Metal Lock',
    'display_name': 'metal lock',
    'parent_item': None,
    'is_storable': False,
    'is_active': False,
    'is_hazard': False,
    'item_description': 'A plain metal lock set into a heavy door.',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {
        'keyhole': {'text': 'A standard keyhole. It would take a whole key to turn it.',
                    'reveals': None},
    },
    },
}
