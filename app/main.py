from sqlmodel import Session
from fastapi import FastAPI, Depends
from typing import List
from models import engine, Website, Check
from services import WebsiteService, CheckService
from repositories import WebsiteRepository, CheckRepository
from schemas import PerformCheckRequest

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session
        
def get_website_service(session: Session = Depends(get_session)) -> WebsiteService:
    repo = WebsiteRepository(session)
    service = WebsiteService(repo)
    return service

def get_check_service(session: Session = Depends(get_session)) -> CheckService:
    check_repo = CheckRepository(session)
    website_repo = WebsiteRepository(session)
    service = CheckService(check_repo, website_repo)
    return service

@app.get("/", response_model=List[Website])
def get_websites(website_service: WebsiteService = Depends(get_website_service)):
    return website_service.get_all()

@app.post("/", response_model=Website)
def create_website(website: Website, website_service: WebsiteService = Depends(get_website_service)):
    return website_service.create_website(website)

@app.post("/perform-check", response_model=Check)
def perform_check(request: PerformCheckRequest, check_service: CheckService = Depends(get_check_service)):
    return check_service.perform_check(request.url)
