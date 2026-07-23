class RecipeEngine:
    '''Resolves a SET of item ids (things the player brought together) against the
       recipe table. Recipes are order-independent and may involve any number of
       ingredients, with some consumed and some acting as reusable catalysts.'''

    def __init__(self, recipes, items):
        self.recipes = recipes
        self.items = items  # {id: Item}

    def active_ids(self):
        return {id for id, item in self.items.items() if item.is_active}

    def find_match(self, ingredient_ids):
        '''Return the first recipe whose `requires` set is exactly satisfied by the
           given ingredient ids AND every required item is currently active.'''
        given = set(ingredient_ids)
        active = self.active_ids()
        for recipe in self.recipes:
            if recipe['requires'] == given and recipe['requires'] <= active:
                return recipe
        return None

    def find_near_miss(self, ingredient_ids):
        '''Return a hint if the given ids match ALL BUT ONE of some recipe's
           requirements (and that recipe has a hint authored). Powers discovery.'''
        given = set(ingredient_ids)
        for recipe in self.recipes:
            if not recipe.get('hint'):
                continue
            required = recipe['requires']
            # Player supplied all-but-one of the requirements, and nothing extraneous.
            if given < required and len(required - given) == 1:
                return recipe['hint']
        return None

    def apply(self, recipe):
        '''Apply a matched recipe's effects: consume ingredients, produce outputs.
           Returns the narration message.'''
        for consumed_id in recipe.get('consumes', set()):
            self.items[consumed_id].deactivate()
        for produced_id, action in recipe.get('produces', {}).items():
            if action == 'activate':
                self.items[produced_id].activate()
            elif action == 'deactivate':
                self.items[produced_id].deactivate()
        return recipe['message']

    def combine(self, ingredient_ids):
        '''Top-level entry point. Given the ids the player brought together, return
           the narration string for whatever happened (success, near-miss, or nothing).'''
        match = self.find_match(ingredient_ids)
        if match:
            return self.apply(match)
        hint = self.find_near_miss(ingredient_ids)
        if hint:
            return hint
        return 'Nothing happens.'
