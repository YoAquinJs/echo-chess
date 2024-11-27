"""user endpoints router"""

from fastapi import APIRouter, HTTPException, Depends, Form
from sqlmodel import Session

#from auth.dependencies import UserTokenDependency
from database.models.user_db import User
from database.models.chess_game_db import ChessGame
from database.models.chess_movement_db import ChessMovement
from database.models.board_client_db import BoardClient
from database.dependencies import DBSessionDependency


router = APIRouter(
    prefix="/user",
    tags=["user"],
    #dependencies=[Depends(UserTokenDependency)],
)

#Original  --->   @router.post("/", response_model=User, dependencies=[])
@router.post("/", response_model=User)
async def create_user(user: User, session: Session= DBSessionDependency):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


#Obtener información de un usuario (requiere autenticación)
@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, session: Session= DBSessionDependency):
    user= session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


#Actualizar información de un usuario (requiere autenticación)
@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: User, session: Session= DBSessionDependency):
    user= session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return user


#Eliminar un usuario (requiere autenticación)
@router.delete("/{user_id}")
async def delete_user(user_id: int, session: Session= DBSessionDependency):
    user= session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.delete(user)
    session.commit()
    return {"detail": "Usuario eliminado"}


#Devuelve una lista de juegos asociados a un usuario, ya sea como jugador blanco o negro.
@router.get("/{user_id}/games", response_model=list[ChessGame])
async def get_user_games(user_id: int, session: Session = DBSessionDependency):
    query = (
        session.query(ChessGame)
        .filter((ChessGame.white_user_id == user_id) | (ChessGame.black_user_id == user_id))
        .all()
    )
    if not query:
        raise HTTPException(status_code=404, detail="No se encontraron juegos para este usuario.")
    return query



#Devuelve una lista de movimientos para un juego específico.
@router.get("/{user_id}/games/{game_id}/movements", response_model=list[ChessMovement])
async def get_game_movements(user_id: int, game_id: int, session: Session = DBSessionDependency):
    # Verificar si el usuario está asociado al juego
    game = (
        session.query(ChessGame)
        .filter(
            ChessGame.id == game_id,
            (ChessGame.white_user_id == user_id) | (ChessGame.black_user_id == user_id),
        )
        .first()
    )
    if not game:
        raise HTTPException(
            status_code=404, detail="Juego no encontrado o el usuario no está asociado."
        )

    # Obtener movimientos del juego usando el campo game_id
    movements = (
        session.query(ChessMovement)
        .filter(ChessMovement.game_id == game_id)  # Relacionar movimientos con el juego
        .order_by(ChessMovement.index)
        .all()
    )
    if not movements:
        raise HTTPException(status_code=404, detail="No se encontraron movimientos para este juego.")
    return movements


# Ruta para mostrar la información del usuario y su token
@router.get("/{user_id}/update_token", response_model=User)
async def get_user_info(user_id: int, session: Session = DBSessionDependency):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return User(id=user.id, name=user.name, board_token=user.board_token)


# Ruta para actualizar el token del usuario
@router.post("/{user_id}/update_token")
async def update_user_token(
    user_id: int,
    token: str = Form(None),
    session: Session = DBSessionDependency
):
    
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validar y actualizar el token
    if token is None or token.strip() == "":
        user.board_token = None
        message = "Token dejado en nulo correctamente"
    else:
        try:
            token_int = int(token)
        except ValueError:
            raise HTTPException(status_code=400, detail="Token debe ser un número entero")

        user.board_token = token_int
        message = "Token actualizado correctamente"

    session.commit()
    return {"message": message, "user_id": user.id, "updated_token": user.board_token}


# Crea o asocia un BoardClient con un token dado al usuario especificado
@router.post("/{user_id}/upload_client_token/{token}")
async def upload_client_token(user_id: int, token: str, session: Session = DBSessionDependency):
   
    # Buscar al usuario
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Buscar un cliente existente con ese token
    board_client = session.query(BoardClient).filter(BoardClient.token == token).first()

    # Crear cliente si no existe
    if not board_client:
        board_client = BoardClient(token=token)
        session.add(board_client)
        session.commit()
        session.refresh(board_client)

    # Asociar el token al usuario
    user.board_token = board_client.token
    session.commit()
    session.refresh(user)

    return {
        "message": "Token asociado correctamente.",
        "user_id": user.id,
        "client_id": board_client.id,
        "client_token": board_client.token,
    }
    

#Elimina el token de todos los usuarios asociados y borra el registro del BoardClient
@router.delete("/remove_client_token/{token}")
async def remove_client_token(token: str, session: Session = DBSessionDependency):
    # Buscar el BoardClient con el token
    board_client = session.query(BoardClient).filter(BoardClient.token == token).first()
    if not board_client:
        raise HTTPException(status_code=404, detail="BoardClient no encontrado")

    # Desasociar el token de los usuarios que lo tengan asignado
    users_with_token = session.query(User).filter(User.board_token == board_client.token).all()
    for user in users_with_token:
        user.board_token = None
        session.add(user)  # Actualizar el usuario

    # Eliminar el BoardClient
    session.delete(board_client)
    session.commit()

    return {
        "message": "Token y cliente eliminados correctamente.",
        "removed_token": token,
        "affected_users": [user.id for user in users_with_token],
    }





#Extras para pruebas

#Crear chess game
@router.post("/game_p/", response_model=ChessGame, tags=["purebas"])
async def create_chess_game(game: ChessGame, session: Session= DBSessionDependency):
    session.add(game)
    session.commit()
    session.refresh(game)
    return game

#Crear chess movement
@router.post("/movement_p/", response_model=ChessMovement, tags=["purebas"])
async def create_chess_movement(movement: ChessMovement, session: Session= DBSessionDependency):
    session.add(movement)
    session.commit()
    session.refresh(movement)
    return movement
