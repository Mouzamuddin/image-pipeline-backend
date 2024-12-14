from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4
from dotenv import load_dotenv

import os
import traceback

app = FastAPI()
load_dotenv()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://imagepipelinemask.netlify.app"],  # React front-end origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)
db = client["image_store"]
collection = db["images"]


IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")

@app.get("/")
async def root():
    return {"message": "Welcome to the Image Upload API"}


#     original_image: UploadFile,
#     mask_image: UploadFile,
#     description: str = Form(...)
# ):
#     try:
#         # Save the uploaded files
#         original_path = f"images/{uuid4()}_{original_image.filename}"
#         mask_path = f"images/{uuid4()}_{mask_image.filename}"

#         # Save original image
#         with open(original_path, "wb") as f:
#             f.write(await original_image.read())

#         # Save mask image
#         with open(mask_path, "wb") as f:
#             f.write(await mask_image.read())

#         # Metadata for the response
#         image_data = {
#             "original_image_url": f"{request.base_url}images/{os.path.basename(original_path)}",
#             "mask_image_url": f"{request.base_url}images/{os.path.basename(mask_path)}",
#             "description": description,
#         }

#         return JSONResponse(
#             content={"message": "Images uploaded successfully", "data": image_data},
#             status_code=201,
#         )

#     except Exception as e:
#         traceback.print_exc()
#         return JSONResponse(content={"error": str(e)}, status_code=500)
from bson import ObjectId

@app.post("/upload/")
async def upload_image(
    request: Request,
    original_image: UploadFile,
    mask_image: UploadFile,
    description: str = Form(...),
):
    try:
        original_path = f"images/{uuid4()}_{original_image.filename}"
        mask_path = f"images/{uuid4()}_{mask_image.filename}"

        with open(original_path, "wb") as f:
            f.write(await original_image.read())

        with open(mask_path, "wb") as f:
            f.write(await mask_image.read())

        image_data = {
            "original_image_url": f"{request.base_url}images/{os.path.basename(original_path)}",
            "mask_image_url": f"{request.base_url}images/{os.path.basename(mask_path)}",
            "description": description,
        }

        insert_result = await collection.insert_one(image_data)
        image_data["_id"] = str(insert_result.inserted_id)  

        return JSONResponse(
            content={"message": "Images uploaded and metadata stored successfully", "data": image_data},
            status_code=201,
        )

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/images/{image_id}")
async def get_image_metadata(image_id: str):
    """Endpoint to fetch image metadata by ID."""
    try:
        return JSONResponse(content={"message": "Metadata retrieval not implemented."}, status_code=200)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
