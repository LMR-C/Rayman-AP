from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
import logging
from .locations import LOCATION_ID_TABLE
from .items import ITEM_ID_TABLE
from .utils import Effect
from collections import defaultdict

logger = logging.getLogger("Client")

if TYPE_CHECKING: 
    from worlds._bizhawk.context import BizHawkClientContext

class RaymanClient(BizHawkClient):
    game="Rayman"
    system = "PSX"
    patch_suffix = None  #no patches


    def __init__(self) -> None:
        super().__init__()
        
    def create_effect_list(items_received):
        add_dict = defaultdict(int)
        set_bit_dict = defaultdict(int)
        set_value_dict = defaultdict(int)
        set_temporary_dict = defaultdict(int)

        for index,network_item in enumerate(items_received):
            id_item = network_item.item
            item_in_table = ITEM_ID_TABLE.get(id_item)

            if item_in_table is None :
                logger.warning(f"item with id {id_item} doesn't exist in rayman item table")
                continue

            match item_in_table.effect:
                case Effect.ADD:
                    pass
                case Effect.SET_BIT:
                    set_bit_dict[item_in_table.address] |= item_in_table.value
                case Effect.SET_VALUE:
                    pass
                case Effect.TEMPORARY:
                    pass
                case Effect.NONE:
                    pass
                case _ :
                    logger.warning("Unknown item effect")
        return (add_dict,set_bit_dict,set_value_dict,set_temporary_dict)


    async def validate_rom(self, ctx:"BizHawkClientContext") -> bool:
        hash_check = "BF460FE0" #hash received with BizHawk
        ctx.game = self.game
        ctx.items_handling= 0b111
        ctx.want_slot_data = False
        return ctx.rom_hash == hash_check

    async def game_watcher(self,ctx:"BizHawkClientContext") -> None: 
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


        except Exception as e :
            logger.exception(e)


