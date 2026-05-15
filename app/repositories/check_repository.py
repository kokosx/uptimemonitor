from sqlmodel import Session, select
from models import Check
from typing import Sequence

class CheckRepository:
    def __init__(self, session: Session):
        self.session = session  

    def get_by_website_id(self, id: int) -> Sequence[Check] | None:
        return self.session.exec(select(Check).where(Check.website_id == id)).all()

    def save(self, check: Check) -> Check:
        self.session.add(check)
        self.session.commit()
        self.session.refresh(check)
        return check