from repositories import WebsiteRepository
from models import Website
from typing import Sequence

class WebsiteService:
    def __init__(self, website_repo: WebsiteRepository):
        self.website_repo = website_repo
        
    def create_website(self, website: Website) -> Website | None:
        return self.website_repo.save(website)
    
    def get_all(self) -> Sequence[Website]:
        return self.website_repo.get_all()
    
    def get_by_name(self, name: str) -> Website | None:
        return self.website_repo.get_by_name(name)