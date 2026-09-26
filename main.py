from pathlib import Path
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from database import create_tables, create_user, get_user, save_recommendation, get_user_history
from gemini_utils import get_home_recommendations, get_party_recommendations, get_jewelry_recommendations

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
load_dotenv(BASE_DIR / '.env')
SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-secret-key')
app = FastAPI(title='PocketSmart AI', version='1.0')
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount('/static', StaticFiles(directory=str(STATIC_DIR)), name='static')
create_tables()

def page(request: Request, template: str, context=None):
    return templates.TemplateResponse(request, template, context or {})

@app.get('/', response_class=HTMLResponse)
async def home(request: Request): return page(request, 'dashboard.html')
@app.get('/dashboard', response_class=HTMLResponse)
async def dashboard(request: Request): return page(request, 'dashboard.html')
@app.get('/login', response_class=HTMLResponse)
async def login_page(request: Request): return page(request, 'login.html')
@app.post('/login')
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = get_user(email)
    if user and user['password'] == password:
        request.session['user_id'] = user['id']; request.session['username'] = user['username']
        return RedirectResponse('/', status_code=303)
    return page(request, 'login.html', {'error':'Invalid email or password.'})
@app.get('/register', response_class=HTMLResponse)
async def register_page(request: Request): return page(request, 'register.html')
@app.post('/register')
async def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    if password != confirm_password: return page(request, 'register.html', {'error':'Passwords do not match.'})
    try:
        create_user(username, email, password); return RedirectResponse('/login', status_code=303)
    except Exception as error: return page(request, 'register.html', {'error':str(error)})
@app.get('/logout')
async def logout(request: Request): request.session.clear(); return RedirectResponse('/', status_code=303)
@app.get('/home-planner', response_class=HTMLResponse)
async def home_planner(request: Request): return page(request, 'home_planner.html')
@app.get('/party-planner', response_class=HTMLResponse)
async def party_planner(request: Request): return page(request, 'party_planner.html')
@app.get('/jewelry-planner', response_class=HTMLResponse)
async def jewelry_planner(request: Request): return page(request, 'jewelry_planner.html')

@app.post('/generate-home', response_class=HTMLResponse)
async def generate_home(request: Request, budget: str=Form(''), room: str=Form(''), items: str=Form(''), style: str=Form(''), preferences: str=Form(''), platforms: str=Form('')):
    result = get_home_recommendations(budget, room, items, style, preferences, platforms)
    uid=request.session.get('user_id')
    if uid: save_recommendation(uid,'Home',budget,{'room':room,'items':items,'style':style,'preferences':preferences,'platforms':platforms},result)
    return page(request,'recommendations.html',{'result':result,'planner_type':'Home Decor','budget':budget})

@app.post('/generate-party', response_class=HTMLResponse)
async def generate_party(request: Request, budget: str=Form(''), guests: str=Form(''), party_type: str=Form(''), venue: str=Form(''), food: str=Form(''), decorations: str=Form(''), platforms: str=Form(''), preferences: str=Form('')):
    result = get_party_recommendations(budget, guests, party_type, venue, food, decorations, platforms, preferences)
    uid=request.session.get('user_id')
    if uid: save_recommendation(uid,'Party',budget,{'guests':guests,'party_type':party_type,'venue':venue,'food':food,'decorations':decorations,'platforms':platforms,'preferences':preferences},result)
    return page(request,'recommendations.html',{'result':result,'planner_type':'Party Planning','budget':budget})

@app.post('/generate-jewelry', response_class=HTMLResponse)
async def generate_jewelry(request: Request, budget: str=Form(''), occasion: str=Form(''), outfit_style: str=Form(''), jewelry_type: str=Form(''), material: str=Form(''), preferences: str=Form(''), image: UploadFile|None=File(None)):
    result = get_jewelry_recommendations(budget, occasion, outfit_style, jewelry_type, material, preferences)
    uid=request.session.get('user_id')
    if uid: save_recommendation(uid,'Jewelry',budget,{'occasion':occasion,'outfit_style':outfit_style,'jewelry_type':jewelry_type,'material':material,'preferences':preferences,'image':image.filename if image else ''},result)
    return page(request,'recommendations.html',{'result':result,'planner_type':'Jewelry','budget':budget})

@app.get('/history', response_class=HTMLResponse)
async def history(request: Request):
    uid=request.session.get('user_id'); data=get_user_history(uid) if uid else []
    return page(request,'history.html',{'history':data})
@app.get('/health')
async def health(): return {'status':'ok','application':'PocketSmart AI'}
@app.get('/startup')
async def startup(): return {'status':'success','message':'PocketSmart AI is running'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app',host='127.0.0.1',port=8000,reload=True)
