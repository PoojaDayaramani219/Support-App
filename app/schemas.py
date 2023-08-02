from datetime import datetime
from typing import Optional
from .dependencies import *
from pydantic import BaseModel, EmailStr, Field

# validation for email
class CustomEmailStr(EmailStr):
    @classmethod
    def validate(cls, value):
        # Custom validation logic
        if not value.endswith("@gmail.com"):
            raise ValueError("Only email addresses from example.com are allowed.")
            # response_data = {"status": False, "message": "Only email addresses from example.com are allowed."}
            # response_content = json.dumps(response_data)
            # return Response(content=response_content)
        return super().validate(value)

class Registration(BaseModel):
    name: str
    gender: str
    email : EmailStr
    password: str
    phone: str
    role: str = "user"
    # is_user: 
    refer_code: Optional[str] = ""

class UserResponse(BaseModel):
    name: str
    gender: str
    email: EmailStr
    phone: str
    # device_token: int
    created_at: datetime

    class Config:
        orm_mode = True

class Login(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class ResetCode(BaseModel):
    email: EmailStr

class Code(BaseModel):
    email: EmailStr 

class ResetPassword(BaseModel):
    code: int
    new_password: str
    confirm_password: str

    class Config:
        orm_mode = True

class AddListener(BaseModel):
    name: str
    email: CustomEmailStr
    mobile_no: str
    image: str = ""
    age : int  
    interest: str
    language : str
    gender : str
    available_on : str
    about: str
    user_type: str = "user"
    charge: float = 0.0
    status: bool = 0
    online_status: bool = 0
    busy_status: bool = 0
    refer_code: str = ""
    used_refer_code:str = ""
    user_refer_code_status: bool = 0  
    ac_delete: bool = 0
    delete_status: bool = 0
    total_review_count: int = 0
    average_rating: int = 0

class AddWallet(BaseModel):
    user_id: int
    mobile_no: str
    payment_id: str
    order_id: str
    signature_id: str
    cr_amount: float

class Feed(BaseModel):
    content: str
    feed_img: str

class LikePost(BaseModel):
    user_id: int
    post_id: int

class CommentPost(BaseModel):
    user_id: int
    post_id: int
    comment: str = ""
    comment_on_id :int = 0 # if new comment then comment on id will be zero, else comment id

class Email(BaseModel):
    sender_email: str
    sender_password: str
    recipient_email: str
    subject: str
    body: str

class Order(BaseModel):
    balance_amt : float 
    total_amt : float 
    requestor : str = ""
    date : str = "17/07/2023"
    requestor_img : str = ""
    description : str = ""
    is_active : bool

class Invoice(BaseModel):
    bill_to : str
    pay_to : str
    address : str
    mobile_no : str
    bank_name : str
    account_name : str
    BSB : str
    account_no : str

class Summary(BaseModel):
    invoice_no : int
    description : str
    rate : float
    hours : int

class MenuItem(BaseModel):
    item : str
    icon : str

    



    







