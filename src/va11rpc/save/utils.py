import os

from loguru import logger


def check_saves_path(path):
    try:
        for file in os.listdir(path):
            if any((file.startswith("Record of Waifu Wars"), file.startswith("record of waifu wars"),
                    file == "Waifu Preferences.txt", file == "waifu preferences.txt")):
                logger.debug(f"Found {file} in {path}")
                return True
        raise Exception
    except Exception:
        logger.debug(f"Path \"{path}\" failed check")
        return False


def find_va11_saves_path_by_default():
    logger.debug(f"Trying to find default path on {os.name}")
    if os.name == "nt":
        path = os.path.expandvars(r"%LOCALAPPDATA%\VA_11_Hall_A\saves")
    else:
        path = fr"~{os.getlogin()}\.config\VA_11_Hall_A\saves"
    if check_saves_path(path):
        return path
    return None
