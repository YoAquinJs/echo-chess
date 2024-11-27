"""board client endpoints router"""

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from random import randint

#from auth.dependencies import ClientTokenDependency
from database.models.board_client_db import BoardClient
from database.models.user_db import User
from database.models.chess_game_db import ChessGame
from database.models.chess_movement_db import ChessMovement
from database.dependencies import DBSessionDependency


router = APIRouter(
    prefix="/client",
    tags=["board client"],
    #dependencies=[ClientTokenDependency],
)

#Crea un nuevo BoardClient con los datos enviados (no se necesita enviar id)
@router.post("/", response_model=BoardClient)
def create_client(client: BoardClient, session: Session = DBSessionDependency):
    session.add(client) 
    session.commit()
    session.refresh(client)
    return client


#Crea un nuevo registro de BoardClient con un token único (7 dígitos) y lo devuelve
@router.get("/new_board_token", response_model=int)
def create_unique_board_token(session: Session = DBSessionDependency):
    while True:
        # Generar un token de 7 dígitos
        new_token = randint(1000000, 9999999)

        # Comprobar si el token ya existe
        existing_token = session.query(BoardClient).filter(BoardClient.token == new_token).first()
        if not existing_token:
            # Crear el nuevo BoardClient si el token es único
            board_client = BoardClient(token=new_token)
            session.add(board_client)
            session.commit()
            session.refresh(board_client)
            return board_client.token

#Regresa el registro del BoardClient indicado con el id mandado
@router.get("/{client_id}", response_model=BoardClient)
def read_client(client_id: int, session: Session = DBSessionDependency):
    client = session.get(BoardClient, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


#Actualiza los dados enviados al BoardClient del id indicado.
@router.put("/{client_id}", response_model=BoardClient)
def update_client(client_id: int, updated_client: BoardClient, session: Session = DBSessionDependency):
    client = session.get(BoardClient, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client.token = updated_client.token
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

#Borra el BoardClient con el id dado
@router.delete("/{client_id}")
def delete_client(client_id: int, session: Session = DBSessionDependency):
    client = session.get(BoardClient, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    session.delete(client)
    session.commit()
    return {"ok": True}


#Devuelve el token del BoardClient_id dado
@router.get("/{client_id}/board_token", response_model=int)
def read_client(client_id: int, session: Session = DBSessionDependency):
    client = session.get(BoardClient, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client.token



#Crea un nuevo juego con los dos primeros User que tengan el token dado. Si no encuentra User con dicho token manda error.
@router.post("/board_game/{token}")
def create_board_game(token: str, session: Session = DBSessionDependency):
    
    # Obtener el BoardClient con el token
    board_client = session.query(BoardClient).filter(BoardClient.token == token).first()
    if not board_client:
        raise HTTPException(status_code=404, detail="BoardClient no encontrado")

    # Obtener los dos primeros usuarios con este token
    users = session.query(User).filter(User.board_token == board_client.token).all()
    if len(users) < 2:
        raise HTTPException(status_code=400, detail="No hay suficientes usuarios con el token dado")

    # Crear el nuevo juego
    chess_game = ChessGame(
        white_user_id=users[0].id,
        black_user_id=users[1].id,
        status=0,  # Estatus inicial del juego
    )
    session.add(chess_game)
    session.commit()
    session.refresh(chess_game)

    return {
        "message": "Juego creado exitosamente.",
        "game_id": chess_game.id,
        "white_user_id": chess_game.white_user_id,
        "black_user_id": chess_game.black_user_id,
    }
    
    
#Crea un ChessMovement conectado con el id del ChessGame especificado
@router.post("/movement/{game_id}")
def create_movement(game_id: int, session: Session = DBSessionDependency):
    
    # Verificar si el juego existe
    chess_game = session.get(ChessGame, game_id)
    if not chess_game:
        raise HTTPException(status_code=404, detail="Juego no encontrado")

    # Crear el movimiento
    new_movement = ChessMovement(
        game_id=game_id,
        index=0,
        encoded_movement=0,
    )
    session.add(new_movement)
    session.commit()
    session.refresh(new_movement)

    return {
        "message": "Movimiento creado exitosamente.",
        "movement_id": new_movement.id,
        "game_id": game_id,
        "index": new_movement.index,
        "encoded_movement": new_movement.encoded_movement,
    }


#Crea un ChessMovement con parametros dados y conectado con el id del ChessGame especificado
@router.post("/movement_with_data/{game_id}")
def create_movement(game_id: int, index: int, encoded_movement: int, session: Session = DBSessionDependency):
    
    # Verificar si el juego existe
    chess_game = session.get(ChessGame, game_id, )
    if not chess_game:
        raise HTTPException(status_code=404, detail="Juego no encontrado")

    # Crear el movimiento
    new_movement = ChessMovement(
        game_id= game_id,
        index= index,
        encoded_movement= encoded_movement,
    )
    session.add(new_movement)
    session.commit()
    session.refresh(new_movement)

    return {
        "message": "Movimiento creado exitosamente.",
        "movement_id": new_movement.id,
        "game_id": game_id,
        "index": new_movement.index,
        "encoded_movement": new_movement.encoded_movement,
    }