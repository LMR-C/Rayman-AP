from worlds.AutoWorld import World, WebWorld
from BaseClasses import Entrance, Region, Item, ItemClassification

from .options import RaymanGameOptions, rayman_options_groups
from .locations import get_location_table, RaymanLocation, LOCATION_NAME_TO_ID
from .regions import REGIONS
from .entrances import get_entrance_table
from .items import ITEM_NAME_TO_ID, ITEM_NAME_TABLE, RaymanItem, get_item_table
from . import rules

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


    def fill_slot_data(self) -> dict:
        return {
            "number_of_starting_life": self.options.number_of_starting_life.value,
            "number_of_continue": self.options.number_of_continue.value,
            "number_of_tings_to_get_a_new_life": self.options.number_of_tings_to_get_a_new_life.value,
            "magic_seed_as_item": self.options.magic_seed_as_item.value,
            "include_life_status_in_location": self.options.include_life_status_in_location.value,
            "include_magician_challenges_in_location": self.options.include_magician_challenges_in_location.value
        }


    def add_completion_event(self, location_name: str, region: str, event_name: str) -> None:
        """Create a fictive item to verify if a location has been reached"""

        original_location = self.multiworld.get_location(location_name, self.player)
        

        event_location = RaymanLocation(
            self.player,
            location_name + " event",
            original_location.parent_region
        )

        event_item = RaymanItem(
            event_name + " event item",
            ItemClassification.progression,
            None,
            self.player
        )

        event_location.place_locked_item(event_item)
        event_location.parent_region.locations.append(event_location)

        self.set_rule(event_location, original_location.access_rule)


    def create_victory_event(self) -> None:

        region = self.multiworld.get_region("Moskito's Nest Betilla", self.player)

        victory_location = RaymanLocation(
            self.player,
            "moskito victory",
            region
        )

        victory_item = RaymanItem(
            "victory",
            ItemClassification.progression,
            None,
            self.player
        )

        victory_location.place_locked_item(victory_item)
        region.locations.append(victory_location)

        # self.set_rule(victory_location, rules.can_acess_moskito_nest & rules.has_fist & rules.has_hang)
        self.set_rule(victory_location, rules.can_acess_moskito_nest)

        self.multiworld.completion_condition[self.player] = (
            lambda state: state.has("victory", self.player)
        )


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

        # Define level complete events
        self.add_completion_event("Pink Plant Woods finished", "Pink Plant Woods Screen 3", "Pink Plant Woods finished")
        self.add_completion_event("Anguish Lagoon finished", "Anguish Lagoon Betilla", "Anguish Lagoon finished")
        self.add_completion_event("The Swamps of Forgetfulness finished", "The Swamps of Forgetfulness Screen 3", "The Swamps of Forgetfulness finished")

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

        self.create_victory_event()


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
