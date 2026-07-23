from rooms_game.content.rooms import rooms
from rooms_game.content.objects import items
from rooms_game.content.recipes import recipes
from rooms_game.item import Item
from rooms_game.player import Player
from rooms_game.room import Room
from rooms_game.map import Map
from rooms_game.game import Game
from rooms_game.recipe_engine import RecipeEngine


def main():
    debug = True
    rooms_list = [Room(x) for x in rooms]
    game_map = Map(rooms_list)
    items_dict = {}
    for name, item_dict in items.items():
        items_dict[name] = Item(item_dict, id=name)
    recipe_engine = RecipeEngine(recipes, items_dict)
    player = Player(items_dict, recipe_engine)
    Game(game_map, player, debug)


if __name__ == '__main__':
    main()
