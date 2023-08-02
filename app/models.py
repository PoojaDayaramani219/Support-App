from .database import Base
import uuid
from sqlalchemy import Integer,TIMESTAMP, Column, String, Boolean, text, Float, ARRAY
from random import randint, random 
import secrets
import string
from sqlalchemy.sql import func

# Generate a unique ID within the specified range
# def generate_unique_id():
#         unique_id = randint(6000, 9000)
#         while Order.query.filter_by(id=unique_id).first() is not None:
#             unique_id = randint(6000, 9000)
#         return unique_id

class ReferralCode():
    def generate_random_characters():
        random_chars = ""
        random_chars = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
        return random_chars
    
class User(Base):   
    randomNum = ReferralCode.generate_random_characters()
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement = True, server_default= text(str(randint(1000, 99999))))
    name = Column(String, nullable=False)
    gender = Column(String, nullable= False )
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(String, nullable=False, server_default='user')
    referral_code = Column(String, unique= True, nullable= False,default=text(str("'" + randomNum + "'")))
    refer_code = Column(String, nullable= True)
    device_token = Column(Integer, nullable= False, autoincrement = True, server_default= text(str(randint(100000, 10000000))))
    wallet = Column(String, nullable=False, default=float(0.0))
    refer_count = Column(Integer, nullable=False, default=0 )
    is_active = Column(Boolean, nullable= False, default= True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


class Code(Base):
    __tablename__ = 'codes'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement = True)
    email = Column(String, unique=True, nullable=False)
    reset_code = Column(Integer)
    # status = Column(Boolean, nullable= False, default='true')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    # expired_in = Column(TIMESTAMP(timezone=True), nullable=False)

class Listener(Base):
    __tablename__ = 'listeners'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement = True, server_default= text(str(randint(3000, 39999))))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mobile_no = Column(String, nullable=True)
    image= Column(String, nullable=True)
    age = Column(Integer, nullable= True)
    interest = Column(String, nullable=True)
    language = Column(String, nullable=True)
    gender = Column(String, nullable= False )
    available_on = Column(String, nullable= True)
    about = Column(String(500), nullable= True)
    user_type = Column(String, nullable= False)
    charge = Column(Float, nullable= False)
    device_token = Column(Integer, nullable= False, autoincrement = True, server_default= text(str(randint(200000, 20000000))))
    status = Column(Boolean, nullable= True)
    online_status = Column(Boolean, nullable= True)
    busy_status = Column(Boolean, nullable= True)
    refer_code = Column(String, nullable= True)
    used_refer_code = Column(String, nullable= True)
    user_refer_code_status = Column(Boolean, nullable= True)
    ac_delete = Column(Boolean, nullable= True)
    delete_status = Column(Boolean, nullable= True)
    total_review_count = Column(Integer, nullable= True)
    average_rating = Column(Integer, nullable= True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class Wallet(Base):
    __tablename__ = 'wallet'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement = True, server_default= text(str(randint(3000, 39999))))
    user_id= Column(Integer, nullable= False)
    mobile_no = Column(String, nullable= False)
    payment_id = Column(String, nullable= True)
    order_id = Column(String, nullable= True)
    signature_id = Column(String, nullable= True)
    cr_amount = Column(Float, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, server_default=text(str(randint(3000, 39999))))
    listener_img = Column(String(1500), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class Withdrawal(Base):
    __tablename__ = "withdrawal"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, server_default=text(str(randint(3000, 39999))))
    user_id = Column(Integer, nullable= False)
    upi_id = Column(String, nullable= True)
    account_no = Column(String, nullable= True)
    ifsc_code = Column(String, nullable= True)
    bank_name = Column(String, nullable= True)
    amount = Column(Float, nullable= True)
    wallet_amount = Column(Float, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class ResetPassword(Base):
    __tablename__ = "passwords"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, server_default=text(str(randint(3000, 39999))))
    email = Column(String, nullable=False)
    password = Column(String, nullable= False)    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class Feed(Base):
    __tablename__ = "feeds"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, server_default=text(str(randint(3000, 39999))))
    user_id = Column(Integer, nullable= True)
    content = Column(String, nullable= True)  
    feed_img = Column(String(3000), nullable=True)
    like_count = Column(Integer, nullable=False, default=0)
    comment_count = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, server_default=text(str(randint(3000, 39999))))
    user_id = Column(Integer, nullable= False)
    post_id = Column(Integer, nullable= False)
    is_like = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, server_default=text(str(randint(3000, 39999))))
    user_id = Column(Integer, nullable= False)
    post_id = Column(Integer, nullable= False)
    comment = Column(String, nullable= True)
    comment_on_id = Column(Integer, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

# orders
class Order(Base):   
    # Set the default value for the id column
    # order_id  = generate_unique_id()

    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, nullable= False, default=text(str(randint(6000, 9999))))
    balance_amt = Column(Float, nullable=False, default=float(0.0))
    total_amt = Column(Float, nullable=False, default=float(0.0))
    requestor = Column(String, nullable=False)
    date = Column(String, nullable=False)
    requestor_img = Column(String, nullable= True)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, nullable= False, default= True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class Invoice(Base):   
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, nullable= False, default=text(str(randint(3000, 4999))))
    bill_to = Column(String, nullable=False)
    pay_to = Column(String, nullable=False)
    address = Column(String, nullable=True)
    mobile_no = Column(String, nullable=True)
    bank_name = Column(String, nullable=False)
    account_name = Column(String, nullable=False)
    BSB = Column(String, nullable= True)
    account_no = Column(String, nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class Invoice_Summary(Base):
    __tablename__ = "summary"
    id = Column(Integer, primary_key=True, nullable= False, default=text(str(randint(1000, 2999))))
    invoice_no = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    hours = Column(Integer, nullable=False)
    amount = Column(Float, nullable= True, default=float(0.0))
    # sub_total = Column(Float, nullable=False, default=float(0.0)) 
    # package_discount = Column(Integer, nullable=False, default=text("in percentage"))
    # total = Column(Float, nullable=False, default=float(0.0))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class Discount(Base):
    __tablename__ = "discounts"
    id = Column(Integer, primary_key=True, nullable= False, default=text(str(randint(1000, 2999))))
    invoice_no = Column(Integer, nullable=False)
    sub_total = Column(Float, nullable=False,default=float(0.0))
    discount_percent = Column(Integer, nullable=False)
    discount_amt = Column(Float, nullable=False,default=float(0.0))
    total = Column(Float, nullable=False,default=float(0.0))
    amount = Column(Float, nullable= True, default=float(0.0))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

class Menu(Base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True, nullable= False, default=text(str(randint(1, 50))))
    item = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


    
    