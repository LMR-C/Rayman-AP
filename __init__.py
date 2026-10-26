from worlds.AutoWorld import World, WebWorld
from BaseClasses import Entrance, Region, Item, ItemClassification

from .options import RaymanGameOptions, rayman_options_groups
from .locations import get_location_table, RaymanLocation, LOCATION_NAME_TO_ID
from .regions import REGIONS, LEVEL_ORDER_BY_REGION, UNLOCK_ITEM_ORDER
from .entrances import get_entrance_table
from .items import ITEM_NAME_TO_ID, ITEM_NAME_TABLE, RaymanItem, get_item_table

from . import rayman_client as rayman_client

class RaymanWeb(WebWorld):
    theme = "grass"
    option_groups = rayman_options_groups
    # TODO: setup, tutorials, options_preset

class RaymanWorld(World):
    game = "Rayman"
    options_dataclass = RaymanGameOptions
    options: RaymanGameOptions
    origin_region_name = "worldmap"
    location_name_to_id = LOCATION_NAME_TO_ID
    item_name_to_id = ITEM_NAME_TO_ID

    def can_place_level_unlock_item(self, item: RaymanItem, location_order: int) -> bool:
        unlock_order = UNLOCK_ITEM_ORDER.get(item.name)

        if unlock_order is None:
            return True

        return location_order < unlock_order

    def create_regions(self) -> None:

        # Region creation
        regions = {
            data.name: Region(data.name, self.player, self.multiworld)
            for data in REGIONS
        }
        self.multiworld.regions.extend(regions.values())

        # Location creation
        location_table = get_location_table(self.options)
        for data in location_table:
            if data.region not in regions:
                raise ValueError(
                    f"Unknown region: {data.region} for location: {data.name}"
                )

            # Skip Life Status location if disabled
            if not self.options.include_life_status_in_location.value :
                if data.id >= 4000 and data.id <= 4999:
                    continue

            # Skip Magician challenges location if disabled
            if not self.options.include_magician_challenges_in_location.value:
                if data.id >= 5000 and data.id <= 5999:
                    continue

            # Declare item and add it to its region
            location = RaymanLocation(self.player, data, regions[data.region])
            regions[data.region].locations.append(location)
            self.set_rule(location, data.rule)

            location_order = LEVEL_ORDER_BY_REGION[data.region]
            previous_item_rule = location.item_rule

            location.item_rule = lambda item, order=location_order, old_rule=previous_item_rule: (
                old_rule(item) and self.can_place_level_unlock_item(item, order)
            )

        # Entrance creation
        for data in get_entrance_table(self.options):
            source = regions[data.from_region]
            target = regions[data.to_region]

            entrance = Entrance(
                self.player,
                data.name,
                source
            )

            source.exits.append(entrance)
            entrance.connect(target)
            self.set_rule(entrance, data.rule)

    def create_item(self, name: str) -> RaymanItem:
        item = ITEM_NAME_TABLE[name]
        return RaymanItem(item.name, item.classification, item.id, self.player)

    def create_filler_pool(self, count: int) -> list[Item]:
        pool = []
        trap_percentage = self.options.trap_fill_percentage.value
        number_of_traps = round(count * trap_percentage / 100)
        number_of_fillers = count - number_of_traps

        if trap_percentage > 0:

            traps = [
                ("Reversed controls", self.options.reversed_controls_weight.value),
                ("Forced Run", self.options.forced_run_weight.value)
            ]

            trap_names = [name for name, _ in traps]
            weights = [weight for _, weight in traps]

            if not any(weights):
                raise ValueError(
                    "Rayman: Cannot generate traps because all traps weights are none "
                    "Please increase the weight of at least one trap"
                )

            selected_traps = self.random.choices(
                trap_names,
                weights=weights,
                k=number_of_traps
            )

            pool.extend(
                self.create_item(name)
                for name in selected_traps
            )
            
        pool.extend(
            self.create_item(self.random.choice([
                "Simple Power",
                "Double Power",
                "Big Power",
                "Life Status",
                "5 tings"
            ]))
            for _ in range(number_of_fillers)
        )

        self.random.shuffle(pool)
        return pool


    def create_items(self) -> None:
        item_pool : list[Item] = []

        # Key item pool
        for data in get_item_table(self.options):
            if data.classification in [ItemClassification.progression, ItemClassification.useful]:
                item_pool.extend(self.create_item(data.name) for _ in range(data.count))

        # Filler pool
        number_unfilled_locations = len(self.multiworld.get_unfilled_locations(self.player))
        needed_number_filler_items = number_unfilled_locations - len(item_pool)

        if needed_number_filler_items < 0 :
            raise ValueError(
                f"Too many items: {len(item_pool)} items for {number_unfilled_locations} available locations"
            )

        item_pool.extend(self.create_filler_pool(needed_number_filler_items))
        self.multiworld.itempool += item_pool
