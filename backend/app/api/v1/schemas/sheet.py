from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class SheetModel(BaseModel):
    id: UUID | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None
    parent_info: str
    parent_number: str
    player_info: str
    player_birth_date: str
    player_adress: str
    player_club: str
    player_position: str
    player_strong_foot: str
    payment: str | None = 'Ödənməyib'

class updateSheetModel(BaseModel):
    id: str