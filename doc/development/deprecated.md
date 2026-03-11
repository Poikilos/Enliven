# Deprecated
## Deprecation of Root Scripts
Bash scripts for installing ENLIVEN based on minetest_game are deprecated (See [Enliven](https://github.com/Poikilos/Enliven) repo instead). They will be kept around, but are not recommended. The mods or URLs that are installed by the script may stop working at any time. The best way to experience the 0.4 version is with the [Windows binary installer](http://www.expertmultimedia.com/index.php?htmlref=tutoring.html) release which comes with Minetest 0.4.15. See also "Deprecated Instructions" below.
## Tasks
- [ ] Remove anything running as root
- [x] etc/change_hardcoded_world_name_first/mts-ENLIVEN deprecated by mtsenliven.py
- [x] Make python build (See https://github.com/Poikilos/Enliven)

## Deprecated Instructions
(kept for archival or reference purposes only--not recommended--see above)
EnlivenMinetest project assists you in setting up ENLIVEN subgame and provides scripts to run it on minetestserver as current user (must be sudoer).
Some of the included scripts help install and manage your git version of Minetest Server on Ubuntu Server or various *buntu flavors (a gui distro neither required nor recommended for minetestserver running ENLIVEN). See also https://github.com/Poikilos/minetest-chunkymap (or https://github.com/Poikilos/mtanalyze) for a map non-redis servers, and some offline minetest management tools.
(minetestserver requires GNU/Linux System -- only tested using apt on Ubuntu Server [14.04 to 16.04] and Lubuntu [14.04 to 16.04])
The installer script (in the "etc/change_world_name_manually_first" folder) downloads the git versions of all of the mods to the ENLIVEN folder which will be placed in your minetest games folder (one of the two folders listed below, otherwise fails)--but change the world name to the name of your world first.
* (optionally) place the ENLIVEN folder in the games folder here into the games folder on your server such as:
  /usr/local/share/minetest/games/
    (If you're not using the git version of Minetest on Ubuntu Server, try something like:
    /usr/share/games/minetest/games/ )
  although the installer script should create the initial version of the minetest.conf in there (NOTE: there is a different version of minetest.conf for clients, as described below)
* BEFORE running game-install-enliven.sh, make sure you FIRST CHANGE the value after "MT_MYWORLD_NAME="
Do not expect the mods from game-install-enliven-testing.sh to work. Also, do not run the file directly -- instead, paste the variables (before backup process) in game-install-enliven.sh into a terminal window, then paste the contents of game-install-enliven-test.sh
* mts-ENLIVEN starts server (place it in $HOME normally), but requires you to FIRST CHANGE the value after worldname to the name of your world
* If you have used cme or tsm_pyramids is your world before, fix issue where cme is required by certain mods by manually placing the folders from etc\Mods,WIP into your mods folder (this may be automated in the future), so mobs (including spawners:mummy) will be used instead.
(There are also WIP TRMs in there to go with the ENLIVEN subgame)
Otherwise just install everything EXCEPT cme_to_spawners & tsm_pyramids_to_spawners.
(NOTE: spawners makes pyramids now, so tsm_pyramids )
* Recommend your users use the binary installer (Windows client) from "Releases" at https://github.com/Poikilos/Enliven/releases or the alternate site above to install, otherwise installation requires a good minetest.conf downloaded such as from the winclient/launcher folder and placed in their minetest folder. The one here has better graphics (opengl 3.0 shaders, smooth lighting).
