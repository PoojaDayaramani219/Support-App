from fastapi import FastAPI
import uvicorn
from app.images import image
from app.auth import auth 
from app.listener import listener
from app.transaction import wallet
from app.withdrawal import withdrawal
from app.user import user
from app.posts import post
from app.comments import comment
from app.others import other
from fastapi.staticfiles import StaticFiles
from app.oauth import oauth
from app.purchase_order import order
from fastapi.middleware.cors import CORSMiddleware
from app.invoice import invoice
from app.menu import menu

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:4200",
    # Add other allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],  # You can specify specific HTTP methods if needed
    allow_headers=["*"],  # You can specify specific headers if needed
)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")
#  the app.mount() function is used to mount a directory or a specific endpoint under a given path. 
# In this case, the code is mounting a directory named "static" under the path "/static".
# The StaticFiles class is imported from the fastapi.staticfiles module. It allows serving static files like HTML, CSS, JavaScript, and images.
    
@app.get("/")
def root():
    return {"message":"We are here to support you !!!"}

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(listener.router)
app.include_router(wallet.router)
app.include_router(withdrawal.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(image.router)
app.include_router(other.router)
app.include_router(oauth.router)
app.include_router(order.router)
app.include_router(invoice.router)
app.include_router(menu.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)