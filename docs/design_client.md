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

Item handling:
Cases of desynchronization between the game and the client:
- Game over (no continues left):
  - If the player returns with a fresh game: give all items again.
  - If the player returns with a save file: force the player to start a fresh game, then give all items again.
- Loading a save state that goes back in time:
  - Use the list in RAM to give only the missing items.
- Client disconnects from the game:
  - Use the list in RAM to give only the missing items.

### Client and Game Location Sync

When a location is obtained, the client records it and reports it to the server.
If the game becomes desynchronized, re-trigger the locations so they can be reported as completed.
