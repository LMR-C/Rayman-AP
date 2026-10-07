from worlds.AutoWorld import World
from .locations import LOCATION_NAME_TO_ID
from .items import ITEM_NAME_TO_ID, ITEM_TABLE, RaymanItem
from . import regions,items

class RaymanWorld(World):
    game = "Rayman"
    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID
    origin_region_name = "Overworld"

    def create_item(self,name) -> RaymanItem:
        return items.create_item_with_table(self,name)

    def create_regions(self) -> None:
        regions.create_regions(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def get_filler_item_name(self):
        #To change later
        return items.get_filler_item_name()


