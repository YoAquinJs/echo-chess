#Main incorrecto. Lo tenía fuera de api y de frontend para conectar ambos

'''
"""
Echo-Chess WEB routes
"""

import uvicorn
import sys
import os

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi.responses import JSONResponse
import httpx  # Cliente HTTP para consumir la API
from fastapi.staticfiles import StaticFiles


# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database.setup import setup_database
from api.routers.setup import register_routers

# Inicializar la base de datos
setup_database()

# Crear la instancia de la aplicación FastAPI
app = FastAPI()

# Configurar plantillas y archivos estáticos
templates = Jinja2Templates(directory="frontend/templates")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Registrar los routers
register_routers(app)


# Rutas para renderizar páginas HTML
@app.get("/web/user/create", response_class=HTMLResponse)
async def serve_create_user_page(request: Request):
    return templates.TemplateResponse("user_create.html", {"request": request})


@app.get("/web/user/login", response_class=HTMLResponse)
async def serve_login_page(request: Request):
    return templates.TemplateResponse("user_login.html", {"request": request})


@app.get("/web/user/{user_id}", response_class=HTMLResponse)
async def serve_user_page(request: Request, user_id: int):
    return templates.TemplateResponse("user_page.html", {"request": request, "user_id": user_id})


@app.get("/web/user/{user_id}/games/{game_id}/movements", response_class=HTMLResponse)
async def serve_game_movements_page(request: Request, user_id: int, game_id: int):
    return templates.TemplateResponse( "game_movements.html", {"request": request, "user_id": user_id, "game_id": game_id})


@app.get("/web/user/{user_id}/update_token", response_class=HTMLResponse)
async def serve_gupdate_token_page(request: Request, user_id: int):
    return templates.TemplateResponse( "update_token.html", {"request": request, "user_id": user_id})



@app.get("/web/user/{user_id}/games", response_class=HTMLResponse)
async def serve_user_games_page(request: Request, user_id: int):
    # Consultar información del usuario desde la API
    async with httpx.AsyncClient() as client:
        user_response = await client.get(f"http://localhost:8000/user/{user_id}")
        #print("Datos del usuario:", user_response.json())
        if user_response.status_code == 404:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        user = user_response.json()
    
    # Consultar los juegos del usuario desde la API
    async with httpx.AsyncClient() as client:
        games_response = await client.get(f"http://localhost:8000/user/{user_id}/games")
        print("Datos de los juegos:", games_response.json())
        if games_response.status_code == 404:
            games = []
        elif games_response.status_code == 200:
            games = games_response.json()
        else:
            raise HTTPException(
                status_code=games_response.status_code,
                detail="Error al obtener los juegos",
            )
    
    # Renderizar la plantilla con datos del usuario y juegos
    return templates.TemplateResponse(
        "user_games.html",
        {"request": request, "user": user, "games": games},
    )


    
def main():
    """start api on script execution"""
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
'''