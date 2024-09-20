import random
from rooms import rooms
from objects import items
from classes import *

if __name__ == '__main__':
    debug = True
    rooms_list = [Room(x) for x in rooms]
    map = Map(rooms_list)
    items_dict = {}
    for name,item_dict in items.items():
        items_dict[name] = Item(item_dict)
    player = Player(items_dict)
    game = Game(map, player, debug)