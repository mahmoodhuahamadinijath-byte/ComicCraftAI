from pathlib import Path
from uuid import uuid4

from huggingface_hub import InferenceClient

from ..config import get_settings


BASE_DIR = Path(__file__).resolve().parents[2]

PANEL_DIR = BASE_DIR / "static" / "panels"
PANEL_DIR.mkdir(parents=True, exist_ok=True)


def generate_image(prompt: str, panel_number: int) -> str:

    settings = get_settings()

    if not settings.hf_token:
        raise RuntimeError(
            "HF_TOKEN is missing. Add your Hugging Face token to .env"
        )

    filename = f"panel_{panel_number}_{uuid4().hex[:8]}.png"

    output_path = PANEL_DIR / filename

    client = InferenceClient(
        token=settings.hf_token
    )

    final_prompt = f"""
Create a high-quality comic book illustration.

Story:
{prompt}

Visual requirements:
- colorful comic book artwork
- cinematic composition
- detailed environment
- expressive characters
- consistent character appearance
- dramatic lighting
- professional digital illustration
- no text
- no letters
- no words
- no captions
- no speech bubbles
- no watermark
"""

    print(f"Generating AI image for panel {panel_number}...")

    image = client.text_to_image(
        prompt=final_prompt,
        model="black-forest-labs/FLUX.1-schnell",
    )

    image.save(output_path)

    print(
        f"AI image created successfully: {output_path}"
    )

    return f"/static/panels/{filename}"
