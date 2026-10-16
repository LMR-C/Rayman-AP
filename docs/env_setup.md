# **WIP** Rayman PS1 APWorld: dev setup & running the game with BizHawk 


Archipelago 0.6.7 runs from source, our world sits in its own repo inside `worlds/rayman`, and BizHawk runs the game.

```
~/dev/Archipelago/        official Archipelago clone, tag 0.6.7
└── worlds/rayman/        our world repo (own git, ignored by the parent)
~/emu/BizHawk-2.10/       emulator
```

## You need

- Linux on x86_64 (BizHawk does not run on ARM).
- Your own Rayman disc image, US version **SLUS-00005**, as `.chd`.
- A PS1 BIOS from your own console. BizHawk only accepts **v3.0 A** (SCPH-5501, 5503 or 7003) for US games.
- Access to our world repository on GitHub.

## 1. Dependencies

All available through `apt` or `pacman`:

- [git](https://git-scm.com/)
- [Python](https://www.python.org/downloads/) 3.11 to 3.13, with venv and headers (Archipelago 0.6.7 rejects newer versions; on Arch, take [python312](https://aur.archlinux.org/packages/python312) from the AUR)
- a C compiler: [build-essential](https://packages.ubuntu.com/noble/build-essential) / [base-devel](https://archlinux.org/packages/core/any/base-devel/)
- [xclip](https://github.com/astrand/xclip)
- For BizHawk: [Mono](https://www.mono-project.com/), [OpenAL Soft](https://openal-soft.org/), [Lua 5.4](https://www.lua.org/), [lsb-release](https://packages.ubuntu.com/noble/lsb-release)

## 2. Clone Archipelago and the world

```bash
git clone https://github.com/ArchipelagoMW/Archipelago.git ~/dev/Archipelago
cd ~/dev/Archipelago
git switch -c ap-0.6.7 0.6.7
git clone git@github.com:LMR-C/Rayman-AP.git worlds/rayman
echo "worlds/rayman/" >> .git/info/exclude
```

The exclude line keeps our folder out of Archipelago's git. Git commands inside `worlds/rayman/` apply to our repo.

## 3. Python environment

Run this at the root of the Archipelago clone.

```bash
cd ~/dev/Archipelago
python3.12 -m venv .venv
source .venv/bin/activate
python ModuleUpdate.py --yes
pip install -r requirements.txt
```

`ModuleUpdate.py` also installs the `requirements.txt` of each world, ours included. The second install avoids a 0.6.7 quirk where every launch asks to reinstall packages. In every new terminal, run `cd ~/dev/Archipelago && source .venv/bin/activate` before any Python command.

## 4. BizHawk

1. Download **BizHawk 2.10** for Linux from the [releases page](https://github.com/TASEmulators/BizHawk/releases). It is the newest version the Archipelago 0.6.7 Lua connector supports.
2. Extract it into its own folder, for example `~/emu/BizHawk-2.10`.
3. Copy your BIOS into its `Firmware/` folder.
4. Run `EmuHawkMono.sh`.
5. Once: `Config > Firmware...` then **Scan** (green check expected), `Config > Preferred Cores > PSX` = **NymaShock**, and tick `Config > Customize > Run in background`.

## 5. Generate a Seed
From `~/dev/Archipelago` with the venv active:
1. Once: `python Launcher.py "Generate Template Options"`, then copy `Players/Templates/Rayman.yaml` to `Players/` and set `name:` (your slot name).
2. Keep only this session's YAML files in `Players/`.
3. `python Generate.py` writes `output/AP_<your_seed>.zip` (spoiler log included).

## 6. Launch the game with local server
1. In BizHawk, `File > Open ROM...` and pick your `.chd`.
2. `Tools > Lua Console`, then open `~/dev/Archipelago/data/lua/connector_bizhawk_generic.lua`.
3. From `~/dev/Archipelago` with the venv active, run `python MultiServer.py output/AP_<your_seed>.zip`. it is open on port 38281.
4. From `~/dev/Archipelago` with the venv active, run `python BizHawkClient.py --connect localhost:38281`. It should log `Connected to BizHawk`.

Client logs: `~/dev/Archipelago/logs/BizHawkClient_<date>.txt`.
