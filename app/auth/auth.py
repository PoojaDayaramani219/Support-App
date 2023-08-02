from datetime import datetime
from fastapi import APIRouter, FastAPI, HTTPException, Depends, status
from sqlalchemy import desc
from app.database import get_db, engine
from fastapi import APIRouter, Request, Response, status, Depends, HTTPException
from .. import schemas, models
from sqlalchemy.orm import Session
from pydantic import EmailStr
from random import randint
import re
import json
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated


models.Base.metadata.create_all(bind = engine)

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", status_code= status.HTTP_200_OK)
async def create_user(payload:schemas.Registration, db: Session = Depends(get_db)):
    user_exist = db.query(models.User).filter(
        models.User.email == EmailStr(payload.email.lower())).first()
    
    mobile_exist = db.query(models.User).filter(models.User.phone == payload.phone).all()
    
    if user_exist or mobile_exist:     
        response_data = {"status": "false", "message": "Account already exists"}
        response_content = json.dumps(response_data)
        # print(response_data["status"])   # to access value of status
        return Response(content=response_content)
        # By using json.dumps, the dictionary will be converted to a JSON string, 
        # which can be properly encoded and returned as the content of the Response object.
        
    if not user_exist:      
        if len(payload.phone) !=10 or not payload.phone.isdigit():
            return {"status":"false", "message": "Invalid phone number"}
        # Check if the password has at least 8 characters
        elif len(payload.password) < 8:
            return {"status":"false", "message":"Password must be at least 8 characters long."}
        # Check if the password contains a special character
        elif not re.search(r"[!@#$%^&*()\-_=+{}[\]|\\;:'\",<.>/?]+", payload.password):
            return {"status":"false", "message":"Password must contain at least one special character."}
        else:
            if payload.refer_code.strip() != "":
                referred_user = db.query(models.User).filter(models.User.referral_code == payload.refer_code).first()
                if not referred_user:
                    return {"status": False, "message": "Referred user not found"}
                referred_user.refer_count += 1
                
                
            print(payload.password)
            payload.password = get_password_hash(payload.password)   
            
            new_user = models.User(**payload.dict())
            db.add(new_user)  
            db.commit()
            

            new_wallet = models.Wallet(
                user_id=new_user.id,
                mobile_no=new_user.phone,
                payment_id="",
                order_id="",
                signature_id="",
                cr_amount=0.0
            )
            
            db.add(new_wallet)
            db.commit()
            db.refresh(new_user)
            
            return {"status": True, "message": "User successfully created", "data": new_user}
        


@router.get("/getReferralCount")
async def refer_count(email: EmailStr,db:Session = Depends(get_db)):
    user_exist = db.query(models.User).filter(
        models.User.email == email).first()

    if user_exist:
        referral_code = user_exist.referral_code
        count = (
            db.query(models.User)
            .filter(referral_code == models.User.refer_code)
            .count()
        )
        
        refer_count = {
            "user_id" : user_exist.id,
            "email": user_exist.email,
            "referred_count": count
        }
        return {"status":True, "message":"Get count", "data":refer_count}

    else:
        return {"status":False, "message":"Email does not exist"}  
    
@router.post("/login")
async def login(payload:schemas.Login, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == (EmailStr(payload.email.lower()))).first()
    print(user)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email does not exist, please register')
    else:
        # print(payload.password)
        # print(user.password)
        # verify entered password and hashed password
        verify = verify_password(payload.password, user.password)
    
        if not verify:
            return {"status": status.HTTP_401_UNAUTHORIZED, "message":"Invalid credentials."}
        else:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.name}, expires_delta=access_token_expires
            )
        
            return {"status":200, "message":"Login successful", "data":user,"access_token": access_token, "token_type": "bearer"} 

# @router.post("/token", response_model=Token)
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
    

@router.get("/forgot-password")
async def forgetPassword(email:EmailStr,db:Session = Depends(get_db)):
    user_exist = db.query(models.User).filter(models.User.email == email).first()

    if not user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email does not exist')
    
    send_code = str(randint(100000, 999999))
    code = db.query(models.Code).filter(models.Code.email == email).first()
    
    if not code:
        new_code = models.Code(email=email, reset_code=send_code)
        db.add(new_code)
    else:
        code.reset_code = send_code

    db.commit()
    return {"status":"true", "message":"Password code has been sent to your email", "data": send_code}

@router.post("/reset-password")
async def resetPassword(payload: schemas.ResetPassword,db:Session = Depends(get_db)):
    get_email = db.query(models.Code).filter(models.Code.reset_code == payload.code).first()
    
    if get_email:
        # get its mail whose code matches
        user = db.query(models.User).filter(models.User.email == get_email.email).first()
        if user:
            # Check if the password has at least 8 characters
            if len(payload.new_password) < 8:
                return {"status":"false", "message":"Password must be at least 8 characters long."}

            # Check if the password contains a special character
            if not re.search(r"[!@#$%^&*()\-_=+{}[\]|\\;:'\",<.>/?]+", payload.new_password):
                return {"status":"false", "message":"Password must contain at least one special character."}
            
            # check password and confirm password
            if (payload.new_password == payload.confirm_password):
                check_password = (
                    db.query(models.ResetPassword)
                    .filter(models.ResetPassword.email == user.email)
                    .order_by(desc(models.ResetPassword.updated_at))
                    .limit(3)
                    .all()
                )
                
                # any keyword is to check if any of the last three passwords match the new_password
                if any(password_table.password == payload.new_password for password_table in check_password):
                    return {"status":"false", "message":"New password cannot match previous passwords"}
                
                # Replace the last third password with the present new_password
                if len(check_password) == 3:
                    check_password[2].password = payload.new_password
                    set_password = check_password[2].password
                    
                    # Update the user's password to the new password
                    user.password = payload.new_password
                    reset_pass = models.ResetPassword(email=user.email, password=set_password)

                    db.commit()
                    return {"status":"true", "message":"Password has been changed successfully"}
                    
                else:
                    # Insert new password
                    reset_password = models.ResetPassword(email = user.email, password = payload.new_password)
                    db.add(reset_password)

                    # Update the user's password to the new password
                    user.password = payload.new_password
                    
                    db.add(reset_password)
                    db.commit()
                    return {"status":"true", "message":"Password has been changed successfully"}
            else:
                return {"status":"false", "message":"Password and confirm password does not match"} 
        else:
            return {"status":"false", "message":"This email does not exist"} 
    else:
        return {"status":"false", "message":"Code is incorrect"}
