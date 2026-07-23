class Player:
    def __init__(self, items_dict, recipe_engine=None) -> None:
        self.name = 'Mike'
        self.items = items_dict  # {item id: Item}
        self.recipe_engine = recipe_engine

    @staticmethod
    def normalize(text):
        '''Collapse a name/id/phrase to a comparable form so 'Metal_key',
           'Metal key', and 'metal  key' all match.'''
        return ' '.join(text.lower().replace('_', ' ').split())

    def resolve_item(self, text):
        '''Resolve free-text (an id, name, or display name) to the canonical, ACTIVE
           Item object, or None. Prefers the longest name match so multi-word names
           win over partial ones.'''
        target = self.normalize(text)
        if not target:
            return None
        best = None
        best_len = -1
        for item in self.items.values():
            if not item.is_active:
                continue
            candidates = {self.normalize(item.id)}
            if item.name:
                candidates.add(self.normalize(item.name))
            if item.display_name:
                candidates.add(self.normalize(item.display_name))
            if target in candidates and len(target) > best_len:
                best = item
                best_len = len(target)
        return best

    def get_active_items(self) -> dict:
        return {id: item for id, item in self.items.items() if item.is_active}

    def check_inventory(self):
        print('You have the following items in your sachel:\n')
        carried = [item for item in self.items.values()
                   if item.is_active and item.is_storable and not item.parent_item]
        if not carried:
            print('  (nothing yet)')
        for item in carried:
            print(f'  - {item.display_name}')

    def read_item(self, item_name):
        item = self.resolve_item(item_name)
        if item:
            print(item.item_writing)
            return True
        return False

    def describe_item(self, item_name):
        item = self.resolve_item(item_name)
        if item:
            print(item.item_description)
            return True
        return False

    def inspect_attribute(self, item_name, part_phrase):
        '''Inspect a named PART of an item. Prints the part's text and applies any
           `reveals` effect (activating newly discovered items). Returns True on hit.'''
        item = self.resolve_item(item_name)
        if not item or not item.attributes:
            return False
        part_norm = self.normalize(part_phrase)
        for key, part in item.attributes.items():
            if self.normalize(key) == part_norm or part_norm in self.normalize(key):
                text = part['text'] if isinstance(part, dict) else part
                print(text)
                if isinstance(part, dict) and part.get('reveals'):
                    for revealed_id, action in part['reveals'].items():
                        target = self.items.get(revealed_id)
                        if target and action == 'activate':
                            target.activate()
                return True
        return False

    def combine_items(self, *item_texts):
        '''Bring any number of items together and resolve them through the recipe
           engine. Unresolvable names produce a helpful message.'''
        resolved = []
        for text in item_texts:
            item = self.resolve_item(text)
            if not item:
                print(f'You don\'t have "{text}".')
                return
            resolved.append(item.id)
        message = self.recipe_engine.combine(resolved)
        print(message)

    # 'use X on Y' is just a two-ingredient combine.
    def use_item(self, use_text, on_text):
        self.combine_items(use_text, on_text)
