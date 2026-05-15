from pydantic import BaseModel

class PerformCheckRequest(BaseModel):
    url: str # Możesz użyć HttpUrl dla automatycznej walidacji adresu