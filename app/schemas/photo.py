from typing import List, Optional
from pydantic import BaseModel, constr, field_validator


class PhotoBase(BaseModel):
    description: Optional[str] = None
    cloudinary_url: str
    unique_slug: str

    model_config = {
        "populate_by_name": True
    }


class PhotoCreate(PhotoBase):
    tags: Optional[List[constr(max_length=50)]] = None # type: ignore

    @field_validator("tags")
    def max_five_tags(cls, v):
        if v and len(v) > 5:
            raise ValueError("Maximum 5 tags allowed")
        return v


class PhotoUpdate(BaseModel):
    description: Optional[str] = None
    tags: Optional[List[constr(max_length=50)]] = None # type: ignore

    @field_validator("tags")
    def max_five_tags(cls, v):
        if v and len(v) > 5:
            raise ValueError("Maximum 5 tags allowed")
        return v


class PhotoOut(PhotoBase):
    id: int
    owner_id: int
    tags: Optional[List[str]] = None
