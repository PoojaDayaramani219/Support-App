from lib2to3.pgen2 import driver
import shutil

from sqlalchemy import JSON
from sqlalchemy import and_
from ..dependencies import *

router = APIRouter(
    tags= ['Feed']
)


@router.post("/add-post/{user_id}")
async def create_post(user_id:int, payload:schemas.Feed, db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        return {"status":False, "message":"User does not exist"}
    else:
        if (not payload.content) and (not payload.feed_img):
            return {"status":False, "message":"Any content or image is required."}
        # elif payload.content or payload.feed_img:
        #         return {"status":False, "message":"You can enter any one among content or image."}
        else:
    
            imageurl = await upload_image(payload.feed_img)

            new_feed = models.Feed(
                user_id = user_id,
                content = payload.content,
                feed_img = imageurl
            )

            if new_feed:
                db.add(new_feed)
                db.commit()
                db.refresh(new_feed)
                return {"status":True, "message":"Post added successfully", "data": new_feed}
            else:
                return {"status":False, "message":"Post not added"}
                
@router.get("/posts")
def all_posts(db:Session = Depends(get_db)):     
    posts = db.query(models.Feed).all()

    if not posts:
        return {"status":False, "message":"Posts not retrieved."}
    else:
        return {"status":True, "message":"Posts retrieved successfully", "data": posts}
    
    
@router.get("/post/{post_id}")
def post_by_id(post_id: int, db: Session = Depends(get_db)):
    get_post = db.query(models.Feed).filter(models.Feed.id == post_id).first()

    if not get_post:
        # f is used for formatted string by which we can get dynamic post_id 
        return {"status":False, "message": f"Post with id: {post_id} not found."}
    else:
        return {"status":True, "message":"Posts retrieved successfully", "data": get_post}
    
    
@router.post("/like-post")
def like_post(payload: schemas.LikePost, db: Session = Depends(get_db)):

    # parameterized functn to increase/decrease like_count value.
    def likeVal(get_islike):
        print(get_islike + "test")
        if get_islike == "like":
            get_post.like_count = get_post.like_count + 1
        elif get_islike == "unlike":
            get_post.like_count = get_post.like_count - 1
        else:
            print("not okay")

    # check if user id and post id are there
    if (payload.user_id == 0 or payload.post_id == 0):
            return {"status":False, "message":f"user id or post post id cannot be zero."}
    else:
        add_like = None  # Declare the variable with a default value None

        # If user table has user or not
        check_user = db.query(models.User).filter(models.User.id == payload.user_id).first()

        if not check_user:
            return {"status":False, "message":f"User with id: {payload.user_id} not found"}
        
        else:
            # if like table already has user and post or not
            user = db.query(models.Like).filter(and_(models.Like.user_id == payload.user_id, models.Like.post_id == payload.post_id)).first()

            if user is None:
                # Add like
                add_like = models.Like(
                    user_id=payload.user_id,
                    post_id=payload.post_id,
                    is_like="like"
                )
                print(add_like.is_like + "add")
                db.add(add_like)
                db.commit()

            # If the user already exists and the post is liked, then unlike it for that user
            else:

                like_status = user.is_like
               
                if like_status == "like":
                    like_status = "unlike"
                else:
                    like_status = "like"
            
                user.is_like = like_status

                if add_like is not None:
                    add_like.is_like = like_status

            # See if the post exists
            get_post = db.query(models.Feed).filter(models.Feed.id == payload.post_id).first()

            if not get_post:
                return {"status": False, "message": f"Post with id:{payload.post_id} not found"}
            
            else:             

                if user is not None:
                    print("user")
                    return_like = user.is_like
                    likeVal(return_like)

                if add_like is not None:
                    print("add-part")
                    return_like = add_like.is_like
                    likeVal(return_like)

            if add_like is not None:
                db.refresh(add_like)

            db.commit()  # Move the commit statement here

            if add_like is None:
                return {"status": True, "message": f"Post Unliked"}
            else:
                return {"status": True, "message": "Post Liked"}
          
            
@router.get("/posts/{user_id}")
def get_posts_byUserId(user_id:int, db:Session = Depends(get_db)):
    # Check for user id 
    if user_id:
        # Check if user id exists in user table 
        user_table = db.query(models.User).filter(models.User.id == user_id).first()

        if user_table:
            # Check if user id exists in user table and feed table
            feed_table =  db.query(models.Feed).filter(models.Feed.user_id == user_id).all()

            if feed_table:
                return {"status": True, "message": "Posts retrieved successfully", "data": feed_table}
            
            else:
                return {"status": False, "message": "User does not have any post."}
           
        # if user not exist in user table 
        else:
            return {"status": False, "message": "User does not exist"}
    
    # if not user id 
    else:
        return {"status": False, "message": "User id required"}
    



        