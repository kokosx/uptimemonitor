from sqlmodel import Session, select
from models import Website
from typing import Sequence

class WebsiteRepository:
    def __init__(self, session: Session):
        self.session = session  

    def get_by_url(self, url: str) -> Website | None:
        return self.session.exec(select(Website).where(Website.url == url)).first()
    
    def get_by_name(self, name: str) -> Website | None:
        return self.session.exec(select(Website).where(Website.name == name)).first()
    
    def get_all(self) -> Sequence[Website]:
        return self.session.exec(select(Website)).all()

    def save(self, website: Website) -> Website:
        self.session.add(website)
        self.session.commit()
        self.session.refresh(website)
        return website