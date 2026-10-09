from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
import logging
from .locations import LOCATION_ID_TABLE

logger = logging.getLogger("Client")

if TYPE_CHECKING: 
    from worlds._bizhawk.context import BizHawkClientContext

class RaymanClient(BizHawkClient):
    game="Rayman"
    system = "PSX"
    patch_suffix = None  #no patches


    def __init__(self) -> None:
        super().__init__()

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
