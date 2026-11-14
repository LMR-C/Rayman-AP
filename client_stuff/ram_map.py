"""RAM addresses and values used by the client (US version, MainRAM domain). See docs/memory_map.md."""

# Game state, read on every tick
MENU_STATE = 0x1F81A0
IN_GAME = 4  # MENU_STATE value while playing
CURRENT_WORLD_ID = 0x1FA688
CURRENT_LEVEL_ID = 0x1F9A68
POS_X = 0x1F9A10
POS_Y = 0x1F9A28
# Number of items_received already applied, written by the client in the same write as the items
ITEM_COUNTER_ADDRESS = 0x1F9C52
ITEM_COUNTER_SIZE = 2
# name -> (address, size)
STATE_READS: dict[str, tuple[int, int]] = {
    "menu_state": (MENU_STATE, 1),
    "world_id": (CURRENT_WORLD_ID, 1),
    "level_id": (CURRENT_LEVEL_ID, 1),
    "pos_x": (POS_X,2),
    "pos_y": (POS_Y,2),
    "items_counter": (ITEM_COUNTER_ADDRESS, ITEM_COUNTER_SIZE),
}

# Given again when the RAM counter goes back to 0. Other apply_once items are never given twice
# (see the data storage counter in rayman_client)
CAGE_ITEM_ID = 3001
RESTORED_ITEM_IDS = frozenset({CAGE_ITEM_ID})




# Magic Seed as item (option magic_seed_as_item)
# Raw bytes in the game's charset (lowercase ASCII, "?" = button, texts end with "/").
# The replacement has the same size as the original (padded with 00).

# "tarayzan gives rayman a magic seed/" -> "tarayzan lost the magic seed/"
SPAWN_SWAMPS_X = 161
MAGIC_SEED_ITEM_ID = 2001

# Betilla: location ids (locations.py) and the power each one gives (items.py)
BETILLA_GIFT_1_LOCATION_ID = 2001
BETILLA_GIFT_2_LOCATION_ID = 2002
BETILLA_GIFT_3_LOCATION_ID = 2003
TELESCOPIC_FIST_ITEM_ID = 1001
HANGING_ITEM_ID = 1002
GRAPPLING_FIST_ITEM_ID = 1003
# (world_id, level_id) of each Betilla level, not checked in game yet
BETILLA_PPW_LEVEL = (1, 3)
BETILLA_AL_LEVEL = (1, 8)
BETILLA_MN_LEVEL = (1, 17)

MAGIC_SEED_TEXT_1_ADDRESS = 0x12BAD1
MAGIC_SEED_TEXT_1_ORIGINAL = bytes.fromhex(
    "74 61 72 61 79 7A 61 6E 20 67 69 76 65 73 20 72 61 79 6D 61 6E 20 61 20 6D 61 67 69 63 20 73 65 65 64 2F")
MAGIC_SEED_TEXT_1_REPLACEMENT = bytes.fromhex(
    "74 61 72 61 79 7A 61 6E 20 6C 6F 73 74 20 74 68 65 20 6D 61 67 69 63 20 73 65 65 64 2F 00 00 00 00 00 00")


# "press the ? button to use the seed/" -> "you need to find it/"
MAGIC_SEED_TEXT_2_ADDRESS = 0x12BAF9
MAGIC_SEED_TEXT_2_ORIGINAL = bytes.fromhex(
    "70 72 65 73 73 20 74 68 65 20 3F 20 62 75 74 74 6F 6E 20 74 6F 20 75 73 65 20 74 68 65 20 73 65 65 64 2F 00")
MAGIC_SEED_TEXT_2_REPLACEMENT = bytes.fromhex(
    "79 6F 75 20 6E 65 65 64 20 74 6F 20 66 69 6E 64 20 69 74 2F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")

