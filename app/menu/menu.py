from ..dependencies import *

router = APIRouter(
    tags=['Menu']
)

# code for image
async def upload_image(image:str):
    # Generate a unique filename
    filename = f'icon_' + str(uuid.uuid4()) + '.png' 

    folder_path = f"app/static/images/icons/"

    # Create the local folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Remove any whitespace or padding characters
    base64Data = image.replace(" ", "+").replace("_", "/")
    padding = len(base64Data) % 4
    if padding > 0:
        base64Data += "=" * (4 - padding)

    imageurlDb = f"{folder_path}{filename}"

    # Generate the URL for accessing the file through the browser
    base_url = f"http://127.0.0.1:8000/static/images/icons"
    file_url = f"{base_url}/{filename}"
    
    async with aiofiles.open(imageurlDb, "wb") as file:
        await file.write(base64.b64decode(base64Data))
    
    return file_url

@router.post("/add-menu-item")
async def add_menu_item(payload: schemas.MenuItem, db: Session = Depends(get_db)):
    image_url = await upload_image(payload.icon)  # Assuming `image` contains the image data
    payload.icon = image_url 

    add_item = models.Menu(**payload.dict())

    db.add(add_item)
    db.commit()
    db.refresh(add_item)

    return {"status":True, "message":"Item has been added", "data": add_item}

@router.get("/menu-items")
async def items(db: Session = Depends(get_db)):

    menu_items = db.query(models.Menu).all()

    if menu_items:        
        return {"status":True, "message":"Items retrieved successfully", "data": menu_items}
    else:
        return {"status":False, "message":"No itmes found"}