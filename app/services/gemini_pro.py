from ..schemas import ComicRequest, PanelOutline, PanelStory


def generate_story(
    request: ComicRequest,
    outline: list[PanelOutline],
) -> list[PanelStory]:

    panels = []

    for panel in outline:

        dialogue = create_dialogue(
            request=request,
            panel=panel,
        )

        panel_story = PanelStory(
            panel_number=panel.panel_number,
            title=panel.title,
            scene_description=panel.scene_description,
            image_prompt=(
                f"{panel.image_prompt}, "
                f"main character: {request.character_name}, "
                f"setting: {request.setting}, "
                f"tone: {request.tone}, "
                f"art style: {request.art_style}, "
                "comic book illustration, "
                "detailed background, "
                "cinematic composition, "
                "consistent character appearance, "
                "no text, no letters, no words, "
                "no speech bubbles"
            ),
            caption=panel.title,
            narration=panel.scene_description,
            dialogue=(
                f"{request.character_name}: "
                f"{dialogue}"
            ),
        )

        panels.append(panel_story)

    return panels


def create_dialogue(
    request: ComicRequest,
    panel: PanelOutline,
) -> str:

    if panel.panel_number == 1:
        return (
            f"I can't believe this is happening "
            f"here in {request.setting}."
        )

    if panel.panel_number == 2:
        return (
            "Something is not right. "
            "I need to understand what is happening."
        )

    if panel.panel_number == 3:
        return (
            "This is getting difficult, "
            "but I can't give up now."
        )

    if panel.panel_number == 4:
        return (
            "Wait! I think I've found the answer."
        )

    if panel.panel_number == 5:
        return (
            "I finally did it! "
            "I knew I could solve this."
        )

    if panel.panel_number >= 6:
        return (
            "What an incredible adventure. "
            "I'll never forget this experience."
        )

    return (
        f"I must keep going here in {request.setting}."
    )
