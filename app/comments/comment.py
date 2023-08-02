from ..dependencies import *

router = APIRouter(
    tags= ['Comment']
)

@router.post("/add-comment")
def add_comment(payload: schemas.CommentPost, db: Session = Depends(get_db)):
    user_id = payload.user_id

    # user exist in user table
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        return {"status":False, "message":"User with id: {user_id} does not exist"}
    
    else:
        add_comment = models.Comment(**payload.dict())
        db.add(add_comment)

        # See if the post exists
        get_post = db.query(models.Feed).filter(models.Feed.id == payload.post_id).first()

        if not get_post:
            return {"status": False, "message": f"Post with id:{payload.post_id} not found"}
             
        # Increment comment count of the post
        get_post.comment_count += 1

        # Commit the changes to the database
        db.commit()

        # Query the comment object from the database to get the updated version
        db.refresh(add_comment)
        return {"status":True, "message":"Comment added", "data": add_comment}

