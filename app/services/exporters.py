from pathlib import Path
from uuid import uuid4

from fpdf import FPDF


BASE_DIR = Path(__file__).resolve().parents[2]
EXPORT_DIR = BASE_DIR / "static" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


class ComicPDF(FPDF):

    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(
            0,
            10,
            "COMICCRAFTAI",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
        )

        self.set_font("Helvetica", "", 10)
        self.cell(
            0,
            7,
            "AI Comic Story Creator",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
        )

        self.ln(5)

    def add_wrapped_text(
        self,
        text: str,
        font_size: int = 11,
        bold: bool = False,
    ):
        style = "B" if bold else ""

        self.set_font("Helvetica", style, font_size)

        text = str(text)
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")

        words = text.split(" ")
        safe_words = []

        for word in words:
            if len(word) > 60:
                for i in range(0, len(word), 30):
                    safe_words.append(word[i:i + 30])
            else:
                safe_words.append(word)

        safe_text = " ".join(safe_words)

        self.multi_cell(
            0,
            7,
            safe_text,
            new_x="LMARGIN",
            new_y="NEXT",
        )

        self.ln(2)


def save_pdf(layout) -> str:

    filename = f"comic_{uuid4().hex[:8]}.pdf"
    output_path = EXPORT_DIR / filename

    pdf = ComicPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    for index, panel in enumerate(layout):

        # Start a page for every panel
        pdf.add_page()

        # Panel heading
        pdf.set_font("Helvetica", "B", 14)

        pdf.multi_cell(
            0,
            8,
            f"Panel {panel['panel_number']}: {panel['title']}",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.ln(3)

        # Image
        image_url = panel.get("image", "")

        if image_url:

            image_path = (
                BASE_DIR
                / image_url.lstrip("/").replace("/", "\\")
            )

            if image_path.exists():

                try:
                    pdf.image(
                        str(image_path),
                        x=15,
                        w=180,
                    )

                    pdf.ln(5)

                except Exception:
                    pass

        # Scene
        pdf.add_wrapped_text(
            "Scene:",
            font_size=11,
            bold=True,
        )

        pdf.add_wrapped_text(
            panel.get("scene_description", ""),
            font_size=10,
        )

        # Caption
        pdf.add_wrapped_text(
            "Caption:",
            font_size=11,
            bold=True,
        )

        pdf.add_wrapped_text(
            panel.get("caption", ""),
            font_size=10,
        )

        # Narration
        pdf.add_wrapped_text(
            "Narration:",
            font_size=11,
            bold=True,
        )

        pdf.add_wrapped_text(
            panel.get("narration", ""),
            font_size=10,
        )

        # Dialogue
        if panel.get("dialogue"):

            pdf.add_wrapped_text(
                "Dialogue:",
                font_size=11,
                bold=True,
            )

            pdf.add_wrapped_text(
                panel.get("dialogue", ""),
                font_size=10,
            )

    pdf.output(str(output_path))

    return f"/static/exports/{filename}"
