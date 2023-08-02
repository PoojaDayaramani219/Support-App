from lib2to3.pgen2 import driver
import uuid
import aiofiles
from fastapi import APIRouter, FastAPI, HTTPException, Depends, status
from app.database import get_db, engine
from fastapi import APIRouter, Request, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import EmailStr
import json, re
from . import schemas, models
from fastapi import File, UploadFile
import base64
import os
import shutil
from bs4 import BeautifulSoup
from datetime import datetime
import requests

# code for image
async def upload_image(image:str(2000)):
    
    # allowed_extensions = {"png", "jpg", "jpeg"}
    # ext = file.filename.split(".")[-1]
    # if ext.lower() not in allowed_extensions:
    #     raise HTTPException(status_code=400, detail="Only .png, .jpg and .jpeg format allowed!")

    f_type = "listeners"
    print(f_type)

    # Specify the path to the local folder
    if f_type == "posts":
        folder_type = "posts"
    elif f_type == "listeners":
        folder_type = "listeners"
    else:
        folder_type = "others"

    # Generate a unique filename
    filename = f'{folder_type}_' + str(uuid.uuid4()) + '.png' 

    folder_path = f"app/static/images/{folder_type}/"

    # Create the local folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Remove any whitespace or padding characters
    base64Data = image.replace(" ", "+").replace("_", "/")
    padding = len(base64Data) % 4
    if padding > 0:
        base64Data += "=" * (4 - padding)

    imageurlDb = f"{folder_path}{filename}"

    # Generate the URL for accessing the file through the browser
    base_url = f"http://127.0.0.1:8000/static/images/{folder_type}"
    file_url = f"{base_url}/{filename}"
    
    async with aiofiles.open(imageurlDb, "wb") as file:
        await file.write(base64.b64decode(base64Data))
    
    return file_url