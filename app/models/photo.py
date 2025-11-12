# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, func
# from sqlalchemy.orm import relationship
# from app.db.base import Base
# from app.models.association import photo_tags

# class Photo(Base):
#     __tablename__ = "photos"

#     id = Column(Integer, primary_key=True, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
#     cloudinary_public_id = Column(String, nullable=False)
#     original_url = Column(String, nullable=False)
#     description = Column(Text, nullable=True)
#     unique_slug = Column(String, unique=True, index=True, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())

#     # Відношення з юзером
#     owner = relationship("User", back_populates="photos")

#     # Відношення з тегами (many-to-many)
#     tags = relationship(
#         "Tag",
#         secondary=photo_tags,
#         back_populates="photos",
#         cascade="all"
#     )

#     # Відношення з коментарями та рейтингами
#     comments = relationship(
#         "Comment",
#         back_populates="photo",
#         cascade="all, delete-orphan"
#     )
#     ratings = relationship(
#         "Rating",
#         back_populates="photo",
#         cascade="all, delete-orphan"
#     )

#     # Відношення з трансф-ними посиланнями
#     transformed_links = relationship(
#         "TransformedLink",
#         back_populates="photo",
#         cascade="all, delete-orphan"
#     )

#     def __repr__(self):
#         return f"Photo(id={self.id}, owner_id={self.owner_id}, slug={self.unique_slug})"
