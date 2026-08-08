from fastapi import APIRouter,Depends,HTTPException
from sqlmodel import Session,select

from app.schemas.user import UserCreate,UserResponse,UserLogin
from app.models.user import User
from app.db.session import get_session
from app.core.security import hash_password,verify_password
from app.core.token import create_access_token


router=APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/register",response_model=UserResponse)
def register(user:UserCreate,session:Session=Depends(get_session)):
    existing_user=session.exec(
        select(User).where(User.email==user.email)).first()
    

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="email already exist"
        )
    
    hashed_password=hash_password(user.password)

    new_user=User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@router.post("/login")
def login(user: UserLogin,session: Session=Depends(get_session)):
    existing_user=session.exec(
        select(User).where(user.email==User.email)).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="incorrect email or password"
        )
        
    if not verify_password(user.password,existing_user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="incorrect email or password"
        )
        
    access_token=create_access_token(existing_user.id)

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }
            
    