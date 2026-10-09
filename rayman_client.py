from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
import logging

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
            
            print(ctx.missing_locations)
        #    code = (await bizhawk.read(ctx.bizhawk_ctx, [(0x1E4D50, 2, "MainRAM")]))[0]
        #    nb_vies = int.from_bytes(code,"little",signed=True)
        #    print(f"nombre de vide : {nb_vies}")
        except Exception as e :
            logger.exception(e)