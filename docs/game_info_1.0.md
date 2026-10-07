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
|:---|:---:|:---:|
| Death Link | If a player die and death link is active Rayman die too | Set ``Rayman mode`` to 3 |
| Number of tings to get a life | Change the amount of tings needed to get a life | If ``Tings counter`` >= X then increments ``Life counter`` |
| Give Rayman magic seed | Rayman get the ability to plant Magic Seed | Set ``Rayman Events 1`` to ``Rayman Events 1`` \| 0x40 |

## Items

All the items a player can get

### Important

| Name | Description | Implementation to give the item |
|:---|:---:|:---:|
| Fist Power | Give Rayman the ability to throw his fist | ``Rayman Events 1`` =  ``Rayman Events 1`` \| 0x1 |
| Hanging | Give Rayman the ability to hang on platforms | ``Rayman Events 1`` = ``Rayman Events 1`` \| 0x2 |
| Grappling Fist | Give Rayman the ability to grab lives and pink rings | ``Rayman Events 1`` = ``Rayman Events 1`` \| 0x80 |
| Helicopter Power | Give Rayman the ability to Helicopter with his hairs | ``Rayman Events 1`` =  ``Rayman Events 1`` \| 0x8 |
| Run Power | Give Rayman the ability to Run | ``Rayman Events 2`` = ``Rayman Events 2`` \| 0x1 |
| Magic Seed | Give Rayman the ability to plant Magic Seeds | ``Rayman Events 1`` = ``Rayman Events 1`` \| 0x40 |
| Super Helicopter | Give Rayman the ability to fly with his hair | ``Rayman Events 1`` \| 0x8 |
| Light Fist | Give Rayman the ability to illumiate the darkness with his fist |  ``Rayman Events 2`` = ``Rayman Events 2`` \| 0x4 |
| Cage | One of the 102 cages in the game | Increments by 1 the ``Total cage counter`` variable |
| Protoon piece | An imaginary item for Archipelago, if you got the necessary amount it unlocks access to Mr.Dark's Dare | Intern logic |
| Level Unlock | Unlock access to a level from another | To implement by editing the world_info structure ? |

### Filler

| Name | Description | Implementation |
|:---|:---:|:---:|
| Simple Power | Give 1 HP to Rayman | Increments ``Health Points`` by 1 |
| Double Power | Give 2 HP to Rayman | Increments ``Health Points`` by 2 |
| Big Power | Restore Rayman's health completely and increase his health bar to 5 points. If Rayman loses a life, the effect is cancelled | Set ``Max Health Points`` and ``Health Points`` to 5 |
| Speed Fist | Increase Raymans's fist range and the speed | Increments ``Fist Level`` |
| Gold Fist | Increase Rayman's fist strenght | ??? |
| Life | Increase Rayman's life counter by 1 | Increments ``Life counter`` by 1 |
| 5 Tings | Increase by 5 the tings counter | Increments ``Tings counter`` by 5 |

### Traps

| Name | Description | Implementation |
|:---|:---:|:---:|
| Reversed Controls | The player's controls will be reversed similar to the start of Mr.Dark's Dare 3 | Set ``Rayman Events 2`` to ``Rayman Events 2`` \| 0x20 |
| Elf Trap | For a limited time, Rayman will be temporarely shrunken, making him slower and his jumps lower | Set ``Rayman Events 1`` to ``Rayman Events 1`` \| 0x2 (+ modify an other address for the sprite size)|
| Forced Run | For a limited time, Rayman will be force to run | Set ``Rayman Events 2`` to ``Rayman Events 2`` \| 0x10 |

## Locations

- value = the value in the ``address`` column
- Dependency : considering the whole level

| Name | address | size | how to check | dependency |
|:---|:---:|:---:|:---:|:---:|
| Fist Power (Betilla gift 1) | 0x1f43d0 | Byte | value & 0x1 == 0x1 | None |
| Hanging (Betilla gift 2)| 0x1F43D0 | Byte | value & 0x2 == 0x2 | Fist Power |
| Grappling Fist (Betilla gift 3)| 0x1F43D0 | Byte | value & 0x80 == 0x80 | Fist Power |
| Helicopter (Betilla gift 4) | 0x1f43d0 |  byte | value & 0x4 == 0x4 | Fist Power, Hanging |
| Run (Betilla gift 5) | 0x1F43D1 | Byte | 0x1 | Fist Power, Super Helicopter |
| Magic Seed | 0x1f43d0 | Byte | 0x40 | None |
| Super Helicopter | 0x1f43d0 | Byte | 0x8 | Fist Power |
| Moskito 1 | 0x1F4EE8 | Byte | value & 0x1 == 0x1 | Fist Power |
| Moskito 1 | 0x1F4EE8 | Byte | value & 0x2 == 0x2 | Fist Power |
| Mr.Sax | 0x1F4EE8 | Byte | 0x4 | Fist, Hanging |
| Mr.Stone | 0x1F4EE8 | Byte | 0x8 | Fist Power, Super Helicopter |
| Viking Mama | 0x1F4EE8 | Byte | 0xA | Fist Power, Hanging, Helicopter, Grappling Fist, Run |
| Space Mama | 0x1F4EE8 | Byte | 0x20 |  Fist Power, Hanging, Helicopter, Grappling Fist |
| Mr.Skops phase 1 | 0x1F4EE8 | Byte | 0x40 | Fist Power, Hanging, Grappling Fist, Helicopter, Run |
| Mr.Dark | 0x1F4E8 | Byte | 0x80 | Fist Power, Hanging, Grappling Fist, Helicopter, Run |
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
| Gong Heights Screen 1 cage 1 | 0x1F9EC8 | Byte | 0x4 | Fist Power |
| Gong Heights Screen 1 cage 2 | 0x1F9EC8 | Byte | 0x20 | Fist Power, Hanging, Helicopter, Run |
| Gong Heights Screen 1 cage 3 | 0x1F9EC8 | Byte | 0x10 | Fist Power |
| Gong Heights Screen 1 cage 4 | 0x1F9EC8 | Byte | 0x80 | Fist Power, Hanging |
| Gong Heights Screen 2 cage 1 | 0x1F9EE8 | Byte | 0x4 | Fist Power, Haning, Helicopter |
| Gong Heights Screen 2 cage 2 | 0x1F9EE8 | Byte | 0x20 | Fist Power, Hanging, Helicopter |
| Mr.Sax's Hullaballo Screen 1 cage 1 | 0x1F9F1C | Byte | 0x8 | Fist Power, Hanging |
| Mr.Sax's Hullaballo Screen 1 cage 2 | 0x1F9F1B | Byte | 0x1 | Fist Power |
| Mr.Sax's Hullaballo Screen 1 cage 3 | 0x1F9F1C | Byte | 0x20 | Fist Power, Hanging |
| Mr.Sax's Hullaballo Screen 1 cage 4 | 0x1F9F1C | Byte | 0x80 | Fist Power |
| Mr.Sax's Hullaballo Screen 1 cage 5 | 0x1F9F1C | Byte | 0x10 | Fist Power, Hanging, Grappling Fist |
| Mr.Sax's Hullaballo Screen 1 cage 6 | 0x1F9F1C | Byte | 0x40 | Fist Power, Hanging |
| Mr.Sax's Hullaballo Screen 1 life 1 | 0x1F9F0B | Byte | 0x10 | Fist Power, Hanging, Grappling Fist |
| Mr.Sax's Hullaballo Screen 1 life 2 | 0x1F9F0F | Byte | 0x10 | Fist Power, Hanging, Grappling Fist |
| Twilight Gulch Screen 1 cage 1 | 0x1F9FB3 | Byte | 0x80 | Fist Power |
| Twilight Gulch Screen 1 cage 2 | 0x1F9FB3 | Byte | 0x20 | Fist Power |
| Twilight Gulch Screen 1 cage 3 | 0x1F9FB2 | Byte | 0x2 | Fist Power |
| Twilight Gulch Screen 1 cage 4 | 0x1F9FB3 | Byte | 0x40 | Fist Power, Grappling Fist |
| Twilight Gulch Screen 1 cage 5 | 0x1F9FB2 | Byte | 0x4 | Fist Power, Grappling Fist, Run |
| Twilight Gulch Screen 1 cage 6 | 0x1F9FB3 | Byte | 0x10 | Fist, Grappling Fist |
| **missable** Twilight Gulch Screen 2 life 1 | 0x1F9FD3 | Byte | value & 0x80 == 0x80 | Fist Power, Grappling Fist |
| The Hard Rocks Screen 1 cage 1 | 0x1F9FFF | Byte | valeu & 0x40 == 0x40 | Fist Power |
| The Hard Rocks Screen 1 life 1 | 0x1F9FEB | Byte | value & 0x20 == 0x20 | Fist Power |
| The Hard Rocks Screen 1 life 2 | 0x1F9FED | Byte | value & 0x2 == 0x2 | Fist Power, Grappling fist, Helicopter |
| The Hard Rocks Screen 2 cage 1 | 0x1FA00C | Byte | value & 0x20 == 0x20 | Fist Power, Helicopter |
| The Hard Rocks Screen 2 cage 2 | 0x1FA00C | Byte | value & 0x40 == 0x40 | Fist Power, Helicopter |
| The Hard Rocks Screen 2 life 1 | 0x1FA010 | Byte | value & 0x20 == 0x20 | Fist Power, Helicopter, Grappling Fist |
| The Hard Rocks Screen 2 magician 1 | 0x1F7F49 | Byte | value & 0x8 == 0x8 | Fist Power, Helicopter |
| The Hard Rocks Screen 3 cage 1 | 0x1FA032 | Byte | value & 0x40 == 0x40 | Fist Power, Helicopter |
| The Hard Rocks Screen 3 cage 2 | 0x1FA031 | Byte | value & 0x1 == 0x1 | Fist Power, Helicopter, Hanging |
| The Hard Rocks Screen 3 cage 3 | 0x1FA031 | Byte | value & 0x2 == 0x2 | Fist Power, Helicopter |
| The Hard Rocks Screen 3 life 1 | 0x1FA02F | Byte | value & 0x20 == 0x20 | Fist Power, Helicopter |
| The Hard Rocks Screen 3 life 2 | 0x1FA02C | Byte | value & 0x2 == 0x2 | Fist Power, Helicopter, Hanging |
| The Hard Rocks Screen 3 life 3 | 0x1FA02C | Byte | value & 0x20 == 0x20 | Fist Power, Helicopter |
| Mr.Stone's Peaks Screen 1 cage 1 | 0x1FA058 | Byte | 0x2 | Fist Power, Super Helicopter |
| Mr.Stone's Peaks Screen 1 cage 2 | 0x1FA058 | Byte | 0x1 | Fist Power, Super Helicopter |
| Mr.Stone's Peaks Screen 1 life 1 | 0x1FA053 | Byte | 0x80 | Super Helicopter |
| Mr.Stone's Peaks Screen 2 cage 1 | 0x1FA06D | Byte | 0x80 | Fist Power, Super Helicopter |
| Mr.Stone's Peaks Screen 3 cage 1 | 0x1FA08E | Byte | 0x2 | Fist Power, Super Helicopter |
| Mr.Stone's Peaks Screen 4 cage 1 | 0x1FA0BB | Byte | 0x1 | Fist Power, Super Helicopter |
| Mr.Stone's Peaks Screen 4 cage 2 | 0x1FA0BC | Byte | 0x80 | Fist Power, Super Helicopter |
| Mr.Stone's Peaks Screen 4 life 1 | 0x1FA0AC | Byte | 0x10 | Fist Power, Super Helicopter, Hanging |
| Mr.Stone's Peaks Screen 4 magician 1 | 0x1F7F49 | Byte | 0x10 | Fist Power, Super Helicopter |
| Eraser Plains Screen 1 cage 1 | 0x1FA15B | Byte | 0x8 | Fist Power |
| Eraser Plains Screen 1 cage 2 | 0x1FA15B | Byte | 0x10 | Fist Power |
| Eraser Plains Screen 1 life 1 | 0x1FA148 | Byte | 0x1 | Fist Power, Grappling Fist, Helicopter, Run |
| Eraser Plains Screen 2 cage 1 | 0x1FA17A | Byte | 0x8 | Fist Power, Helicopter or Run |
| Eraser Plains Screen 2 life 1 | 0x1FA16B | Byte | 0x10 | Fist Power |
| Eraser Plains Screen 2 life 2 | 0x1FA16A | Byte | 0x40 | Fist Power, Hanging |
| Eraser Plains Screen 2 life 3 | 0x1FA16E | Byte | 0x4 | Fist Power, Hanging or Helicoper or Run, Grappling Fist |
| Eraser Plains Screen 3 cage 1 | 0x1FA198 | Byte | 0x80 | Fist Power, Helicoper or Run, Grappling Fist |
| Eraser Plains Screen 3 cage 2 | 0x1FA198 | Byte | 0x2 | Fist Power, Hanging, Helicoper, Grappling Fist |
| Eraser Plains Screen 3 cage 3 | 0x1FA197 | Byte | 0x4 | Fist Power, Hanging, Helicopter, Gappling Fist |
| Eraser Plains Screen 3 life 1 | 0x1FA190 | Byte | 0x40 | Fist Power, Hanging, Helicopter, Grappling Fist |
| Eraser Plains Screen 3 life 2 | 0x1FA193 | Byte | 0x40 | Fist Power, Hanging, Helicopter, Grappling Fist |
| Eraser Plains Screen 3 magician 1 | 0x1F7F4D | Byte | 0x8 | Fist Power, Hanging, Helicopter, Grappling Fist, Run |
| Pencil Pentathlon Screen 1 cage 1 | 0x1FA1DF | Byte | 0x4 | Fist Power, Hanging, Helicopter |
| Pencil Pentathlon Screen 1 cage 2 | 0x1FA1DF | Byte | 0x2 | Fist Power, Hanging, Helicopter, Grappling Fist |
| Pencil Pentathlon Screen 1 life 1 | 0x1FA1D3 | Byte | 0x1 | Fist Power, Hanging, Helicoper, Grappling Fist |
| Pencil Pentathlon Screen 1 life 2 | 0x1FA1D0 | Byte | 0x1 | Fist Power, Hanging, Helicopter, Grappling Fist, Run |
| Pencil Pentathlon Screen 1 life 3 | 0x1fA1F1 | Byte | 0x20 | Fist Power, Hanging, Helicopter, Grappling Fist, Run |
| Pencil Pentathlon Screen 2 cage 1 | 0x1FA1F2 | Byte | 0x4 | Fist Power, Hanging, Helicopter, Grappling Fist, Run, Super Helicopter |
| Pencil Pentathlon Screen 2 cage 2 | 0x1FA1F2 | Byte | 0x1 | Fist Power, Hanging, Helicopter, Grappling Fist, Run, Super Helicopter |
| Pencil Pentathlon Screen 2 life 1 | 0x1FA1F0 | Byte | 0x40 | Fist Power, Hanging, Helicopter, Grappling Fist, Run, Super Helicopter |
| Pencil Pentathlon Screen 3 cage 1 | 0x1FA214 | Byte | 0x80 | Fist Power, Hanging, Helicopter, Grappling Fist, Run, Super Helicopter |
| Pencil Pentathlon Screen 3 cage 2 | 0x1FA213 | Byte | 0x2 | Fist Power, Hanging, Helicopter, Grappling Fist, Run, Super Helicopter |
| Pencil Pentathlon Screen 3 life 1 | 0x1FA20B | Byte | 0x80 | Fist Power, Hanging, Helicopter, Grappling Fist, Run, Super Helicopter |
| Space Mama's Crater Screen 1 cage 1 | 0x1FA230 | Byte | 0x4 | Fist Power, Hanging, Helicopter, Grappling Fist |
| Space Mama's Crater Screen 1 cage 2 | 0x1FA230 | Byte | 0x8 | Fist Power, Hanging, Helicopter, Grappling Fist | 
| Space Mama's Crater Screen 1 life 1 | 0x1FA22F | Byte | 0x10 | Fist Power, Hanging, Helicopter, Grappling Fist, Run |
| Space Mama's Crater Screen 1 life 2 | 0x1FA22C | Byte | 0x8 | Fist Power, Hanging, Helicopter, Grappling Fist |
| Space Mama's Crater Screen 2 cage 1 | 0x1FA249 | Byte | 0x1 | Fist Power, Hanging, Helicopter, Grappling Fist |
| Space Mama's Crater Screen 2 cage 2 | 0x1FA249 | Byte | 0x4 | Fist Power, Hanging, Helicopter, Grappling Fist |
| Space Mama's Crater Screen 2 life 1 | 0x1FA257 | Byte | 0x20 | Fist Power, Hanging, Helicopter, Grappling Fist |
| Space Mama's Crater Screen 2 Macigian 1 | 0x1F7F4D | Byte | 0x10 | Fist Power, Hanging, Helicopter, Grappling Fist |
| Space Mama's Crater Screen 3 cage 1 | 0x1FA27B | Byte | 0x20 | Fist Power, Hanging, Helicopter, Grappling Fist |
| Space Mama's Crater Screen 3 cage 2 | 0x1FA27B | Byte | 0x10 | Fist Power, Hanging, Helicopter, Grappling Fist |
| Space Mama's Crater Screen 3 life 1 | 0x1FA274 | Byte | 0x20 | Fist Power, Hanging, Helicopter, Grappling Fist |
| Crystal Palace Screen 1 cage 1 | 0x1FA2F4 | Byte | 0x2 | Fist Power |
| Crystal Palace Screen 1 cage 2 | 0x1FA2F4 | Byte | 0x20 | Fist Power, Grappling Fist |
| Crystal Palace Screen 1 cage 3 | 0x1FA2F4 | Byte | 0x10 | Fist Power, Grappling Fist |
| Crystal Palace Screen 2 cage 1 | 0x1FA314 | Byte | 0x40 | Fist Power, Grappling Fist |
| Crystal Palace Screen 2 cage 2 | 0X1fa313 | Byte | 0x1 | Fist Power, Hanging, Grappling Fist, Helicopter or Run |
| Crystal Palace Screen 2 cage 3 | 0x1FA314 | Byte | 0x80 | Fist Power, Hanging, Grappling Fist, Helicopter or Run |
| Crystal Palace Screen 2 life 1 | 0x1FA30D | Byte | 0x20 | Fist Power, Grappling Fist |
| Crystal Palace Screen 2 life 2 | 0x1FA309 | Byte | 0x4 | Fist Power, Hanging, Grappling Fist |
| Crystal Palace Screen 2 magician 1 | 0x1F7F51 | Byte | 0x8 | Fist Power, Hanging, Grappling Fist, Helicopter |
| Eat At Joe's Screen 1 cage 1 | 0x1FA34F | Byte | 0x8 | Fist Power, Helicopter |
| Eat At Joe's Screen 1 life 1 | 0x1FA34C | Byte | 0x40 | Fist Power, Hanging, Helicopter |
| Eat At Joe's Screen 1 life 2 | 0x1FA34C | Byte | 0x80 | Fist Power, Helicopter |
| Eat At Joe's Screen 1 life 3 | 0x1FA34A | Byte | 0x10 | Fist Power, Hanging, Helicopter, Run |
| Eat At Joe's Screen 2 cage 1 | 0x1FA379 | Byte | 0x8 | Fist Power, Grappling Fist, Helicopter | 
| Eat At Joe's Screen 2 cage 2 | 0x1FA379 | Byte | 0x18 | Fist Power, Grappling Fist, Helicopter |
| Eat At Joe's Screen 2 cage 3 | 0x1FA379 | Byte | 0x2 | Fist Power, Grappling Fist, Helicopter |
| Eat At Joe's Screen 2 life 1 | 0x1FA373 | Byte | 0x10 | Fist Power, Grappling Fist, Helicopter | 
| Eat At Joe's Screen 2 life 2 | 0x1FA372 | Byte | 0x10 | Fist Power, Grappling Fist, Helicopter | 
| Eat At Joe's Screen 3 life 1 | 0x1FA389 | Byte | 0x8 | Fist Power, Grappling Fist, Helicopter |
| Eat At Joe's Screen 4 cage 1 | 0x1FA3A8 | Byte | 0x40 | Fist Power, Grappling Fist, helicopter |
| Eat At Joe's Screen 4 life 1 | 0x1FA3B2 | Byte | 0x8 | Fist Power, Grappling Fist, Helicopter |
| Eat At Joe's Screen 5 cage 1 | 0x1FA3CE | Byte | 0x2 | Fist Power, Grappling Fist, Helicopter |
| Mr.Skops' Stalactites Screen 1 cage 1 | 0x1FA3E8 | Byte | 0x8 | Fist Power |
| Mr.Skops' Stalactites Screen 1 cage 2 | 0x1FA3E8 | Byte | 0x4 | Fist Power, Helicopter |
| Mr.Skops' Stalactites Screen 1 cage 3 | 0x1FA3E8 | Byte | 0x20 | Fist Power, Helicopter, Grappling Fist |
| Mr.Skops' Stalactites Screen 1 cage 4 | 0x1FA3E8 | Byte | 0x40 | Fist Power, Helicopter, Grappling Fist |
| Mr.Skops' Stalactites Screen 1 cage 5 | 0x1FA3E8 | Byte | 0x10 | Fist Power, Helicopter, Grappling Fist |
| Mr.Skops' Stalactites Screen 1 cage 6 | 0x1FA3E8 | Byte | 0x2 | Fist Power, Helicopter, Grappling Fist |
| Mr.Skops' Stalactites Screen 1 life 1 | 0x1FA3EF | Byte | 0x40 | Fist Power, Helicopter, Grappling Fist |
| Mr.Dark's Dare Screen 2 life 1 | 0x1FA48D | 0x4 | None |
| Mr.Dark's Dare Screen 3 life 1 | 0x1FA4B5 | 0x8 | Fist Power, Hanging, Grappling Fist, Helicopter, Run |
| Mr.Dark's Dare Screen 3 life 2 | 0x1FA4B7 | 0x40 | Fist Power, Hanging, Grappling Fist, Helicopter, Run |
| Game End | 0x1D8B40 | Byte | 0x1 | Fist Power |
