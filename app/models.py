from sqlmodel import Field, SQLModel, Relationship, create_engine
import datetime
from typing import List

class Website(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(index=True)
    url: str = Field(index=True)
    interval: int = Field(default=60)
    timeout: int = Field(default=10)
    
    checks: List["Check"] = Relationship(back_populates="website")
    
class Check(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    response_code: int | None = Field()
    error: str | None = Field()
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    
    website_id: int = Field(foreign_key="website.id")
    
    website: Website = Relationship(back_populates="checks")
    
    
engine = create_engine("postgresql://postgres:@127.0.0.1:5432/uptime", echo=True)
SQLModel.metadata.create_all(engine)