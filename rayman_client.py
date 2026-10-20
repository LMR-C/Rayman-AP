import logging
from typing import TYPE_CHECKING

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .client_stuff.ram_operation import build_item_operations
from .locations import LOCATION_ID_TABLE

logger = logging.getLogger("Client")

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

class RaymanClient(BizHawkClient):
    game="Rayman"
    system = "PSX"
    patch_suffix = None  #no patches
    items_index_counter: int = 0


    def __init__(self) -> None:
        super().__init__()
        self.items_index_counter = 0



    async def validate_rom(self, ctx:"BizHawkClientContext") -> bool:
        hash_check = "BF460FE0" #hash received with BizHawk
        ctx.game = self.game
        ctx.items_handling= 0b111
        ctx.want_slot_data = False
        return ctx.rom_hash == hash_check

    async def game_watcher(self,ctx:"BizHawkClientContext") -> None:
        if ctx.server is None or ctx.slot is None:
            return

        try :
            #Location check part
            id_list = list(ctx.missing_locations)
            read_list =[(LOCATION_ID_TABLE[id].address, LOCATION_ID_TABLE[id].size.value, "MainRAM") for id in id_list]
            locations_from_game = await bizhawk.read(ctx.bizhawk_ctx, read_list)
            # if adress & mask =1 : adding loc_id in set
            ids_to_check = {
                loc_id for loc_id, data in zip(id_list, locations_from_game, strict=True)
                if int.from_bytes(data, "little") & LOCATION_ID_TABLE[loc_id].mask
            }
            #send ids to server for checking
            await ctx.check_locations(ids_to_check)
            #Op
            item_id_list: list[int] = [item.item for item in ctx.items_received]
            operations_item_dict = build_item_operations(item_id_list,self.items_index_counter)

            #Reading item to modify
            read_list = [(address, op.size, "MainRAM") for address, op in operations_item_dict.items()]

            #building items modifications
            write_list = []
            guard_list = []
            items_from_game = await bizhawk.read (ctx.bizhawk_ctx, read_list)
            for (address, op), data in zip(operations_item_dict.items(),items_from_game,strict=True):
                read_value = int.from_bytes(data,"little")
                new_value,_overflow = op.apply(read_value)
                if new_value != read_value :
                    write_list.append((address, new_value.to_bytes(op.size,"little"), "MainRAM"))
                    guard_list.append((address,data,"MainRAM"))
            #To change when counter will be in game's RAM
            delivered = True
            if write_list:
                delivered = await bizhawk.guarded_write(ctx.bizhawk_ctx, write_list, guard_list)
            if delivered:
                self.items_index_counter = max(self.items_index_counter, len(item_id_list))

        except bizhawk.RequestFailedError:
            pass
        except Exception as e:
            logger.exception(e)


