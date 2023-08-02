from typing import Optional
from fastapi import Form
from sqlalchemy import func
from ..dependencies import *
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import add_pagination

router = APIRouter(
    # prefix = '/user',
    tags= ['User']
)

app = FastAPI()

@router.post("/users")
def get_all_users(page_num:int = 1, db:Session = Depends(get_db)):
    per_page = 10
    # offset = per_page * (page_num - 1)
    start_id = (page_num  - 1) * (per_page + 1)
    # end_id = start_id + per_page - 1

    users = (
        db.query(models.User)  
        .filter(models.User.id >= start_id)  
        .order_by(models.User.id.asc())   
        .limit(per_page)    
        .all()  
    )

    if not users:
        response_data = {"status": False, "message": "User does not exist."}
        return response_data

    return {"status": True, "message": "Users retrieved successfully", "data": users}

@router.get("/user/{user_id}")
def get_all_users(user_id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        response_data = {"status": False, "message": "User not found."}
        response_content = json.dumps(response_data)
        return Response(content=response_content)
    
    return {"status":True, "message":"User retrieved successfully", "data":user}

@router.get("/user/user_search/{search}")
def user_search(search: str = "", db: Session = Depends(get_db)):
    if search == " ":
        users = db.query(models.User).order_by(models.User.id).all()
    else:
        users = db.query(models.User).filter(func.lower(models.User.name).ilike(f"%{search.lower()}%")).order_by(models.User.id).all()
    if users:
        return {"status": True, "message": "Users retrieved successfully", "data": users}
    else:
        return {"status": False, "message": "Users not found"}
    

