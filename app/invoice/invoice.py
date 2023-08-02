from ..dependencies import *

router = APIRouter(
    tags=['Invoice']
)

@router.post("/create-invoice")
async def create_invoice(payload: schemas.Invoice, db: Session = Depends(get_db)):
    add_invoice = models.Invoice(**payload.dict())
    db.add(add_invoice)
    db.commit()
    db.refresh(add_invoice)
    return {"status":True, "message":"Order added", "data": add_invoice}


@router.get("/invoice/{invoice_id}")
def get_invoice(invoice_id: int, db:Session = Depends(get_db)):
    if not db.query(models.Invoice):
        err_msg = "The 'invoice' table does not exist in the database."
        return {"status": False, "message": err_msg}
    
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

    if not invoice:
        return {"status":False, "message":"No invoice found"}
    else:
        return {"status":True, "message":"Invoice retrieved successfully", "data":invoice}


@router.post("/create-summary")
async def create_summary(payload: schemas.Summary, db: Session = Depends(get_db)):
    amount = payload.rate * payload.hours
    add_summary = models.Invoice_Summary(**payload.dict(), amount=amount)
    db.add(add_summary)    
    db.commit()
    db.refresh(add_summary)
    return {"status":True, "message":"Order added", "data": add_summary}


@router.get("/summary/{invoice_id}")
def summary_by_invoiceId(invoice_id: int, db:Session = Depends(get_db)):
    if not db.query(models.Invoice_Summary):
        err_msg = "The 'Invoice Summary' table does not exist in the database."
        return {"status": False, "message": err_msg}
    
    invoice_summary = db.query(models.Invoice_Summary).filter(models.Invoice_Summary.invoice_no == invoice_id).all()

    if not invoice_summary:
        return {"status":False, "message":"No invoice summary found"}
    else:
        return {"status":True, "message":"Invoice retrieved successfully", "data":invoice_summary}


@router.get("/discount/{invoice_no}/{discount}")
async def discount(invoice_no : int, 
    discount : int = 0, db: Session = Depends(get_db)):
    amt = 0
    invoice = db.query(models.Invoice_Summary).filter(models.Invoice_Summary.invoice_no == invoice_no)
    get_invoice = invoice.all()
    if get_invoice:
        for x in get_invoice:
            amt = amt + x.amount 
        sub_total = amt
        discount_amt = (sub_total * discount)/100
        total = sub_total - discount

        add_discount = {"sub_total":sub_total, "discount_percent": discount, "package_discount": discount_amt, "total": total}
        # db.add(add_summary)
        return {"status":True, "message":"Total retrieved successfully", "data": add_discount}
    else:
        return {"status":False, "message":"Invoice no does not match"}