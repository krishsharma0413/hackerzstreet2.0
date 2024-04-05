import fastapi
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import motor.motor_asyncio
from dotenv import dotenv_values
import markdown
import certifi
from secrets import token_urlsafe
from pydantic import BaseModel
from hashlib import sha256

ca = certifi.where()

data = dotenv_values("./cred.env")

client = motor.motor_asyncio.AsyncIOMotorClient(data["mongo_url"], tlsCAFile=ca)
database = client["hackerzstreet2"]


app = fastapi.FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Login(BaseModel):
    username: str
    password: str

class Signup(BaseModel):
    username: str
    password: str

@app.get("/", response_class=HTMLResponse)
async def root(request: fastapi.Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signuppage(request: fastapi.Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/blog/{blogid}", response_class=HTMLResponse)
async def blogpage(request: fastapi.Request, blogid: str):
    try:
        content = open(f"./database/blogs/{blogid}.md", "r", encoding="utf-8").read()
        data = await database["blogs"].find_one({"_id": blogid})
        company = data["company"]
        title = data["title"]
        date = (data["date"]).strftime("%d %B, %Y")
        readtime = (len((content.split())) // 100 if len(content[2].split()) > 100 else 1)

    except:
        return RedirectResponse("/")
    
    return templates.TemplateResponse("blog.html", {
        "request": request,
        "content": markdown.markdown(content),
        "company": company,
        "title": title,
        "date": date,
        "readtime": readtime
    
    })

@app.get("/login", response_class=HTMLResponse)
async def loginpage(request: fastapi.Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/auth/login")
async def login(login: Login):
    data = await database["users"].find_one({
        "_id": login.username,
        "password": sha256(str(login.password).encode("utf-8")).hexdigest()
    })
    if data:
        return {"status": "success", "token": data["token"]}
    else:
        return {"status": "failed"}
    
@app.post("/auth/signup")
async def login(signup: Signup):
    token = token_urlsafe(32)
    data = await database["users"].insert_one({
        "_id": signup.username,
        "password": sha256(str(signup.password).encode("utf-8")).hexdigest(),
        "token": token
    })
    if data:
        return {"status": "success", "token": token}
    else:
        return {"status": "failed"}
    
