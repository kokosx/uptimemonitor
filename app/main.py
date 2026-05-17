from sqlmodel import Session
from fastapi import FastAPI, Depends
from typing import List
from models import engine, Website
from services import WebsiteService, CheckService
from repositories import WebsiteRepository, CheckRepository
from apscheduler.schedulers.asyncio import AsyncIOScheduler # pyright: ignore[reportMissingTypeStubs]
from contextlib import asynccontextmanager




scheduler = AsyncIOScheduler()

async def run_website_check(website_id: int):
    print(f"checked for {website_id}")
    with Session(engine) as session:
        check_repo = CheckRepository(session=session)
        website_repo = WebsiteRepository(session=session)
        check_service = CheckService(check_repo, website_repo)
        
        await check_service.perform_check(website_id)
        
def add_job(website:Website):
    print("Adding a job")
    scheduler.add_job(run_website_check, 'interval', seconds=website.interval, args=[website.id], id=f"check_site_{website.id}") # pyright: ignore[reportUnknownMemberType]

        
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    with Session(engine) as session:
        website_repo = WebsiteRepository(session=session)
        website_service = WebsiteService(website_repo)
        websites = website_service.get_all()
        
        for site in websites:
            assert site.id is not None
            add_job(site)
            
    yield
    scheduler.shutdown()

def get_session():
    with Session(engine) as session:
        yield session
        
def get_website_service(session: Session = Depends(get_session)) -> WebsiteService:
    repo = WebsiteRepository(session)
    service = WebsiteService(repo)
    return service

def get_check_service(session: Session = Depends(get_session)) -> CheckService:
    check_repo = CheckRepository(session=session)
    website_repo = WebsiteRepository(session=session)
    service = CheckService(check_repo, website_repo)
    return service

app = FastAPI(lifespan=lifespan)

@app.get("/", response_model=List[Website])
def get_websites(website_service: WebsiteService = Depends(get_website_service)):
    return website_service.get_all()

@app.post("/", response_model=Website)
def create_website(website: Website, website_service: WebsiteService = Depends(get_website_service)):
    new_site =  website_service.create_website(website)
    assert new_site is not None
    assert new_site.id is not None
    add_job(new_site)
    return new_site
