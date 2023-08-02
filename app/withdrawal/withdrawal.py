from typing import Optional
from fastapi import Form
from ..dependencies import *

router = APIRouter(
    prefix = '/transaction',
    tags= ['Withdrawal']
)

@router.post("/withdrawal")
async def withdrawal(
                    user_id: int = Form(...),  # ... suggests that there might be additional code
                    upi_id : Optional[str] = Form(""),
                    account_no : Optional[str] = Form(""),
                    ifsc_code : Optional[str] = Form(""),
                    bank_name : Optional[str] = Form(""),
                    amount : float = Form(...),       
                    db: Session = Depends(get_db)
                ):
        
        
        # to check if the user exists
        user = db.query(models.User).filter(models.User.id == user_id).first()
        
        if user is None:
            response_data = {"status": False, "message": f"No user with id:{user_id} found."}
            response_content = json.dumps(response_data)
            return Response(content=response_content)              
        
        new_withdrawal = models.Withdrawal(
            user_id = user_id,
            upi_id = upi_id,
            account_no = account_no,
            ifsc_code = ifsc_code,
            bank_name = bank_name,
            amount = amount,
            wallet_amount = user.wallet
        )

        if (new_withdrawal.upi_id and new_withdrawal.account_no):
            response_data = {"status": False, "message": f"User can prefer one among upi_id and account_no"}
            response_content = json.dumps(response_data)
            return Response(content=response_content)  
        
        if ((new_withdrawal.upi_id and new_withdrawal.ifsc_code) or (new_withdrawal.upi_id and new_withdrawal.bank_name)):
            response_data = {"status": False, "message": f"User can enter ifsc_code and bank_name only when using account_no"}
            response_content = json.dumps(response_data)
            return Response(content=response_content)  

        if new_withdrawal.account_no:
        # account_no is provided, validate bank_name and ifsc_code
            if not new_withdrawal.bank_name or not new_withdrawal.ifsc_code:
                return {"status":True, "message": "Bank name and IFSC code are mandatory when account number is provided."}

        if new_withdrawal.ifsc_code:
        # account_no is provided, validate bank_name and ifsc_code
            if not new_withdrawal.account_no or not new_withdrawal.bank_name:
                return {"status":True, "message": "Account name and bank name are mandatory when ifsc code is provided."}
        
        if new_withdrawal.bank_name:
        # account_no is provided, validate bank_name and ifsc_code
            if not new_withdrawal.account_no or not new_withdrawal.ifsc_code:
                return {"status":True, "message": "Account no and ifsc code are mandatory when bank name is provided."}
        
        db.add(new_withdrawal)
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            # Update the user's wallet value
            user.wallet = str(float(user.wallet) - new_withdrawal.amount)  
            new_withdrawal.wallet_amount = user.wallet
            print(user.wallet)     

            # Commit the changes to the database
            db.commit()
        else:
            return {"status":True, "message": "User not found"}

        db.commit()
        db.refresh(new_withdrawal)
        return {"status":True, "message":"Withdrawal successful", "data":new_withdrawal}