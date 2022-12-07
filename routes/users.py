from fastapi import APIRouter, HTTPException, status
from models.models import User, UserSignIn

user_router = APIRouter(
    tags = ["User"]
)
users = {}

@user_router.post("/signup")	
async	def	sign_new_user(data:	NewUser) ->	dict:	
    if	data.email	in	users:	
        raise	HTTPException(
            status_code=status.HTTP_409_CONFLICT,	
            detail="Username	exists"	
        )	
    users[data.email]	=	data	
    return	{	
        "message":	"User	successfully	registered!"	
    }	