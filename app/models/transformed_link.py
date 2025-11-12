# """ Користувачі можуть створювати посилання на трансформоване зображення 
#     для перегляду світлини в вигляді URL та QR-code """


# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, func
# from sqlalchemy.orm import relationship
# from app.db.base import Base

# class TransformedLink(Base):
#     __tablename__ = "transformed_links"

#     id = Column(Integer, primary_key=True, index=True)
#     photo_id = Column(Integer, ForeignKey("photos.id", ondelete="CASCADE"), nullable=False)
#     transformation_params = Column(JSON, nullable=False)  # зберіг. параметри Cloudinary-трансф.
#     url = Column(String, nullable=False)  # для вже трансф. зображ.
#     qr_code_url = Column(String, nullable=False)
#     created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

#     # Зв’язки
#     photo = relationship("Photo", back_populates="transformed_links")
#     creator = relationship("User", foreign_keys=[created_by])

#     def __repr__(self):
#         return f"TransformedLink(id={self.id}, photo_id={self.photo_id}, url={self.url})"
