from ..dependencies import *

router = APIRouter(
    tags=['Order']
)

# code for image
async def upload_image(image:str):
    # Generate a unique filename
    filename = f'user_' + str(uuid.uuid4()) + '.png' 

    folder_path = f"app/static/images/"

    # Create the local folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Remove any whitespace or padding characters
    base64Data = image.replace(" ", "+").replace("_", "/")
    padding = len(base64Data) % 4
    if padding > 0:
        base64Data += "=" * (4 - padding)

    imageurlDb = f"{folder_path}{filename}"

    # Generate the URL for accessing the file through the browser
    base_url = f"http://127.0.0.1:8000/static/images"
    file_url = f"{base_url}/{filename}"
    
    async with aiofiles.open(imageurlDb, "wb") as file:
        await file.write(base64.b64decode(base64Data))
    
    return file_url

@router.post("/add-order")
async def add_comment(payload: schemas.Order, db: Session = Depends(get_db)):
    image_url = await upload_image(payload.requestor_img)  # Assuming `image` contains the image data
    payload.requestor_img = image_url 

    add_order = models.Order(**payload.dict())

    db.add(add_order)

    # Commit the changes to the database
    db.commit()

    # Query the comment object from the database to get the updated version
    db.refresh(add_order)

    return {"status":True, "message":"Order added", "data": add_order}

@router.get("/orders")
def get_orders(db:Session = Depends(get_db)):
    # Check if the 'listeners' table exists in the database
    if not db.query(models.Order):
        err_msg = "The 'order' table does not exist in the database."
        return {"status": False, "message": err_msg}
    
    order_list = db.query(models.Order).all()

    if not order_list:
        return {"status":False, "message":"There are no orders"}
    else:
        return {"status":True, "message":"Orders retrieved successfully", "data":order_list}


