# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
# from app.db.base import Base 
# from app.models.association import photo_tags

# class Tag(Base):
#     __tablename__ = "tags"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
    
#     photos = relationship("Photo", secondary=photo_tags, back_populates="tags")