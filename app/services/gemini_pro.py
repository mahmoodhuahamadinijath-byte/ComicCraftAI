import json

from google import genai
from google.genai import types
from pydantic import TypeAdapter

from ..config import get_settings
from ..schemas import (
    ComicRequest,
    PanelOutline,
    PanelStory,
)


settings = get_settings()

story_adapter = TypeAdapter(
    list[PanelStory]
)


def get_client():

    if not settings.gemini_api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add it to your .env file."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_story(
    request: ComicRequest,
    outline: list[PanelOutline]
) -> list[PanelStory]:

    client = get_client()

    outline_json = json.dumps(
        [
            panel.model_dump()
            for panel in outline
        ],
        ensure_ascii=False,
    )

    prompt = f"""
Expand the following comic outline into a complete comic story.

User story:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Comic outline:
{outline_json}

For every panel generate:

- panel_number
- title
- scene_description
- image_prompt
- caption
- narration
- dialogue

Requirements:

1. Maintain character continuity.
2. Maintain location continuity.
3. Make the story easy to understand.
4. Keep dialogue natural.
5. Keep narration concise.
6. Make each image prompt visually detailed.
7. Do not put written words inside image prompts.
8. Do not generate speech bubbles inside the image.
9. Return exactly the same number of panels as the outline.
"""

    response = client.models.generate_content(

        model=settings.gemini_story_model,

        contents=prompt,

        config=types.GenerateContentConfig(

            temperature=0.9,

            response_mime_type="application/json",

            response_schema=list[PanelStory],
        ),
    )

    try:

        data = json.loads(
            response.text
        )

        panels = story_adapter.validate_python(
            data
        )

    except Exception as exc:

        raise RuntimeError(
            f"Gemini story response could not be parsed: {exc}"
        ) from exc

    if len(panels) != len(outline):

        raise RuntimeError(
            "Gemini story response does not contain "
            "the expected number of panels."
        )

    return panels
