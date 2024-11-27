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


#Devuelve el token del BoardClient_id dado
@router.get("/{client_id}/board_token", response_model=int)
def read_client(client_id: int, session: Session = DBSessionDependency):
    client = session.get(BoardClient, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client.token



#Crea un nuevo juego con los dos primeros User que tengan el token dado. Si no encuentra User con dicho token manda error.
@router.post("/board_game/{token}/{opponent_id}")
def create_board_game(token: str, opponent_id: int, session: Session = DBSessionDependency):
    
    # Obtener el BoardClient con el token
    board_client = session.query(BoardClient).filter(BoardClient.token == token).first()
    if not board_client:
        raise HTTPException(status_code=404, detail="BoardClient no encontrado")

    # Obtener el usuario respectivo al token
    user = session.query(User).filter(User.board_token == board_client.token).first()
    if not user:
        raise HTTPException(status_code=400, detail="No se encontró un usuario conectado a ese token")
    
    # Verifica que el usuario oponente exista
    user_opponent = session.query(User).filter(User.id == opponent_id).first()
    if not user_opponent:
        raise HTTPException(status_code=400, detail="No se encontró un usuario oponente con ese id")
    
    if user.id == opponent_id:
        raise HTTPException(status_code=400, detail="Ambos jugadores no pueden ser el mismo")

    # Crear el nuevo juego
    chess_game = ChessGame(
        white_user_id= user.id,
        black_user_id= opponent_id,
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


#Crea un ChessMovement con parametros dados y conectado con el id del ChessGame especificado
@router.post("/movement/{game_id}")
def create_movement(game_id: int, index: int, start_move: str, end_move: str, session: Session = DBSessionDependency):
    
    # Verificar si el juego existe
    chess_game = session.get(ChessGame, game_id, )
    if not chess_game:
        raise HTTPException(status_code=404, detail="Juego no encontrado")

    # Crear el movimiento
    new_movement = ChessMovement(
        game_id= game_id,
        index= index,
        start_move= start_move,
        end_move= end_move
    )
    session.add(new_movement)
    session.commit()
    session.refresh(new_movement)

    return {
        "message": "Movimiento creado exitosamente.",
        "movement_id": new_movement.id,
        "game_id": game_id,
        "index": new_movement.index,
        "start_move": new_movement.start_move,
        "end_move": new_movement.end_move
    }