from typing import List

from pydantic import BaseModel, Field, field_validator


class ComicRequest(BaseModel):

    story_prompt: str = Field(
        ...,
        min_length=10,
        max_length=2000
    )

    character_name: str = Field(
        ...,
        min_length=1,
        max_length=80
    )

    setting: str = Field(
        ...,
        min_length=1,
        max_length=200
    )

    tone: str = Field(
        ...,
        min_length=1,
        max_length=80
    )

    art_style: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    panels: int = Field(
        default=5,
        ge=3,
        le=8
    )

    @field_validator("*")
    @classmethod
    def strip_values(cls, value):

        if isinstance(value, str):

            value = value.strip()

            if not value:
                raise ValueError(
                    "This field cannot be empty."
                )

        return value


class PanelOutline(BaseModel):

    panel_number: int

    title: str

    scene_description: str

    image_prompt: str


class PanelStory(BaseModel):

    panel_number: int

    title: str

    scene_description: str

    image_prompt: str

    caption: str

    narration: str

    dialogue: str


class ComicResponse(BaseModel):

    panels: List[PanelStory]

    pdf_url: str
