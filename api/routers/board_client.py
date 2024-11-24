"""board client endpoints router"""

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

#from auth.dependencies import ClientTokenDependency
from api.database.models.board_client_db import BoardClient
from api.database.dependencies import DBSessionDependency


router = APIRouter(
    prefix="/client",
    tags=["board client"],
    #dependencies=[ClientTokenDependency],
)


@router.post("/", response_model=BoardClient)
def create_client(client: BoardClient, session: Session = DBSessionDependency):
    session.add(client) 
    session.commit()
    session.refresh(client)
    return client

#@router.get("/", response_model=list[BoardClient])
#def read_clients(session: Session = DBSessionDependency):
#    clients = session.exec(select(BoardClient)).all()
#    return clients

@router.get("/{client_id}", response_model=BoardClient)
def read_client(client_id: int, session: Session = DBSessionDependency):
    client = session.get(BoardClient, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

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

@router.delete("/{client_id}")
def delete_client(client_id: int, session: Session = DBSessionDependency):
    client = session.get(BoardClient, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    session.delete(client)
    session.commit()
    return {"ok": True}