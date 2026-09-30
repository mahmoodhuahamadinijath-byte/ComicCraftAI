from ..schemas import PanelOutline


def generate_outline(
    prompt: str,
    panel_count: int = 6
) -> list[PanelOutline]:

    panel_count = max(3, min(panel_count, 8))

    scenes = [
        (
            "The Beginning",
            f"The story begins with {prompt}. "
            "The main character is introduced and the situation is established.",
            f"{prompt}, story opening, main character introduction"
        ),
        (
            "A New Discovery",
            f"The main character discovers something unexpected while dealing with {prompt}.",
            f"{prompt}, unexpected discovery, curious main character"
        ),
        (
            "The Challenge",
            f"A difficult situation develops in the story about {prompt}. "
            "The main character must decide what to do next.",
            f"{prompt}, dramatic challenge, main character facing difficulty"
        ),
        (
            "The Turning Point",
            f"The situation changes when the main character takes action in the story about {prompt}.",
            f"{prompt}, turning point, action scene, dramatic moment"
        ),
        (
            "The Solution",
            f"The main character finds a way to deal with the main problem in the story about {prompt}.",
            f"{prompt}, solution, heroic moment, successful action"
        ),
        (
            "The Ending",
            f"The story about {prompt} reaches a meaningful conclusion.",
            f"{prompt}, story ending, peaceful conclusion, cinematic final scene"
        ),
        (
            "A Final Moment",
            f"The main character reflects on the events of {prompt} after overcoming the main challenge.",
            f"{prompt}, final reflection, emotional cinematic scene"
        ),
        (
            "The New Beginning",
            f"The experience of {prompt} leads the main character toward a new beginning.",
            f"{prompt}, new beginning, hopeful ending, cinematic comic scene"
        ),
    ]

    panels = []

    for index in range(panel_count):

        title, description, image_prompt = scenes[index]

        panels.append(
            PanelOutline(
                panel_number=index + 1,
                title=title,
                scene_description=description,
                image_prompt=(
                    f"{image_prompt}, "
                    "comic book illustration, "
                    "detailed environment, "
                    "expressive character, "
                    "cinematic composition"
                ),
            )
        )

    return panels
