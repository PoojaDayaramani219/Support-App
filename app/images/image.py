from ..dependencies import *

router = APIRouter(
    prefix = '/image',
    tags= ['Images']
)

@router.post("/upload_image")
async def image_upload(image:str):
    # Use the await keyword when calling the upload_image function: 
    # Since upload_image is an asynchronous function, you need to use the await keyword when calling it to properly await its completion.
    imageurl = await upload_image(image)
    return {"status":"True", "message": "Image uploaded successfully", "data": imageurl}

@router.post("/download-image")
async def download_image(image: UploadFile = File(...)):
    try:
        # Create a path to save the image
        # save_path = "E:\Resumes"
        save_path = "app/images"
        os.makedirs(save_path, exist_ok=True)
        
        # Save the image to the specified path
        image_path = os.path.join(save_path, image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        return {"message": "Image downloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))