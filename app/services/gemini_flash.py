import json

from google import genai
from google.genai import types
from pydantic import TypeAdapter

from ..config import get_settings
from ..schemas import ComicRequest, PanelOutline


settings = get_settings()

outline_adapter = TypeAdapter(
    list[PanelOutline]
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


def generate_outline(
    request: ComicRequest
) -> list[PanelOutline]:

    client = get_client()

    prompt = f"""
Create a coherent {request.panels}-panel comic outline.

Story idea:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Story tone:
{request.tone}

Art style:
{request.art_style}

Requirements:

1. Create exactly {request.panels} panels.
2. Keep the same main character throughout.
3. Give the story a clear beginning.
4. Develop the story in the middle.
5. Give the story a satisfying ending.
6. Each panel needs:
   - panel_number
   - title
   - scene_description
   - image_prompt
7. Make image prompts visually detailed.
8. Do not include dialogue inside image_prompt.
9. Keep visual continuity between panels.
"""

    response = client.models.generate_content(

        model=settings.gemini_outline_model,

        contents=prompt,

        config=types.GenerateContentConfig(

            temperature=0.8,

            response_mime_type="application/json",

            response_schema=list[PanelOutline],
        ),
    )

    try:

        data = json.loads(
            response.text
        )

        panels = outline_adapter.validate_python(
            data
        )

    except Exception as exc:

        raise RuntimeError(
            f"Gemini outline response could not be parsed: {exc}"
        ) from exc

    if len(panels) != request.panels:

        raise RuntimeError(
            f"Gemini returned {len(panels)} panels "
            f"instead of {request.panels}."
        )

    return panels
