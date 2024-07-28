import motor.motor_asyncio
import os

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_URL',default='mongodb://localhost:27017'))
db = client.image_processing_db