

class Player:
    def __init__(self, items_dict) -> None:
        self.name = 'Mike'
        self.items = items_dict # {item name: item object}


    @staticmethod
    def format_item_name(item_name):
        return item_name.lower().replace(' ', '_')
    

    def get_active_items(self) -> list:
        active_items = {}
        for name, item in self.items.items():
            if item.is_active:
                active_items[name] = item
        return active_items


    def is_item_active(self, item_name):
        print(self.items[item_name].is_active)


    def validate_item(self, item_name):
        item_name = self.format_item_name(item_name)
        active_items_names = [x for x in self.get_active_items().keys()]
        if item_name in active_items_names:
            return True
        return False


    def describe_item(self, item_name):
        if self.validate_item(item_name):
            print(self.items[item_name].print_item_description())
        else:
            print(f'You don\'t have "{item_name.lower()}"')


    def read_item(self, item_name):
        if self.validate_item(item_name):
            print(self.items[item_name].item_writing)
        else:
            print(f'You don\'t have "{item_name.lower()}"')


    def inspect_item_attribute(self, item_name, attribute):
        if attribute in self.items[item_name].attributes.keys():
            attribute_name = self.items[item_name].attributes[attribute]
            print(self.items[attribute_name].item_description)
        else:
            print(f'Cannot inspect "{attribute}"')


    def check_inventory(self):
        print('You have the following items in your sachel:\n')
        for name,item in self.items.items():
            if item.is_active and not item.parent_item:
                print(item.name)


    def parse_effects_dict(self, effects_dict):
        # "effects": {'brass_key_piece_1': 'deactivate',  
        #             'brass_key_piece_2': 'deactivate',
        #             'brass_key_full': 'activate'}
        for k,v in effects_dict.items():
            if v == 'deactivate':
                print('parse_effects_dict')
                self.items[k].deactivate()
            if v == 'activate':
                self.items[k].activate()


    def use_item(self, use_item:str, on_item:str):
        active_items = self.get_active_items()
        if not use_item in active_items:
            print(f'You don\'t have "{use_item}"')
        elif not on_item in active_items:
            print(f'You don\'t have "{on_item}"')
        if on_item in self.items[use_item].interactions.keys():
            self.parse_effects_dict(self.items[use_item].interactions[on_item]['effects'])
            print(self.items[use_item].interactions[on_item]["message"])
        else:
            print(f'{use_item} cannot be used on {on_item}.')


    def combine_items(self, item1, item2):
        if item1.name in item2.combinations.keys() and item2.name in item1.combinations.keys():
            print(item1.combinations[item2.name]["message"])
            new_item = self.items[item1.combinations[item2.name]["produces"]]
            new_item.activate()
            new_item.print_item_description()
            item1.deactivate()
            item2.deactivate()
        else:
            return 'There was no effect.'