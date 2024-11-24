"""user endpoints router"""

from fastapi import APIRouter, HTTPException, Depends, Form, Request, status
from sqlmodel import Session
from sqlalchemy.sql import func
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from api.database.models.user_db import User
from api.database.models.chess_game_db import Chess_game
from api.database.models.chess_movement_db import Chess_movement
from api.database.dependencies import DBSessionDependency

# Configuración general del router
router = APIRouter(
    prefix="/user",
    tags=["user"],
)

templates = Jinja2Templates(directory="frontend/templates")

# ======================================================
# **Funciones auxiliares**
# ======================================================

def get_user_by_id(user_id: int, session: Session) -> User:
    """Obtiene un usuario por ID o lanza un error 404 si no existe."""
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

def create_user(name: str, password: str, session: Session) -> User:
    """Crea un nuevo usuario si el nombre no está ocupado."""
    existing_user = session.query(User).filter(User.name == name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nombre ocupado")
    user = User(name=name, password=password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_games(user_id: int, session: Session):
    """Obtiene todas las partidas asociadas a un usuario."""
    return session.query(Chess_game).filter(
        (Chess_game.black_user_id == user_id) | (Chess_game.white_user_id == user_id)
    ).order_by(Chess_game.id).all()

def get_game_and_validate_user(game_id: int, user_id: int, session: Session) -> Chess_game:
    """Obtiene un juego y valida que el usuario esté asociado a él."""
    game = session.query(Chess_game).filter(
        Chess_game.id == game_id,
        (Chess_game.white_user_id == user_id) | (Chess_game.black_user_id == user_id),
    ).first()
    if not game:
        raise HTTPException(status_code=404, detail="Juego no encontrado o el usuario no está asociado.")
    return game

def render_template(template_name: str, request, **context):
    """Renderiza una plantilla con las variables de contexto proporcionadas."""
    return templates.TemplateResponse(template_name, {"request": request, **context})

# ======================================================
# **Rutas del endpoint /user**
# ======================================================

@router.get("/create", response_class=HTMLResponse)
async def create_user_form(request: Request):
    """Muestra el formulario para crear un usuario."""
    return render_template("user_create.html", request=request)

@router.post("/create", response_class=HTMLResponse)
async def create_user_endpoint(
    request: Request,
    name: str = Form(...),
    password: str = Form(...),
    session: Session = DBSessionDependency,
):
    """Crea un nuevo usuario desde el formulario."""
    try:
        user = create_user(name, password, session)
        return RedirectResponse(url=f"/user/{user.id}", status_code=status.HTTP_303_SEE_OTHER)
    except HTTPException as e:
        return render_template("user_create.html", request=request, error=e.detail)

@router.get("/login", response_class=HTMLResponse)
async def show_login_page(request: Request):
    """Muestra el formulario de login."""
    return render_template("user_login.html", request=request)

@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: Session = DBSessionDependency,
):
    """Valida las credenciales del usuario."""
    user = session.query(User).filter(User.name == username).first()
    if not user or user.password != password:
        return render_template("user_login.html", request=request, error="Usuario o contraseña incorrectos")
    
    response = RedirectResponse(url=f"/user/{user.id}", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="session", value="token_de_sesion")
    return response

@router.get("/{user_id}", response_class=HTMLResponse)
async def get_user_page(request: Request, user_id: int, session: Session = DBSessionDependency):
    """Muestra la página del perfil del usuario."""
    user = get_user_by_id(user_id, session)
    return render_template("user_page.html", request=request, user=user)

@router.get("/{user_id}/games", response_class=HTMLResponse)
async def get_user_games_endpoint(request: Request, user_id: int, session: Session = DBSessionDependency):
    """Muestra las partidas asociadas al usuario."""
    user = get_user_by_id(user_id, session)
    games = get_user_games(user_id, session)
    return render_template("user_games.html", request=request, user=user, games=games)

@router.get("/{user_id}/games/{game_id}/movements", response_class=HTMLResponse)
async def get_game_movements_html(
    request: Request,
    user_id: int,
    game_id: int,
    session: Session = DBSessionDependency,
):
    """Muestra los movimientos de una partida asociada a un usuario."""
    game = get_game_and_validate_user(game_id, user_id, session)
    movements = session.query(Chess_movement).filter(
        Chess_movement.game_id == game.id
    ).order_by(Chess_movement.index).all()

    white_user = get_user_by_id(game.white_user_id, session)
    black_user = get_user_by_id(game.black_user_id, session)

    return render_template(
        "game_movements.html",
        request=request,
        game_id=game.id,
        user_id=user_id,
        white_user=white_user.name,
        black_user=black_user.name,
        movements=movements,
    )


# Ruta para mostrar la página de actualizar token
@router.get("/{user_id}/update_token", response_class=HTMLResponse)
async def show_update_token_page(request: Request, user_id: int, session: Session = DBSessionDependency):
    user = get_user_by_id(user_id, session)
    return templates.TemplateResponse("update_token.html", {"request": request, "user": user})

# Ruta para actualizar el token del usuario
@router.post("/{user_id}/update_token", response_class=HTMLResponse)
async def update_token(
    request: Request,
    user_id: int,
    token: str = Form(None),
    session: Session = DBSessionDependency
):
    user = get_user_by_id(user_id, session)

    # Si el token está vacío, lo dejamos en nulo
    if token is None or token.strip() == "":
        user.board_token = None
        message = "Token dejado en nulo correctamente"
    else:
        # Si el token no está vacío, lo actualizamos
        user.board_token = token
        message = "Token actualizado correctamente"
    
    session.commit()
    
    return templates.TemplateResponse("update_token.html", {"request": request, "user": user, "message": message})






#Extras para pruebas

#Crear chess game
@router.post("/game_p/", response_model=Chess_game, tags=["purebas"])
async def create_chess_game(game: Chess_game, session: Session= DBSessionDependency):
    session.add(game)
    session.commit()
    session.refresh(game)
    return game

#Crear chess movement
@router.post("/movement_p/", response_model=Chess_movement, tags=["purebas"])
async def create_chess_movement(movement: Chess_movement, session: Session= DBSessionDependency):
    session.add(movement)
    session.commit()
    session.refresh(movement)
    return movement
