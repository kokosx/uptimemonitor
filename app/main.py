from sqlmodel import Session
from fastapi import FastAPI, Depends
from typing import List
from models import engine, Website
from services import WebsiteService
from repositories import WebsiteRepository

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session
        
def get_website_service(session: Session = Depends(get_session)) -> WebsiteService:
    repo = WebsiteRepository(session)
    service = WebsiteService(repo)
    return service


@app.get("/", response_model=List[Website])
def get_websites(session: Session = Depends(get_session)):
    website_service = get_website_service(session)
    return website_service.get_all()

@app.post("/", response_model=Website)
def create_website(website: Website, session: Session = Depends(get_session)):
    session.add(website)
    session.commit()
    session.refresh(website)
    return website

