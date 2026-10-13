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

if world id = 1 and level_id = 9, remove the seed's power
if item found: let the game handle it

#### Super helicopter:

if world id = 3 and level_id = 6, remove the Super Helicopter's power
if item found: let the game handle it

#### light fist:

if world id = 5 and level_id = 4, remove the Light Fist's power
if item found: let the game handle it

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
