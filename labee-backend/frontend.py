

import gemini_service
import data_processing
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import gemini_service
import data_processing

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = gemini_service.apikey()
app = FastAPI()


def picload(files):
    images = []

    for file in files:
        contents = file.file.read()
        images.append(contents)

    return images


def exnum(report):
    return int(report)


@app.post("/analyze")
async def analyze(
    report: str = Form(...),
    images: list[UploadFile] = File(...)
):

    print("\n========== NEW REQUEST ==========")

    print("Report received:", report)

    print("Number of images received:", len(images))
    for img in images:
        print("Image filename:", img.filename)

    # učitaj slike
    imgs = picload(images)

    print("Images converted to bytes:", len(imgs))

    if len(imgs) > 0:
        with open("debug_image.png", "wb") as f:
            f.write(imgs[0])
        print("Saved first image as debug_image.png")

    # koji je report
    exr = exnum(report)

    print("Exercise ID:", exr)

    # Gemini analiza
    response = data_processing.analysis(client, imgs, exr)

    print("\nGemini raw response:")
    print(response.text)

    # obrada rezultata
    result = data_processing.func[exr](response)

    print("\nProcessed result:")
    print(result)

    # VRATI FRONTENDU
    return JSONResponse(content=result)