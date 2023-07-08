# This file contains the descriptions of all objects in the game that a player can interact with, 
# including items as well as hazards. The game will read this file in order to randomly 
# populate each room with objects

[
    {'Name':'Torn paper 1',
     'initial_description': 'An old, stained piece of parchment, a section is torn away on the bottom.',
     'inspect_message_read': '''It reads: "Dearest Sylvia I barely knew you before I was taken away to this place. \n I wish I had more time so that I can" but the rest has been torn off.''',
     'inspect_message_physical': 'The back of the parchment reads "3490" in hand-written ink but the sequence may continue on the torn section.'
     },
    {'name':'Brass key',
     'initial_description': 'A brass key, with head ornate carvings on the head and shoulder',
     'inspect_message_read': 'There\'s nothing to read.',
     'inspect_message_physical': 'Some of the teeth appear to have been snapped off'
     }
]