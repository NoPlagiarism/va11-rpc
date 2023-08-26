import os

import tomlkit

from .models import Va11RPCModel


DEFAULT_CONFIG = """
version = 1

[discord]
# You can get your own app_id. Don't forget to load assets
app_id = 926111385182687282
# It's 2 description texts
state = "Bartending on day {ctx.day}"
details = "Time to mix drinks and change lives"
# Large Image
large_image = "panz_san_jill"
large_image_text = "VA-11 Hall-A: Cyberpunk Bartender Action"
# It's New Game plus
new_game_small_image = true
new_game_small_image_id = "ng_pixel_heart"
new_game_small_image_text = "NG+"

[va11finder]
# Responsible for reading saves
save_path = false

[loop]
timeout_seconds=15
"""

class Config:
    def __init__(self, path):
        self.path = path
        self.data = None

    @property
    def loaded(self) -> bool:
        return self.data is not None

    @property
    def exists(self) -> bool:
        return os.path.exists(self.path)

    def load(self):
        with open(self.path, mode="r") as f:
            self.data = tomlkit.load(f)

    def loads(self, data_string):
        self.data = tomlkit.loads(data_string)

    def validate(self):
        return Va11RPCModel.model_validate_json(self.dump_json())

    def create_new(self):
        self.data = tomlkit.loads(DEFAULT_CONFIG)
        self.save()

    def save(self):
        with open(self.path, mode="w+") as f:
            tomlkit.dump(self.data, f)

    def dump_json(self):
        return self.data.value
