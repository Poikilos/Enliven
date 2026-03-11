import shutil
import os

from collections import OrderedDict
from decimal import Decimal
from logging import getLogger
from typing import Dict, List

from pyenliven import echo0


logger = getLogger(__name__)

gamespec: OrderedDict[str, any] = OrderedDict()
gamespec['remove_mods'] = [
    "facade",           # no recipes
    "placecraft",       # interferes with eating
    "more_chests",      # https://github.com/Poikilos/Enliven/issues/446
    "emeralds",         # https://github.com/Poikilos/Enliven/issues/497
    "give_initial_stuff",
    "xban2",
    "dynamic_liquid",
    # "stamina",
    "hbarmor",
    "hbhunger",
    "hudbars",
    "hbsprint",
    # "dungeon_loot",     # or treasurer + trm_*
    "helicopter",       # known crash issues in older versions
    # add others from issue #310 if desired
]

gamespec['add_mods']: List[Dict[str, any]] = [

    # ── Utility / Admin ────────────────────────────────────────
    {'name': "advancedban",    'repo': "https://github.com/srifqi/advancedban"},
    {'name': "areas",          'repo': "https://github.com/ShadowNinja/areas.git"},
    {'name': "invhack",        'repo': "https://github.com/salahzar/minetest-invhack.git",
     'privs': {'moderator': ['invhack']},
     'items': {'moderator': ['invhack:tool']},
     'comments': ["See also inventory_admin mod which is purely command-based"]},
    {'name': "metatools",      'repo': "https://github.com/Poikilos/metatools.git"},
    {'name': "modlist",        'repo': "https://github.com/SkyBuilder1717/modlist.git"},
    {'name': "protect_block_area", 'repo': "https://github.com/C-C-Minetest-Server/protect_block_area.git"},
    # {'name': "protector",      'repo': ["https://notabug.org/TenPlus1/protector.git",
    #                                     "https://codeberg.org/tenplus1/protector.git"]},
    {'name': "super_give", 'repo': "https://github.com/daneldragondanel-boop/super_give.git",
     'content_url': "https://content.luanti.org/packages/daneldragondanel-boop/super_give/"},
    {'name': "vote",           'repo': "https://github.com/minetest-mods/vote.git"},
    {'name': "whitelist",      'repo': "https://github.com/ShadowNinja/whitelist.git"},
    {'name': "worldedit",      'repo': "https://github.com/Uberi/MineTest-WorldEdit.git"},

    # Mobs
    {'name': "animalia", 'repo': "https://github.com/ElCeejo/animalia.git",
     'what': "Various creatures with sounds such as bats, frogs, etc. using creatura",
     'requires': "creatura"},
    # TODO: ^ Change beef to meat
    # TODO: ^ Make it work with x_farming if doesn't work with minetest_game farming
    {'name': "creatura", 'repo': "https://github.com/ElCeejo/creatura.git",
     'description': "A performant Animal focused Mob API "},
    # TODO: ^ Make sure spawning crystals are only in creative
    {'name': "mobs",      'repo': ["https://notabug.org/TenPlus1/mobs_redo.git",
                                   "https://codeberg.org/tenplus1/mobs_redo.git"],
     'settings': OrderedDict(mobs_attack_creatura=True)},
    # {'name': "mobs_to_creatura", 'repo': "https://github.com/Poikilos/mobs_to_creatura.git",
    #  'why-not': "creatura is light on features, so making mobs with custom logic within Mobs Redo or not using Mobs Redo are better solutions that re-implementing large parts of it."},
    {'name': "mobs_monster",   'repo': ["https://notabug.org/TenPlus1/mobs_monster.git",
                                       "https://codeberg.org/tenplus1/mobs_monster.git"]},
    {'name': "mobs_animal",    'repo': ["https://notabug.org/TenPlus1/mobs_animal.git",
                                       "https://codeberg.org/tenplus1/mobs_animal.git"]},
    {'name': "mob_horse",      'repo': ["https://notabug.org/tenplus1/mob_horse.git",
                                       "https://codeberg.org/tenplus1/mob_horse.git"]},
    {'name': "mobs_sky",       'repo': "https://github.com/Poikilos/mobs_sky.git"},
    {'name': "mobs_water", 'repo': "https://github.com/blert2112/mobs_water.git"},
    #{'name': "dmobs", 'repo': ["https://github.com/minetest-mobs-mods/dmobs.git",
    #                           "https://codeberg.org/tenplus1/dmobs"]},
    # TODO: ^ Make open_ai mobs api bridge for these?
    # {'name': "open_ai", 'repo': "https://github.com/Poikilos/open_ai.git",
    #  'why': "creatura is light on features; no projectiles etc. Mobs Redo AI is low-functioning."},
    # {'name': "spawners",       'repo': "https://bitbucket.org/minetest_gamers/spawners.git"},

    # Worldgen
    {'name': "bakedclay",      'repo': ["https://notabug.org/tenplus1/bakedclay.git",
                                        "https://codeberg.org/tenplus1/bakedclay.git"]},
    {'name': "bedrock2", 'repo': "https://codeberg.org/Wuzzy/minetest_bedrock2.git",
     'settings': OrderedDict(bedrock2_y=-64)},
    # TODO: ^ Consider adding something useful further down, then increasing it to -128
    # TODO: Add build limit of 192 (maybe 256 at most)
    {'name': "biome_lib",      'repo': "https://github.com/mt-mods/biome_lib.git"},
    # {'name': "birthstones",    'repo': "https://github.com/Poikilos/birthstones.git"},  # commented to reduce inventory overload
    {'name': "bushes_soil",    'repo': "https://github.com/Poikilos/bushes_soil.git"},
    {'name': "caverealms",     'repo': "https://github.com/FaceDeer/minetest-caverealms.git"},
    {'name': "lapis",          'repo': "https://github.com/Napiophelios/LapisLazuli.git",
     'settings': OrderedDict(enable_lapis_mod_columns=True),
     'why': "Unlike, minetest-mods/lapis, LapisLazuli has more things you can make."},
    {'name': "livingjungle", 'repo': "https://github.com/Skandarella/livingjungle.git"},
    {'name': "loot", 'repo': "https://github.com/minetest-mods/loot.git",
     'why': "Defines loot API and adds loot to dungeons",
     'settings': OrderedDict(loot_dungeons=True)},
    {'name': "mapgen_helper",  'repo': "https://github.com/minetest-mods/mapgen_helper.git"},
    {'name': "mesecons",       'repo': "https://github.com/minetest-mods/mesecons"},
    # TODO: ^ trim down mesecons or make registered nodes configurable
    # {'name': "moreblocks",     'repo': "https://github.com/minetest-mods/moreblocks.git",
    #  'why-not': "permanently changes default stairs. Has many registrations. Has its own ropes (vine-like ones).",
    #  'why': "Can use place_rotated. Has stairsplus."},
    # TODO: Make a mod to auto-convert corners on place&harvest (for stairsio items merged into mtg)
    {'name': "rope_bridges", 'repo': "https://github.com/sfence/rope_bridges.git"},
    # TODO: ^ Make rope_bridges use x_farming if moreblocks not present (can also use ropes or vines mods)
    # {'name': "moreores",       'repo': "https://github.com/minetest-mods/moreores.git",
    #  'what': "tin (such as to make bronze), silver and mithril. Bronze, silver, gold, mithril tools. Copper rails."},
    # TODO: ^ Maybe switch to 2019 updated https://codeberg.org/tenplus1/moreores.git
    # TODO: ^ Add gold tools without all the other stuff (Maybe use add_tool mod instead).
    # TODO: ^ See also "ShadMordre's lib_trm, which is a combination of toolranks and Terraria's tool modifiers"
    # {'name': "lib_trm", 'repo': "https://github.com/ShadMOrdre/lib_trm.git",
    #  'description': "Combines Tool Ranks (toolranks) and Crafted Tools Modifiers (ctm) into a single working mod."},
    # {'name': "toolranks", 'repo': "https://codeberg.org/tenplus1/toolranks.git",
    #  'what': "level up tools with use"}
    {'name': "moretrees",      'repo': "https://github.com/mt-mods/moretrees.git"},
    {'name': "naturalbiomes", 'repo': "https://github.com/Skandarella/naturalbiomes.git",
     'recommends': ["winuserleafdecay"]},
    {'name': "plantlife_modpack", 'repo': "https://github.com/mt-mods/plantlife_modpack.git"},
    # TODO: ^ Remove any mods that overlap naturalbiomes
    {'name': "subterrane",     'repo': "https://github.com/minetest-mods/subterrane.git"},
    # {'name': "technic",        'repo': "https://github.com/minetest-mods/technic.git",
    #  'depends': ["default", "pipeworks", "technic_worldgen", "basic_materials"],
    #  'optional_depends': ["bucket", "screwdriver", "mesecons", "mesecons_mvps",
    #                       "digilines", "digiline_remote", "intllib",
    #                       "unified_inventory", "vector_extras", "dye",
    #                       "craftguide", "i3", "everness", "nether"],
    #  'why-not': "Automatic mining, and too many ores"},
    # {'name': "technic_armor",  'repo': ["https://github.com/stujones11/technic_armor.git",
    #                                     "https://github.com/mt-mods/technic_armor.git"]},
    # {'name': "tsm_pyramids",   'repo': "https://github.com/Poikilos/tsm_pyramids.git"},
    # {'name': "tsm_chests_dungeon", 'repo': "http://repo.or.cz/minetest_tsm_chests_dungeon.git"},  # see "loot" mod instead
    # {'name': "treasurer",      'repo': "http://repo.or.cz/minetest_treasurer.git"},
    # {'name': "trm_pyramids"},  # special – files copied directly in bash → handle manually or stopgap
    # {'name': "tsm_mines",      'repo': "http://repo.or.cz/tsm_mines.git"},  fork of BlockMen’s [Mines](https://forum.minetest.net/viewtopic.php?f=11&t=6307) replaced by tsm_railcorridors
    # {'name': "tsm_railcorridors", 'repo': ["http://repo.or.cz/RailCorridors/tsm_railcorridors.git",
    #                                       "https://codeberg.org/Wuzzy/minetest_tsm_railcorridors.git"]},
    # TODO: ^ Make loot version of each trm_*, trmp_*, and tsm_*
    {'name': "magma_conduits", 'repo': "https://github.com/FaceDeer/magma_conduits.git"},
    # {'name': "quartz",         'repo': "https://github.com/minetest-mods/quartz"},  # commented to reduce inventory overload
    {'name': "winuserleafdecay", 'repo': "https://github.com/Skandarella/winuserleafdecay.git"},
    {'name': "worldedge",      'repo': "https://github.com/minetest-mods/worldedge.git"},

    # Worldgen - Underwater
    # {'name': "decorations_sea", 'repo': "https://github.com/mt-historical/decorations_sea.git",
    #  'recommends': ["lootchests_modpack", "shipwrecks"],
    #  'what': "Sea decorations, mostly 2D",
    #  'why-not': "Use marinara+marinaramobs instead"},
    {'name': "marinara", 'repo': "https://github.com/Skandarella/marinara.git",
     'description': "adds water structures and coral reefs to the oceans of your world",
     'what': "Nice sea plants, plantlike creatures, coral, seaweed, cattails"},
    {'name': "marinaramobs", 'repo': "https://github.com/Skandarella/marinaramobs.git"},
    # TODO: Make a "mobs" adapter mod for creatura so marinaramobs can register mobs
    # {'name': "wc_sealife", 'repo': "https://github.com/wintersknight94/NodeCore-SeaLife.git",
    #  'content_url': "https://content.luanti.org/packages/Winter94/wc_sealife/",
    #  'what': ("All 2D. Sea life for seas & rivers. Coral of various colors,"
    #           " anemones, kelp. Depth-based seajellies & urchins")},
    # TODO: May be contribute graphics for the "Planned Features" list. Maybe 3D.

    # ── Gameplay / Items ───────────────────────────────────────
    # TODO: from https://content.luanti.org/packages/PetiAPocok/minetest_extended/ add:
    # TODO: snowball (or use minetest-mods/throwing or x_bows and fork https://codeberg.org/TPH/exile_snow or simpler https://content.luanti.org/packages/ComputeGraphics/snowball/ so snow drops it)
    # TODO: ice and snow melting by furnace (also torch/fire if not in mtg)
    # TODO: craft for green dye from cactus
    # TODO: Chests drop the items what are inside of it when broke
    # TODO: furnaces drop the items what are inside of it when broke
    # TODO: Improved mese monster texture
    {'name': "3d_armor",       'repo': ["https://github.com/stujones11/minetest-3d_armor.git",
                                        "https://github.com/minetest-mods/3d_armor.git"]},
    {'name': "anvil",          'repo': "https://github.com/minetest-mods/anvil.git"},
    {'name': "armor_expanded", 'repo': "https://github.com/Crystalwarrior/armor_expanded.git",
     'what': "Grass & leather armor. Works with animalia (based on creatura)."},
    # TODO: ^ Make dyed leather armor.
    {'name': "awards",         'repo': "https://gitlab.com/rubenwardy/awards.git"},
    {'name': "awards_board",   'repo': "https://framagit.org/xisd-minetest/awards_board.git"},
    {'name': "banners", 'repo': "https://github.com/evrooije/banners.git"},
    {'name': "basic_materials",'repo': "https://github.com/mt-mods/basic_materials.git"},
    # {'name': "basic_machines", 'repo': "https://content.luanti.org/packages/waxtatect/basic_machines",
    #  'why-not': "automatic mining"},
    # {'name': "boost_cart",     'repo': "https://github.com/SmallJoker/boost_cart.git",
    #  'why-not': "Use mesecons_carts which uses minetest_game carts and is improvement by composition"},
    {'name': "builtin_item", 'repo': "https://codeberg.org/tenplus1/builtin_item.git",
     'description': "Dropped items can now be pushed by water, burn quickly in lava and have their own custom functions.",
     'why': "Each craftitem has more physics, and if stuck inside a block will free itself."},
    {'name': "compassgps",     'repo': "https://github.com/Poikilos/compassgps.git"},
    {'name': "controls", 'repo': "https://github.com/mt-mods/controls.git",
     'why': "Required by visible_sneak"},
    # {'name': "digilines",      'repo': "https://github.com/minetest-mods/digilines.git"},
    {'name': "fakelib", 'repo': "https://github.com/OgelGames/fakelib.git",
     'why': "Required by pipeworks"},
    {'name': "fishing",        'repo': "https://github.com/MinetestForFun/fishing.git",
     'issues': ["Make sure fishing rods recipe works"],
     'version-note': "Minetestforfun's (NOT wulfsdad's) fishing <https://forum.minetest.net/viewtopic.php?f=11&t=13659>"},
    {'name': "flowerpot", 'repo': "https://github.com/minetest-mods/flowerpot.git",
     'what': "Works with most plants, and lightweight as in no entity"},
    # ^ Make sure it works with x_farming--Make compat mod if necessary. See api.md.
    {'name': "frame", 'repo': "https://github.com/minetest-mods/frame.git"},
    # {'name': "homedecor_modpack", 'repo': "https://github.com/mt-mods/homedecor_modpack.git"},
    # {'name': "homedecor_ua",   'repo': "https://github.com/Poikilos/homedecor_ua.git"},
    {'name': "item_drop",      'repo': "https://github.com/minetest-mods/item_drop.git",
     'settings': {'item_drop.pickup_radius': "1.425"}},
    {'name': "mesecons_carts", 'repo': "https://cheapiesystems.com/git/mesecons_carts.git"},
    # {'name': "mymasonhammer",  'repo': "https://github.com/minetest-mods/mymasonhammer.git",
    #  'what': "A hammer that cuts stairs and ladders in blocks"},
    {'name': "mywalls",        'repo': "https://github.com/minetest-mods/mywalls.git",
     'what': "Adds more wall types for walls mod from minetest_game."},
    # {'name': "painting", 'repo': "https://github.com/evrooije/painting.git",
    #  'why': "Required by Painted 3D Armor"},
    # TODO: ^ Simplify Painted 3D Armor and just make banners combine with shields
    {'name': "pipeworks",      'repo': "https://github.com/mt-mods/pipeworks.git"},
    {'name': "ropes",          'repo': "https://github.com/minetest-mods/ropes.git",
     'why-not': "Use ropes from x_farming instead."},
    # {'name': "sling",          'repo': "https://github.com/minetest-mods/sling.git"},
    {'name': "signs_lib",      'repo': "https://github.com/mt-mods/signs_lib.git"},
    {'name': "slimenodes",     'repo': "https://github.com/Poikilos/slimenodes.git"},
    {'name': "sounding_line",  'repo': "https://github.com/minetest-mods/sounding_line.git"},
    # {'name': "stamina", 'repo': "https://codeberg.org/tenplus1/stamina.git",
    #  'comment': "Patches item_eat to affect saturation instead of health.",
    #  'help-dev': "Changes ItemStack before register_on_item_eat callbacks, but they can use 6th param for original ItemStack",
    #  'privs': {'invincible': ['no_hunger']}},
    # TODO: ^ Modify stamina to depend on hunger_ng *or* hbhunger, which many mods use (usually hunger_ng, but often either)
    # {'name': "sponge", 'repo': "https://github.com/BenjieFiftysix/sponge"},
    # TODO: ^ Test, make sure is in worldgen. Integrate with marinara?
    {'name': "throwing",       'repo': "https://github.com/minetest-mods/throwing.git"},
    # {'name': "throwing_arrows", 'repo': "https://github.com/minetest-mods/throwing_arrows.git",
    #  'settings': {'throwing.enable_arrow': "true"}},
    {'name': "x_bows", 'repo': "https://bitbucket.org/minetest_gamers/x_bows.git",
     'why': "Makes arrows stick into things"},
    {'name': "travelnet",      'repo': "https://github.com/Sokomine/travelnet.git"},
    # {'name': "ts_furniture",   'repo': "https://github.com/minetest-mods/ts_furniture.git"},
    # TODO: ^ Make sitting work for steps (and slabs?) instead.
    # {'name': "trmp_minetest_game",'repo': "https://github.com/Poikilos/trmp_minetest_game.git"},
    # TODO: ^ Make a version for loot
    # {'name': "unifieddyes",    'repo': "https://github.com/mt-mods/unifieddyes.git"},
    # TODO: ^ Add Poikilos/dyed mod instead
    # {'name': "sea",
    #  'why-not': "deprecated & gone, replaceable by decorations_sea or oceans. Recommends scuba which is also gone"}
    {'name': "lootchests_modpack", 'repo': "https://github.com/mt-historical/lootchests_modpack.git",
     'why': "shipwrecks uses lootchests_default from this to generate chests",
     'exclude': ["lootchests_magic_materials"]},
    {'name': "shipwrecks", 'repo': "https://github.com/mt-historical/shipwrecks.git",
     'settings': OrderedDict(shipwrecks_chance=192)},
    # ^ Default chance is 10, which is 1 in 10 chunks (way too
    #   many--there are 16 16x16 chunks across a 64x64 surface)
    # TODO: ^ Convert shipwrecks to use loot mod instead
    {'name': "x_farming", 'repo': "https://bitbucket.org/minetest_gamers/x_farming.git",
     'description': "Farming with bees, new plants, crops, trees, ice fishing, bees, candles, scarecrow, crates, composter, bonemeal, ropes, pies...",
     'what': "Additional farming including giant cacti, bonemeal, empty soup bowl, placeable food",
     'why': "better graphics than farming redo"},
    # TODO: ^ Make sure x_farming works with: minetest_game/farming, hunger_ng
    # TODO: ^ Add white dye from bonemeal recipe if not present
    {'name': "xcompat", 'repo': "https://github.com/mt-mods/xcompat.git"},
    {'name': "xdecor", 'repo': "https://codeberg.org/Wuzzy/xdecor-libre.git"},
    # TODO: ^ Remove shaped nodes.
    # TODO: ^ Make kc_modpack unregister the enchanting table and register a table for its system
    # TODO: Add version of vessels with jars from minetest_extended?

    # ── Player UX ──────────────────────────────────────────────
    {'name': "ambience",       'repo': ["https://notabug.org/tenplus1/ambience.git",
                                        "https://codeberg.org/tenplus1/ambience.git"]},
    {'name': "edit_skin", 'repo': "https://github.com/MrRar/edit_skin.git",
     'content_url': "https://content.luanti.org/packages/Mr.%20Rar/edit_skin/"},
    {'name': "effervescence", 'repo': "https://github.com/EmptyStar/effervescence.git"},
    # TODO: ^ designed for Asuna, so may need work for: naturalbiomes, livingjungle, plantlife_modpack
    {'name': "environment_music", 'repo': "https://github.com/Poikilos/environment_music.git"},
    {'name': "fire_plus", 'repo': "https://github.com/Dumpster-Studios/fire_plus.git"},
    {'name': "hbsprint", 'repo': "https://github.com/minetest-mods/hbsprint.git"},
    # {'name': "sprint_lite", 'repo': "https://github.com/mt-historical/sprint_lite.git",
    #  'why-not': "Can't use hunger_ng, hbsprint now can. Mini API not necessary (?) since hbsprint works with unified_stamina"},
    # TODO: Port mini-api from sprint_lite to hbsprint if other mods can't check/affect stamina (Try via unified_stamina)
    # TODO: Port feature to not recover when dead from sprint_lite to hbsprint
    {'name': "hunger_ng",      'repo': ["https://gitlab.com/4w/hunger_ng.git",
                                        "https://git.0x7be.net/dirk/hunger_ng"],
     'why': "Many mods including marinara depend on it"},
    {'name': "lightning",      'repo': "https://github.com/minetest-mods/lightning.git"},
    # {'name': "money",          'repo': ["https://notabug.org/TenPlus1/money",
    #                                     "https://codeberg.org/tenplus1/money.git"],
    #  'why-not': "This fork removes everything except barter stations"},
    {'name': "music_modpack", 'repo': "https://github.com/mt-historical/music_modpack.git",
     'exclude': ["music_default", "music_dfcaverns"],
     'what': "music_api such as for Poikilos' environment_music"},
    {'name': "place_rotated", 'repo': "https://github.com/12Me21/place_rotated.git"},
    {'name': "player_monoids", 'repo': "https://github.com/minetest-mods/player_monoids.git"},
    # {'name': "playeranim",     'repo': "https://github.com/minetest-mods/playeranim.git",
    #  'what': "Makes the head, and the right arm when you're mining, face the way you're facing"},
    {'name': "bodyanim", 'repo': "https://github.com/dacctal/luanti-bodyanim.git",
     'description': "Player bodies follow their walk direction, and player heads follow their look direction. Based on Lone_Wolf's headanim"},
    # TODO: ^ Make sneak animation for bodyanim
    # {'name': "ore_info", 'repo': "https://github.com/TwigGlenn4/ore_info.git",
    #  'content_url': "https://content.luanti.org/packages/TwigGlenn4/ore_info/"},
    # ^ TODO: Make an ore_info fork where players discover & trade books to find ore info
    {'name': "playereffects",  'repo': "https://github.com/sys4-fr/playereffects"},
    {'name': "playerlist", 'repo': "https://github.com/LizzyFleckenstein03/playerlist.git",
     'what': "Show player list on sneak. Has color API and ping.",
     'content_url': "https://content.luanti.org/packages/AiTechEye/invisible/"},
    # {'name': "skinsdb",        'repo': "https://github.com/minetest-mods/skinsdb.git"},
    # {'name': "sprint",         'repo': "https://github.com/GunshipPenguin/sprint.git"},
    # {'name': "unified_inventory",'repo': [
    #     "https://github.com/minetest-mods/unified_inventory.git",
    #     "https://github.com/MinetestForFun/unified_inventory"  # fork with "nicer interface"
    # ]},
    # {'name': "sfinv", 'repo': "https://github.com/rubenwardy/sfinv.git",
    #  'why': "Unified inventory is ugly and has a bloated API.",
    #  'why-not': "Now included in minetest_game"},
    # {'name': "bags", 'repo': "https://github.com/cornernote/minetest-bags.git"},
    {'name': "prestibags", 'repo': "https://github.com/Poikilos/prestibags.git"},
    # TODO: ^ Make sure prestibags drop item if destroyed with regard to their momentum, and are pushed by TNT
    # TODO: make dyed_prestibags (See also https://codeberg.org/Codiac/prestibags)
    # {'name': "woodcutting",    'repo': "https://github.com/minetest-mods/woodcutting.git",
    #  'what': "harvest tree while sneak pressed to gather whole tree"},
    # {'name': "radiant_damage", 'repo': "https://github.com/minetest-mods/radiant_damage.git"},
    # TODO: ^ Make walking on hardened lava cause damage
    {'name': "invisible", 'repo': "https://github.com/AiTechEye/invisible.git",
     'items': {'moderator': ['invisible:tool']},  # i is alias for invisible:tool
     'privs': {'moderator': ['invisible']}},
    # NOTE: ^ See also visible_sneak
    {'name': "unified_stamina", 'repo': "https://github.com/t-affeldt/unified_stamina.git",
     'why': "Works with various stamina mods including hbsprint"},
    {'name': "visible_sneak", 'repo': "https://github.com/wireva/visible_sneak.git"}
    # TODO: ^ Make sure can sneak under things (1.5 m), otherwise switch to https://content.luanti.org/packages/zempik10/good_sneaking/ and fix non-moving legs

    # ── Legacy / Special ───────────────────────────────────────
    # {'name': "animal_materials_legacy"},
    # {'name': "elk_legacy"},
    # {'name': "glooptest_missing"},
    # {'name': "nftools_legacy"},
]

# Preprocess add_mods for repo.or.cz
for entry in gamespec['add_mods']:
    repos = entry.get('repo')
    if repos is None:
        continue
    if isinstance(repos, str):
        repos = [repos]
    for repo in repos:
        if repo and "repo.or.cz" in repo:
            entry['distributor'] = "Wuzzy"
        break

# Per-mod overrides / extras
why = {}
why["https://github.com/MinetestForFun/unified_inventory"] = '''
This fork makes a "nicer interface". The fork hasn't been tested yet.
'''
# deprecates https://github.com/Poikilos/vines.git fork of Facedeer's:
why["https://github.com/FaceDeer/vines.git"] = '''
> I've finally done it, I've split this mod in twain. The new
> stand-alone ropes mod has no dependency on biome_lib and no vine
> content, though its crafting recipes remain compatible with the vines
> produced by this mod.
>
> My fork of this vines mod has had the rope-related content removed
> from it, leaving it as just a vines mod. Note that I haven't tested
> it extensively - I have to admit, I've mainly been in this for the
> ropes. :) I'll do what I can to maintain it, though, if anyone has
> bug reports or requests.
>
> I've added a node upgrade function to the new ropes mod that will
> convert the ropes from both my fork of the vines mod and the original
> version of the vines mod by bas080 to the new ropes mod's ropes. So
> if you wish to upgrade an existing world it should work.

- FaceDeer on [[Mod] Vines and Rope [2.3] [vines]]
  (https://forum.minetest.net/viewtopic.php?f=11&t=2344&start=50&sid=bf15c996963e891cd3f2460c2525044a)

Note that vines requires:

default
biome_lib
moretrees?
doc?
intllib?
mobs?
creatures?
'''
gamespec['disable_mobs'] = [
    "old_lady",
]


server_only_mods = [
    'ircpack',
    'chat3',
]

# ──────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────
#     Collected minetest.conf settings from the bash script
# ──────────────────────────────────────────────────────────────

BASE_ENLIVEN_CONF_SETTINGS = OrderedDict(
    # General / map
    map_generation_limit=5000,
    # HUD / Controls
    # "stamina_disable_aux1 = true",  # require double tap for run (Prevent stamina from taking up aux1 key)
    # "stamina_hud_x =",
    # "stamina_hud_y =",
    # "stamina_double_tap_time =",   # 0 to disable
    # Protector
    protector_radius=7,
    protector_flip=True,
    protector_pvp=True,
    protector_pvp_spawn=10,
    protector_drop=False,
    protector_hurt=3,
    # Other gameplay
    world_edge=5000,
    default_privs="interact,shout,home",
    max_users=50,
    motd="Actions and chat messages are logged. Use inventory to see recipes (use web for live map if available).",
    disallow_empty_passwords=True,
    server_dedicated=False,
    bones_position_message=True,
    # Sprint (GunshipPenguin sprint settings)
    sprint_speed=2.25,
    sprint_jump=1.25,
    sprint_stamina_drain=.5,
)
BASE_ENLIVEN_CONF_SETTINGS['secure.trusted_mods'] = "advanced_npc"
BASE_ENLIVEN_CONF_SETTINGS['secure.http_mods'] = "modlist"



def encode_cv(v):
    """Encode the value to minetest.conf syntax"""
    if v is None:
        return ""  # results in "name =" which is valid syntax
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float, Decimal)):
        return str(v)
    if isinstance(v, str):
        return f'{v}'  # no quotes in minetest.conf format
    raise TypeError(
        "{} type is not implemented in pyenliven Luanti conf encoder"
        .format(type(v).__name__))


def update_conf(path, new_settings):
    tmp_path = path + ".tmp"
    if os.path.isfile(tmp_path):
        os.remove(tmp_path)
    changed = 0
    added = 0
    same = 0
    if os.path.isfile(path):
        lineN = 0
        with open(path, 'r', encoding="utf-8") as src:
            with open(tmp_path, 'w', encoding="utf-8") as dst:
                for rawL in src:
                    lineN += 1
                    line = rawL.strip()
                    if line.startswith("#"):
                        dst.write(rawL)
                        continue
                    if not line:
                        dst.write(rawL)
                        continue
                    if "=" not in line:
                        logger.warning(
                            f"{path}, line {lineN}:"
                            f" No '=' in {rawL.rstrip()}")
                        dst.write(rawL)
                        continue
                    parts = line.split("=", 1)
                    parts[0] = parts[0].strip()
                    if not parts[0]:
                        logger.warning(
                            f"{path}, line {lineN}:"
                            f" No name before '=' in {rawL.rstrip()}")
                        dst.write(rawL)
                        continue
                    if len(parts) > 1:
                        parts[1] = parts[1].strip()
                    else:
                        # f"{name} =" is null value syntax for conf
                        parts[1] = None
                    if parts[0] in new_settings:
                        encoded = encode_cv(new_settings[parts[0]])
                        if parts[1] == encoded:
                            # no change
                            same += 1
                            dst.write(rawL)
                            del new_settings[parts[0]]
                            continue
                        changed += 1
                        if new_settings[parts[0]] is not None:
                            dst.write(f"{parts[0]} = {encoded}\n")
                        else:
                            dst.write(f"{parts[0]} =\n")
                        del new_settings[parts[0]]
    if new_settings:
        mode = "a" if os.path.isfile(tmp_path) else "w"
        with open(tmp_path, mode, encoding="utf-8") as dst:
            for k, v in new_settings.items():
                if v is not None:
                    dst.write(f"{k} = {encode_cv(v)}\n")
                else:
                    dst.write(f"{k} =\n")  # "{k} = " is null value syntax
    if os.path.isfile(path):
        os.remove(path)
    shutil.move(tmp_path, path)

    echo0(f"Updated {path}: added {added} new line(s), changed {changed}, {same} value(s) already matched")
