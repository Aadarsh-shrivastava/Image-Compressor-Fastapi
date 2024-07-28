import asyncio
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
import cloudinary.uploader
import httpx
from db.database import db
import requests
import os
import uuid
import csv

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
    secure=True,
)


def save_image(image_buffer: BytesIO, dir: str) -> str:
    os.makedirs(dir, exist_ok=True)
    output_path = f"{dir}/{str(uuid.uuid4())}.jpg"
    with open(output_path, "wb") as f:
        f.write(image_buffer.getvalue())
    return output_path


def save_image_oncloud(image_buffer: BytesIO, dir: str) -> str:
    response = cloudinary.uploader.upload(image_buffer, folder=dir)
    return response["url"]


def process_images(request_id: str, all_requests):

    data = []
    for sno, req in enumerate(all_requests):

        output_urls = []

        for url in req["input_image_urls"]:

            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            # save_image(BytesIO(response.content), "input")

            img = img.convert("RGB")
            img = img.resize((img.width // 2, img.height // 2))

            output_buffer = BytesIO()
            img.save(output_buffer, format="JPEG", quality=95)
            output_buffer.seek(0)

            output_url = save_image_oncloud(output_buffer, "compressed")
            output_urls.append(output_url)

        db["image_requests"].update_one(
            {"_id": req["_id"]},
            {"$set": {"output_image_urls": output_urls, "status": "completed"}},
        )

        data.append(
            {
                "Serial Number": sno,
                "Product Name": req["product_name"],
                "Input Image Urls": req["input_image_urls"],
                "Output Image Urls": output_urls,
            }
        )

        if req.get("webhook_url"):
            httpx.post(
                req["webhook_url"],
                json={
                    "output_image_urls": output_urls,
                },
            )

    with open("output.csv", "w", newline="") as csvfile:
        fieldnames = [
            "Serial Number",
            "Product Name",
            "Input Image Urls",
            "Output Image Urls",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
