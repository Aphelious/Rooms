# This file contains the descriptions of all objects in the game that a player can interact with, 
# including items as well as hazards. The game will read this file in order to randomly 
# populate each room with objects

## Here the game action will be something like player calls use_item(brass_key) on brass_lock
## use_item() looks at the interactions attribute of brass key, looping through the dictionary keys
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
    'lighter': {
    'name': 'lighter',
    'display_name':'Lighter',
    'parent_item': None,
    'is_storable': True,
    'is_active': True,
    'item_description': 'A brass lighter, it works but it\'s not clear how much fuel is left',
    'item_writing': 'There\'s nothing to read.',
    'attributes': None,
    'interactions': {'torn_paper_1': {"produces": None,
                                      "message": 'The flame tears through the paper until it is nothing but ash',
                                      "effects": {'torn_paper_1':'deactivate'}
                                     },
                    'torn_paper_2': {"produces": None,
                                     "message": 'The flame tears through the paper until it is nothing but ash',
                                     "effects": {'torn_paper_2':'deactivate'}
                                     },
                    'full_paper': {"produces": None,
                                   "message": 'The flame tears through the paper until it is nothing but ash',
                                   "effects": {'full_paper':'deactivate'}
                                  }},
    'combinations': None,
    'effects': None
    },
    'torn_paper_1': {
    'name': 'torn_paper_1',
    'display_name':'Torn paper 1',
    'parent_item': None,
    'is_storable': True,
    'is_active': True,
    'item_description': 'An old, stained piece of parchment, a section is torn away on the bottom.',
    'item_writing': '''It reads: "I don't have enough time to explain everything \n just know this: the Paxilon-487 is not safe, it" but the rest has been torn off.''',
    'attributes': ['back of parchment'],
    'interactions': None,
    'combinations': {'torn_paper_2': {"produces": 'full_paper',
                                       "message": 'The two papers combine to form the whole. ',
                                       "effects": {'torn_paper_1': "deactivate",
                                                   'torn_paper_2': "deactivate",
                                                   'full_paper': "activate"}
                                      }},
    'effects': None
    },
    'torn_paper_2': {
    'name': 'torn_paper_2',
    'display_name':'Torn paper 2',
    'parent_item': None,
    'is_storable': True,
    'is_active': True,
    'item_description': 'An old, stained piece of parchment, a section is torn away on the top.',
    'item_writing': '''It reads: "causes an aggresive change in the bio-chemistry of the test subjects. Consider them extremely dangerous!''',
    'attributes': ['back of parchment'],
    'interactions': None,
    'combinations': {'torn_paper_1': {"produces": 'full_paper',
                                      "message": 'The two papers combine to form the whole.',
                                      "effects": {'torn_paper_1': "deactivate",
                                                  'torn_paper_2': "deactivate",
                                                  'full_paper': "activate"}
                                      }},
    'effects': None
    },
    'full_paper': {
    'name': 'full_paper',
    'display_name':'Full paper',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'item_description': 'An old, stained piece of parchment, the torn halves have been reunited.',
    'item_writing': '''It reads: 
    "I don't have enough time to explain everything
    just know this: the Paxilon-487 is not safe, it causes an aggresive
    change in the bio-chemistry of the test subjects. Consider them extremely dangerous!
    ''',
    'attributes': {'back of parchment': 'full_paper_back',
                   'back of paper': 'full_paper_back'},
    'interactions': None,
    'combinations': None,
    'effects': None
    },
    'torn_paper_1_back': {
    'name': 'torn_paper_1_back',
    'display_name':'Back of torn paper 1',
    'parent_item': 'torn_paper_1',
    'is_storable': False,
    'is_active': True,
    'item_description': 'The back of the parchment reads "3490" in hand-written ink but the sequence may continue on the torn section.',
    'item_writing': 'The back of the parchment reads "3490" in hand-written ink but the sequence may continue on the torn section.',
    'attributes': None,
    'interactions': None,
    'combinations': None,
    'effects': None
    },
    'torn_paper_2_back': {
    'name': 'torn_paper_2_back',
    'display_name':'Back of torn paper 2',
    'parent_item': 'torn_paper_2',
    'is_storable': False,
    'is_active': True,
    'item_description': 'The back of the parchment reads "77" in hand-written ink but the sequence may continue on the torn section.',
    'item_writing': 'The back of the parchment reads "77" in hand-written ink but the sequence may continue on the torn section.',
    'attributes': None,
    'interactions': None,
    'combinations': None,
    'effects': None
    },
    'full_paper_back': {
    'name': 'full_paper_back',
    'display_name':'Back of full paper',
    'parent_item': 'torn_paper_2',
    'is_storable': False,
    'is_active': True,
    'item_description': 'The back of the parchment reads "349077" in hand-written ink.',
    'item_writing': 'The back of the parchment reads "349077" in hand-written ink.',
    'attributes': None,
    'interactions': None,
    'combinations': None,
    'effects': None
    },
    'brass_key_piece_1': {
    'name': 'brass_key_piece_1',
    'display_name':'Brass key fragment 1',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'item_description': 'A brass key, nothing very remarkable other than the teeth, some of which appear to have been snapped off.',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {"teeth": 'Some of the teeth appear to have been snapped off cleanly.'},
    'interactions':{'Brass Lock': {"produces": None,
                                    "message": 'The key enters the lock but doesn\'t turn.',
                                    "effects": None
                                   },
                    ('lighter', 'solder'): {"produces": None,
                                            "message": 'The key enters the lock but doesn\'t turn.',
                                            "effects": None
                                           },
                    ('flame', 'solder'): {"produces": None,
                                          "message": 'The key enters the lock but doesn\'t turn.',
                                          "effects": {'brass_key_piece_1': 'deactivate',
                                                      'brass_key_piece_2': 'deactivate',
                                                      'brass_key_full': 'activate'}
                                          },
                   },
    'combinations': [],
    'effects':[]
    },
    'brass_key_piece_2': {
    'name': 'brass_key_piece_2',
    'display_name':'Brass key fragment 2',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'item_description': 'Part of the teeth section of a brass key, apparently snapped off the main section.',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {"teeth": 'Some of the teeth appear to have been snapped off cleanly.'},
    'interactions':{'Brass Lock': {"produces": None,
                                    "message": 'The key turns three times and produces a satisfying mechanical click, popping the lock open',
                                    "effects": {"deactivate": "brass_lock"}
                                   }},
    'combinations': [],
    'effects':[]
    },
    'brass_key_full': {
    'name': 'brass_key_full',
    'display_name':'Brass key',
    'parent_item': None,
    'is_storable': True,
    'is_active': False,
    'item_description': 'Part of the teeth section of a brass key, apparently snapped off the main section.',
    'item_writing': 'There\'s nothing to read.',
    'attributes': {"teeth": 'The section of the teeth that were snapped off have been repaired with solder.'},
    'interactions':{'Brass Lock': {"produces": None,
                                    "message": 'The key turns three times and produces a satisfying mechanical click, popping the lock open',
                                    "effects": {"deactivate": "brass_lock"}
                                   }},
    'combinations': [],
    'effects':[]
    }
    # 'wooden_cube': {
    # 'name': 'wooden_cube',
    # 'display_name': 'Wooden cube',
    # 'parent_item': None,
    # 'is_storable': True,
    # 'is_active': False,
    # 'item_description': 'A smooth, wooden cube with sides roughly 3 inches long.',
    # 'item_writing': 'There\'s nothing to read.',
    # 'item_writing': 'It appears to be made of mahogany.\nThere is a square seam in the center of one face, with sides measuring roughly 1 inch.',
    # 'attributes': {'seam': {'item_writing_physical': 'The seam is very tight, almost unnoticable. When pushed it does not budge.',
    #                         'magnet': 'The magnet abruptly clings to the cube in the area of the seam. When pulled, a rectangular section of the cube is removed, revealing a hollowed-out section of the piece you removed.'}},
    # 'interactions':{'gray_metal_cube': {"produces": None,
    #                                     "message": '',
    #                                     "effects": {"activate":''}}},
    # 'combinations': None,
    # 'effects': None
    # }
    }