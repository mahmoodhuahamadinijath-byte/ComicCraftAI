# ComicCraftAI

## AI Comic Story Creator

ComicCraftAI is a web application that creates comic-style stories from a user's story idea. It generates multiple story panels, creates AI image prompts, generates comic illustrations using Stable Diffusion, and allows the completed comic to be exported as a PDF.

## Features

- Create a comic from a story prompt
- Choose the main character
- Choose the story setting
- Choose the story tone
- Choose an art style
- Generate 3–8 comic panels
- Generate comic illustrations using Stable Diffusion
- Generate captions, narration, and dialogue
- Preview the completed comic
- Export the comic as a PDF

## Technologies Used

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic

### AI
- Stable Diffusion
- Hugging Face Diffusers
- PyTorch
- NVIDIA CUDA

### Frontend
- HTML
- CSS
- Jinja2 Templates

### Export
- FPDF2

## Project Structure

```text
ComicCraftAI-main/
│
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   ├── config.py
│   │
│   └── services/
│       ├── gemini_flash.py
│       ├── gemini_pro.py
│       ├── image_generator.py
│       ├── layout_builder.py
│       └── exporters.py
│
├── static/
│   ├── panels/
│   └── exports/
│
├── templates/
│   ├── index.html
│   └── comic_preview.html
│
├── tests/
│   └── test_app.py
│
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## Requirements

- Windows
- Python 3.13
- NVIDIA GPU recommended for local image generation
- CUDA-enabled PyTorch
- Internet connection for downloading the Stable Diffusion model the first time

## Installation

### 1. Open the project folder

```powershell
cd "C:\Users\user\OneDrive\Documents\ComicCraftAI-main (2)\ComicCraftAI-main"
```

### 2. Create the virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell asks for permission to run the script, choose **Run once**.

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Install CUDA-enabled PyTorch

For an NVIDIA CUDA GPU:

```powershell
python -m pip install torch==2.11.0 torchvision==0.26.0 torchaudio==2.11.0 --index-url https://download.pytorch.org/whl/cu128
```

### 6. Check GPU support

```powershell
python -c "import torch; print('Torch:', torch.__version__); print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
```

Expected result:

```text
CUDA: True
GPU: NVIDIA GeForce RTX 4050 Laptop GPU
```

## Environment Configuration

Create a `.env` file in the project root.

Example:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

HF_TOKEN=

GEMINI_OUTLINE_MODEL=gemini-2.5-flash
GEMINI_STORY_MODEL=gemini-2.5-pro

IMAGE_PROVIDER=diffusers
IMAGE_MODEL=stable-diffusion-v1-5/stable-diffusion-v1-5

IMAGE_WIDTH=512
IMAGE_HEIGHT=512
IMAGE_STEPS=20
IMAGE_GUIDANCE=7.5
IMAGE_SEED=42

MOCK_IMAGES=false
```

Do not upload or commit real API keys or access tokens to GitHub.

## Run the Application

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start the application:

```powershell
uvicorn app.main:app --port 8002
```

Open the application in your browser:

```text
http://127.0.0.1:8002
```

## Creating a Comic

1. Open ComicCraftAI in your browser.
2. Enter a story prompt.
3. Enter the main character name.
4. Enter the setting.
5. Select the tone.
6. Select the art style.
7. Select the number of panels.
8. Submit the form.
9. Wait while the application generates the comic panels.
10. Review the comic preview.
11. Download the generated PDF.

## AI Image Generation

ComicCraftAI uses the Diffusers library and Stable Diffusion for local image generation.

The image-generation process:

```text
User Story
    ↓
Story Outline
    ↓
Panel Story
    ↓
Image Prompt
    ↓
Stable Diffusion
    ↓
Comic Image
    ↓
Comic Preview
    ↓
PDF Export
```

The Stable Diffusion model is downloaded the first time it is used. Subsequent runs can use the locally cached model.

## Testing

Run the test suite with:

```powershell
pytest
```

You can also check that the Python files contain no syntax errors:

```powershell
python -m py_compile .\app\services\image_generator.py
```

## Stopping the Application

In the terminal running Uvicorn, press:

```text
Ctrl + C
```

## Troubleshooting

### CUDA is False

Check the installed PyTorch version:

```powershell
python -c "import torch; print(torch.__version__)"
```

Then check:

```powershell
python -c "import torch; print(torch.cuda.is_available())"
```

If CUDA is unavailable, verify that the NVIDIA driver is installed and that CUDA-enabled PyTorch is installed.

### PowerShell blocks `.venv`

Run the activation command again:

```powershell
.\.venv\Scripts\Activate.ps1
```

If Windows asks whether to run the script, choose **Run once**.

### Uvicorn keeps restarting

For this project, start without `--reload`:

```powershell
uvicorn app.main:app --port 8002
```

This prevents the development reloader from repeatedly monitoring files inside `.venv`.

### Stable Diffusion takes time

The first image-generation run can take longer because the model may need to be downloaded and loaded into GPU memory.

## License

This project is intended for educational and project-development purposes.
