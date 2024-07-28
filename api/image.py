from fastapi import APIRouter, Form, UploadFile, File, HTTPException, BackgroundTasks
import csv
import uuid
from db.database import db
from db.images_model import ImageRequest
from utils.csv_validator import validate_csv
from worker.image_processing_worker import image_processing_worker

router = APIRouter()


@router.post("/upload/")
async def upload_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    webhook_url: str = Form(None),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format")

    reader = csv.DictReader(validate_csv(file))

    request_id = str(uuid.uuid4())
    requests = []

    for row in reader:
        requests.append(
            ImageRequest(
                product_name=row["Product Name"],
                input_image_urls=row["Input Image Urls"].split(","),
                request_id=request_id,
                webhook_url=webhook_url if webhook_url else ""
            ).model_dump(by_alias=True)
        )

    await db["image_requests"].insert_many(requests)

    background_tasks.add_task(image_processing_worker, request_id)

    return {"request_id": request_id}


@router.get("/status/{request_id}")
async def get_status(request_id: str):
    requests = await db["image_requests"].find({"request_id": request_id}).to_list(None)
    output_urls={}
    for request in requests:
        output_urls[request['product_name']]=request['output_image_urls']
        
    request = requests[-1]
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if(request["status"]=='completed'):
        return {"request_id": request_id, "status": request["status"],"output_urls":output_urls}
    
    return {"request_id": request_id, "status": request["status"]}
