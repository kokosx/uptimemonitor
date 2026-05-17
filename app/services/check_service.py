import httpx
from repositories import CheckRepository, WebsiteRepository
from models import Check
from fastapi import HTTPException
import asyncio


        
class CheckService:
    def  __init__(self, check_repository: CheckRepository, website_repository: WebsiteRepository):
        self.check_repository = check_repository
        self.website_repository = website_repository
        
    async def perform_check(self, website_id: int) -> Check:
        website = await asyncio.to_thread(self.website_repository.get_by_id, website_id)
        if not website:
            raise HTTPException(status_code=404)
        assert website.id is not None
        # if not website:
        #     raise
        # assert website.id is not None
        # res = self.check_url(url)
        # new_check = Check(error=None, response_code=res, website_id=website.id)
        # return self.check_repository.save(new_check)
        try:
            async with httpx.AsyncClient() as client:
                res = await client.head(website.url, timeout=website.timeout)
                response_code = res.status_code
                error_msg = None
        except httpx.RequestError as e:
            response_code = None
            error_msg = str(e)
        new_check = Check(website_id = website.id,
                          response_code=response_code,
                          error=error_msg)
        return await asyncio.to_thread(self.check_repository.save, new_check)
                
        
