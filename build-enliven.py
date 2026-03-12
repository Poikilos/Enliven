#!/usr/bin/env python3
'''
ENLIVEN subgame builder - creates ENLIVEN based on minetest_game
Merges mods & settings from old bash installer script

mt_conf_by_mod settings should be placed in minetest.conf
but go in f"{destination}/minetest.conf" by default. See also:
- patches/subgame/minetest.conf
  To define the game.
- patches/subgame/minetest.server-example.conf goes in the server only.
  - Place the result in the game directory such as will result in
    f"worlds/{world}/ENLIVEN/minetest.conf"
- patches/subgame/minetest.client-example.conf goes in clients only.
'''
from __future__ import print_function
from collections import OrderedDict
import sys
import os
import argparse
# import configparser
import logging

# Assuming these exist in your pyenliven module
from pyenliven import (
    echo0,
    # getSGPath,           # not used here anymore
    # profile,
)

from pyenliven.gamebuilder import GameBuilder

logger = logging.getLogger(os.path.split(__file__)[1])

# ──────────────────────────────────────────────────────────────
#           M O D   L I S T   F R O M   B A S H   S C R I P T
# ──────────────────────────────────────────────────────────────

# Format:
#   'name':          folder name expected in mods/ or mods_stopgap/
#   'repo':          git URL (str or list[str] — first = highest priority)
#   'branch':        optional branch name
#   'stopgap':  True → only use from MODS_STOPGAP_DIR, ignore repo

def main():
    parser = argparse.ArgumentParser(description="Build ENLIVEN subgame from minetest_game")
    parser.add_argument("minetest_game_path", help="Path to minetest_game directory")
    parser.add_argument("--conf", "-c", dest="conf_path",
                        help="Path to write/append ENLIVEN minetest.conf settings "
                             "(default: minetest_game_path/minetest.conf.enliven)")
    parser.add_argument("--minetest-version", "-v", dest="minetest_version",
                        choices=["0.4", "5"], default="5",
                        help="Target Minetest version compatibility: '5' (default) or '0.4'")
    parser.add_argument("--offline", "-o", action="store_true",
                        help="Do not pull in repos (fail if not cloned yet).")
    parser.add_argument("--delete", "-d", action="store_true",
                        help="Erase target completely first")
    parser.add_argument("--no-pull", "-n", action="store_true",
                        help="Skip pull command on existing repos")
    args = parser.parse_args()

    # try:
    builder = GameBuilder(
        args.minetest_game_path,
        minetest_version=args.minetest_version,
        offline=args.offline,
        delete=args.delete,
        pull=(not args.no_pull),
    )
    builder.build(conf_path=args.conf_path)
    return 0
    # except Exception as exc:
    #     echo0(f"ERROR: {exc}")
    #     return 1


def detect_games(programs_dir, name="minetest_game"):
    games = []
    if not os.path.isdir(programs_dir):
        print(f"No {repr(programs_dir)}")
        return games
    for engine in os.listdir(programs_dir):
        engine_path = os.path.join(programs_dir, engine)
        # such as "luanti"
        for version in os.listdir(engine_path):
            # such as "luanti-5.15.1"
            version_path = os.path.join(engine_path, version)
            games_path = os.path.join(version_path, "games")
            game_path = os.path.join(games_path, name)
            if os.path.isdir(game_path):
                games.append(OrderedDict(
                    name=name,
                    path=game_path,
                ))
            else:
                print(f"No {repr(game_path)}")
    return games


if __name__ == "__main__":
    base_game_name = "minetest_game"
    programs_dir = os.path.expanduser("~/.config/EnlivenMinetest/versions")
    games = detect_games(programs_dir)
    seqCount = 0
    for argI in range(1, len(sys.argv)):
        arg = sys.argv[argI]
        if arg.startswith("-"):
            continue
        seqCount += 1
    if seqCount < 1:
        if len(games) < 1:
            raise ValueError(f"No {base_game_name} in {programs_dir}/<<engine>-<version>>/games. Download it there first.")
        if len(games) > 1:
            print(f"Detected {games}")
        print(f"No base game folder specified. Using {games[0]}")
        sys.argv.insert(1, games[0]['path'])
    sys.exit(main())
