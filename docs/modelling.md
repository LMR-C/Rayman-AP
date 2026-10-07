# Modelling

This document aims to set the model for items, locations, regions, entrances, options 
and rules of this world

## Item Data
- Namming convention : 
    - item name : Use the name written in the [game_info_1.0.MD](game_info_1.0.md) file
    - variable name : Use the name written in the [game_info_1.0.MD](game_info_1.0.md) file but in snakecase
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

## Locations Data
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
    - 4xxx : life
    - 5xxx : magician
    - 6xxx : special items (magic seed, super helicopter)
- Fields :
    - Id : to identify the location in the game
    - Name : to show the name of the location
    - Address : The game's memory address to find the check
    - size : the number of bytes to read
    - Masks : If the check is in a bitfield it needs a mask
    - world_id : The world's id where the location is
    - level_id : The level's id where the location is
    - region : the region where the item can be found
    - rule : the access rule for the location
    - Classification : used for placement logic in game

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
- The Dream Forest
    - Pink Plant Woods
        - Screen 1
        - Screen 2
        - Betilla
        - Screen 3
    - Anguish Lagoon
        - Screen 1
        - Screen 2 (boss)
        - Screen 3
        - Betilla
    - The Swamps of Forgetfulness
        - Screen 1
        - Screen 2
        - Screen 3
    - Moskito's Nest
        - Screen 1
        - Screen 2
        - Screen 4
        - Screen 5 (boss)
        - Betilla
- Band Land
    - Bongo Hills
        - Screen 1
        - Screen 2
        - Screen 3
        - Screen 4
        - Screen 5
        - Screen 6
    - Allegro Presto
        - Screen 1
        - Screen 2
        - Screen 3
        - Betilla
    - Bongo Heights
        - Screen 1
        - Screen 2
    - Mr.Sax's Hullaballo
        - Screen 1
        - Screen 3 (boss)
- Blue Montains
    - Twilight Gulch
        - Screen 1
        - Screen 2
    - The Hard Rocks
        - Screen 1
        - Screen 2
        - Screen 3
    - Mr.Stone's Peaks
        - Screen 1
        - Screen 2
        - Screen 3
        - Screen 4
        - Screen 5 (boss)
        - Betilla
- Picture City
    - Eraser Plains
        - Screen 1
        - Screen 2
        - Screen 3
        - Screen 4 (boss)
    - Pencil Pentathlon
        - Screen 1
        - Screen 2
        - Screen 3
    - Space Mama's Crater
        - Screen 1
        - Screen 2
        - Screen 3
        - Screen 4 (boss)
- The Cave of Skops
    - Crystal Palace
        - Screen 1
        - Screen 2
    - Eat At Joe's
        - Screen 1
        - Screen 2
        - Screen 3
        - Screen 4
        - Screen 5
    - Mr.Skops' Stalactites
        - Screen 1
        - Screen 2 (boss part 1)
        - Screen 3 (boss part 2)
- Candy Chateau
    - Mr.Dark's Dare
        - Screen 2
        - Screen 3
        - Screen 4 (boss)

## Entrances

| Entrance | requirements |
|:---|:---:|


## Options

| Option name | choice or choice configuration | effect |
|:---|:---:|:--:|
| Number of starting life | Range :<br>range_start = 0<br>range_end = 99<br>default = 3 | Change the base number of life |
| Number of continue | Range :<br>range_start = 0<br>range_end = 99<br>default = 3 | Change the base number of continue available when you loose all your lives |
| Number of tings to get a new life | Range :<br>range_start = 50<br>range_end = 100<br>default = 100 | The number of tings to get in order to obtain a new life |
| Goal | Options :<br>- cages<br>-Great protoon pieces<br>Boss Rush | - Defeat Mr.Dark : Defeat Mr.Dark to save the Rayman's world ! You can choose how many cages needed to unlock Mr.Dark's Dare.<br>- Great Protoon pieces : The Great Protoon has split into multiple pieces, find the pieces to complete the run, or additionally, find them all and then beat Mr.Dark<br>- Boss Rush : Find Mr.Dark's generals and defeat them, then beat Mr.Dark |
| Number of cages required | Range : <br>range_start = 25 <br> range_end = 102<br>default = 102 |Number of cages required to unlock Mr.Dark's Dare |
| Number of great protoon piece required | Range : <br>range_start = tdb <br>range_end = tdb<br>default = tdb |Number of great protoon pieces required to unlock Mr.Dark's Dare |
| Shuffle objects position inside levels | Toggle :<br>True<br>False | Shuffle ennemies, life status, cages, and tings position in a level |
| Randomnize level | Options :<br>- levels<br>- sub-level inside levels<br>- All sub-levels | - level : randomnize levels between each others<br>- sub-level inside levels : shuffle sub-levels inside a level<br>- All sub-levels : Randomnize every sub-levels between levels |

## Rules
