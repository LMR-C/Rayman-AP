# Modelling

This document aims to set the model for items, locations, regions, entrances, options 
and rules of this world

## Item
### Item Data
- Namming convention : 
    - item name : Use the name written in the [game_info_1.0.md](game_info_1.0.md) file
    - variable name : Use the name written in the [game_info_1.0.md](game_info_1.0.md) file but in snakecase
- Id scheme : in decimal
    - 1xx : Important items
    - 2xx : Filler items
    - 3xx : Trap items
- Fields :
    - id : to identify the item in the game (must be unique)
    - name : to show the name of the item
    - address : The game's memory address to give the item
    - size : the number of bytes to read
    - mask : If the item is stored in a bitfield it needs a mask
    - count : the number of time this item needs to be in the item pool (depend on the options)
    - classification : to qualify the item for placement logic

```python
fist_power = ItemData(
    101,
    "Fist Power",
    0x1f43d0,
    1,
    0x1,
    1,
    Classification.progression
)
```

### Item Init

- id : is to be choosen when implementing
- name : precised earlier
- address : can be found in [game_info_1.0.MD](game_info_1.0.md)
- size : can be found in [game_info_1.0.MD](game_info_1.0.md)
- mask : can be found in [game_info_1.0.MD](game_info_1.0.md)
- count and classification are defined below

#### Options independant
| Item | count | classification |
|:---|:---:|:---:|
| Fist Power | 1 | ItemClassification.progression |
| Hanging | 1 | ItemClassification.progression |
| Grappling Fist | 1 | ItemClassification.progression |
| Helicopter | 1 | ItemClassification.progression |
| Run | 1 | ItemClassification.progression |
| Magic Seed | 1 | ItemClassification.progression |
| Super Helicopter | 1 | ItemClassification.progression |
| Light Fist | 1 | ItemClassification.progression |
| Simple Power | filler | ItemClassification.filler |
| Double Power | filler | ItemClassification.filler |
| Big Power | filler | ItemClassification.filler |
| 5 Tings | filler | ItemClassification.filler |
| life | filler | ItemClassification.filler |
| Gold Fist | filler | ItemClassification.filler |
| Life | filler | ItemClassification.filler |

#### Options dependent

##### Cage

- Goal is cages :
    - count : Options.number_of_cages_required
- Goal is something else :
    - count : 0
- classification : ItemClassification.progression

##### protoon piece

- Goal is Great Protoon pieces :
    - count : Options.number_of_great_protoon_pieces_required
- Goal is something else :
    - count : 0
- classification : ItemClassification.progression

##### level unlock

maybe make unique item for each level ?

- open world enabled : 
    - count : 0
- open world disabled : 
    - count : 17
- classification : ItemClassification.progression

#####  Life status
- include life status enabled :
    - count : 65
- include life status disabled :
    - count : 0
- classification : ItemClassification.useful or ItemClassification.filler ?

##### Reversed Controls 

- Reversed Controls weight :
    - None : count : 0
    - Low : remaining_items * (Trap_fill_percentage / 100) * 0.25
    - medium : remaining_items * (Trap_fill_percentage / 100) * 0.5
    - High : remaining_items * (Trap_fill_percentage / 100) * 0.75
- Classification : ItemClassification.trap

##### Elf Trap

- Reversed Controls weight :
    - None : count : 0
    - Low : remaining_items * (Trap_fill_percentage / 100) * 0.25
    - medium : remaining_items * (Trap_fill_percentage / 100) * 0.5
    - High : remaining_items * (Trap_fill_percentage / 100) * 0.75
- Classification : ItemClassification.trap

##### Forced Run 

- Reversed Controls weight :
    - None : count : 0
    - Low : remaining_items * (Trap_fill_percentage / 100) * 0.25
    - medium : remaining_items * (Trap_fill_percentage / 100) * 0.5
    - High : remaining_items * (Trap_fill_percentage / 100) * 0.75
- Classification : ItemClassification.trap

## Locations

### Locations Data
- Namming convention : 
    - location name : Use the name written in the [game_info_1.0.MD](game_info_1.0.md) file
    - variable name : 
        - Use snakecase
        - format : levelname_screen_type
        - levelname : The first letter of each word in the level name
        - screen : s + the number of the screen
        - type : the item's type + its number
        - i.e : Pink Plant Wood Screen 1 life 1 -> ppw_s1_life1
- Id scheme :
    - 1xxx : cage
    - 2xxx : powers
    - 3xxx : boss
    - 4xxx : life status
    - 5xxx : magician
    - 6xxx : special items (magic seed, super helicopter)
    - 7xxx : Level unlock
- Fields :
    - id : to identify the location in the game
    - name : to show the name of the location
    - address : The game's memory address to find the check
    - size : the number of bytes to read
    - mask : If the check is in a bitfield it needs a mask
    - world_id : The world's id where the location is
    - level_id : The level's id where the location is
    - region : the region where the item can be found
    - rule : the access rule for the location
    - classification : used for placement logic in game

```python
ppw_s1_life1 = LocationData(
    4001,
    "Pink Plant Wood Screen 1 life 1",
    0x1F9AC8,
    1,
    0x80,
    1,
    1,
    Region.ppw_s1,
    None,
    Classification.DEFAULT
)
```

### Locations init

- id : is to be choosen when implementing
- name : precised earlier
- address : can be found in [game_info_1.0.md](game_info_1.0.md)
- size : can be found in [game_info_1.0.md](game_info_1.0.md)
- mask : can be found in [game_info_1.0.md](game_info_1.0.md)
- world_id : can be found in [memory_map.md](memory_map.md)
- level_id : can be found in [memory_map.md](memory_map.md)
- rule : can be found in [game_info_1.0.md](game_info_1.0.md)

For classification :
- Cage : LocationProgressType.DEFAULT
- Powers : LocationProgressType.PRIORITY
- boss : LocationProgressType.PRIORITY
- Life status : LocationProgressType.DEFAULT
- magician : LocationProgressType.DEFAULT
- Special items : LocationProgressType.DEFAULT
- Level Unlock : LocationProgressType.DEFAULT

## Region

### Namming convention

- region name : ``"LevelName Screen"``
- variable name :
    - snakecase
    - format : first letter of each word in level name + s + number of the screen
    - i.e : 
        - region name : Pink Plant Wood Screen 1 -> ``"Pink Plant Wood Screen 1"``
        - variable name :Pink Plant Wood Screen 1 -> ppw_s1

### Regions list

- Pink Plant Woods Screen 1
- Pink Plant Woods Screen 2
- Pink Plant Woods Betilla
- Pink Plant Woods Screen 3
- Anguish Lagoon Screen 1
- Anguish Lagoon Screen 2 (boss)
- Anguish Lagoon Screen 3
- Anguish Lagoon Betilla
- The Swamps of Forgetfulness Screen 1
- The Swamps of Forgetfulness Screen 2
- The Swamps of Forgetfulness Screen 3
- Moskito's Nest Screen 1
- Moskito's Nest Screen 2
- Moskito's Nest Screen 4
- Moskito's Nest Screen 5 (boss)
- Moskito's Nest Betilla
- Bongo Hills Screen 1
- Bongo Hills Screen 2
- Bongo Hills Screen 3
- Bongo Hills Screen 4
- Bongo Hills Screen 5
- Bongo Hills Screen 6
- Allegro Presto Screen 1
- Allegro Presto Screen 2
- Allegro Presto Screen 3
- Allegro Presto Betilla
- Bongo Heights Screen 1
- Bongo Heights Screen 2
- Mr.Sax's Hullaballo Screen 1
- Mr.Sax's Hullaballo Screen 2
- Mr.Sax's Hullaballo Screen 3 (boss)
- Twilight Gulch Screen 1
- Twilight Gulch Screen 2
- The Hard Rocks Screen 1
- The Hard Rocks Screen 2
- The Hard Rocks Screen 3
- Mr.Stone's Peaks Screen 1
- Mr.Stone's Peaks Screen 2
- Mr.Stone's Peaks Screen 3
- Mr.Stone's Peaks Screen 4
- Mr.Stone's Peaks Screen 5 (boss)
- Mr.Stone's Peaks Betilla
- Eraser Plains Screen 1
- Eraser Plains Screen 2
- Eraser Plains Screen 3
- Eraser Plains Screen 4 (boss)
- Pencil Pentathlon Screen 1
- Pencil Pentathlon Screen 2
- Pencil Pentathlon Screen 3
- Space Mama's Crater Screen 1
- Space Mama's CraterScreen 2
- Space Mama's Crater Screen 3
- Space Mama's Crater Screen 4 (boss)
- Crystal Palace Screen 1
- Crystal Palace Screen 2
- Eat At Joe's Screen 1
- Eat At Joe's Screen 2
- Eat At Joe's Screen 3
- Eat At Joe's Screen 4
- Eat At Joe's Screen 5
- Mr.Skops' Stalactites Screen 1
- Mr.Skops' Stalactites Screen 2 (boss part 1)
- Mr.Skops' Stalactites Screen 3 (boss part 2)
- Mr.Dark's Dare Screen 1
- Mr.Dark's Dare Screen 2
- Mr.Dark's Dare Screen 3
- Mr.Dark's Dare Screen 4 (boss)

## Entrances

format :
- entrance : rule

### Level entrances from worldmap:
worldmap_to_ppw_s1 :
- options.open_world_disabled : none
- options.open_world_enabled : none

### Back to worldmap from levels
ppw_s1_to_worldmap : None

### Levels connections

pink plant wood :
- ppw_s1_to_ppw_s2 : none 
- ppw_s2_to_ppw_betilla : none
- ppw_betilla_to_ppw_s3 : has_fist or has_hang
- ppw_s3_to_worldmap :
    - option.difficulty_normal : has_fist
    - option.difficulty_hard : none

## Options

| Option name | choice or choice configuration | effect |
|:---|:---:|:--:|
| Number of starting life | Range :<br>range_start = 0<br>range_end = 99<br>default = 3 | Change the base number of life |
| Number of continue | Range :<br>range_start = 0<br>range_end = 99<br>default = 3 | Change the base number of continue available when you loose all your lives |
| Number of tings to get a new life | Range :<br>range_start = 50<br>range_end = 100<br>default = 100 | The number of tings to get in order to obtain a new life |
| Difficulty | Options :<br>- Normal<br>- Hard | - Normal : Casual playthrough for progression, don't require damage boos, speedrun tricks or other tricky moves to get the checks<br>- Hard : progression and checks may require speedrun tricks, damage boost and other tricky moves |
| Goal | Options :<br>- cages<br>- Great protoon pieces<br>Boss Rush | - Defeat Mr.Dark : Defeat Mr.Dark to save the Rayman's world ! You can choose how many cages needed to unlock Mr.Dark's Dare.<br>- Great Protoon pieces : The Great Protoon has split into multiple pieces, find the pieces to complete the run, or additionally, find them all and then beat Mr.Dark<br>- Boss Rush : Find Mr.Dark's generals and defeat them, then beat Mr.Dark |
| Number of cages required | Range : <br>range_start = 25 <br> range_end = 102<br>default = 102 |Number of cages required to unlock Mr.Dark's Dare |
| Number of great protoon piece required | Range : <br>range_start = tdb <br>range_end = tdb<br>default = tdb |Number of great protoon pieces required to unlock Mr.Dark's Dare |
| Include life status | Toggle :<br>True<br>False | Life status count as checks |
| Include magician challenges | Toggle :<br>True<br>False | Magician challenges count as checks |
| Shuffle objects position inside levels | Toggle :<br>True<br>False | Shuffle ennemies, life status, cages, and tings position in a level |
| Open world | Toggle :<br>True<br>False | All levels are unlocked (except Mr.Dark's Dare) from the beginning of the game |
| Randomnize level | Options :<br>- levels<br>- sub-level inside levels<br>- All sub-levels | - level : randomnize levels between each others<br>- sub-level inside levels : shuffle sub-levels inside a level<br>- All sub-levels : Randomnize every sub-levels between levels |
| Trap fill percentage | Range : <br>range_start = 0 <br> range_end = 100<br>default = 0 | The percentage of filler items to replace by traps |
| Reversed Controls weight | Options :<br>- None<br>- Low<br>- Medium<br>- High | the likelyhood of receiving a trap wich reverses controls |
| Elf weight | Options :<br>- None<br>- Low<br>- Medium<br>- High | the likelyhood of receiving a trap wich shrinks Rayman |
| Forced Run weight | Options :<br>- None<br>- Low<br>- Medium<br>- High | the likelyhood of receiving a trap wich forces Rayman to run |

## Rules

Powers :
- has_fist
- has_hang
- has_grappling_fist
- has_helicopter
- has_run

Special items :
- has_magic_seed
- has_super_helicopter
- has_light_fist

Levels :
- can_access_pink_plant_wood
- can_access_anguish_lagoon
- can_access_swalo_of_forgetfulness
- can_acess_moskito_nest
- can_access_bongo_hills
- can_access_allegro_presto
- can_access_gong_height
- can_access_sax_hullaballo
- can_access_twilight_gulch
- can_access_hard_rocks
- can_access_stone_peaks
- can_access_eraser_plains
- can_access_pencil_pentathlon
- can_access_space_mama_crater
- can_access_crystal_palace
- can_access_eat_at_joe
- can_access_skop_stalactites
- can_access_dark_dare
