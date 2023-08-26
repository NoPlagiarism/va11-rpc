from loguru import logger
import httpx
from pydantic import BaseModel, PositiveInt, model_validator, FilePath, conint

from typing import Union, Literal


class WrongDiscordAppID(ValueError):
    pass


class WrongAssetName(ValueError):
    pass


class DiscordModel(BaseModel):
    app_id: PositiveInt

    large_image: str
    large_image_text: str

    new_game_small_image: bool
    new_game_small_image_id: str
    new_game_small_image_text: str

    state: str
    details: str

    pipe: conint(ge=1, le=9)

    @model_validator(mode='after')
    def check_assets(self):
        logger.debug("Validating Discord model")
        response = httpx.get(f"https://discord.com/api/oauth2/applications/{self.app_id}/assets")
        logger.debug(f"Response for assets is {response.status_code}")
        if response.status_code == 404:
            logger.error(f"{self.app_id} failed Discord ID check")
            raise WrongDiscordAppID("Please enter valid Discord ID")
        # Checking assets
        assert response.status_code == 200, f'Unknown Error. Discord response must be ok'
        data = response.json()
        logger.trace(data)
        all_assets = [x['name'] for x in data]
        for name, value in self.model_dump(include={"new_game_small_image_id", "large_image"}).items():
            if name not in all_assets:
                logger.error(f"Didn't found {value} ({name}) in assets.")
                raise WrongAssetName(f"'{value}' does not exist in assets. Please, replace '{value}'")


class Va11FinderModel(BaseModel):
    save_path: Union[Literal[False], FilePath]


class LoopModel(BaseModel):
    timeout_seconds: int


class Va11RPCModel(BaseModel):
    version: Literal[1]
    discord: DiscordModel
    va11finder: Va11FinderModel
    loop: LoopModel
