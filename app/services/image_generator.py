from pathlib import Path

import hashlib
import re

from PIL import Image
from PIL import ImageDraw


from ..config import get_settings


settings = get_settings()

PIPELINE = None


def create_filename(
    text: str,
    panel_number: int
) -> str:

    slug = re.sub(
        r"[^a-zA-Z0-9]+",
        "-",
        text
    )

    slug = slug.strip("-").lower()

    slug = slug[:45]

    if not slug:
        slug = "panel"

    digest = hashlib.sha1(
        text.encode("utf-8")
    ).hexdigest()[:8]

    return (
        f"panel-{panel_number}-"
        f"{slug}-{digest}.png"
    )


def create_mock_image(
    prompt: str,
    path: Path,
    panel_number: int
):

    image = Image.new(
        "RGB",
        (
            settings.image_width,
            settings.image_height,
        ),
        "white",
    )

    draw = ImageDraw.Draw(
        image
    )

    draw.rectangle(
        (
            8,
            8,
            settings.image_width - 8,
            settings.image_height - 8,
        ),
        outline="black",
        width=5,
    )

    draw.text(
        (25, 25),
        f"COMIC PANEL {panel_number}",
        fill="black",
    )

    text = prompt[:300]

    lines = []

    for index in range(
        0,
        len(text),
        55
    ):

        lines.append(
            text[index:index + 55]
        )

    draw.text(
        (25, 90),
        "\n".join(lines),
        fill="black",
    )

    image.save(path)


def load_pipeline():

    global PIPELINE

    if PIPELINE is not None:
        return PIPELINE

    import torch

    from diffusers import (
        StableDiffusionPipeline
    )

    if torch.cuda.is_available():

        dtype = torch.float16

    else:

        dtype = torch.float32

    kwargs = {
        "torch_dtype": dtype
    }

    if settings.hf_token:

        kwargs["token"] = settings.hf_token

    PIPELINE = StableDiffusionPipeline.from_pretrained(
        settings.image_model,
        **kwargs,
    )

    device = (
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    PIPELINE = PIPELINE.to(
        device
    )

    if device == "cuda":

        PIPELINE.enable_attention_slicing()

    return PIPELINE


def generate_image(
    prompt: str,
    panel_number: int
) -> str:

    output_directory = (
        Path(__file__)
        .resolve()
        .parents[2]
        / "static"
        / "panels"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = create_filename(
        prompt,
        panel_number,
    )

    output_path = (
        output_directory
        / filename
    )

    # Development/testing mode
    if settings.mock_images:

        create_mock_image(
            prompt,
            output_path,
            panel_number,
        )

        return (
            f"/static/panels/{filename}"
        )

    try:

        pipeline = load_pipeline()

        generator = None

        try:

            import torch

            generator = (
                torch.Generator(
                    device=pipeline.device
                ).manual_seed(
                    settings.image_seed
                    + panel_number
                )
            )

        except Exception:

            generator = None

        result = pipeline(

            prompt=prompt,

            width=settings.image_width,

            height=settings.image_height,

            num_inference_steps=settings.image_steps,

            guidance_scale=settings.image_guidance,

            generator=generator,
        )

        image = result.images[0]

        image.save(
            output_path
        )

    except Exception as exc:

        raise RuntimeError(
            "Stable Diffusion image generation failed. "
            f"Original error: {exc}"
        ) from exc

    return (
        f"/static/panels/{filename}"
    )
