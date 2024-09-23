from rooms import rooms
from objects import items
from classes.item import Item
from classes.player import Player
from classes.room import Room
from classes.hazard import Hazard
from classes.map import Map
from classes.game import Game

if __name__ == '__main__':
    debug = True
    rooms_list = [Room(x) for x in rooms]
    map = Map(rooms_list)
    items_dict = {}
    for name,item_dict in items.items():
        items_dict[name] = Item(item_dict)
    player = Player(items_dict)
    game = Game(map, player, debug)