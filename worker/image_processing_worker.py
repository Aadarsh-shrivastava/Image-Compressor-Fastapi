import asyncio
from concurrent.futures import ThreadPoolExecutor
from services.process_image import process_images
from db.database import db

async def fetch_requests(request_id: str):
    return await db["image_requests"].find({"request_id": request_id}).to_list(None)

async def image_processing_worker(request_id: str):
    all_requests = await fetch_requests(request_id)
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, process_images, request_id, all_requests)
