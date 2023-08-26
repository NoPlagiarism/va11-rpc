from datetime import datetime
import os
from strenum import StrEnum
import re

from loguru import logger

from .save_model import Save, read_save


class DayPhase(StrEnum):
    APT = "apt"      # Apartments
    BREAK = "break"  # Break
    NG = "ng"        # NewGame+


class SaveCTX(Save):
    @property
    def day_phase(self) -> DayPhase:
        return DayPhase[self["dayphase"].upper()]

    @property
    def money(self) -> int:
        return self['jillwallet']

    @property
    def day(self) -> int:
        return self['cur_day']

    @property
    def new_game_plus(self) -> bool:
        return bool(self['ngplus_flag'])

    def get_save_date(self) -> datetime:
        save_datetime_string = self["dt_string"]
        save_date_str, save_time_str = save_datetime_string.split(" ")[:2]
        save_date, save_time = tuple(map(int, save_date_str.split("/"))), tuple(map(int, save_time_str.split(":")))

        return datetime(day=save_date[0], month=save_date[1], year=save_date[2],
                        hour=save_time[0], minute=save_time[1], second=save_time[2])


class SaveManager:
    SAVE_FILENAME_REGEX = re.compile(r"[rR]ecord of [wW]aifu [wW]ars\[(?P<num>\d{1,2})\]\.txt")

    def __init__(self, path, save_cls=None):
        self.save_cls = save_cls if save_cls is not None else SaveCTX
        self.path = path
        self.saves = dict()

    def clear(self):
        self.saves.clear()

    @property
    def dict(self) -> dict:
        return self.saves

    @property
    def list(self) -> list:
        return list(self.saves.values())

    def load(self):
        # TODO: load only updated
        saves = dict()
        for filename in os.listdir(self.path):
            if match := self.SAVE_FILENAME_REGEX.fullmatch(filename):
                saves[int(match.groupdict()['num'])] = read_save(os.path.join(self.path, filename), cls=self.save_cls)
        else:
            if not saves:
                logger.warning(f"No saves data loaded!\nPath: {self.path}")
                return
        self.saves.clear()
        self.saves.update(saves)

    def get_newest(self) -> SaveCTX:
        return max(self.list, key=SaveCTX.get_save_date)
