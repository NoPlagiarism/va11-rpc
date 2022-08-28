import psutil
from typing import Optional
import os
from saveModel import read_save
import time
from datetime import datetime

USE_DATE_STRING = True


def check_saves_path(path):
    try:
        saves_path = [os.path.join(path, x) for x in os.listdir(path) if "Record of Waifu Wars" in x or "record of waifu wars" in x]
    except FileNotFoundError:
        return False
    if not saves_path:
        return False
    return True


def find_va11_saves_path():
    if os.name == "nt":
        path = r"%LOCALAPPDATA%\VA_11_Hall_A\saves"
    else:
        path = fr"~{os.getlogin()}\.config\VA_11_Hall_A\saves"
    if check_saves_path(path):
        return path
    return None


def find_va11halla_pid(va11_part_name="VA-11 Hall A") -> Optional[int]:
    pid = None
    for process in psutil.process_iter(['pid', 'name']):
        if va11_part_name in process.info["name"]:
            pid = process.info["pid"]
            break
    return pid


def wait_for_va11halla_pid(va11_part_name="VA-11 Hall A", timeout=5) -> int:
    pid = None
    while pid is None:
        pid = find_va11halla_pid(va11_part_name)
        time.sleep(timeout)
    return pid


if USE_DATE_STRING:
    def get_save_date(save_path, only_dt=False):
        save = read_save(save_path)
        save_datetime_string = save["dt_string"]
        save_datestr, save_timestr = save_datetime_string.split(" ")[:2]
        save_date = tuple(map(int, save_datestr.split("/")))
        save_time = tuple(map(int, save_timestr.split(":")))
        save_datetime = datetime(day=save_date[0], month=save_date[1], year=save_date[2],
                                 hour=save_time[0], minute=save_time[1], second=save_time[2])
        if only_dt:
            return save_datetime
        else:
            return save_datetime, save
else:
    get_save_date = os.path.getmtime


if USE_DATE_STRING:
    def get_newest_save(path):
        saves_path = [os.path.join(path, x) for x in os.listdir(path) if "Record of Waifu Wars" in x]
        saves_and_dt = [get_save_date(x) for x in saves_path]
        return max(saves_and_dt, key=lambda x: x[0])[1]
else:
    def get_newest_save(path):
        saves_path = [os.path.join(path, x) for x in os.listdir(path) if "Record of Waifu Wars" in x]
        newest_path = max(saves_path, key=get_save_date)
        return read_save(newest_path)
