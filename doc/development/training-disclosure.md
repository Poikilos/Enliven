## buildenliven.py
- https://grok.com/share/c2hhcmQtMg_233dcdbc-ef83-4da9-ae8d-4b8991b430f4
- paste previous commit of utilities/extra/install-ENLIVEN-minetest_game.sh
To include any missing mods from the following bash script, but ignore any features at the binary level such as minetestmapper, and anything specific to manipulating a world such as world.mt. Make the Python script to build upon the more limited minetest_game like the old script, rather than trying to find [not_minetest_game] or makes assumptions from it.
Make the script accept require a path to minetest_game via argparse. Note that "name" is for a mod in the stopgap mods folder obtained via (assume the method already exists and is implemented): import pyenliven; pyenliven.get_mods_stopgap_path(). However, if there is a repo url in the bash script add it (or an updated post-2018 git URL) for the "repo" key; allow 'repo' to be list or string when you make the installMod method (which uses the last string in the list if 'repo' is a list not str; the method should be in a GameBuilder class which takes minetest_game path in the constructor, and automatically makes an ENLIVEN folder in os.path.dirname(sourceGamePath)), and the constructor sets self.gamePath to that, and if there is a different URL in the bash script and there is already a URL in the python script, change the 'repo' entry in the Python script to the list, and place the bash script's url first so it will be lower in priority; and when you complete the install_mod function which takes a single entry from the add_mods list, if the name option is present and the repo path is also present, prefer the repo_path.
- paste previous commit of python script (with edits that don't assume minetest_game)

Ok here is my improved version. Add all of the minetest.conf settings from the bash script. Implement the writing in a separate method, update_conf(path) which appends the line if it is not yet in the file, and uses 'w' mode only if the path doesn't exist yet, otherwise 'a' and reads it to a list of existingLines in stripped form. When checking if the line exists, strip the proposed line and see if it is in the existingLines. Call the method like builder.update_conf(confPath) after build. Add a --conf -c option in argparse. If the argument is not set, set confPath to os.path.join(args.minetest_game_path, "minetest.conf.enliven").
- paste previous LLM output, with some changes to bring back parts of previous version

default the version to "5" (Minetest 5 was formerly called "0.5") and add the switching features between "0.4" and that from the bash script. Add a --minetest-version argument to set it, but only allow "0.4" or "5".

Add real git cloning. If the mod already exists in os.expanduser(f"~/Downloads/{author}/{repo_name}") try pull, otherwise allow the git module's exception to stop the program (don't use any try blocks in the entire program except the one in main) unless the "--offline" argparse argument is set. If the folder doesn't exist and offline is set, raise FileNotFoundError, but if offline is not set, clone the repo. Make install_mod check if the "distributor" key is set in the entry. If not set, 'distributor' is not set, set distributor to "Poikilos" and if 'repo' is set, set author to entry['repo'].split("/")[-2]. Regardless of the author, if os.expanduser(f"~/git/{repo_name}"), use the mod as is (no pull whether offline or not) and show a warning with logger (where logger = getLogger(os.path.split(__file__, 1)). For each repo in gamespec['add_mods'] where the domain is repo.or.cz, set maintainer to "Wuzzy"

## utilities/find-mirror
- https://grok.com/share/c2hhcmQtMg_97b2b713-2623-4109-8001-f4f87970c75a
Write a find-fork Python script that accepts a github username via argparse, and uses the github api to list all repositories for the user such as https://github.com/{user}. For each repository name, see if the repository exists under github.com/mt-mods, github.com/minetest-mods, or github.com/mt-historical in that order. Keep the first one found. Output all repos in json format. Use OrderedDict while doing the collecting. Use indent=2 for json output. write the json to stdout. Write everything else via the logging module. If there are any non-error messages that are not the single json print, write them using logging.info. Set the log level to INFO. Collect all repos, inserting the detected mirror copy in the first index. For example, if a repo named fsg for the given user doesn't exist on any of the three hard-coded forker usernames, but the repo animalworld exists in mt-mods, then stdout should be like:
[
  {
    "name": "fsg",
    "repo": ["https://github.com/Skandarella/fsg"]
  },
  {
    "name": "animalworld",
    "repo": ["https://github.com/mt-mods/animalworld", "https://github.com/Skandarella/animalworld"]
  }
]

call main like sys.exit(main()) and return 0 if good, otherwise nonzero (or raise exception--Don't catch except ones used for logic such as requests.RequestException). Make a MirrorFinder class to hold active code and the given github user. Follow PEP8 such as 79-long lines max, 72 for comments. Add shebang and magic utf-8 comment.