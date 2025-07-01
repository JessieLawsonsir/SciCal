# requirements.txt
# ----------------
# fastapi
# uvicorn
# httpx
# sqlalchemy
# pymysql
# python-multipart
# loguru
# python-jose[cryptography]
# passlib[bcrypt]

from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from math import sqrt, log10, sin, tan
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from loguru import logger
import asyncio
import os

# --------------------------- CONFIGURATION ---------------------------
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = "mysql+pymysql://user:password@localhost/scicalc"
MUSIC_FILE_PATH = "sample_music.mp3"
SEQ_URL = "http://localhost:5341"

logger.add(
   f"seq://{SEQ_URL}",
   level="INFO",
   backtrace=True,
   diagnose=True,
   serialize=True
)

# --------------------------- DATABASE SETUP ---------------------------
engine = create_engine(DATABASE_URL)
print(f"Connecting using DATABASE_URL: {DATABASE_URL}")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class LogEntry(Base):
   __tablename__ = "logs"
   id = Column(Integer, primary_key=True, index=True)
   operation = Column(String(50))
   result = Column(Text)
   timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# --------------------------- AUTH SETUP ---------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
   "testuser": {
       "username": "testuser",
       "hashed_password": pwd_context.hash("testpass")
   }
}

class Token(BaseModel):
   access_token: str
   token_type: str

class User(BaseModel):
   username: str

# --------------------------- UTILS ---------------------------
def verify_password(plain_password, hashed_password):
   return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
   if username in db:
       return User(username=username)

def authenticate_user(username: str, password: str):
   user = fake_users_db.get(username)
   if not user or not verify_password(password, user["hashed_password"]):
       return False
   return User(username=username)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
   to_encode = data.copy()
   expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
   to_encode.update({"exp": expire})
   return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
   credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
   try:
       payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
       username: str = payload.get("sub")
       if username is None:
           raise credentials_exception
   except JWTError:
       raise credentials_exception
   return get_user(fake_users_db, username)

# --------------------------- FASTAPI SETUP ---------------------------
app = FastAPI()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

# --------------------------- ROUTES ---------------------------
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
   user = authenticate_user(form_data.username, form_data.password)
   if not user:
       raise HTTPException(status_code=400, detail="Incorrect username or password")
   access_token = create_access_token(data={"sub": user.username})
   return {"access_token": access_token, "token_type": "bearer"}

async def log_operation(db: Session, operation: str, result: str):
   db_log = LogEntry(operation=operation, result=result)
   db.add(db_log)
   db.commit()
   logger.info(f"{operation}: {result}")

@app.get("/sqrt")
async def calc_sqrt(x: float, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
   result = sqrt(x)
   await log_operation(db, "SQRT", str(result))
   return {"sqrt": result}

@app.get("/cbrt")
async def calc_cbrt(x: float, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
   result = x ** (1/3)
   await log_operation(db, "CBRT", str(result))
   return {"cbrt": result}

@app.get("/log")
async def calc_log(x: float, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
   result = log10(x)
   await log_operation(db, "LOG", str(result))
   return {"log10": result}

@app.get("/sin")
async def calc_sin(x: float, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
   result = sin(x)
   await log_operation(db, "SIN", str(result))
   return {"sin": result}

@app.get("/tan")
async def calc_tan(x: float, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
   result = tan(x)
   await log_operation(db, "TAN", str(result))
   return {"tan": result}

@app.get("/integrate")
async def calc_integrate(a: float, b: float, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
   result = (b**2 - a**2)/2
   await log_operation(db, "INTEGRATION", str(result))
   return {"integration": result}

MUSIC_FOLDER = "music"

@app.get("/music")
async def get_music(track: str = "track1"):
    filename = f"{track}.mp3"
    full_path = os.path.join(MUSIC_FOLDER, filename)

    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail=f"Music file '{filename}' not found.")

    return Response(content=open(full_path, "rb").read(), media_type="audio/mpeg")


@app.get("/async-task")
async def async_demo():
   async def background_job():
       await asyncio.sleep(2)
       logger.info("Async job complete")
   asyncio.create_task(background_job())
   return {"status": "async job started"}

if __name__ == "__main__":
   import uvicorn
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)