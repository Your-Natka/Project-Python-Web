from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.schemas import TagCreate
from typing import List, Optional

def get_tag_by_name(db: Session, name: str) -> Optional[Tag]:
    """Отримати тег за назвою"""
    return db.query(Tag).filter(Tag.name == name).first()

def create_tag(db: Session, tag: TagCreate) -> Tag:
    """Створити новий тег"""
    db_tag = Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def get_tags(db: Session, skip: int = 0, limit: int = 100) -> List[Tag]:
    """Отримати список тегів"""
    return db.query(Tag).offset(skip).limit(limit).all()

def delete_tag(db: Session, tag_id: int) -> Optional[Tag]:
    """Видалити тег за id"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag
