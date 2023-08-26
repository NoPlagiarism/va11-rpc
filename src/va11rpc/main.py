from functools import wraps
import os
import sys
import time
import typing

from platformdirs import PlatformDirs
from loguru import logger
from tomlkit.exceptions import ParseError
from pydantic import ValidationError
from pypresence import Presence


from .config import Config
from .save import SaveManager, check_saves_path, find_va11_saves_path_by_default, Save


class AppPaths:
    def __init__(self):
        self._pdir = PlatformDirs('Va11RPC', appauthor='noplagi', ensure_exists=True)
        self.home_dir = self._pdir.user_config_dir
        # self.logs_dir = self._pdir.user_log_dir
        logger.debug(f"Home Dir: {self.home_dir}")
        # logger.debug(f"Home Dir: {self.home_dir}\nLogs Dir: {self.logs_dir}")

        self.config_path = os.path.join(self.home_dir, "config.toml")

    def makedirs(self):
        os.makedirs(self.home_dir)
        # os.makedirs(self.home_dir, self.logs_dir)


def discord_rpc_update_with_ctx(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        save_ctx = kwargs.pop("save_ctx")
        if save_ctx:
            args = list(map(lambda x: x.format(ctx=save_ctx) if isinstance(x, str) else x, args))
            kwargs = dict(zip(kwargs.keys(), tuple(map(lambda x: x.format(ctx=save_ctx) if isinstance(x, str) else x, kwargs.values()))))
        return func(self, *args, **kwargs)
    return wrapped


class Va11Presence:
    def __init__(self):
        self.start = int(time.time())
        self.va11_pid: typing.Optional[int] = None
        self.paths = AppPaths()
        self.config: Config = Config(self.paths.config_path)

        self.discord: typing.Optional[Presence] = None
        self.saves: typing.Optional[SaveManager] = None

        # Initialization
        self.load_config()
        self.load_saves()
        self.create_discord_rpc_client()

    def load_config(self):
        if not self.config.exists:
            self.config.create_new()
            return
        try:
            self.config.load()
            self.config.validate()
        except ParseError as exc:
            logger.opt(exception=exc).error("Config parse error. You can try reset config or contact me")
            exit(-1)
        except ValidationError as exc:
            logger.opt(exception=exc).error("There's something wrong about values. Please edit them to be valid")
            exit(-1)

    def load_saves(self):
        saves_path = self.config.data['va11finder']['save_path']
        if saves_path is False or not check_saves_path(saves_path):
            logger.info("Trying to find VA-11 HALL-A saves path")
            saves_path = find_va11_saves_path_by_default()
            if saves_path is None:
                logger.error("Can't find saves path. Try state in config")
                exit(-1)
            logger.info(f"Found new saves path: {saves_path}")
        logger.debug("Saves path is valid")
        self.saves = SaveManager(path=saves_path)

    def create_discord_rpc_client(self):
        self.discord = Presence(self.config.data['discord']['app_id'])
        self.discord.update = discord_rpc_update_with_ctx(Presence.update)
        logger.info("Connecting to an RPC")
        self.discord.connect()

    def update_rpc_with_newest_save(self):
        self.saves.load()
        newest_save = self.saves.get_newest()
        logger.debug(f"Found newest save with from {newest_save.get_save_date()}")
        self.update_rpc_with_save(newest_save)

    def update_rpc_with_save(self, save: Save):
        params = dict(state=self.config.data['discord']['state'],
                      details=self.config.data['discord']['details'],
                      large_image=self.config.data['discord']['large_image'],
                      large_text=self.config.data['discord']['large_image_text'],
                      save_ctx=save,
                      self=self.discord)
        if self.config.data['discord']['new_game_small_image'] and save.new_game_plus:
            params.update(dict(small_image=self.config.data['discord']['new_game_small_image_id'],
                               small_text=self.config.data['discord']['new_game_small_image_text']))
        self.discord.update(**params)

    def start_rpc(self):
        logger.info("Starting")
        try:
            while True:
                self.update_rpc_with_newest_save()
                logger.trace(f"Sleeping for {self.config.data['loop']['timeout_seconds']}")
                time.sleep(self.config.data['loop']['timeout_seconds'])
        except KeyboardInterrupt:
            logger.info("Bye-Bye")
            exit(1)


def main():
    va11 = Va11Presence()
    va11.start_rpc()


if __name__ == '__main__':
    main()
