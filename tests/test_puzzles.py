import unittest
from rooms_game.content.objects import items
from rooms_game.content.recipes import recipes
from rooms_game.item import Item
from rooms_game.player import Player
from rooms_game.recipe_engine import RecipeEngine
from rooms_game.game import Game


def build():
    items_dict = {name: Item(d, id=name) for name, d in items.items()}
    engine = RecipeEngine(recipes, items_dict)
    player = Player(items_dict, engine)
    return items_dict, player


class ParserlessGame(Game):
    """Game subclass that skips the interactive loop and screen clears for testing."""
    def __init__(self, player):
        self.player = player
    def clear_screen(self):
        pass


class TestPuzzles(unittest.TestCase):

    def test_paper_puzzle_full_solve(self):
        items_dict, player = build()
        game = ParserlessGame(player)
        # Discovery activates both halves.
        items_dict['Torn Paper 2'].activate()
        game.parse_item_instructions('combine torn paper (top half) with torn paper (bottom half)')
        self.assertFalse(items_dict['Torn Paper 1'].is_active)
        self.assertFalse(items_dict['Torn Paper 2'].is_active)
        self.assertTrue(items_dict['Full Paper'].is_active)

    def test_paper_near_miss_hint(self):
        # With only one half active, combining a half toward the full paper is not
        # possible; but the burn recipe near-miss should not fire spuriously.
        items_dict, player = build()
        engine = player.recipe_engine
        # Only Torn Paper 1 active: all-but-one of {Torn Paper 1, Torn Paper 2}.
        msg = engine.combine({'Torn Paper 1'})
        self.assertIn('part of something larger', msg)

    def test_burn_consumes_paper_keeps_lighter(self):
        items_dict, player = build()
        game = ParserlessGame(player)
        game.parse_item_instructions('use lighter on torn paper (top half)')
        self.assertFalse(items_dict['Torn Paper 1'].is_active)
        self.assertTrue(items_dict['Lighter'].is_active)  # catalyst survives
        self.assertTrue(items_dict['Ash'].is_active)

    def test_key_fusion_multi_ingredient(self):
        items_dict, player = build()
        game = ParserlessGame(player)
        for i in ['Metal Key Fragment 1', 'Metal Key Fragment 2', 'Metal Wire']:
            items_dict[i].activate()
        game.parse_item_instructions(
            'combine broken key (bow end) and broken key (teeth end) and coil of metal wire and lighter')
        self.assertTrue(items_dict['Metal Key'].is_active)
        self.assertFalse(items_dict['Metal Wire'].is_active)     # consumed
        self.assertTrue(items_dict['Lighter'].is_active)         # catalyst survives

    def test_key_fusion_near_miss_without_wire(self):
        items_dict, player = build()
        engine = player.recipe_engine
        for i in ['Metal Key Fragment 1', 'Metal Key Fragment 2']:
            items_dict[i].activate()
        # fragments + lighter but no wire = all-but-one -> hint
        msg = engine.combine({'Metal Key Fragment 1', 'Metal Key Fragment 2', 'Lighter'})
        self.assertIn("won't hold", msg)
        self.assertFalse(items_dict['Metal Key'].is_active)

    def test_inspect_item_and_part(self):
        items_dict, player = build()
        game = ParserlessGame(player)
        # inspect whole item
        self.assertTrue(player.describe_item('lighter'))
        # inspect a named part
        self.assertTrue(player.inspect_attribute('torn paper (top half)', 'back'))

    def test_read(self):
        items_dict, player = build()
        self.assertTrue(player.read_item('torn paper (top half)'))

    def test_unknown_command_rejected(self):
        items_dict, player = build()
        game = ParserlessGame(player)
        # Should not raise; just prints rejection.
        game.parse_item_instructions('teleport to mars')
        game.parse_item_instructions('')


if __name__ == '__main__':
    unittest.main(verbosity=2)
