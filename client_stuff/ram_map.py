"""RAM addresses and values used by the client (US version, MainRAM domain). See docs/memory_map.md."""

# Game state, read on every tick
MENU_STATE = 0x1F81A0
IN_GAME = 4  # MENU_STATE value while playing
CURRENT_WORLD_ID = 0x1FA688
CURRENT_LEVEL_ID = 0x1F9A68

# name -> (address, size)
STATE_READS: dict[str, tuple[int, int]] = {
    "menu_state": (MENU_STATE, 1),
    "world_id": (CURRENT_WORLD_ID, 1),
    "level_id": (CURRENT_LEVEL_ID, 1),
}
