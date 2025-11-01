from pydantic import BaseModel, field_validator
from typing import List, Optional

MAX_TAGS = 5
MAX_TAG_LENGTH = 50


class PhotoBase(BaseModel):
    description: Optional[str] = None



class PhotoCreate(PhotoBase):
    tags: Optional[List[str]] = []

    @field_validator("tags", mode="before")
    def validate_tags(cls, v):
        if v is None:
            return []
        if len(v) > MAX_TAGS:
            raise ValueError(f"Maximum {MAX_TAGS} tags allowed")
        for tag in v:
            if len(tag) > MAX_TAG_LENGTH:
                raise ValueError(f"Tag '{tag}' exceeds {MAX_TAG_LENGTH} characters")
        print(f"Received tags: {v}")  # логую теги
        return v



class PhotoUpdate(BaseModel):
    description: Optional[str] = None
    tags: Optional[List[str]] = []

    @field_validator("tags", mode="before")
    def validate_tags(cls, v):
        if v is None:
            return []
        if len(v) > MAX_TAGS:
            raise ValueError(f"Maximum {MAX_TAGS} tags allowed")
        for tag in v:
            if len(tag) > MAX_TAG_LENGTH:
                raise ValueError(f"Tag '{tag}' exceeds {MAX_TAG_LENGTH} characters")
        print(f"Updated tags: {v}")  # логую теги
        return v

class PhotoOut(PhotoBase):
    id: int
    owner_id: int
    cloudinary_url: str
    unique_slug: str
    tags: List[str] = []
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
