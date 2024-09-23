# This file contains the descriptions of all objects in the game that a player can interact with, 
# including items as well as hazards. The game will read this file in order to randomly 
# populate each room with objects

## Here the game action will be something like player calls use_item(Metal_key) on Metal_lock
## use_item() looks at the interactions attribute of Metal key, looping through the dictionary keys
## to see if the item receieving that action has an interaction

# Players can 
#   - inspect items     = return item description
#   - read items        = return item writing, if any
#   - inspect attribute = return attribute description
#   - Store items 
#   - Use one item on another, or on the self = interaction
#   - Combine one item with another = combination

# 1. You find an item when moving to a space with an item
# 2. The item description is read automatically
# 2a. You can choose to read the item if it has writing on it
# 3. You can chose to inspect the item, whereby attribute(s) are revealed
# 4. You can choose to inspect attributes
# 5. You can choose to use one item on another or group of items, or on a specific attribute, producing an effect or
#    revealing another item
# 6. you can combine items to produce a resulting item, where the component items then are unavailable
# 7. Some items are not storable, as in they exist as part of a map or trap, but you can use the items in your inventory
#    to produce an effect on them: ex. using a key in a lock




items = {
    'Lighter': {
    'name': 'Lighter',
    'parent_item': None,
    'is_storable': True,
    'is_active': True,
    'item_description': 'A brass lighter, it works but it\'s not clear how much fuel is left\n',
    'item_writing': 'There\'s nothing to read.\n',
    'attributes': None,
    'interactions': {'Torn Paper 1': {"message": 'The flame tears through the paper until it is nothing but ash\n',
                                      "effects": {'Torn Paper 1':'deactivate'}
                                     },
                     'Torn Paper 2': {"message": 'The flame tears through the paper until it is nothing but ash\n',
                                     "effects": {'Torn Paper 2':'deactivate'}
                                     },
                       'Full Paper': {"message": 'The flame tears through the paper until it is nothing but ash\n',
                                      "effects": {'Full Paper':'deactivate'}
                                     }},
    'combinations': None,
    'effects': None
    },
    'Torn Paper 1': {
    'name': 'Torn Paper 1',
    'parent_item': None,
    'is_storable': True,
    'is_active': True,
    'item_description': 'An old, stained piece of parchment, a section is torn away on the bottom.',
    'item_writing': '''It reads: "I don't have enough time to explain everything \n just know this: the Paxilon-487 is not safe, it" but the rest has been torn off.''',
    'attributes': {'back of parchment': 'The back of the parchment reads "3490" in hand-written ink but the sequence may continue on the torn section.',
                   'back of paper': 'The back of the parchment reads "3490" in hand-written ink but the sequence may continue on the torn section.'},
    'interactions': None,
    'combinations': {'Torn Paper 2': {"message": 'The two papers combine to form the whole.',
                                      "effects": {'Torn Paper 1': "deactivate",
                                                  'Torn Paper 2': "deactivate",
                                                  'Full Paper': "activate"}
                                      }},
    'effects': None
    },
    'Torn Paper 2': {
    'name': 'Torn Paper 2',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'item_description': 'An old, stained piece of parchment, a section is torn away on the top.',
    'item_writing': '''It reads: "causes an aggresive change in the bio-chemistry of the test subjects. Consider them extremely dangerous!''',
    'attributes': {'back of parchment': 'Back of Torn Paper 2',
                   'back of paper': 'Back of Torn Paper 2'},
    'interactions': None,
    'combinations': {'Torn Paper 1': {"message": 'The two papers combine to form the whole.',
                                      "effects": {'Torn Paper 1': "deactivate",
                                                  'Torn Paper 2': "deactivate",
                                                  'Full Paper': "activate"}
                                      }},
    'effects': None
    },
    'Full Paper': {
    'name': 'Full Paper',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'item_description': 'An old, stained piece of parchment, the torn halves have been reunited.',
    'item_writing': '''It reads: 
    "I don't have enough time to explain everything
    just know this: the Paxilon-487 is not safe, it causes an aggresive
    change in the bio-chemistry of the test subjects. Consider them extremely dangerous!
    ''',
    'attributes': {'back of parchment': 'The back of the parchment reads "349077" in hand-written ink.',
                   'back of paper': 'The back of the parchment reads "349077" in hand-written ink.'},
    'interactions': None,
    'combinations': None,
    'effects': None
    },
    # 'Back of Torn Paper 1': {
    # 'name': 'Back of Torn Paper 1',
    # 'parent_item': 'Torn Paper 1',
    # 'is_storable': False,
    # 'is_active': False,
    # 'item_description': 'The back of the parchment reads "3490" in hand-written ink but the sequence may continue on the torn section.',
    # 'item_writing': 'The back of the parchment reads "3490" in hand-written ink but the sequence may continue on the torn section.',
    # 'attributes': None,
    # 'interactions': None,
    # 'combinations': None,
    # 'effects': None
    # },
    # 'Back of Torn Paper 2': {
    # 'name': 'Back of Torn Paper 2',
    # 'parent_item': 'Torn Paper 2',
    # 'is_storable': False,
    # 'is_active': False,
    # 'item_description': 'The back of the parchment reads "77" in hand-written ink but the sequence may continue on the torn section.',
    # 'item_writing': 'The back of the parchment reads "77" in hand-written ink but the sequence may continue on the torn section.',
    # 'attributes': None,
    # 'interactions': None,
    # 'combinations': None,
    # 'effects': None
    # },
    # 'Back of Full Paper': {
    # 'name': 'Back of Full Paper',
    # 'parent_item': 'Torn Paper 2',
    # 'is_storable': False,
    # 'is_active': False,
    # 'item_description': 'The back of the parchment reads "349077" in hand-written ink.',
    # 'item_writing': 'The back of the parchment reads "349077" in hand-written ink.',
    # 'attributes': None,
    # 'interactions': None,
    # 'combinations': None,
    # 'effects': None
    # },
    'Metal Key Fragment 1': {
    'name': 'Metal Key Fragment 1',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'item_description': 'A metal key, nothing very remarkable other than the teeth, some of which appear to have been snapped off.',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {"teeth": 'Some of the teeth appear to have been snapped off cleanly.'},
    'interactions':{'Metal Lock': {"message": 'The key enters the lock but doesn\'t turn.',
                                    "effects": None
                                   },
                    ('lighter', 'solder'): {"message": 'The key enters the lock but doesn\'t turn.',
                                            "effects": {'Metal_key_fragment_1': 'deactivate',
                                                        'Metal_key_fragment_2': 'deactivate',
                                                        'Metal_key_full': 'activate'}
                                          },
                    ('flame', 'solder'): {"message": 'The key enters the lock but doesn\'t turn.',
                                          "effects": {'Metal_key_fragment_1': 'deactivate',
                                                      'Metal_key_fragment_2': 'deactivate',
                                                      'Metal_key_full': 'activate'}
                                          },
                   },
    'combinations': {},
    'effects':{}
    },
    'Metal_key_fragment_2': {
    'name': 'Metal Key Fragment 2',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'item_description': 'Part of the teeth section of a metal key.',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {"teeth": 'These teeth appear to have been snapped off cleanly from the main section.'},
    'interactions':{'Metal Lock': {"message": 'The teeth section slides into the lock but you\'re unable to retrieve it.',
                                   "effects": {'Metal Key Fragment 2': 'deactivate',
                                               'Metal lock with key fragment 2': 'activate'}
                                   },
                    ('lighter', 'solder'): {"message": 'The key enters the lock but doesn\'t turn.',
                                            "effects": {'Metal_key_fragment_1': 'deactivate',
                                                        'Metal_key_fragment_2': 'deactivate',
                                                        'Metal_key_full': 'activate'}
                                          },
                    ('flame', 'solder'): {"message": 'The key enters the lock but doesn\'t turn.',
                                          "effects": {'Metal_key_fragment_1': 'deactivate',
                                                      'Metal_key_fragment_2': 'deactivate',
                                                      'Metal_key_full': 'activate'}
                                          },
                   },
    'combinations': {},
    'effects':{}
    },
    'Metal_key': {
    'name': 'Metal key',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'item_description': 'A metal key, the teeth have been repaired by soldering them back to the main section.',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {"teeth": 'The section of the teeth that were snapped off have been repaired with solder.'},
    'interactions':{'Metal Lock': {"message": 'The key turns three times and produces a satisfying mechanical click, popping the lock open',
                                    "effects": {"deactivate": "Metal_lock"}
                                   }},
    'combinations': {},
    'effects':{}
    },
    'Metal_Lock': {
    'name': 'Metal Lock',
    'parent_item': None,
    'is_storable': False,
    'is_active': False,
    'item_description': 'A plain Metal lock',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {'Key hole': ''},
    'interactions': {},
    'combinations': {},
    'effects':{}
    },
    'Metal lock with key fragment 2': {
    'name': 'Metal lock with key fragment 2',
    'parent_item': None,
    'is_storable': False,
    'is_active': False,
    'item_description': 'A plain Metal lock',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {'Key hole': ''},
    'interactions':{'Gray metal chunk': {"message": 'The teeth of the key ',
                                         "effects": {"deactivate": "Metal_lock"}
                                        }},
    'combinations': {},
    'effects':{}
    },
    # 'Metal_Wire': {
    # },
    'Wooden cube': {
    'name': 'Wooden cube',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'item_description': 'A smooth, wooden cube with sides roughly 3 inches long. It appears to be made of mahogany.',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {'bottom': {'message': 'There is a square seam in the center of one face, with sides measuring roughly 1 inch.'},
                   'seam': {'message': 'The seam is very tight, almost unnoticable. When pushed it does not budge.'
                           }},
    'interactions':{'Gray metal chunk': {"message": 'The gray metal bar abruptly clings to the cube in the area of the seam.\nWhen pulled, a rectangular section of the cube is comes with it.\n This section of the cube has been hollowed-out revealing a vile of yellow liquid.',
                                         "effects": {'Vial':'activate'}}},
    'combinations': None,
    'effects': None
    },
    'Vial': {
    'name': '',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'item_description': '',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {'': {'message': ''}
                       },
    'interactions':{'': {"message": '',
                         "effects": {'':'activate'}
                         }},
    'combinations': {'': {"message": '',
                         "effects": {'':'activate'}
                         }},
    'effects': None
    }
    }

## Blank item:
    # '': {
    # 'name': '',
    # 'parent_item': None,
    # 'is_storable': True,
    # 'is_active': False,
    # 'item_description': '',
    # 'item_writing': 'There\'s nothing to read.',
    # 'attributes': {'': {'message': ''}
    #                    },
    # 'interactions':{'': {"message": '',
    #                      "effects": {'':'activate'}
    #                      }},
    # 'combinations': {'': {"message": '',
    #                      "effects": {'':'activate'}
    #                      }},
    # 'effects': None
    # }