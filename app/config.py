from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Gemini
    gemini_api_key: str = ""

    # Hugging Face
    hf_token: str = ""

    # Gemini models
    gemini_outline_model: str = "gemini-2.5-flash"
    gemini_story_model: str = "gemini-2.5-pro"

    # Image generation
    image_provider: str = "diffusers"

    image_model: str = (
        "stable-diffusion-v1-5/stable-diffusion-v1-5"
    )

    image_width: int = 512
    image_height: int = 512
    image_steps: int = 20
    image_guidance: float = 7.5
    image_seed: int = 42

    # Development mode
    mock_images: bool = False

    app_name: str = "ComicCraft"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
