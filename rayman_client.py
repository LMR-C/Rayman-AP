import logging
from typing import TYPE_CHECKING

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .client_stuff.operation_builder import build_ram_operations
from .locations import LOCATION_ID_TABLE
from .client_stuff.ram_map import STATE_READS, IN_GAME

logger = logging.getLogger("Client")

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

class RaymanClient(BizHawkClient):
    game="Rayman"
    system = "PSX"
    patch_suffix = None  #no patches

    def __init__(self) -> None:
        super().__init__()
        self.items_index_counter: int = 0
        # Locations reversed but not yet confirmed by the server (avoids reversing them on every tick)
        self.pending_reversed_ids: set[int] = set()
        self.is_init = False
        self.banned_locations : set[int] = set()
        self.banned_items : set[int] =set()
        self.extra_items_to_apply : set[int] = set()

    async def validate_rom(self, ctx:"BizHawkClientContext") -> bool:
        hash_check = "BF460FE0" #hash received with BizHawk
        ctx.game = self.game
        ctx.items_handling= 0b111
        ctx.want_slot_data = True
        return ctx.rom_hash == hash_check



    async def game_watcher(self,ctx:"BizHawkClientContext") -> None:
        if ctx.server is None or ctx.slot is None:
            return


        try :
            #States to read 
            state_read_list = [(address, size, "MainRAM") for address, size in STATE_READS.values()]

            #Location check part
            id_list = [loc_id for loc_id in ctx.missing_locations if loc_id in LOCATION_ID_TABLE]
            loc_read_list = [(LOCATION_ID_TABLE[loc_id].address, LOCATION_ID_TABLE[loc_id].size.value, "MainRAM")
                         for loc_id in id_list]

            #Merging for one read_list
            read_list = state_read_list + loc_read_list

            reads_from_game = await bizhawk.read(ctx.bizhawk_ctx, read_list)

            #Checking that we are at the first "game screen"
            state = {
                name: int.from_bytes(raw, "little") for name, raw in zip(STATE_READS, reads_from_game,strict=False)
                }
            self.banned_locations.clear()
            self.extra_items_to_apply.clear()
            self.banned_items.clear()
            match state:
                case {"menu_state" : m } if m!= IN_GAME :
                    return
                case {"world_id" : w, "level_id" : l} if w==1 and l==1:
                    self.banned_locations.add(2001)
                    self.extra_items_to_apply.add(1001)
            print(self.banned_locations)
            print(self.extra_items_to_apply)
            # if adress & mask =1 : adding loc_id in set
            locations_from_game = reads_from_game[len(STATE_READS):]
            ids_to_check = {
                loc_id for loc_id, data in zip(id_list, locations_from_game, strict=True)
                if (int.from_bytes(data, "little") & LOCATION_ID_TABLE[loc_id].mask) and loc_id not in self.banned_locations
            }
            # Forget the locations confirmed by the server, then reverse only the new ones
            self.pending_reversed_ids &= ctx.missing_locations
            to_reverse = ids_to_check - self.pending_reversed_ids
            #Op
            item_id_list: list[int] = [item.item for item in ctx.items_received]

            operations_dict = build_ram_operations(item_id_list,
                                                  checked_ids=ctx.checked_locations,  # no-op until resync is implemented
                                                  to_reverse=to_reverse,
                                                  to_ban =self.banned_items,
                                                  to_apply = self.extra_items_to_apply,
                                                  counter_state=self.items_index_counter)
            # Special cases (game-specific operations that do not come from an item/location,
            # e.g. depending on state["world_id"] / state["level_id"] or ctx.slot_data):
            # add them HERE, after build_ram_operations and before the read, merged into operations_dict.
            print(operations_dict)
            #Reading item to modify
            read_list = [(address, op.size, "MainRAM") for address, op in operations_dict.items()]

            #building items modifications
            write_list = []
            guard_list = []
            items_from_game = await bizhawk.read (ctx.bizhawk_ctx, read_list)
            for (address, op), data in zip(operations_dict.items(),items_from_game,strict=True):
                read_value = int.from_bytes(data,"little")
                new_value = op.apply(read_value)
                if new_value != read_value :
                    write_list.append((address, new_value.to_bytes(op.size,"little"), "MainRAM"))
                    guard_list.append((address,data,"MainRAM"))
            #To change when counter will be in game's RAM
            delivered = True
            if write_list:
                delivered = await bizhawk.guarded_write(ctx.bizhawk_ctx, write_list, guard_list)
            if delivered:
                self.items_index_counter = max(self.items_index_counter, len(item_id_list))
                self.pending_reversed_ids |= to_reverse
                # Sent only once the reverse is written: a crash in between can't leave a vanilla reward un-reversed
                await ctx.check_locations(ids_to_check)

        except bizhawk.RequestFailedError:
            pass
        except Exception as e:
            logger.exception(e)


