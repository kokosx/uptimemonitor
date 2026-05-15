import requests
from repositories import CheckRepository, WebsiteRepository
from models import Check

def check_url(url: str) -> int:
    try:
        res = requests.head(url, timeout=5)
        
        return res.status_code
        
    except requests.exceptions.RequestException:
        return -1
        
class CheckService:
    def  __init__(self, check_repository: CheckRepository, website_repository: WebsiteRepository):
        self.check_repository = check_repository
        self.website_repository = website_repository
    
    def perform_check(self, url: str) -> Check:
        website = self.website_repository.get_by_url(url)
        if not website:
            raise
        assert website.id is not None
        res = check_url(url)
        new_check = Check(error=None, response_code=res, website_id=website.id)
        return self.check_repository.save(new_check)
        
