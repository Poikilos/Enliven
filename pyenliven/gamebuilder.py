import platform
import shutil
import os

from collections import OrderedDict
from logging import getLogger
from typing import Dict

from git import Repo

from pyenliven import MODS_STOPGAP_DIR, PATCHES_SUBGAME_DIR, echo0
from pyenliven.metadata import (
    BASE_ENLIVEN_CONF_SETTINGS,
    gamespec,
    update_conf,
)


logger = getLogger(__name__)


class GameBuilder:
    """Manage creation of a game from scratch.
    See set_gamespec for mod list, minetest.conf settings, etc.

    Attributes:
        more_conf (OrderedDict): minetest.conf settings collected from
            entry(ies) such as from install_mod calls.
    """
    def __init__(self, minetest_game_path: str, minetest_version: str = "5",
                 offline: bool = False, delete: bool = False,
                 pull: bool = True):
        self.source_game = os.path.realpath(minetest_game_path)
        self.target_parent = os.path.dirname(self.source_game)
        self.target_game = os.path.join(self.target_parent, "ENLIVEN")
        self.pull = pull
        if os.path.exists(self.target_game):
            if delete:
                print(f"rm -rf {repr(self.target_game)}")
                shutil.rmtree(self.target_game)
        self.mods_target = os.path.join(self.target_game, "mods")
        self.minetest_version = minetest_version  # "5" or "0.4"
        self.offline = offline
        self.more_conf = OrderedDict()
        self.meta = OrderedDict()
        self.meta['mods'] = OrderedDict()
        self.set_gamespec(gamespec)
        if minetest_version not in ("5", "0.4"):
            raise ValueError("minetest_version must be '5' or '0.4'")

        if not os.path.isdir(self.source_game):
            raise FileNotFoundError(f"minetest_game not found: {self.source_game}")
        if os.path.realpath(self.source_game) == os.path.realpath(self.target_game):
            raise ValueError("source game and target game are both"
                             f" {repr(os.path.realpath(self.source_game))}")
        echo0(f"Building ENLIVEN → {self.target_game}")
        echo0(f"  from base: {self.source_game}")
        echo0(f"  target Minetest compatibility: {self.minetest_version}")
        echo0(f"  offline mode: {self.offline}")

    def set_gamespec(self, _gamespec: Dict):
        """Set all metadata required to build the game.
        The GameBuilder constructor sets self._gamespec to Enliven's
        gamespec from metadata.py, but you can call this method again
        before calling build method(s) to build a different game.

        Args:
            _gamespec (dict): Format:
                - 'name' (str): folder name expected in mods/ or
                  mods_stopgap/
                - 'repo' (Union[str,list[str]]): git URL (str, or
                  list[str] with highest priority last)
                - 'branch' (str): optional branch name
                - 'stopgap' (bool):  True → only use from
                  MODS_STOPGAP_DIR, ignore repo
        """
        self._gamespec = gamespec

    def prepare_target(self):
        """Copy minetest_game → ENLIVEN if needed"""
        if os.path.exists(self.target_game):
            raise FileExistsError(f"Target already exists: {self.target_game}")
            # return
        echo0("Copying minetest_game → ENLIVEN ...")
        print(f"cp -R {repr(self.source_game)} {repr(self.target_game)}")
        shutil.copytree(self.source_game, self.target_game)

    def install_mod(self, entry: Dict[str, any], remove_git=True):
        name = entry.get('name')
        url = entry.get('repo')
        branch = entry.get('branch')
        stopgap = entry.get('stopgap', False)
        settings = entry.get('settings')
        if settings:
            for k, v in settings.items():
                self.more_conf[k] = v

        if not name:
            raise ValueError(f"Missing 'name' in {entry}")
        if name in self.meta['mods']:
            raise KeyError(f"Already installed a mod named {name}")
        dest = os.path.join(self.mods_target, name)

        # 1. Prefer stopgap if exists
        stopgap_src = os.path.join(MODS_STOPGAP_DIR, name)

        if stopgap:
            if os.path.isdir(stopgap_src):
                echo0(f"  [stopgap] {name}")
                if os.path.exists(dest):
                    if os.path.islink(dest):
                        print(f"rm {repr(dest)}  # remove link before installing stopgap")
                        os.remove(dest)
                    else:
                        print(f"rm -rf {repr(dest)}  # remove folder before installing stopgap")
                        shutil.rmtree(dest)
                print(f"cp -R {repr(stopgap_src)} {repr(dest)}  # stopgap_src to dest")
                shutil.copytree(stopgap_src, dest)
                self.meta['mods'][name] = entry
                return
            raise FileNotFoundError(
                f"stopgap={stopgap} but there is no {stopgap_src}")

        # 2. Git clone if we have repo URL(s)
        urls = None
        if url:
            urls = [url] if isinstance(url, str) else url
            url = urls[-1]  # prefer last one
            del urls
            user = entry.get('distributor')
            if not user:
                user = url.split("/")[-2]
            repo_name = url.split("/")[-1].replace(".git", "")
        else:
            repo_name = name

        source_path = os.path.expanduser(f"~/git/{repo_name}")
        if not url and not os.path.isdir(source_path):
            raise ValueError(f"Missing 'repo' for {entry}")
        symlink = False
        if os.path.isdir(source_path):
            # Use the development copy on the computer
            logger.warning(
                "  [local] using local git repo without update:"
                f" {source_path}")
            symlink = True
        else:
            source_path = os.path.expanduser(
                f"~/Downloads/git/{user}/{repo_name}")
            if os.path.isdir(source_path):
                if not self.offline:
                    repo = Repo(source_path)
                    if self.pull:
                        if branch:
                            if hasattr(repo, 'switch'):
                                echo0(f"  [{branch} branch] {source_path}")
                                repo.git.switch(branch)
                            else:
                                echo0(f"  [{branch} branch] Updating remotes for {source_path}")
                                repo.remotes.origin.fetch()
                                # remote_ref = f"origin/{branch}"
                                if branch in repo.heads:
                                    # Just switch to existing local branch
                                    repo.heads[branch].checkout()
                                    echo0(f"    Switched to existing local branch '{branch}'")
                                else:
                                    # Create local branch tracking the remote one + switch to it
                                    remote_head = repo.remotes.origin.refs[branch]   # origin/feature-xyz
                                    new_local = repo.create_head(branch, remote_head.commit)
                                    new_local.set_tracking_branch(remote_head) # optional but recommended
                                    new_local.checkout()
                                    echo0(f"    Created and checked out local branch '{branch}' ← origin/{branch}")

                        echo0(f"  [git] pulling {source_path}")
                        repo.remotes.origin.pull()
                    else:
                        echo0(f"  [--no-pull] using existing {source_path}")
            else:
                if self.offline:
                    raise FileNotFoundError(
                        f"Mod {name} not found in offline mode:"
                        f" {source_path}")
                else:
                    echo0(f"  [git] cloning {url} → {source_path}")
                    Repo.clone_from(url, source_path)
        if os.path.exists(dest):
            raise FileExistsError(f"Remove {dest} first.")
            # shutil.rmtree(dest)
        if symlink:
            if platform.system() == "Windows":
                symlink = False  # since making symlink requires elevation
        if symlink:
            target_is_directory = True
            print(f"ln -s {repr(source_path)} {repr(dest)}  # source_path to dest target_is_directory={target_is_directory}")
            os.symlink(source_path, dest, target_is_directory=target_is_directory)
        else:
            print(f"cp -R {repr(source_path)} {repr(dest)}  # source_path to dest")
            shutil.copytree(source_path, dest)
        exclude = entry.get('exclude')
        if exclude:
            for sub in exclude:
                subPath = os.path.join(dest, sub)
                if os.path.islink(subPath) or os.path.isfile(subPath):
                    print(f"    rm {repr(subPath)}")
                    os.remove(subPath)
                elif os.path.isdir(subPath):
                    print(f"    rm -r {repr(subPath)}")
                    shutil.rmtree(subPath)
                else:
                    logger.warning(
                        f"There is no {subPath} though it"
                        f" was specified in 'exclude' in {entry}")
        # dest_git = os.path.join(dest, ".git")
        # if os.path.isdir(dest_git):
        #     shutil.rmtree(dest_git)
        self.meta['mods'][name] = entry
        if not symlink:
            if remove_git:
                destGit = os.path.join(dest, ".git")
                if os.path.isdir(destGit):
                    print(f"    rm -rf {repr(destGit)}")
                    shutil.rmtree(destGit)

    def remove_mod(self, name: str):
        path = os.path.join(self.mods_target, name)
        if os.path.isdir(path):
            echo0(f"  removing {name}")
            shutil.rmtree(path)

    def apply_remove_list(self):
        for m in self._gamespec.get('remove_mods', []):
            self.remove_mod(m)

    def install_all_mods(self):
        for entry in self._gamespec.get('add_mods', []):
            self.install_mod(entry)

    def write_game_conf(self):
        path = os.path.join(self.target_game, "game.conf")
        with open(path, "w", encoding="utf-8") as f:
            f.write("name = ENLIVEN\n")
            f.write("description = For building immersive worlds using ramping, consistent style, and emphasizing world interaction over menus\n")

    def update_conf(self, path: str):
        """Append settings only if not already present (line-based, stripped comparison)"""
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Collect base settings
        new_settings = BASE_ENLIVEN_CONF_SETTINGS.copy()
        new_settings.update(self.more_conf)

        # Add version-specific player animation setting
        if 'playeranim' in self.meta['mods']:
            # TODO: Make version keys and values in gamespec
            if self.minetest_version == "5":
                new_settings['playeranim.model_version'] = "MTG_4_Nov_2017"
            else:  # "0.4"
                new_settings['playeranim.model_version'] = "MTG_4_Jun_2017"

        if not new_settings:
            return
        update_conf(path, new_settings)
        # desired_set = {line.strip() for line in desired_lines if line.strip()}

    def apply_subgame_patch(self, name, src_parent=None, level=0):
        if src_parent is None:
            src_parent = os.path.join(PATCHES_SUBGAME_DIR, name)
        dst_parent = os.path.join(self.target_game, name)
        if os.path.isdir(src_parent):
            for sub in os.listdir(src_parent):
                src = os.path.join(src_parent, sub)
                dst = os.path.join(dst_parent, sub)
                if os.path.isdir(src):
                    if not os.path.isdir(dst):
                        os.makedirs(dst)
                    self.apply_subgame_patch(
                        os.path.join(name, sub),
                        src_parent=src,
                        level=level+1)
                    continue
                if os.path.isfile(dst):
                    os.remove(dst)
                shutil.copy(src, dst)
        else:
            logger.warning(f"There is no {src_parent},"
                           " so the icon and header will not be patched.")
        # if level == 0:
        echo0(f"Applied overwrite-based patch:\n-{dst_parent}\n+{src_parent}")

    def build(self, conf_path: str = None):
        self.prepare_target()
        self.apply_remove_list()
        self.install_all_mods()
        self.write_game_conf()

        # Default conf path if not provided
        if not conf_path:
            games_path = os.path.dirname(self.target_game)
            engine_path = os.path.dirname(games_path)
            try_conf_path = os.path.join(engine_path, "minetest.conf")
            if os.path.isfile(try_conf_path):
                conf_path = try_conf_path
                print(f"[build] Detected {repr(try_conf_path)}")
            else:
                print(f"[build] There is no {repr(try_conf_path)}")
            if not conf_path:
                print(f"[build] Creating example {repr(try_conf_path)}")
                conf_path = os.path.join(self.target_game, "minetest.conf.enliven")
        else:
            print(f"[build] Using specified {repr(try_conf_path)}")

        self.update_conf(conf_path)
        self.apply_subgame_patch("menu")

        echo0("\nBuild finished.")
        echo0(f"Game location: {self.target_game}")
        echo0(f"       Config: {conf_path}")
        echo0("Next steps:")
        echo0("  • review & edit the minetest.conf file")
        echo0("  • test in Minetest")
