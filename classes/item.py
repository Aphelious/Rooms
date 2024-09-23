class Item:
    def __init__(self, dict):
        self.name = dict.get("name", None)
        self.display_name = dict.get("display_name", None)
        self.parent_item = dict.get("parent_item", None)
        self.is_storable = dict.get("is_storable", None)
        self.is_active = dict.get("is_active", None)
        self.is_hazard = dict.get("is_hazard", None)
        self.item_description = dict.get("item_description", None)
        self.item_writing = dict.get("item_writing", None)
        self.attributes = dict.get("attributes", None)
        self.interactions = dict.get("interactions", None)
        self.combinations = dict.get("combinations", None)
        self.effects = dict.get("effects", None)


    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True

    def print_item_description(self):
        print(self.item_description)