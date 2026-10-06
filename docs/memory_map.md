# Rayman PS1 Memory Map
This is the main memory addresses used in the Rayman Archipalego world.
All addresses here stands for the US version.

## Main addresses

| Meaning | Address | Values | Size |
|:---|:---:|:---:|---:|
| Tings counter | 0x1E4D56 | Indicate the number of tings you get | Byte |
| Life counter | 0x1E4D50 | Indicate the number of life remaining | Byte |
| Continue counter | 0x1E5A10 | Indicate the number of continue remaining | Byte |
| Health Points | 0x1F6200 | Indicate the number of HP remaining (minus 1) | Byte |
| Max Health Points | 0x1E4D59 | Indicate the max amount of HP for Rayman (minus 1)<br>2: base Max HP<br>4: Upgraded Max HP | Byte |
| Is paused | 0x1CEE80 | 0: While playing<br>1: When paused | Byte |
| Menu State | 0x1f81a0 | 0: Title screen<br>1: Save type selection<br>3: Memory Card Save Slot choice<br>4: The rest of the game | Byte |
| is Rayman drowning | 0x1E5950 | 0: Everything is ok<br>1: Rayman is drowning | Byte |
| Rayman mode | 0x1E5420 | 1: Normal Mode<br>2: Moskito mode<br>3: Dying | Byte |
| Fist Level | 0x1D8B34 | min : 0x1<br>max : 0xC | Byte |
| Gold Fist | 0xAE9C9 (level 1) | mirror of Fist Level. We need to find the address of the fist in each level | Byte |
| World index | 0x1e6330 | See Worlds and Levels Indexes | Byte |
| World info | 0x1c335c | See Worlds and Levels Indexes | Byte |
| Rayman Events 1 | 0x1f43d0 | Bifield for powers : masks in rayman_archipelago_modelisation.md | Byte |
| Rayman Events 2 | 0x1f43d1 | Bitfield for other special situation | Byte |
| Boss encounter | 0x1f4ee8 | Bitfield for boss battle : masks in game_info_1.0.md | Byte |
| Total cage counter | 0x1F8138 | Indicate the number of cages broked in the game | Byte |
| Current world id | 0x1FA688 | See Wolrds and levels table | Byte |
| Current level id | 0x1F9A68 | See Wolrds and levels table | Byte |

## Worlds and Levels ids

| Zone | World id| Level id|
|:---|:---:|---:|
| Pink Plant Wood Screen 1 | 1 | 1 |
| Pink Plant Wood Screen 2 | 1 | 2 |
| Pink Plant Wood Betilla | 1 | 3 |
| Pink Plant Wood Screen 3 | 1 | 4 |
| Anguish Lagoon Screen 1 | 1 | 5 |
| Anguish Lagoon Screen 2 | 1 | 6 |
| Anguish Lagoon Screen 3 | 1 | 7 |
| Anguish Lagoon Betilla | 1 | 8 |
| The Swamp of Forgetfulness Screen 1 | 1 | 9 |
| The Swamp of Forgetfulness Screen 2 | 1 | 10 |
| The Swamp of Forgetfulness Screen 3 | 1 | 11 |
| Moskito's Nest Screen 1 | 1 | 12 |
| Moskito's Nest Screen 2 | 1 | 13 |
| Moskito's Nest Screen 3 | 1 | 14 |
| Moskito's Nest Screen 4 | 1 | 15 |
| Moskito's Nest Screen 5 | 1 | 16 |
| Moskito's Nest Betilla | 1 | 17 |
| Bongo Hills Screen 1 | 2 | 1 |
| Bongo Hills Screen 2 | 2 | 2 |
| Bongo Hills Screen 3 | 2 | 3 |
| Bongo Hills Screen 4 | 2 | 4 |
| Bongo Hills Screen 5 | 2 | 5 |
| Bongo Hills Screen 6 | 2 | 6 |
| Allegro Presto Screen 1 | 2 | 7 |
| Allegro Presto Screen 2 | 2 | 8 |
| Allegro Presto Screen 3 | 2 | 9 |
| Allegro Presto Screen 4 | 2 | 10 |
| Allegro Presto Betilla | 2 | 11 |
| Gong Height Screen 1 | 2 | 12 |
| Gong Height Screen 2 | 2 | 13 |
| Mr.Sax's Hullaballo Screen 1 | 2 | 14 |
| Mr.Sax's Hullaballo Screen 2 | 2 | 15 |
| Twilight Gulch Screen 1 | 3 | 1 |
| Twilight Gulch Screen 2 | 3 | 2 |
| The Hard Rocks Screen 1 | 3 | 3 |
| The Hard Rocks Screen 2 | 3 | 4 |
| The Hard Rocks Screen 3 | 3 | 5 |
| Mr.Stone's Peaks Screen 1 | 3 | 6 |
| Mr.Stone's Peaks Screen 2 | 3 | 7 |
| Mr.Stone's Peaks Screen 3 | 3 | 8 |
| Mr.Stone's Peaks Screen 4 | 3 | 9 |
| Eraser Plains Screen 1 | 4 | 1 |
| Eraser Plains Screen 2 | 4 | 2 |
| Eraser Plains Screen 3 | 4 | 3 |
| Eraser Plains Screen 4 | 4 | 4 |
| Pencil Pentathlon Screen 1 | 4 | 5 |
| Pencil Pentathlon Screen 2 | 4 | 6 |
| Pencil Pentathlon Screen 3 | 4 | 7 |
| Space Mama's Crater Screen 1 | 4 | 8 |
| Space Mama's Crater Screen 2 | 4 | 9 |
| Space Mama's Crater Screen 3 | 4 | 10 |
| Crystal Palace Screen 1 | 5 | 1 |
| Crystal Palace Screen 2 | 5 | 2 |
| Eat at Joe's Screen 1 | 5 | 4 |
| Eat at Joe's Screen 2 | 5 | 5 |
| Eat at Joe's Screen 3 | 5 | 6 |
| Eat at Joe's Screen 4 | 5 | 7 |
| Eat at Joe's Screen 5 | 5 | 8 |
| Mr.Skop's Stalactites Screen 1 | 5 | 9 |
| Mr.Skops Phase 1 | 5 | 10 | 
| Mr.Skops Phase 2 | 5 | 11 |
| Mr.Dark's Dare Screen 1 | 6 | 1 |
| Mr.Dark's Dare Screen 2 | 6 | 2 |
| Mr.Dark's Dare Screen 3 | 6 | 3 |

## World map info

### structure

| Field | Address | Size | Description |
|:---|:---:|:---:|:---:|
| x_pos | 0x1C335C | Half-Word | x_position of the level on the map |
| y_pos | +0x2 | Half-Word | y_position of the level on the map |
| index_up | +0x4 | Byte | The index of the level to reach when pressing up |
| index_down | +0x5 | Byte | The index of the level to reach when pressing down |
| index_left | +0x6 | Byte | The index of the level to reach when pressing left |
| index_right | +0x7 | Byte | The index of the level to reach when pressing left |
| is_unlocked | +0x8 | Byte | 0: not unlocked<br>4: Unlocking<br>3: Unlocked |
| nb_cage | +0x9 | Byte | The number of cages in the level |
| world | +0xA | Byte | The world id of the level to load |
| Level | +0xB | Byte | The level id of the level to load |
| color | +0xC | Half-Word | The color for the level text |
| is unlocking ??? | +0xE | Half-Word | ??? |
| Level Name | +0x10 | Word | The pointer to the level name |

### Level indexes and addresses

| Index | Level Name | Address |
|:---|:---:|:---:|
| 0 | Pink Plant Woods | 0x1C335C |
| 1 | Anguish Lagoon | 0x1C3370 |
| 2 | The Swamps of forgetfulness | 0x1C3384 |
| 3 | Moskito's Nest | 0x1C3398 |
| 4 | Bongo Hills | 0x1C33AC |
| 5 | Allegro Presto | 0x1C33C0 |
| 6 | Gong Height | 0x1C33D4 |
| 7 | Mr.Sax' Hullaballo | 0x1C33E8 |
| 8 | Twilight Gulch | 0x1C33FC |
| 9 | The Hard Rocks | 0x1C3410 |
| A | MR.Stone's Peaks | 0x1C3424 | 
| B | Eraser Plains | 0x1C3438 |
| C | Pencil Pentathlon | 0x1C344C |
| D | Space Mama's Crater | 0x1C3460 |
| E | Crystal Palace | 0x1C3474 |
| F | Eat At Joe's | 0x1C3488 |
| 10 | Mr.Sops' Stalactites | 0x1C349C |
| 11 | Mr.Dark's Dare | 0x1C34B0 |
| 12 | First Save | 0x1C34C4 |
| 13 | Second Save | 0x1C34D8 |
| 14 | Third Save | 0x1C34EC |
| 15 | Fourth Save | 0x1C3500 |
| 16 | Fith Save | 0x1C3514 |
