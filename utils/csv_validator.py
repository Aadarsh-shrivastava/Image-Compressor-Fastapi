import csv, re
from fastapi import HTTPException, UploadFile


def validate_csv(file: UploadFile):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format")

    content = file.file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(content)

    required_columns = ["Serial Number", "Product Name", "Input Image Urls"]

    if not all(column in reader.fieldnames for column in required_columns):
        raise HTTPException(
            status_code=400, detail="CSV does not contain the required columns"
        )

    for row in reader:
        try:
            int(row["Serial Number"])
        except ValueError:
            raise HTTPException(
                status_code=400, detail=f"Invalid Serial Number: {row['Serial Number']}"
            )

        if not row["Product Name"].strip():
            raise HTTPException(status_code=400, detail="Product Name cannot be empty")

    return content
