from sqlalchemy.orm import Session
from app.models.tag import Tag          
from app.schemas import TagCreate
from typing import List, Optional

def get_tag(db: Session, tag_id: int) -> Optional[Tag]:
    return db.query(Tag).filter(Tag.id == tag_id).first()

def get_tag_by_name(db: Session, name: str) -> Optional[Tag]:
    return db.query(Tag).filter(Tag.name == name).first()

def get_tags(db: Session, skip: int = 0, limit: int = 100) -> List[Tag]:
    return db.query(Tag).offset(skip).limit(limit).all()

def create_tag(db: Session, tag: TagCreate) -> Tag:
    db_tag = Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, tag_id: int) -> Optional[Tag]:
    tag = get_tag(db, tag_id)
    if tag:
        db.delete(tag)
        db.commit()
    return tag

def update_tag(db: Session, tag_id: int, new_name: str) -> Optional[Tag]:
    tag = get_tag(db, tag_id)
    if tag:
        tag.name = new_name
        db.commit()
        db.refresh(tag)
    return tag
