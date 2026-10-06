# Modelling

This document aims to set the model for items, locations and regions of this world

## Items

- Namming convention : 
    - item name : Use the name written in the [game_info_1.0.MD](game_info_1.0.md) file
    - variable name : Use snakecase
- Id scheme : in decimal
    - 1xx : Important items
    - 2xx : Junk items
    - 3xx : Trap items
- Fields :
    - id : to identify the item in the game (must be unique)
    - name : to show the name of the item
    - address : The game's memory address to give the item
    - mask : If the item is stored in a bitfield it needs a mask
    - type : The type of the item :
        - Power
        - special objects (magic seed, super helicopter)
        - cage
        - junk
        - traps
    - classification : to qualify the item for placement logic

```python
fist_power = ItemData(
    101,
    "Fist Power",
    0x1f43d0,
    0x1,
    "Power"
    Classification.progression
)
```

## Locations
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
Fields :
    - Id : to identify the location in the game
    - Name : to show the name of the location
    - Address : The game's memory address to find the check
    - Masks : If the check is in a bitfield it needs a mask
    - Type : the type of item in game (for setup the pool) :
        - cage
        - power
        - boss
        - life
        - magician
        - special items
    - Classification : used for placement logic in game

```python
ppw_s1_life1 = LocationData(
    4001,
    "Pink Plant Wood Screen 1 life 1",
    0x1F9AC8,
    0x80,
    "life",
    Classification.DEFAULT
)
```

## Region

TBD
