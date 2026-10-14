# Modelling

This document aims to set the model for items, locations, regions, entrances, options 
and rules of this world

## Item
### Item Data
- Namming convention : 
    - item name : Use the name written in the [game_info_1.0.md](game_info_1.0.md) file
    - variable name : Use the name written in the [game_info_1.0.md](game_info_1.0.md) file but in snakecase
- Id scheme : in decimal
    - 1xxx : Powers
    - 2xxx : Special items
    - 3xxx : Cages
    - 4xxx : Protoon pieces
    - 5xxx : Level Unlocks
    - 6xxx : Power (HP : simple, double and big)
    - 7xxx : Fists (speed and gold)
    - 8xxx : Life status and life
    - 9xxx : 5 tings
    - 10xxx : Traps
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

For every level unlock

- open world enabled : 
    - count : 0
- open world disabled : 
    - count : 1
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
- life in twilight gulch screen 2 : LocationProgressType.DEFAULT

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

- worldmap
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
- Moskito's Nest Screen 3
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
- Allegro Presto Screen 4
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
- Victory

## Entrances

format :
- entrance : rule

### Level entrances from worldmap:
worldmap_to_ppw_s1 :
- options.open_world_disabled : none
- options.open_world_enabled : none

worldmap_to_al_s1 :
- options.open_world_disabled : can_access_anguish_lagoon
- options.open_world_enabled : none

worldmmap_to_sf_s1 :
- options.open_world_disabled : can_access_swamps_of_forgetfulness
- options.open_world_enabled : none

worldmap_to_mn_s1 :
- options.open_world_disabled : can_access_moskito_nest
- options.open_wolrd_enabled : none

worldmap_to_bhills_s1 :
- options.open_world_disabled : can_access_bongo_hills
- options.open_world_enabled : none

worldmap_to_ap_s1 :
- options.open_world_disabled : can_access_allegro_presto
- options.open_world_enabled : none

worldmap_to_bheights_s1 :
- options.open_world_disabled : can_access_bongo_heights
- options.open_world_enabled : none

worldmap_to_sh_s1 :
- options.open_world_disabled : can_access_sax_hullaballo
- options.open_world_enabled : none

worldmap_to_tg_s1 :
- options.open_world_disabled : can_access_twilight gulch
- options.open_world_enabled : none

worldmap_to_thr_s1 :
- options.open_world_disabled : can_access_hard_rocks
- options.open_world_enabled : none

worldmap_to_sp_s1 :
- options.open_world_disabled : can_access_stone_peaks
- options.open_world_enabled : none

worlmap_to_ep_s1 : 
- options.open_world_disabled : can_access_eraser_plains
- options.open_world_enabled : none

worldmap_to_pp_s1 :
- options.open_world_disabled : can_access_pencil_pentathlon
- options.open_world_enabled : none

worldmap_to_spc_s1 :
- options.open_world_disabled : can_access_space_mama_crater
- options.open_world_enabled : none

worldmap_to_cp_s1 :
- options.open_world_disabled : can_access_crystal_palace
- options.open_world_enabled : none

worldmap_to_eaj_s1 :
- options.open_world_disabled : can_access_eat_at_joe
- options.open_world_enabled : none

worldmap_to_mss_s1 :
- options.open_world_disabled : can_access_skop_stalactites
- options.open_world_enabled : none

worldmap_to_dd_s1 :
- options.open_world_disabled : can_access_dark_dare
- options.open_world_enabled : none

### Back to worldmap from levels

- ppw_s1_to_worldmap : none
- al_s1_to_worldmap : none
- sf_s1_to_worldmap : none
- mn_s1_to_worldmap : none
- bhills_s1_to_worldmap : none
- ap_s1_to_worldmap : none
- bheights_s1_to_worldmap : none
- sh_s1_to_worldmap : none
- tg_s1_to_worldmap : none
- thr_s1_to_worldmap : none
- sp_s1_to_worldmap : none
- ep_s1_to_worldmap : none
- pp_s1_to_worldmap : none
- spc_s1_to_worldmap : none
- cp_s1_to_worldmap : none
- eaj_s1_to_worlmap : none

### Levels connections

pink plant wood :
- ppw_s1_to_ppw_s2 : none 
- ppw_s2_to_ppw_betilla : none
- ppw_betilla_to_ppw_s3 : has_fist or has_hang
- ppw_s3_to_worldmap :
    - options.difficulty_normal : has_fist
    - options.difficulty_hard : none

Anguish Lagoon :
- al_s1_to_al_s2 : has_fist
- al_s2_to_al_s3 : has_fist
- al_s3_to_al_betilla : none
- al_betilla_to_worldmap : has_hang

The Swamps of Forgetfullness :
- sf_s1_to_sf_s2 : 
    - options.difficulty_normal : has_magic_seed and has_fist
    - options.difficulty_hard : has_magic_seed
- sf_s2_to_sf_s3 :
    - options.difficulty_normal : has_fist
    - options.difficulty_hard : none
- sf_s3_to_worlmap : has_fist

Moskito's Nest :
- mn_s1_to_mn_s2 : has_fist
- mn_s2_to_mn_s3 : none
- mn_s3_to_mn_s4 : none
- mn_s4_to_mn_s5 : none
- mn_s5_to_mn_betilla : has_fist
- mn_betilla_to_worldmap : has_fist and has_hang and has_grappling_fist

Bongo Hills :
- bhills_s1_to_bhills_s2 : has_hang
- bhills_s2_to_bhills_s3 : 
    - options.difficulty_normal : has_fist and has_hang
    - options.difficulty_hard : has_hang
- bhills_s3_to_bhills_s4 : 
    - options.difficulty_normal : has_hang
    - options.difficulty_hard : none
- bhills_s4_to_bhills_s5 :
    - options.difficulty_normal : has_fist and has_hang
    - options.difficulty_hard : none
- bhills_s5_to_bhills_s6 :
    - options.difficulty_normal : has_fist
    - options.difficulty_hard : none
- bhills_s6_to_worldmap : has_hang

Allegro Presto :
- ap_s1_to_ap_s2 : none
- ap_s2_to_ap_s3 : 
    - options.difficulty_normal : has_fist
    - options.difficulty_hard : none
- ap_s3_to_ap_s4 :
    - options.difficulty_normal : has_hang
    - options.difficulty_hard : has_fist
- ap_s4_to_ap_betilla : none
- ap_betilla_to_worldmap : has_helicopter or (has_hang and has_run)

Bongo Heigths :
- bhills_s1_to_bheights_s2 : has_hang or has_run or has_helicopter
- bhills_s2_to_worldmap :
    - options.difficulty_normal : has_helicopter or has_run
    - options.difficulty_hard : has_helicopter or has_run

Mr Sax's Hullaballo :
- sh_s1_to_sh_s2 : 
    - options.difficulty.normal : has_fist and (has_run or has_helicoper)
    - options.difficulty.hard : has_fist and has_hang

Mr Sax's Hullaballo :
- sh_s1_to_sh_s2 : 
    - options.difficulty_normal : has_fist and has_hang and (has_helicoper or has_run)
    - options.difficulty_hard : has_fist
- sh_s2_to_sh_s3 : has_fist
- sh_s3_to_worldmap : has_fist

Twilight_gulch :
- tg_s1_to_tg_s2 : has_fist and has_grappling_fist and has_helicopter
- tg_s1_to_tg_worlmap : 
    - options.difficulty_normal : has_fist and has_hang and has_helicopter and has_grappling_fist
    - options.difficulty_hard : has_fist and has_grappling_fist

The Hard Rocks :
- thr_s1_to_thr_s2 : 
    - options.difficulty_normal : has_fist and has_helicopter
    - options.difficulty_hard : has_fist
- thr_s2_to_thr_s3 :
    - options.difficulty_normal : has_fist and has_hang
    - options.difficulty_hard : has_hang
- thr_s3_to_worldmap : has_hang

Mr Stone's Peaks :
- sp_s1_to_sp_s2 : has_fist and has_super_helicopter
- sp_s2_to_sp_s3 : has_super_helicopter
- sp_s3_to_sp_s4 : has_hang and (has_helicoper or has_run)
- sp_s4_to_sp_s5 : 
    - options.difficulty_normal : has_fist and and has_hang
    - options.difficulty_hard : has_hang
- sp_s4_to_sp_betilla : has_fist
- sp_betilla_to_worldmap : has_helicopter and has_run

Eraser Plains :
- ep_s1_to_ep_s2 :
    - options.difficulty_normal : has_fist and has_helicopter
    - options.difficulty_hard : has_fist
- ep_s2_to_ep_s3 : has_fist and has_grappling_fist and has_hang 
- ep_s3_to_ep_s4 : has_fist and has_hang and has_grappling_fist and has_helicopter and has_run
- ep_s4_to_worldmap : has_fist

Pencil Pentathlon :
- pp_s1_to_pp_s2 : 
    - options.difficulty_normal : has_fist and has_hang and has_grappling_fist and has_helicopter and has_run
    - options.difficulty_hard : has_fist and has_grappling_fist and has_helicopter and has_run
- pp_s2_to_pp_s3 : 
    - options.difficulty_normal : has_fist and has_super_helicopter
    - options.difficulty_hard : has_super_helicopter
- pp_s3_to_worldmap :
    - options.difficulty_normal : has_fist and has_hang and has_grappling_fist and has_helicopter
    - options.difficulty_hard : has_hang and has_helicopter

Space Mama's Crater :
- spc_s1_to_spc_s2 : has_fist and has_hang and has_grappling_fist and has_helicopter
- spc_s2_to_spc_s3 :
    - options.difficulty_normal : has_fist and has_hang and has_grappling_fist
    - options.difficulty_hard : has_fist and has_grappling_fist
- spc_s3_to_spc_s4 :
    - options.difficulty_normal : has_fist and has_hang and has_helicopter
    - options.difficulty_hard : has_fist and has_hang
- spc_s4_to_worldmap :
    - options.difficulty_normal : has_fist and has_run
    - options.difficulty_hard : has_fist

Crystal Palace :
- cp_s1_to_cp_s2 : 
    - options.difficulty_normal : has_fist and has_grappling_fist and has_helicoper
    - options.difficulty_hard : has_fist and has_grappling_fist
- cp_s2_to_worldmap :
    - options.difficulty_normal : has_fist and has_hang and has_helicopter and has_grappling_fist
    - options.difficulty_hard : has_fist and has_hang and has_grappling_fist

Eat at Joe's :
- eaj_s1_to_eaj_s2 :
    - options.difficulty_normal : has_fist and has_light_fist
    - options.difficulty_hard : none
- eaj_s2_to_eaj_s3 :
    - options.difficulty_normal : has_fist and has_grappling_fist and has_helicopter
    - options.difficulty_hard : has_fist and has_grappling_fist
- eaj_s3_to_eaj_s4 :
    - options.difficulty_normal : has_fist and has_hang and has_grappling_fist
    - options.difficulty_hard : has_fist and has_grappling_fist
- eaj_s4_to_eaj_s5 : has_fist and has_grappling_fist
- eaj_s5_to_worlmap : has_fist and has_grappling_fist and has_helicopter

Mr Skops' Stalactites :
- mss_s1_to_mss_s2 :
    - options.difficulty_normal : has_fist and has_grappling_fist and has_helcopter
    - options.difficulty_hard : has_fist and has_grappling_fist
- mss_s2_to_mss_s3 : has_fist and has_hang and has_grappling_fist and has_helicopter and has_run
- mss_s3_to_worlmap : has_fist

Mr Dark's Dare :
- dd_s1_to_dd_s2 : none
- dd_s2_to_dd_s3 : has_fist and has_hang and has_grappling_fist and has_helicopter
- dd_s3_to_dd_s4 : 
    - options.difficulty_normal : has_fist and has_hang
    - options.difficulty_hard : has_hang
- dd_s4_to_victory : has_fist and has_run

## Options

| Option name | choice or choice configuration | effect |
|:---|:---:|:--:|
| Number of starting life | Range :<br>range_start = 0<br>range_end = 99<br>default = 3 | Change the base number of life |
| Number of continue | Range :<br>range_start = 0<br>range_end = 99<br>default = 3 | Change the base number of continue available when you loose all your lives |
| Number of tings to get a new life | Range :<br>range_start = 50<br>range_end = 100<br>default = 100 | The number of tings to get in order to obtain a new life |
| Difficulty | Options :<br>- Normal<br>- Hard | - Normal : Casual playthrough for progression, don't require damage boos, speedrun tricks or other tricky moves to get the checks<br>- Hard : progression and checks may require speedrun tricks, damage boost and other tricky moves |
| Goal | Options :<br>- cages<br>- Great protoon pieces<br>Boss Rush | - Defeat Mr.Dark : Defeat Mr.Dark to save the Rayman's world ! You can choose how many cages needed to unlock Mr.Dark's Dare.<br>- Great Protoon pieces : The Great Protoon has split into multiple pieces, find the pieces to complete the run, or additionally, find them all and then beat Mr.Dark<br>- Boss Rush : Find Mr.Dark's generals and defeat them, then beat Mr.Dark |
| Shuffle objects position inside levels | Toggle :<br>True<br>False | Shuffle ennemies, life status, cages, and tings position in a level |
| Open world | Toggle :<br>True<br>False | All levels are unlocked (except Mr.Dark's Dare) from the beginning of the game |
| Randomnize level | Options :<br>- levels<br>- sub-level inside levels<br>- All sub-levels | - level : randomnize levels between each others<br>- sub-level inside levels : shuffle sub-levels inside a level<br>- All sub-levels : Randomnize every sub-levels between levels |
| Trap fill percentage | Range : <br>range_start = 0 <br> range_end = 100<br>default = 0 | The percentage of filler items to replace by traps |
| Reversed Controls weight | Options :<br>- None<br>- Low<br>- Medium<br>- High | the likelyhood of receiving a trap wich reverses controls |
| Elf weight | Options :<br>- None<br>- Low<br>- Medium<br>- High | the likelyhood of receiving a trap wich shrinks Rayman |
| Forced Run weight | Options :<br>- None<br>- Low<br>- Medium<br>- High | the likelyhood of receiving a trap wich forces Rayman to run |
| Magic Seed as item | Toggle :<br>True<br>False | You need to find the magic seed in order to use it in The Swamps of Forgetfulness |
| Level Unlock as locations and items | Toggle :<br>True<br>False | When you finish a level it counts as a location obtained. Unlocking access to a level require the associated item |
| Super Helicopter Potion as item | Toggle :<br>True<br>False | You need to find the Super Helicopter Potion in order to use it in Mr Stone's Peaks |
| Firefly as item | Toggle :<br>True<br>False | You need to find the Firefly to use it in Eat at Joe's |
| Number of cages required | Range : <br>range_start = 25 <br> range_end = 102<br>default = 102 |Number of cages required to unlock Mr.Dark's Dare |
| Number of great protoon piece required | Range : <br>range_start = tdb <br>range_end = tdb<br>default = tdb | Number of great protoon pieces required to unlock Mr.Dark's Dare |
| Include life status | Toggle :<br>True<br>False | Life status count as checks |
| Include magician challenges | Toggle :<br>True<br>False | Magician challenges count as checks |
| Location to exlcude | | Allow the player to exclude locations from the game |

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
- can_access_swamps_of_forgetfulness
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
