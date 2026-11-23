# Design client

## Blocking default behavior

### Powers (fist, hang, grappling fist, helicopter, run): 
- if location obtained before item : The client detect the location, send it to the server
and retrieve (cancel the location) it from the game
- if item obtained before the location :
    - if power (item) already obtained :
    In the screen preceding betilla when rayman is really close to the end sign. Retrieve the power
    in order to be able to enter the betilla screen. Then once the location obtained, give back the
    power once the region has changed
    - if the location has already been obtained : give the power once Rayman is closed to the end sign
    in order to skip the betilla screen, once the region has changed, retrieve the power

#### Preceding screen condition
- coord_x : ``0x1F9A10``
- coord_y : ``0x1F9A28``

Pink Plant Wood screen 2 : if betilla hasn't been encountered then retrieve the fist
  - 0xC51 <= x <= 0xC63
  - 0x117 <= y <= 0x13A

Anguish Lagoon screen 3 : if betilla hasn't been encountered then retrieve hang
  - 0x2518 <= x <= 0x2548
  - 0x2D <= y <= 0x45

Moskito's Nest screen 5 : if betilla hasn't been encountered then retrieve grappling_fist
during the moskito boss fight

Allegro Presto screen 4 : if betilla hasn't been encountered then retrieve helicopter
  - 0x18A9 <= x <= 0x18CD
  - 0x470 <= y <= 0x48A

Mr Stone's Peaks screen 5 : if betilla hasn't been encountered then retrieve run
during the Mr Stone boss fight

### cage

item: adds +1 to the total cage counter
location: once the location is detected, report it to the server, then decrement the global cage counter and the local counter

### life status
item: adds +1 to the life counter
location: detect the location, send it to the server, then decrement the life counter

### Magician
item: adds one life
location: send the location to the server, then decrement the life counter

### Special item

#### magic seed:

if world id = 1 and level_id = 9, remove the seed's power and modify the text  
if item found: let the game handle it

to remove the seed : set ``0xAF63C`` to 0xFF (while Rayman is in the screen)
and replace the text : 
- ``0x12BAD1`` : Tarayzan gives Rayman a magic seed
- ``0x12BAF9`` : Press the o button to use the seed

to modify : 
- ``0x12BAD1`` : Tarayzan lost the magic seed : ``74 61 72 61 79 71 61 6E 20 6C 6F 73 74 20 74 68 65 20 6D 61 67 69 63 20 73 65 65 64 2F 00``
- ``0x12BAF9`` : You need to find it : ``79 6F 75 20 6E 65 65 64 20 74 34 20 66 69 6E 64 20 69 74 00``

to restore :
- Restore the 35 bytes of ``0x12BAD1``
- Restore the 36 bytes of ``0x12BAF9``

#### Super helicopter:

if world id = 3 and level_id = 6, remove the Super Helicopter potion and modify the text  
if item found: let the game handle it

to remove the potion : set ``0xA6769`` to 0x00
and replace the text :
- ``0x12BB21`` : The musician gives rayman
- ``0x12BB3D`` : a super helicopter power

to modify :
- ``0x12BB21`` : "the potion has been lost" : ``74 68 65 20 70 6F 74 69 6F 6E 20 68 61 73 20 62 65 65 6E 20 6C 6F 73 74 00``
- ``0x12BB3D`` : "you must find it" : ``79 6F 75 20 6D 75 73 74 20 66 6E 63 64 20 69 74 00``

to restore :
- 26 bytes of ``0x12BB21``
- 25 bytes of ``0x12BB3D``

#### light fist:

if world id = 5 and level_id = 4, remove the Light Fist's power (read [game_info_1.0md](game_info_1.0.md)) and replace text  
if item found: let the game handle it

replace the text :
- ``0x12BBBD`` : Joe offers Rayman a firefly
- ``0x12BBDD`` : to light up the dark

to modify :
- ``0x12BBBD`` : "joe lost the firefly" : ``6A 6F 65 20 6C 6F 73 74 20 74 68 65 20 66 69 72 65 66 6C 79 00``
- ``0x12BBDD`` : "you must find it" : ``79 6F 75 20 6D 75 73 74 20 66 69 6E 64 20 69 74 00``

to restore :
- 29 bytes of ``0x12BBBD``
- 21 bytes of ``0x12BBDD``

### Level Unlock

if open world: no items and no level unlock locations
if not open world:
once a level is completed, if the memory location indicates a 4 (is_unlocked) for the next level, send the location to the server and reset it to 0


## Game, Client and Server Synchronization

### Client and Game Item Sync

Receive items from the server.
Store whether items have been given in a list in RAM.

Ram list layout :
``0x1F9C52`` : 271 free bytes : 2168 items

other candidates (keep it just in case)
``0x1F9B20`` : 8 bytes : 64 items
``0x1F9B34`` : 22 bytes : 174 items
``0x1F9B50`` : 55 bytes : 440 items
``0x1F9B94`` : 51 bytes : 408 items
``0x1F9BCA`` : 35 bytes : 280 items
``0x1F9C11`` : 29 bytes : 232 items
``0x1F9C30`` : 32 bytes : 256 items
``0x1F9D6C`` : 5 bytes : 40 items
``0x1F9D73`` : 28 bytes : 224 items
``0x1F9D91`` : 9 bytes : 72 items
``0x1F9D9C`` : 12 bytes : 96 items
``0x1F9DA9`` : 6 bytes : 48 items
``0x1F9D81`` : 24 bytes : 192 items

Item handling:
Cases of desynchronization between the game and the client:
- Game over (no continues left):
  - If the player returns with a fresh game: give all items again.
  (if the levels are not managed by the client (not in item pool and location) the player will have to unlock the level to get back his progression)
  - If the player returns with a save file: Use the list in RAM to give only the missing items.
- Loading a save state that goes back in time:
  - Use the list in RAM to give only the missing items.
- Client disconnects from the game:
  - Use the list in RAM to give only the missing items.

### Client and Game Location Sync

When a location is obtained, the client records it and reports it to the server.
If the game becomes desynchronized, re-trigger the locations so they can be reported as completed in game.

#### Special case

Powers : keep a variable to record if the RayEvts address has been modify by the client.
It is important to not check a location if it hasn't been obtained by the player

## Level access

For later version of this world level order will be shuffle and screen may be randomnize.
In order to be sure that every screen is playable here is a liste of things to do :
- when in allegro presto screen 3 : retrieve the Mr Sax's encounter to be able to enter
screen 4
