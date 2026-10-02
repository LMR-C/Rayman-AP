# Game information 1.0

This document aims to provide every information necessary to develop the Rayman's Archipelago
client version 1.0.

## Details

- Little-endian is used here
- To number the item: from the closest to farthest from the spawn point
- In the implementation columns: When an address is written please consider the value contained inside.
i.e: ``0x1F43D0`` means: the value inside ``0x1F43D0``
- When a variable is labelled you can see the address in the [memory_map.md](memory_map.md) file
- To find the mask from bitfield values: old XOR new = mask
- To set a bit in a bitfield: ``address`` = ``address`` | mask
- To know if a bit is set in a bitfield: ``address`` & mask == mask

## Game Detection

The word at ``0x125000`` must be equal to ``0x6D61672F``


## Effects

| Name | Description | Implementation |
|:---|:---:|---:|
| Death Link | If a player die and death link is active Rayman die too | Set ``Rayman mode`` to 3 |
| Number of tings to get a life | Change the amount of tings needed to get a life | If ``Tings counter`` >= X then increments ``Life counter`` |

## Items

All the items a player can get

### Main

| Name | Description | Implementation to give the item |
|:---|:---:|---:|
| Fist Power | Give Rayman the ability to throw his fist | ``Rayman Events 1`` =  ``Rayman Events 1`` \| 0x1 |
| Hanging | Give Rayman the ability to hang on platforms | ``Rayman Events 1`` = ``Rayman Events 1`` \| 0x2 |
| Grappling Fist | Give Rayman the ability to grab lives and pink rings | ``Rayman Events 1`` = ``Rayman Events 1`` \| 0x80 |
| Helicopter Power | Give Rayman the ability to Helicopter with his hairs | ???|
| Run Power | Give Rayman the ability to Run | ??? |
| Cage | One of the 102 cages in the game | Increments by 1 the ``Total cage counter`` variable |
| Protoon piece | An imaginary item for Archipelago, if you got the necessary amount it unlocks access to Mr.Dark's Dare | Intern logic |
| Level Unlock | Unlock access to a level from another | To implement by editing the world_info structure ? |

### Junk

| Name | Description | Implementation |
|:---|:---:|---:|
| Simple Power | Give 1 HP to Rayman | Increments ``Health Points`` by 1 |
| Double Power | Give 2 HP to Rayman | Increments ``Health Points`` by 2 |
| Big Power | Restore Rayman's health completely and increase his health bar to 5 points. If Rayman loses a life, the effect is cancelled | Set ``Max Health Points`` and ``Health Points`` to 5 |
| Speed Fist | Increase Raymans's fist range and the speed | Increments ``Fist Level`` |
| Gold Fist | Increase Rayman's fist strenght | ??? |
| Life | Increase Rayman's life counter by 1 | Increments ``Life counter`` by 1 |
| 5 Tings | Increase by 5 the tings counter | Increments ``Tings counter`` by 5 |

### Traps

| Name | Description | Implementation |
|:---|:---:|---:|
| Reversed Controls | The player's controls will be reversed similar to the start of Mr.Dark's Dare 3 | ??? |
| Elf Trap | For a limited time, Rayman will be temporarely shrunken, making him slower and his jumps lower | ??? |

## Locations

- value = the value in the ``address`` column
- Dependency : considering the whole level

| Name | address | size | how to check | dependency |
|:---|:---:|:---:|:---:|---:|
| Fist Power (Betilla gift 1) | 0x1f43d0 | Byte | value & 0x1 == 0x1 | None |
| Hanging (Betilla gift 2)| 0x1F43D0 | Byte | value & 0x2 == 0x2 | Fist Power |
| Grappling Fist (Betilla gift 3)| 0x1F43D0 | Byte | value & 0x80 == 0x80 | Fist Power |
| Helicopter | 0x1f43d0 |  byte | value & 0x4 == 0x4 | Fist Power, Hanging |
| Moskito 1 | 0x1F4EE8 | Byte | value & 0x1 == 0x1 | Fist Power |
| Moskito 1 | 0x1F4EE8 | Byte | value & 0x2 == 0x2 | Fist Power |
| Pink Plant Wood Screen 1 life 1 | 0x1F9AC8 | Byte | value & 0x80 == 0x80 | None |
| Pink Plant Wood Screen 2 life 1 | 0x1F9AE9 | Byte | value & 0x80 == 0x80 | None |
| Pink Plant Wood Screen 2 life 2 | 0x1F9AE9 | Byte | value & 0x40 == 0x40 | Hanging |
| Pink Plant Wood Screen 2 cage 1 | 0x1F9AF1 | Byte | value & 0x20 == 0x20 | Fist, Hanging |
| Pink Plant Wood Screen 2 cage 2 | 0x1F9AF1 | Byte | value & 0x10 == 0x10 | Fist, Hanging |
| Pink Plant Wood Screen 2 cage 3 | 0x1F9AF1 | Byte | value & 0x4 == 0x4 | Fist |
| Pink Plant Wood Screen 2 magician 1 | 0x1f7f40 | Word | value & 0x00100000 == 0x00100000 | None |
| Pink Plant Wood Screen 3 life 1 | 0x1F9B28 | Byte | value & 0x80 == 0x80 | Fist Power |
| Pink Plant Wood Screen 3 life 2 | 0x1F9B28 | Byte | value & 0x40 == 0x40 | None |
| Pink Plant Wood Screen 3 life 3 | 0x1F9B2A | Byte | value & 0x20 == 0x20 | Fist Power |
| Pink Plant Wood Screen 3 life 4 | 0x1F9B2A | Byte | value & 0x4 == 0x4 | Fist Power |
| Pink Plant Wood Screen 3 life 5 | 0x1F9B28 | Byte | value & 0x10 == 0x10 | None |
| Pink Plant Wood Screen 3 cage 1 | 0x1F9B31 | Half-Word | value & 0x2000 == 0x2000 | Fist Power |
| Pink Plant Wood Screen 3 cage 2 | 0x1F9B31 | Half-Word | value & 0x01 == 0x01 | Fist Power |
| Pink Plant Wood Screen 3 cage 3 | 0x1F9B31 | Half-Word | value & 0x8000 == 0x8000 | Fist Power |
| Pink Plant Wood Screen 3 magician 1 | 0x1f7f40 | Word | value & 0x80000 == 0x80000 | Fist Power |
| Anguish Lagoon Screen 1 cage 1 | 0x1F9B4C | Byte | value & 0x20 == 0x20 | Fist, Hanging |
| Anguish Lagoon Screen 1 cage 2 | 0x1F9B4C | Byte | value & 0x40 == 0x40 | Fist, Hanging, Grappling fist|
| Anguish Lagoon Screen 1 cage 3 | 0x1F9B4B | Half-Word | value & 0x1 == 0x1 | Fist Power |
| Anguish Lagoon Screen 1 cage 4 | 0x1F9B4B | Half-Word | value & 0x8000 == 0x8000 | Fist Power |
| Anguish Lagoon Screen 1 cage 5 | 0x1F9B4C | Byte | value & 0x8 == 0x8 | Fist |
| Anguish Lagoon Screen 1 life 1 | 0x1F9B4A | Byte | value & 0x10 == 0x10 | Fist |
| Anguish Lagoon Screen 3 life 1 | 0x1F9B92 | Byte | value & 0x4 == 0x4 | Fist Power |
| Anguish Lagoon Screen 3 life 2 | 0xAF9B93 | Byte | value & 0x2 == 0x2 | Fist Power |
| Anguish Lagoon Screen 3 cage 1 | 0x1F9B8B | Half-Word | value & 0x40 == 0x40 | Fist Power |
| The Swamp of Forgetfulness Screen 1 cage 1 | 0x1F9BC8 | Byte | value & 0x10 == 0x10 | Fist Power |
| The Swamp of Forgetfulness Screen 1 cage 2 | 0x1F9BCA | Byte | value & 0x20 == 0x20 | Fist Power |
| The Swamp of Forgetfulness Screen 1 life 1 | 0x1F9BCA | Byte | value & 0x8 == 0x8 | Fist Power |
| The Swamp of Forgetfulness Screen 2 cage 1 | 0x1F9BEE | Half-Word | value & 0x2 == 0x2 | Fist Power |
| The Swamp of Forgetfulness Screen 2 cage 2 | 0x1F9BEE | Half-Word | value & 0x800 == 0x8000 | Fist Power |
| The Swamp of Forgetfulness Screen 3 cage 1 | 0x1F9C10 | Byte | value & 0x4 == 0x4 | Fist Power |
| The Swamp of Forgetfulness Screen 3 cage 2 | 0x1F9C10 | Byte | value & 0x2 == 0x2 | Fist Power |
| The Swamp of Forgetfulness Screen 3 magician 1 | 0x1f7f40 | Word | value & 0x20000 == 0x20000 | Fist Power |
| Moskito's Nest Screen 1 cage 1 | 0x1F9C2F | Byte | value & 0x40 == 0x40 | Fist Power, Hanging, Grappling fist |
| Moskito's Nest Screen 1 cage 2 | 0x1F9C2F | Byte | value & 0x8 == 0x8 | Fist Power |
| Moskito's Nest Screen 1 cage 3 | 0x1F9C2F | Byte | value & 0x4 == 0x4 | Fist Power |
| Moskito's Nest Screen 1 magician 1 | 0x1f7f40 | Byte | value & 0x40000 == 0x40000 | Fist Power |
| Moskito's Nest Screen 2 cage 1 | 0x1F9C51 | Byte | value & 0x8 == 0x8 | Fist Power |
| Moskito's Nest Screen 2 cage 2 | 0x1F9C51 | Byte | value & 0x2 == 0x2 | Fist Power |
| Moskito's Nest Screen 2 cage 3 | 0x1F9C51 | Byte | value & 0x1 == 0x1 | Fist Power |
| Moskito's Nest Screen 4 life 1 | 0x1F9C8D | Byte | value & 0x2 == 0x2 | Fist Power, Grappling Fist |
| Bongo Hills Screen 1 cage 1 | 0x1F9D72 | Byte | value & 0x1 == 0x1 | Fist Power, Hanging |
| Bongo Hills Screen 1 life 1 | 0x1F9D6B | Byte | value & 0x2 == 0x2 | None |
| Bongo Hills Screen 2 cage 1 | 0x1F9D98 | Byte | value & 0x20 == 0x20 | Fist Power |
| Bongo Hills Screen 2 life 1 | 0x1F9D90 | Byte | value & 0x80 == 0x80 | None |
| Bongo Hills Screen 3 cage 1 | 0x1F9DB0 | Byte | value & 0x8 == 0x8 | Fist Power |
| Bongo Hills Screen 3 life 1 | 0x1F9DA8 | Byte | valeu & 0x20 == 0x20 | None |
| Bongo Hills Screen 4 cage 1 | 0x1F9DD8 | Byte | value & 0x8 == 0x8 | Fist Power, Grappling Fist |
| Bongo Hills Screen 4 life 1 | 0x1F9DCA | Byte | value & 0x20 == 0x20 | Fist Power |
| Bongo Hills Screen 4 magician 1 | 0x1F7F46 | Byte | value & 0x1 == 0x1 | None |
| Bongo Hills Screen 5 cage 1 | 0x1F9DFA | Byte | value & 0x2 == 0x2 | Fist Power |
| Bongo Hills Screen 5 cage 2 | 0x1F9DFA | Byte | value & 0x1 == 0x1 | Fist Power |
| Bongo Hills Screen 6 life 1 |0x1F9E10 | Byte | value & 0x2 == 0x2 | Fist Power (but not mandatory) |
| Allegro Presto Screen 1 cage 1 | 0x1F9E28 | Byte | value & 0x20 == 0x20 | Fist Power, hanging |
| Allegro Presto Screen 1 cage 2 | 0x1F9E28 | Byte | value & 0x4 == 0x4 | Fist Power |
| Allegro Presto Screen 1 cage 3 | 0x1F9E28 | Byte | value & 0x10 == 0x10 | Fist Power |
| Allegro Presto Screen 2 cage 1 | 0x1F9E57 | Byte | valeu & 0x80 == 0x80 | Fist Power, Hanging |
| Allegro Presto Screen 2 life 1 | 0x1F9E48 | Byte | value & 0x8 == 0x8 | None |
| Allegro Presto Screen 3 cage 1 | 0x1F9E69 | Byte | value & 0x1 == 0x1 | Fist Power, Hanging |
| Allegro Presto Screen 3 cage 2 | 0x1F9E69 | Byte | value & 0x4 == 0x4 | Fist Power |
| Allegro Presto Screen 3 life 1 | 0x1F9E6B | Byte | value & 0x4 == 0x4 | Hanging |
| Allegro Presto Screen 3 life 2 | 0x1F9E6E | Byte | valeu & 0x80 == 0x80 | Fist Power |
| Allegro Presto Screen 3 magician 1 | 0x1F7F46 | byte | value & 0x2 == 0x2 | Fist Power, Hanging |
