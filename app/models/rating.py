# from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
# from sqlalchemy.orm import relationship
# from app.db.base import Base


# class Rating(Base):
#     __tablename__ = "ratings"

#     id = Column(Integer, primary_key=True, index=True)
#     score = Column(Integer, nullable=False)

#     user_id = Column(
#         Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
#     )
#     photo_id = Column(
#         Integer, ForeignKey("photos.id", ondelete="CASCADE"), nullable=False
#     )

#     user = relationship("User", back_populates="ratings")
#     photo = relationship("Photo", back_populates="ratings")

#     __table_args__ = (
#         UniqueConstraint("user_id", "photo_id", name="unique_user_photo_rating"),
#     )
