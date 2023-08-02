
from fastapi import Form
from ..dependencies import *

router = APIRouter(
    prefix = '/transaction',
    tags= ['Wallet']
)

@router.post("/add-wallet")
async def add_wallet(
                    user_id: int = Form(...),
                    mobile_no: str = Form(...),
                    payment_id: str = Form(...),
                    order_id: str = Form(...),
                    signature_id: str = Form(...),
                    cr_amount: float = Form(...),           
                    db: Session = Depends(get_db)
                ):
        
        # Query the database to check if the user exists
        user = db.query(models.User).filter(models.User.id == user_id).first()

        if user is None:
            response_data = {"status": False, "message": f"No user with id:{user_id} found."}
            response_content = json.dumps(response_data)
            return Response(content=response_content)
        else:       
            # To check mobile no
            mobile_match_exist = db.query(models.User).filter(user.phone == mobile_no).first()

            if mobile_match_exist:
        
                new_wallet = models.Wallet(
                    user_id=user_id,
                    mobile_no=mobile_no,
                    payment_id=payment_id,
                    order_id=order_id,
                    signature_id=signature_id,
                    cr_amount=cr_amount,
                    # mode = "recharge",
                    # type = "user"
                )
                db.add(new_wallet)
                
                # Update the user's wallet value
                user.wallet = str(float(user.wallet) + new_wallet.cr_amount)  
                print(user.wallet)        

                # Commit the changes to the database
                db.commit()
                db.refresh(new_wallet)  # refresh is used to reflect changes from db
                return {"status":True, "message":"Transaction details stored successfully", "data":new_wallet}
            else:
                return {"status":True, "message":"Mobile no does not match"}


@router.get("/show-wallet/{user_id}")
def get_wallet_by_id(user_id:int, db:Session = Depends(get_db)):
    user_wallet = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user_wallet:
        return {"status":False, "message":"User not found"}
      
    else:
        wallet_amt = user_wallet.wallet             
        return {"status":True, "message":"Transaction details retrieved successfully", "wallet_amount":wallet_amt}


    