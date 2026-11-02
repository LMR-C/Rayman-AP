# Rayman Randomizer Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- BizHawk from: [TASVideos](https://tasvideos.org/BizHawk)
- Your legally obtained Rayman ROM file (*.chd or bin + *.cue)
- Your legally obtained Playstation BIOS (*.bin)
- The Rayman APWorld

## Installation Procedures

1. Download and install [Archipelago](<https://github.com/ArchipelagoMW/Archipelago/releases/latest>). **The installer 
file is located in the assets section at the bottom of the version information.**
2. Open the Archipelago Launcher and search for the `Install APWorld` option then click `Open`. Then choose
the Rayman APWorld file
3. Download and install [BizHawk](https://tasvideos.org/BizHawk) and launch it
4. Go to `Config > Firmware...` and scroll down to `PlayStation` in the list of supported hardwares.
Double click on the row corresponding to the region of you bios and browse to your bios file. Finally click on `Scan`
in the menu bar.

## Create a config (.yaml) file

### What is a config file and why do I need one ?

YAML is the file format wich Archipelago uses in order to configure a player's world. It allows
you to dictate which game you will be playing as well as the options you would like for that game.

### Where do I get a config file ?

Open the Archipelago Launcher and search for the `Generate Template Options` option then click `Open`.
It should open the folder with yaml files for every supported games. If you had correcly install the Rayman APWorld
you should see the `Rayman.yaml` file.

### How to complete the YAML file ?

Copy the `Rayman.yaml` file and open it with the text editor of your choice. Then read the F.A.Q
at the beginning of the file and choose your options for your seed.

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
validator page: [YAML Validation page](/check)

## Hosting a MultiWorld game

The recommended way to host a game is to use our hosting service. The process is relatively simple:

1. Collect config files from your players.
2. If you play with APWolrd (unoficially supported ones) make sure to install all APWorld that you and your friends want to play
3. In the launcher search for the `Generate Template Options` and click on `Open`. This should open you the `Template` folder.
  Go back in the `Players` right above the `Template` one and copy all you config files from your players.
4. In the launcher search for the `Generate` option and click on `Open`. This should open a terminal and generate the seed.
   If an error occured make sure you yaml is valid and ensure you have installed all used APWorld.
5. When the seed is generated, you can get it in the `Ouputs` folder in the Archipelago folders as a zip file
6. Then go to the [Host Game Page](https://archipelago.gg/uploads) and upload your generated zip file.
   You sould be redirected to a room page that hosts your seed.
7. Note that a link to a MultiWorld Tracker is at the top of the room page. The tracker shows the progress of all
   players in the game. Any observers may also be given the link to this page.
8. Once all players have joined, you may begin playing.

## Joining a MultiWorld Game

### Launch the game

1. Launch BizHawk and open the game `File > Open ROM`
2. In game create a new save file by using memory card save. If you don't use memory card,
  You should use save states to save you progress between sessions.
3. You should be at the options page in game. Now follow the next steps before playing.

### Connect to the client

1. In the Archipelago launcher search for `Bizhawk Client` and open it.
2. In BizHawk go to `Tools > Lua Console`
3. In the opened Lua Console fo to `Scripts > Open Script` and select the BizHawk connector scripts.
  It should be located in your Archipelago data Folders in `Archipelago Data Folder/data/lua/connector_bizhawk_generic.lua`
4. The BizHawk client should display `Running handler for Rayman`


### Connect to the Archipelago Server

1. From you Archipelago room page (the one you accessed during the `Hosting a MultiWorld game` section)
  copy the command `/connect archipelago.gg:xxxx` and enter it in the client
2. Your client is connected to the Archipelago Server and you are ready to play !
