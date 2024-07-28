from pydantic import BaseModel, Field, HttpUrl
from bson import ObjectId
from typing import List
import motor.motor_asyncio


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)


class ImageRequest(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    product_name: str
    input_image_urls: List[str]
    output_image_urls: List[str] = []
    status: str = "pending"
    request_id: str
    webhook_url: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
