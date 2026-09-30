from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import ValidationError

from .config import get_settings
from .schemas import ComicRequest
from .services.gemini_flash import generate_outline
from .services.gemini_pro import generate_story
from .services.image_generator import generate_image
from .services.layout_builder import build_comic_layout
from .services.exporters import save_pdf


router = APIRouter()

settings = get_settings()

BASE_DIR = Path(__file__).resolve().parent.parent


def get_templates():
    from fastapi.templating import Jinja2Templates

    return Jinja2Templates(
        directory=str(BASE_DIR / "templates")
    )


def create_comic(payload: ComicRequest):

    outline = generate_outline(
        payload.story_prompt,
        payload.panels,
    )

    story = generate_story(
        payload,
        outline,
    )

    image_urls = []

    for panel in story:

        image_url = generate_image(
            panel.image_prompt,
            panel.panel_number,
        )

        image_urls.append(image_url)

    layout = build_comic_layout(
        story,
        image_urls,
    )

    pdf_url = save_pdf(layout)

    return layout, pdf_url


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    templates = get_templates()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.app_name,
        },
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
    panels: int = Form(5),
):

    templates = get_templates()

    try:

        payload = ComicRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
            panels=panels,
        )

        layout, pdf_url = create_comic(payload)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "layout": layout,
                "pdf_url": pdf_url,
                "app_name": settings.app_name,
            },
        )

    except (ValidationError, ValueError) as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "error": str(exc),
                "app_name": settings.app_name,
            },
            status_code=500,
        )


@router.post("/generate-comic/json")
async def generate_comic_json(
    payload: ComicRequest,
):

    try:

        layout, pdf_url = create_comic(payload)

        return JSONResponse(
            {
                "success": True,
                "layout": layout,
                "pdf_url": pdf_url,
            }
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(request: Request):

    templates = get_templates()

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "app_name": settings.app_name,
        },
    )


@router.get("/test-image")
async def test_image(
    prompt: str = (
        "A friendly fox exploring "
        "an enchanted forest, "
        "comic book art"
    ),
):

    try:

        image_url = generate_image(
            prompt,
            0,
        )

        return {
            "success": True,
            "image_url": image_url,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.get("/health")
async def health():

    return {
        "status": "ok",
        "gemini_configured": bool(
            settings.gemini_api_key
        ),
        "image_provider": settings.image_provider,
        "mock_images": settings.mock_images,
    }


@router.get("/download/{filename}")
async def download_pdf(
    filename: str,
):

    if (
        Path(filename).name != filename
        or not filename.endswith(".pdf")
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid filename.",
        )

    file_path = (
        BASE_DIR
        / "static"
        / "exports"
        / filename
    )

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="PDF not found.",
        )

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=filename,
    )
