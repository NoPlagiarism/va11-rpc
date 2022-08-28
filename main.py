from pypresence import Presence
from saveModel import Save, read_save
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
import time
from utils import wait_for_va11halla_pid, get_newest_save, find_va11halla_pid, check_saves_path, find_va11_saves_path
from psutil import pid_exists
import configparser
import os


class Va11SavesNotFound(Exception):
    def __str__(self):
        return "Please edit SavePath string to actual VA_11_Hall_A saves folder"


class Va11Presence(Presence):
    def __init__(self, *args, **kwargs):
        super(Va11Presence, self).__init__(*args, **kwargs)
        self.start = time.time()

    def update_from_save(self, save: Save):
        self.update(start=int(self.start),
                    large_image="panz_san_jill",  # Tnx to reddit user u/PanzSan
                    large_text="NG+" if save["ngplus_flag"] else "Anna",
                    state="Day " + str(save["cur_day"]),
                    details="Very Good Bartender VN")


class SaveDirHandler(RegexMatchingEventHandler):
    def __init__(self, *args, callback, **kwargs):
        super(SaveDirHandler, self).__init__(*args, **kwargs)
        self.callback = callback

    def on_created(self, event):
        time.sleep(0.5)
        save = read_save(event.src_path)
        self.callback(save)

    def on_modified(self, event):
        time.sleep(0.5)
        save = read_save(event.src_path)
        self.callback(save)


def save_config(config):
    with open("config.ini", encoding="utf-8", mode="w+") as f:
        config.write(f)


def main():
    config = configparser.ConfigParser(inline_comment_prefixes="#", comment_prefixes=('#',), allow_no_value=True)
    config.read("config.ini")

    save_path = os.path.expanduser(config.get("DEFAULT", "SavePath", raw=True))
    discord_app_id = config.getint("DEFAULT", "DiscordAppId")
    path_find_attempt_accepted = bool(config.getint("DONOTEDIT", "PathFindAttemptAccepted"))

    if not path_find_attempt_accepted:
        if not check_saves_path(save_path):
            path = find_va11_saves_path()
            if path is not None:
                save_path = path
                config.set("DEFAULT", "SavePath", save_path)
        config.set("DONOTEDIT", "PathFindAttemptAccepted", "1")
        save_config(config)
    elif not check_saves_path(save_path):
        raise Va11SavesNotFound

    presence = Va11Presence(discord_app_id)
    presence.connect()
    try:
        newest = get_newest_save(save_path)
    except FileNotFoundError as e:
        raise Va11SavesNotFound
    presence.update_from_save(newest)
    event_handler = SaveDirHandler([".*[rR]ecord of [wW]aifu [wW]ars\[\d{1,2}\]\.txt"], callback=presence.update_from_save)
    observer = Observer()
    try:
        observer.schedule(event_handler, save_path, recursive=False)
        observer.start()
    except FileNotFoundError as e:
        raise Va11SavesNotFound
    while True:
        va11_pid = find_va11halla_pid()
        if va11_pid is None:
            print("Waiting for VA-11 HALL-A to start")
            va11_pid = wait_for_va11halla_pid()
        while pid_exists(va11_pid):
            try:
                while observer.is_alive() and pid_exists(va11_pid):
                    observer.join(3)
            finally:
                observer.stop()
                observer.join()


if __name__ == '__main__':
    try:
        main()
    except Va11SavesNotFound as e:
        print("ERROR: " + str(e))
        exit(-1)
    except KeyboardInterrupt:
        print("Bye :>")
