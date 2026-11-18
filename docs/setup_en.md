# Rayman Randomizer Setup Guide

## Required Software

Before getting started, make sure you have the following:

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- BizHawk from: [TASVideos](https://tasvideos.org/BizHawk)
- Your legally obtained Rayman ROM file (*.chd or bin + *.cue)
- Your legally obtained Playstation BIOS (*.bin)

## Installation Procedures

1. Download and install [Archipelago](<https://github.com/ArchipelagoMW/Archipelago/releases/latest>). **The installer 
file is located in the assets section at the bottom of the version information.**
2.Download the [Rayman AP World]()
2. Open the Archipelago Launcher and search for the `Install APWorld` option then click `Open`. Then choose
the Rayman APWorld file
3. Download and install [BizHawk](https://tasvideos.org/BizHawk) and launch it
4. Go to `Config > Firmware...` and scroll down to `PlayStation` in the list of supported hardwares.
Double click on the row corresponding to the region of you bios and browse to your bios file. Finally click on `Scan`
in the menu bar.

## Create a config (.yaml) file

### What is a config file and why do I need one ?

Archipelago uses YAML files to configure each player's world.

These files allow you to specify which game you want to play and customize the options
available for that game.

### Where do I get a config file ?

Open the Archipelago Launcher, search for `Generate Template Options`, and click `Open`.

This will open a folder containing YAML templates for all supported games. If the Rayman
APWorld was installed correctly, you should find a `Rayman.yaml` file in this folder.

### How to complete the YAML file ?

Copy the `Rayman.yaml` file and open it with the text editor of your choice.
Then read the F.A.Q at the beginning of the file and choose the options according to your
preferences.

### Verifying your config file

If you want to make sure your YAML file is valid, you can use the
[YAML Validator](https://archipelago.gg/check).

## Hosting a MultiWorld game

The recommended way to host a game is through the Archipelago hosting service.

1. Collect a YAML configuration file from each player participating in the game.
2. If you or your friends are playing unofficially supported APWorlds, make sure all required APWorlds are installed before generating the game.
3. In the Archipelago Launcher, search for `Generate Template Options` and click `Open`. This will open the `Templates` folder.
Navigate to the `Players` folder, located one level above `Templates`, and copy all the players' YAML files into it.
4. In the launcher, search for `Generate` and click `Open`. A terminal will open and generate your seed.
If an error occurs, check that all YAML files are valid and that every required APWorld is installed.
5. Once generation is complete, you can find the generated seed as a ZIP file in Archipelago's `Output` folder.
6. Then go to the [Host Game Page](https://archipelago.gg/uploads) and upload your generated zip file.
   You sould be redirected to a room page that hosts your seed.
7. At the top of your room page, you will find a link to the MultiWorld Tracker.
It displays the progress of every player in the game. You can also share this link with anyone who wants to observe the game.
8. Once all players have joined the room, you're ready to start playing!

## Joining a MultiWorld Game

### Launch the game

1. Launch BizHawk and open your Rayman ROM using `File > Open ROM`.
2. Create a new in-game save file using the memory card.
   - If you are not using a memory card, make sure to use save states to preserve your progress between sessions.
3. Once you reach the in-game options screen, stop there and follow the next steps before starting your game.

### Connect to the client

1. Open the Archipelago Launcher and search for `BizHawk Client`.
2. In BizHawk, go to `Tools > Lua Console`.
3. In the Lua Console, go to `Scripts > Open Script` and select the BizHawk connector script.
The script should be located in your Archipelago data folder:
`Archipelago Data Folder/data/lua/connector_bizhawk_generic.lua`
4. The BizHawk client should display the following message: `Running handler for Rayman`
This means the connector has successfully detected Rayman.

### Connect to the Archipelago Server

1. Go to your Archipelago room page (the one you accessed during the [Hosting a MultiWorld Game](#hosting-a-multiworld-game) section).
2. Copy the connection command displayed on the page (for example, `/connect archipelago.gg:xxxx`) and paste it into the Archipelago client.
3. Once connected to the server, you're ready to play!
