from ..dependencies import *

models.Base.metadata.create_all(bind = engine)

router = APIRouter(
    tags=['Listener']
)

@router.post("/add_listener",status_code=status.HTTP_201_CREATED)
async def add_listener(payload: schemas.AddListener, db: Session = Depends(get_db)):
    
    if len(payload.mobile_no) !=10 or not payload.mobile_no.isdigit():
        response_data = {"status": False, "message": "Invalid phone number"}
        response_content = json.dumps(response_data)
        return Response(content=response_content)

    listener_exist = db.query(models.Listener).filter(models.Listener.email == payload.email).first()
    mobile_exist = db.query(models.Listener).filter(models.Listener.mobile_no == payload.mobile_no).first()

    if listener_exist or mobile_exist:
        response_data = {"status": False, "message": "Listener already exists"}
        response_content = json.dumps(response_data)
        return Response(content=response_content)
    
    if not listener_exist:    
        image_url = await upload_image(payload.image)  # Assuming `image` contains the image data
        payload.image = image_url      
        new_listener = models.Listener(**payload.dict()) 

        # Add validation here       
        if(payload.user_type == 'listener'):            
            db.add(new_listener)

            user = db.query(models.User).filter(models.User.email == payload.email and models.User.phone == payload.mobile_no).first()
            if user:                  
                user_delete = db.query(models.User).filter(models.User.email == payload.email)
                users = user_delete.first()

                if users == None:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"User in user table does not exist")
                
                user_delete.delete(synchronize_session= False)

                db.commit()
                print("User deleted from table")
            db.commit()
            db.refresh(new_listener)
            return {"status":True, "message":"Listener successfully created", "data":new_listener}
        return {"status":False, "message":"Listener not created and is not removed from user table"}
    
@router.get("/listeners")
def get_listeners(db:Session = Depends(get_db)):
    # Check if the 'listeners' table exists in the database
    if not db.query(models.Listener):
        err_msg = "The 'listeners' table does not exist in the database."
        return {"status": False, "message": err_msg}
    
    listener_list = db.query(models.Listener).all()

    if not listener_list:
        response_data = {"status": False, "message": "No listeners found"}
        response_content = json.dumps(response_data)
        return Response(content=response_content)
    
    return {"status":True, "message":"Listeners retrieved successfully", "data":listener_list}

@router.get("/listeners/{id}")
def get_listener_by_Id(id:int, db:Session = Depends(get_db)):
    listener = db.query(models.Listener).filter(models.Listener.id == id).first()

    if not listener:
        response_data = {"status": False, "message": f"Listener with id: {id} does not exist"}
        response_content = json.dumps(response_data)
        return Response(content=response_content)
    
    return {"status":True, "message":"Listener retrieved successfully", "data":listener}





    
    

