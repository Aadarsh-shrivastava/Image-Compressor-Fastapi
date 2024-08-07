# Image Compression and Processing System

This project is an asynchronous image compression and processing system built with FastAPI, MongoDB, and various other tools. The system allows users to upload a CSV file containing image URLs, processes these images asynchronously, and stores the results in a MongoDB database. It also supports webhook notifications for completed requests.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Asynchronous Workers](#asynchronous-workers)
- [System Design](#system-design)
- [License](#license)

## Features

- **CSV Upload:** Upload a CSV file containing image URLs.
- **Asynchronous Processing:** Processes images in the background.
- **Image Compression:** Compresses images and uploads them to Cloudinary.
- **Webhook Notifications:** Sends a notification when processing is complete.
- **Status Tracking:** Check the status of image processing requests.

## Prerequisites

- Python 3.8+
- MongoDB Atlas account
- Cloudinary account

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/image-compression-system.git
    cd image-compression-system
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add your MongoDB and Cloudinary credentials:

    ```env
    MONGO_URI="your_mongodb_connection_string"
    CLOUD_NAME="your_cloudinary_cloud_name"
    API_KEY="your_cloudinary_api_key"
    API_SECRET="your_cloudinary_api_secret"
    ```

## Usage

### API Endpoints

#### 1. Upload CSV

**Endpoint:** `/upload/`  
**Method:** `POST`  
**Parameters:**
- `file`: CSV file containing image URLs (required)
- `webhook_url`: URL to send a POST request upon completion (optional)

**Example:**

```bash
curl -X POST "http://127.0.0.1:8000/upload/" -F "file=@images.csv" -F "webhook_url=http://your-webhook-url.com"