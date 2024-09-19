import random
from rooms import rooms
from objects import items
from classes import *

# def game():

#     # Game(all_rooms)
#     # room1 = Room(name='Room1', enter_message='Hello this is room one', objects = ['object 1', 'object 2'])

#     # item_list = [Item(x) for x in items.values()]
#     items_dict = {}
#     for k,v in items.items():
#         items_dict[k] = Item(v)
#     player = Player(items_dict)
#     # player.combine_items(player.items['torn_paper_1'], player.items['torn_paper_2'])
#     # player.use_item('lighter', 'full_paper')
#     breakpoint()

if __name__ == '__main__':
    debug = True
    rooms_list = [Room(x) for x in rooms]
    map = Map(rooms_list)
    player = Player(items)
    breakpoint()
    game = Game(map, player, debug)