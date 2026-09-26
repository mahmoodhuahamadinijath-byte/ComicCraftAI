from datetime import datetime
from pathlib import Path

from fpdf import FPDF
from PIL import Image


def make_pdf_safe(
    text: str
) -> str:

    replacements = {
        "—": "-",
        "–": "-",
        "“": '"',
        "”": '"',
        "’": "'",
        "…": "...",
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    return (
        text
        .encode(
            "latin-1",
            "replace"
        )
        .decode("latin-1")
    )


def save_pdf(layout) -> str:

    base_directory = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    export_directory = (
        base_directory
        / "static"
        / "exports"
    )

    export_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = (
        "comic-"
        + datetime.now().strftime(
            "%Y%m%d-%H%M%S"
        )
        + ".pdf"
    )

    output_path = (
        export_directory
        / filename
    )

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    for panel in layout:

        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            18,
        )

        title = (
            f"Panel "
            f"{panel['panel_number']}: "
            f"{panel['title']}"
        )

        pdf.cell(
            0,
            12,
            make_pdf_safe(title),
            ln=True,
        )

        relative_image = (
            panel["image"]
            .replace(
                "/static/",
                ""
            )
            .lstrip("/")
        )

        image_path = (
            base_directory
            / "static"
            / relative_image
        )

        if image_path.exists():

            with Image.open(
                image_path
            ) as image:

                width, height = (
                    image.size
                )

            max_width = 180
            max_height = 105

            scale = min(
                max_width / width,
                max_height / height,
            )

            display_width = (
                width * scale
            )

            display_height = (
                height * scale
            )

            x = (
                210
                - display_width
            ) / 2

            y = 28

            pdf.image(
                str(image_path),
                x=x,
                y=y,
                w=display_width,
                h=display_height,
            )

            pdf.set_y(
                y
                + display_height
                + 7
            )

        else:

            pdf.set_y(40)

            pdf.cell(
                0,
                10,
                "Image unavailable",
                ln=True,
            )

        pdf.set_font(
            "Helvetica",
            "I",
            10,
        )

        pdf.multi_cell(
            0,
            6,
            make_pdf_safe(
                panel[
                    "scene_description"
                ]
            ),
        )

        pdf.ln(2)

        pdf.set_font(
            "Helvetica",
            "B",
            11,
        )

        pdf.multi_cell(
            0,
            6,
            make_pdf_safe(
                "Caption: "
                + panel["caption"]
            ),
        )

        pdf.set_font(
            "Helvetica",
            "",
            11,
        )

        pdf.multi_cell(
            0,
            6,
            make_pdf_safe(
                "Narration: "
                + panel["narration"]
            ),
        )

        if panel["dialogue"]:

            pdf.set_font(
                "Helvetica",
                "B",
                11,
            )

            pdf.multi_cell(
                0,
                6,
                make_pdf_safe(
                    "Dialogue: "
                    + panel["dialogue"]
                ),
            )

    pdf.output(
        str(output_path)
    )

    return (
        f"/static/exports/{filename}"
    )
