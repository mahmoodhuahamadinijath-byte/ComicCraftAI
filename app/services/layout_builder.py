def build_comic_layout(
    story_panels,
    image_urls
):

    layout = []

    for panel, image_url in zip(
        story_panels,
        image_urls
    ):

        layout.append({

            "panel_number":
                panel.panel_number,

            "title":
                panel.title,

            "image":
                image_url,

            "scene_description":
                panel.scene_description,

            "caption":
                panel.caption,

            "narration":
                panel.narration,

            "dialogue":
                panel.dialogue,

            "image_prompt":
                panel.image_prompt,
        })

    return layout
